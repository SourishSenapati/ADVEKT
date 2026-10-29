"""
Agentic ChemEng - DWSIM Tool Definitions & Schemas for MCP & Agent Suites
"""

DWSIM_TOOLS = [
    {
        "name": "dwsim_get_status",
        "description": "Checks DWSIM installation status, version, and CAPE-OPEN thermodynamic packages supported.",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "dwsim_inspect_flowsheet",
        "description": "Parses and inspects an open-source DWSIM flowsheet file (.dwsim, .dwxml), extracting compounds, property packages, material streams, and unit operations.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "filepath": {"type": "string", "description": "Path to .dwsim or .dwxml flowsheet file"}
            },
            "required": ["filepath"]
        }
    },
    {
        "name": "dwsim_flash_calculation",
        "description": "Performs rigorous vapor-liquid equilibrium (VLE) flash calculations (isothermal/isobaric TP flash) using Rachford-Rice equation.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "temperature_C": {"type": "number", "description": "Temperature in degrees Celsius"},
                "pressure_bar": {"type": "number", "description": "System pressure in bar absolute"},
                "compounds": {"type": "array", "items": {"type": "string"}, "description": "List of compound names"},
                "mole_fractions": {"type": "array", "items": {"type": "number"}, "description": "List of feed mole fractions corresponding to compounds"}
            },
            "required": ["temperature_C", "pressure_bar", "compounds", "mole_fractions"]
        }
    }
]

