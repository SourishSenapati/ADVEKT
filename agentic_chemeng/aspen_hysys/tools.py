"""
Agentic ChemEng - Aspen HYSYS Tool Definitions & Schemas for MCP & Agent Suites
"""

ASPEN_HYSYS_TOOLS = [
    {
        "name": "aspen_hysys_get_status",
        "description": "Checks connectivity with Aspen HYSYS COM server (HYSYS.Application), active simulation cases, and solver state.",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "aspen_hysys_open_case",
        "description": "Opens an Aspen HYSYS simulation case (.hsc) via COM automation.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "filepath": {"type": "string", "description": "Absolute or relative path to the .hsc case file."}
            },
            "required": ["filepath"]
        }
    },
    {
        "name": "aspen_hysys_inspect_case",
        "description": "Extracts material streams, unit operations, and property packages from the active or specified HYSYS simulation case.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "filepath": {"type": "string", "description": "Optional path to the .hsc file. If omitted, inspects active case."}
            },
            "required": []
        }
    },
    {
        "name": "aspen_hysys_solve",
        "description": "Triggers or resumes the flowsheet solver in the active Aspen HYSYS simulation case.",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
]

