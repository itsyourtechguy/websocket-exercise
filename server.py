"""
WebSocket RPC Server
===================
A production-ready WebSocket server that allows clients to call functions remotely.
Key features:
- Handles multiple clients simultaneously
- Validates input types to prevent errors
- Provides meaningful error messages
- Uses a registry pattern for easy function extension
"""

import asyncio
import json
import logging
from typing import Any, Callable

import websockets

from protocol import parse_request, make_response, RPCError
from functions import FUNCTION_REGISTRY

# Set up logging (connection/disconnection, errors)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


async def handle_connection(ws: websockets.WebSocketServerProtocol) -> None:
    """
    Handle a single client connection throughout its lifetime.
    
    This function runs for each connected client until they disconnect.
    It listens for incoming messages and processes them one by one.
    
    Args:
        ws: The WebSocket connection to the client
    """
    # Get the client's IP address for logging purposes
    peer = ws.remote_address
    logging.info("Client connected: %s", peer)
    
    try:
        # Keep listening for messages from this client until they disconnect
        async for raw in ws:
            # Log the raw message for debugging
            logging.debug("Raw message from %s: %s", peer, raw)
            
            # Parse the incoming message and handle parsing errors gracefully
            try:
                request = parse_request(raw)
            except RPCError as e:
                # If the message is malformed, send an error response and continue
                await ws.send(json.dumps(e.to_dict()))
                continue

            # Extract the essential parts of the request
            request_id = request["request_id"]  # Unique ID for this request
            action = request["action"]          # The function to call
            params = request.get("params", {})  # Parameters for the function call

            # Look up the function in our registry
            func: Callable[..., Any] = FUNCTION_REGISTRY.get(action)
            
            # If the function doesn't exist, send an error response
            if func is None:
                err = RPCError(
                    request_id=request_id,
                    code="unknown_action",
                    message=f"Unknown action '{action}'"
                )
                await ws.send(json.dumps(err.to_dict()))
                continue

            try:
                # Execute the function - handle both sync and async functions
                if asyncio.iscoroutinefunction(func):
                    # If it's an async function, await it
                    result = await func(**params)
                else:
                    # If it's a regular function, call it directly
                    result = func(**params)

                # Send the successful result back to the client
                resp = make_response(request_id=request_id, status="ok", result=result)
                await ws.send(json.dumps(resp))

            except TypeError as e:
                # If the function was called with wrong parameter types
                err = RPCError(request_id=request_id, code="invalid_params", message=str(e))
                await ws.send(json.dumps(err.to_dict()))

            except Exception as e:
                # For any other unexpected errors, log them and send a server error
                logging.exception("Unhandled error while executing '%s'", action)
                err = RPCError(request_id=request_id, code="server_error", message=str(e))
                await ws.send(json.dumps(err.to_dict()))

    except websockets.ConnectionClosed:
        # The client disconnected normally
        logging.info("Client disconnected: %s", peer)
    except Exception:
        # Something unexpected happened at the connection level
        logging.exception("Unexpected connection-level error for client %s", peer)


async def main(host: str = "localhost", port: int = 8000):
    """
    Start the WebSocket server and keep it running indefinitely.
    
    Args:
        host: The hostname to bind to (usually localhost for development)
        port: The port number to listen on
    """
    logging.info("Starting RPC WebSocket server on ws://%s:%d", host, port)
    # Create the WebSocket server and keep it running forever
    async with websockets.serve(handle_connection, host, port):
        # This line keeps the server running - it never completes
        await asyncio.Future()


if __name__ == "__main__":
    try:
        # Start the server when the script is run directly
        asyncio.run(main())
    except KeyboardInterrupt:
        # Handle Ctrl+C
        logging.info("Server shutting down.")