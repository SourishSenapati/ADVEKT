"""
Agentic ChemEng - Thermo Tool Definitions & Schemas for MCP & Agent Suites
"""

THERMO_TOOLS = [
    {
        "name": "thermo_steam_properties",
        "description": "Calculates thermodynamic properties of steam and water (enthalpy, entropy, density, specific volume, saturation pressure/temperature) per ASME STEAM-TA / IAPWS.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "temperature_C": {"type": "number", "description": "Temperature in °C (optional if pressure_bar is provided)"},
                "pressure_bar": {"type": "number", "description": "Pressure in bar absolute (optional if temperature_C is provided)"}
            },
            "required": []
        }
    },
    {
        "name": "thermo_peng_robinson_eos",
        "description": "Computes compressibility factor Z, fugacity coefficients phi, and two-phase envelope using the Peng-Robinson Cubic Equation of State (PR-EOS).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "compounds": {"type": "array", "items": {"type": "string"}, "description": "List of component names (e.g. ['methane', 'ethane', 'propane', 'water', 'ethanol'])"},
                "mole_fractions": {"type": "array", "items": {"type": "number"}, "description": "Mole fractions of components summing to 1.0"},
                "temperature_C": {"type": "number", "description": "System temperature in °C"},
                "pressure_bar": {"type": "number", "description": "System pressure in bar absolute"}
            },
            "required": ["compounds", "mole_fractions", "temperature_C", "pressure_bar"]
        }
    }
]

