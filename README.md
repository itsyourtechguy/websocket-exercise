<h1 align="center">WebSocket RPC Server & Client</h1>

<p align="center">
  <strong>A clean, scalable, RPC-style WebSocket implementation in Python.</strong><br>
  Asynchronous. Modular. Production-style structure. Easy to extend.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.10%2B-blue" />
  <img src="https://img.shields.io/badge/websockets-asyncio-orange" />
  <img src="https://img.shields.io/badge/tests-passing-brightgreen" />
  <img src="https://img.shields.io/badge/license-MIT-green" />
</p>

---

## 📦 Project Overview

This project implements a fully asynchronous **WebSocket RPC server** and a matching ** Python client**.  
It uses a clear message protocol, dynamic function registry, modular architecture, and structured error handling.

Perfect for demonstrating:

- async networking  
- RPC patterns  
- protocol design  
- clean Python software structure  

---

## 📁 Folder Structure

websocket-exercise/
├── server.py          # RPC WebSocket server
├── client.py          # Example RPC client
├── protocol.py        # Request parsing & response helpers
├── functions.py       # RPC function implementations
├── README.md          # Project documentation
├── requirements.txt   # Python dependencies
├── .gitignore         # Files to ignore in git
└── tests/
    └── test_functions.py  # Unit tests for functions


---

## 🔧 Requirements

- Python **3.10+**
- `websockets` library
- `pytest` (optional, for testing)

Install dependencies:

```bash
pip install websockets pytest

🚀 Getting Started
1. Clone the repository

git clone https://github.com/itsyourtechguy/websocket-exercise.git
cd websocket-exercise

2. Set up a virtual environment

python -m venv venv
source venv/bin/activate      # macOS / Linux
venv\Scripts\activate         # Windows

3. Install dependencies

pip install websockets

pip install pytest

▶️ Run the Server

python server.py

The server starts at:

ws://localhost:8000

📡 Run the Client

Open another terminal and run:

python client.py

The client performs three RPC calls:

    add_numbers

    multiply_numbers

    echo

Example output:

{'request_id': '...', 'status': 'ok', 'result': 30}
{'request_id': '...', 'status': 'ok', 'result': 21}
{'request_id': '...', 'status': 'ok', 'result': 'hello'}

🧠 Supported RPC Methods
add_numbers(a, b)

Returns a + b.
multiply_numbers(a, b)

Returns a * b.
echo(message)

Returns message unchanged.

To add new RPC functions:

    Write the function in functions.py

    Add it to FUNCTION_REGISTRY

No changes needed in server/client code.
🔌 RPC Message Protocol
Request Format

{
  "request_id": "uuid-string",
  "action": "add_numbers",
  "params": { "a": 5, "b": 10 }
}

Success Response

{
  "request_id": "uuid-string",
  "status": "ok",
  "result": 15
}

Error Response

{
  "request_id": "uuid-string",
  "status": "error",
  "error": {
    "code": "invalid_params",
    "message": "Parameters 'a' and 'b' must be numbers"
  }
}

🧪 Testing

Tests are located in the tests/ directory.

Run them:

pytest -q

Expected:

4 passed in X.XXs

📘 Reference

The exercise PDF provided is stored at:

/mnt/data/Coding Exercise @ Synapse_251120_170332.pdf

📄 License

MIT License.
Use freely for education or production.
⭐ Final Notes

This project intentionally uses:

    clear separation of concerns

    dynamic RPC behavior

    typed, validated message protocol

    async WebSocket networking