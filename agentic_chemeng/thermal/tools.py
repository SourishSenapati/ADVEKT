"""
Agentic ChemEng - Thermal Tool Definitions & Schemas for MCP & Agent Suites
"""

THERMAL_TOOLS = [
    {
        "name": "thermal_lmtd_calculation",
        "description": "Calculates Logarithmic Mean Temperature Difference (LMTD) and FT configuration correction factor for heat exchangers.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "th_in": {"type": "number", "description": "Hot stream inlet temperature in °C"},
                "th_out": {"type": "number", "description": "Hot stream outlet temperature in °C"},
                "tc_in": {"type": "number", "description": "Cold stream inlet temperature in °C"},
                "tc_out": {"type": "number", "description": "Cold stream outlet temperature in °C"},
                "shell_passes": {"type": "integer", "description": "Number of shell passes (default: 1)"},
                "tube_passes": {"type": "integer", "description": "Number of tube passes (default: 2)"}
            },
            "required": ["th_in", "th_out", "tc_in", "tc_out"]
        }
    },
    {
        "name": "thermal_rate_tema_shell_and_tube",
        "description": "Rates a TEMA E shell-and-tube heat exchanger via Kern method, computing clean/fouled U, actual vs required area, and overdesign margin.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "duty_kW": {"type": "number", "description": "Heat duty in kW"},
                "th_in": {"type": "number", "description": "Hot stream inlet temperature in °C"},
                "th_out": {"type": "number", "description": "Hot stream outlet temperature in °C"},
                "tc_in": {"type": "number", "description": "Cold stream inlet temperature in °C"},
                "tc_out": {"type": "number", "description": "Cold stream outlet temperature in °C"},
                "shell_id_mm": {"type": "number", "description": "Shell internal diameter in mm (default: 600)"},
                "tube_od_mm": {"type": "number", "description": "Tube outside diameter in mm (default: 19.05)"},
                "tube_wt_mm": {"type": "number", "description": "Tube wall thickness in mm (default: 1.65)"},
                "tube_length_m": {"type": "number", "description": "Tube length in meters (default: 4.0)"},
                "tube_count": {"type": "integer", "description": "Total number of tubes (default: 240)"}
            },
            "required": ["duty_kW", "th_in", "th_out", "tc_in", "tc_out"]
        }
    },
    {
        "name": "thermal_mvr_evaporator_design",
        "description": "Designs an MVR (Mechanical Vapor Recompression) falling film evaporator, sizing heat transfer area, compressor shaft power, and specific energy consumption.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "feed_flow_kg_h": {"type": "number", "description": "Feed flow rate in kg/h"},
                "feed_solids_pct": {"type": "number", "description": "Feed dry solids percentage (e.g. 5.0)"},
                "product_solids_pct": {"type": "number", "description": "Product dry solids percentage (e.g. 35.0)"},
                "evaporator_temp_C": {"type": "number", "description": "Evaporator boiling temperature in °C (default: 80.0)"},
                "compressor_temp_rise_C": {"type": "number", "description": "Vapor compressor saturation temperature lift in °C (default: 8.0)"}
            },
            "required": ["feed_flow_kg_h", "feed_solids_pct", "product_solids_pct"]
        }
    }
]

