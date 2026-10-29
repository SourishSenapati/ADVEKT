"""
Agentic ChemEng - Aspen Plus Tool Definitions & Schemas for MCP & Agent Suites
"""

ASPEN_PLUS_TOOLS = [
    {
        "name": "aspen_plus_get_status",
        "description": "Checks connectivity with Aspen Plus 40.0 OLE Services (Apwn.Document COM server), software version, and licensing state.",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "aspen_plus_open_simulation",
        "description": "Opens a native Aspen Plus simulation file (.bkp, .apw, or .inp).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "filepath": {"type": "string", "description": "Absolute or relative path to the simulation file (.bkp, .apw, or .inp)"}
            },
            "required": ["filepath"]
        }
    },
    {
        "name": "aspen_plus_inspect_flowsheet",
        "description": "Extracts flowsheet topology, unit operation blocks, process streams, and thermodynamic property methods (STEAM-TA, NRTL, ELECNRTL).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "filepath": {"type": "string", "description": "Optional path to simulation file"}
            },
            "required": []
        }
    },
    {
        "name": "aspen_plus_get_stream_table",
        "description": "Returns the complete converged stream balance table (temperature, pressure, mass flow rate, vapor fraction, enthalpy).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "filepath": {"type": "string", "description": "Optional path to simulation file"}
            },
            "required": []
        }
    },
    {
        "name": "aspen_plus_get_block_data",
        "description": "Extracts technical schedule and thermal performance data for unit operation blocks (heat duty, outlet temperature/pressure).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "filepath": {"type": "string", "description": "Optional path to simulation file"},
                "block_id": {"type": "string", "description": "Specific block identifier (e.g. EVAP-1, FLASH-1, COND-1)"}
            },
            "required": []
        }
    },
    {
        "name": "aspen_plus_run_simulation",
        "description": "Executes the rigorous Aspen Plus simulation engine (Run2) on the loaded flowsheet.",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
]

