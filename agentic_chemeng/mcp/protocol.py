"""
Agentic ChemEng - MCP JSON-RPC 2.0 Protocol Handler
Conforms to Model Context Protocol specification 2024-11-05.
"""

import json
import traceback

MCP_VERSION = "2024-11-05"
SERVER_NAME = "agentic-chemeng-mcp"
SERVER_VERSION = "1.0.0"


def format_response(req_id, result):
    return json.dumps({
        "jsonrpc": "2.0",
        "id": req_id,
        "result": result
    })


def format_error(req_id, code, message):
    return json.dumps({
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {
            "code": code,
            "message": message
        }
    })


def format_tool_content(data):
    return {
        "content": [
            {
                "type": "text",
                "text": json.dumps(data, indent=2, default=str)
            }
        ]
    }

