"""
Agentic ChemEng - CHEMCAD Tool Definitions & Schemas for MCP & Agent Suites
"""

CHEMCAD_TOOLS = [
    {
        "name": "chemcad_get_status",
        "description": "Checks connectivity with Chemstations CHEMCAD COM automation server (CHEMCAD.Application) and reports license status.",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "chemcad_inspect_flowsheet",
        "description": "Parses and inspects a CHEMCAD flowsheet file (.ccx, .cc5, .cc6), extracting unit operations, streams, and property methods.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "filepath": {"type": "string", "description": "Path to CHEMCAD case file (.ccx, .cc5, .cc6)"}
            },
            "required": ["filepath"]
        }
    },
    {
        "name": "chemcad_run_simulation",
        "description": "Triggers the CHEMCAD simulation solver on the active flowsheet.",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
]

