"""
Agentic ChemEng - Honeywell UniSim Tool Definitions & Schemas for MCP & Agent Suites
"""

UNISIM_TOOLS = [
    {
        "name": "unisim_get_status",
        "description": "Checks connectivity with Honeywell UniSim Design COM automation server (UniSimDesign.Application).",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "unisim_inspect_case",
        "description": "Parses and inspects a Honeywell UniSim simulation case (.usc, .hsc), reporting property packages and operations.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "filepath": {"type": "string", "description": "Path to UniSim case file (.usc, .hsc)"}
            },
            "required": ["filepath"]
        }
    }
]

