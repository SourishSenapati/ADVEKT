"""
Agentic ChemEng - Ansys Fluent & CFX Tool Definitions & Schemas for MCP & Agent Suites
"""

ANSYS_TOOLS = [
    {
        "name": "ansys_get_status",
        "description": "Checks connectivity with Ansys Fluent & CFX, detecting AWP_ROOT environment installations and batch solvers.",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "ansys_inspect_case",
        "description": "Inspects an Ansys Fluent / CFX case file (.cas, .cas.gz, .msh), extracting dimension, boundary conditions, cell zones, and reacting flow models.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "filepath": {"type": "string", "description": "Path to Ansys case file (.cas, .cas.gz, .cas.h5, .msh)"}
            },
            "required": ["filepath"]
        }
    },
    {
        "name": "ansys_run_journal",
        "description": "Dispatches headless batch CFD calculation in Ansys Fluent via journal script (fluent 3ddp -g -i script.jou) with timeout supervision.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "journal_path": {"type": "string", "description": "Path to Fluent journal file (.jou, .txt)"},
                "dimensions": {"type": "string", "description": "Solver architecture (default: 3ddp; or 2ddp, 3d, 2d)"},
                "timeout_sec": {"type": "number", "description": "Timeout in seconds (default: 180.0)"}
            },
            "required": ["journal_path"]
        }
    }
]
