"""
Agentic ChemEng - COMSOL Multiphysics Tool Definitions & Schemas for MCP & Agent Suites
"""

COMSOL_TOOLS = [
    {
        "name": "comsol_get_status",
        "description": "Checks connectivity with COMSOL Multiphysics, detecting batch CLI binaries and license availability.",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "comsol_inspect_model",
        "description": "Inspects a COMSOL Multiphysics model file (.mph), extracting physics interfaces (Reaction Engineering, Transport of Diluted Species, Heat Transfer, Flow), geometries, studies, and parameters.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "filepath": {"type": "string", "description": "Path to COMSOL model file (.mph)"}
            },
            "required": ["filepath"]
        }
    },
    {
        "name": "comsol_run_study",
        "description": "Dispatches headless batch simulation of a COMSOL model (.mph) via comsol batch CLI with timeout supervision.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "filepath": {"type": "string", "description": "Path to COMSOL model file (.mph)"},
                "study_tag": {"type": "string", "description": "Specific study tag (e.g. std1) to solve"},
                "output_path": {"type": "string", "description": "Output path for solved .mph file"},
                "timeout_sec": {"type": "number", "description": "Timeout in seconds (default: 120.0)"}
            },
            "required": ["filepath"]
        }
    }
]
