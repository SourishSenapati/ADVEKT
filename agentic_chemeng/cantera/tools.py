"""
Agentic ChemEng - Cantera Tool Definitions & Schemas for MCP & Agent Suites
"""

CANTERA_TOOLS = [
    {
        "name": "cantera_get_status",
        "description": "Checks connectivity with Cantera open-source chemical kinetics & thermodynamics engine.",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "cantera_arrhenius_kinetics",
        "description": "Computes reaction rate constant k and reactant conversion in batch/PFR using Arrhenius law (A, Ea, T).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "A_pre_exponential": {"type": "number", "description": "Pre-exponential frequency factor A"},
                "Ea_kJ_mol": {"type": "number", "description": "Activation energy Ea in kJ/mol"},
                "temperature_C": {"type": "number", "description": "Reaction temperature in °C"},
                "order": {"type": "number", "description": "Reaction order (default: 1.0)"},
                "initial_conc_mol_m3": {"type": "number", "description": "Initial reactant concentration in mol/m3 (default: 100.0)"},
                "time_seconds": {"type": "number", "description": "Reaction time in seconds (default: 60.0)"}
            },
            "required": ["A_pre_exponential", "Ea_kJ_mol", "temperature_C"]
        }
    },
    {
        "name": "cantera_gas_transport_properties",
        "description": "Computes gas density, dynamic viscosity (Sutherland formula), thermal conductivity (Eucken), and Prandtl number.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "gas_species": {"type": "string", "description": "'air', 'n2', 'o2', 'co2', 'h2', 'ch4', 'steam' (default: 'air')"},
                "temperature_C": {"type": "number", "description": "Temperature in °C (default: 25.0)"},
                "pressure_bar": {"type": "number", "description": "Pressure in bar (default: 1.01325)"}
            },
            "required": []
        }
    }
]

