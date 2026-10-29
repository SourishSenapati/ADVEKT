"""
Agentic ChemEng - PRO/II Tool Definitions & Schemas for MCP & Agent Suites
"""

PROII_TOOLS = [
    {
        "name": "proii_get_status",
        "description": "Checks connectivity with AVEVA SimSci PRO/II COM automation server (PROII.Application).",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "proii_inspect_flowsheet",
        "description": "Parses and inspects an AVEVA SimSci PRO/II simulation archive (.prz, .pr2, .inp), extracting unit operations and streams.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "filepath": {"type": "string", "description": "Path to PRO/II simulation archive (.prz, .pr2, .inp)"}
            },
            "required": ["filepath"]
        }
    },
    {
        "name": "proii_run_simulation",
        "description": "Triggers the PRO/II flowsheet calculation engine on the active simulation case.",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
]

