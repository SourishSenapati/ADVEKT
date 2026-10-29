"""
Agentic ChemEng - Siemens gPROMS Tool Definitions & Schemas for MCP & Agent Suites
"""

GPROMS_TOOLS = [
    {
        "name": "gproms_get_status",
        "description": "Checks connectivity with Siemens/PSE gPROMS ProcessBuilder & ModelBuilder, checking CLI executable and COM registration.",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "gproms_inspect_project",
        "description": "Parses and inspects a Siemens gPROMS project file (.gPJ, .gPA, .xml), extracting equation-oriented models, processes, tasks, and variable types.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "filepath": {"type": "string", "description": "Path to gPROMS project file (.gPJ, .gPA, .xml, .txt)"}
            },
            "required": ["filepath"]
        }
    },
    {
        "name": "gproms_run_simulation",
        "description": "Executes batch simulation of a gPROMS project/process via gproms.exe -batch with hard execution timeout.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "filepath": {"type": "string", "description": "Path to gPROMS project file"},
                "process_name": {"type": "string", "description": "Specific process entity to simulate (optional)"},
                "timeout_sec": {"type": "number", "description": "Timeout in seconds (default: 60.0)"}
            },
            "required": ["filepath"]
        }
    }
]
