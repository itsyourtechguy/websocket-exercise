"""
RPC Protocol Definition
=======================
Defines the message format and parsing/validation rules for our WebSocket RPC system.
"""

import json
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class RPCError(Exception):
    """
    Represents an error that occurs during RPC processing.
    
    Args:
        request_id: The ID of the original request (or None if parsing failed)
        code: A short error code for programmatic handling
        message: A human-readable description of the error
    """
    request_id: Optional[str]
    code: str
    message: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert the error to a dictionary that can be JSON-serialized."""
        return {
            "request_id": self.request_id,
            "status": "error",
            "error": {
                "code": self.code,
                "message": self.message
            },
        }


def parse_request(raw: str) -> Dict[str, Any]:
    """
    Convert a raw JSON string into a structured request dictionary.
    
    Args:
        raw: The raw JSON string received from the client
        
    Returns:
        A dictionary with the parsed request data
        
    Raises:
        RPCError: If the message is invalid in any way
    """
    # First, try to parse the JSON
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        # If it's not valid JSON, we can't even determine the request_id
        raise RPCError(
            request_id=None,
            code="invalid_json",
            message="Payload is not valid JSON"
        )

    # The message must be a JSON object (dictionary), not a string or array
    if not isinstance(payload, dict):
        raise RPCError(None, "invalid_payload", "Payload must be a JSON object")

    # Extract the request ID (used to match responses to requests)
    request_id = payload.get("request_id")

    # Every request must have an action (which function to call)
    action = payload.get("action")
    if not action or not isinstance(action, str):
        raise RPCError(request_id, "invalid_action", "Missing or invalid 'action'")

    # Parameters must be a dictionary (can be empty)
    params = payload.get("params", {})
    if not isinstance(params, dict):
        raise RPCError(request_id, "invalid_params", "'params' must be a dictionary")

    # Return the validated, structured request
    return {
        "request_id": request_id,
        "action": action,
        "params": params
    }


def make_response(request_id: Optional[str], status: str, result: Any = None) -> Dict[str, Any]:
    """
    Create a standardized response message.
    
    Args:
        request_id: The ID of the original request (for matching responses)
        status: Either "ok" for success or "error" for failure
        result: The result of the function call (for success) or error details (for failure)
        
    Returns:
        A dictionary representing the response message
    """
    # Start with the basic structure
    base = {
        "request_id": request_id,
        "status": status
    }

    # Add either the result (success) or error details (failure)
    if status == "ok":
        base["result"] = result
    else:
        base["error"] = result

    return base