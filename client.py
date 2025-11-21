"""
WebSocket RPC Client
====================
A client that can call functions on the WebSocket RPC server.
"""

import asyncio
import json
import logging
import uuid
from typing import Any, Dict

import websockets

# The server URL
SERVER_URL = "ws://localhost:8000"

# Set up logging to see what's happening
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


async def call_action(action: str, params: Dict[str, Any], timeout: float = 5.0) -> Dict[str, Any]:
    """
    Make a remote procedure call to the server.
    
    This function handles the complete request-response cycle:
    1. Creates a unique request ID
    2. Sends the request to the server
    3. Waits for and validates the response
    4. Returns the server's response
    
    Args:
        action: The name of the function to call (e.g., "add_numbers")
        params: The parameters to pass to the function (e.g., {"a": 5, "b": 3})
        timeout: Maximum time to wait for a response (in seconds)
        
    Returns:
        The server's response as a dictionary
        
    Raises:
        RuntimeError: If the response doesn't match the request
        asyncio.TimeoutError: If the server doesn't respond in time
    """
    # Generate a unique ID for this request - this is crucial for matching responses
    # If multiple calls are made simultaneously, each needs its own ID
    request_id = str(uuid.uuid4())
    
    # Create the request message following our protocol
    payload = {
        "request_id": request_id,  # So the server knows which request this is
        "action": action,          # Which function to call
        "params": params,          # The arguments to pass
    }

    # Connect to the server, send the request, and wait for the response
    # The 'async with' ensures the connection is properly closed
    async with websockets.connect(SERVER_URL) as ws:
        # Send the request to the server
        await ws.send(json.dumps(payload))
        
        # Wait for the response (with a timeout to prevent hanging)
        raw = await asyncio.wait_for(ws.recv(), timeout=timeout)
        
        # Parse the response
        response = json.loads(raw)

        # Verify that the response is for our request
        # This is critical when making multiple concurrent calls
        if response.get("request_id") != request_id:
            raise RuntimeError("Unexpected response ID")

        return response


async def main():
    """
    Demonstrate the client by making several function calls.
    
    This shows that the client works correctly by making multiple calls
    with different parameters and printing the results.
    """
    # Make several calls to demonstrate the system works
    print("Calling add_numbers(10, 20):")
    print(await call_action("add_numbers", {"a": 10, "b": 20}))
    
    print("\nCalling multiply_numbers(3, 7):")
    print(await call_action("multiply_numbers", {"a": 3, "b": 7}))
    
    print("\nCalling echo('hello'):")
    print(await call_action("echo", {"message": "hello"}))


if __name__ == "__main__":
    # Run the demonstration when the script is executed directly
    asyncio.run(main())