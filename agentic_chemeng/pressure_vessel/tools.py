"""
Agentic ChemEng - Pressure Vessel Tool Definitions & Schemas for MCP & Agent Suites
"""

PRESSURE_VESSEL_TOOLS = [
    {
        "name": "pv_asme_ug27_shell",
        "description": "Calculates minimum required cylindrical shell thickness and MAWP per ASME BPVC Section VIII Division 1 UG-27(c)(1).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "design_pressure_bar": {"type": "number", "description": "Design internal pressure in bar"},
                "inside_diameter_mm": {"type": "number", "description": "Inside shell diameter in mm"},
                "design_temp_C": {"type": "number", "description": "Design temperature in °C (default: 100.0)"},
                "material": {"type": "string", "description": "ASME specification material, e.g. 'SA-240 316L', 'SA-240 304', 'SA-516 Gr 70'"},
                "weld_joint_efficiency": {"type": "number", "description": "Joint efficiency E (1.0 = full RT, 0.85 = spot RT, 0.70 = no RT)"},
                "corrosion_allowance_mm": {"type": "number", "description": "Corrosion allowance in mm (default: 1.5)"}
            },
            "required": ["design_pressure_bar", "inside_diameter_mm"]
        }
    },
    {
        "name": "pv_asme_ug32_head",
        "description": "Calculates minimum required 2:1 ellipsoidal or torispherical dished head thickness per ASME Section VIII Division 1 UG-32.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "design_pressure_bar": {"type": "number", "description": "Design internal pressure in bar"},
                "inside_diameter_mm": {"type": "number", "description": "Inside diameter in mm"},
                "head_type": {"type": "string", "description": "'ellipsoidal_2_1' or 'torispherical' (default: 'ellipsoidal_2_1')"},
                "design_temp_C": {"type": "number", "description": "Design temperature in °C"},
                "material": {"type": "string", "description": "ASME specification material"},
                "weld_joint_efficiency": {"type": "number", "description": "Joint efficiency (default: 1.0)"},
                "corrosion_allowance_mm": {"type": "number", "description": "Corrosion allowance in mm (default: 1.5)"}
            },
            "required": ["design_pressure_bar", "inside_diameter_mm"]
        }
    },
    {
        "name": "pv_asme_ug37_nozzle",
        "description": "Calculates nozzle opening reinforcement area replacement (A_req vs A_avail) per ASME Section VIII Division 1 UG-37.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "vessel_id_mm": {"type": "number", "description": "Vessel shell inside diameter in mm"},
                "shell_thickness_mm": {"type": "number", "description": "Actual shell nominal thickness in mm"},
                "nozzle_od_mm": {"type": "number", "description": "Nozzle neck outside diameter in mm"},
                "nozzle_thickness_mm": {"type": "number", "description": "Nozzle neck wall thickness in mm"},
                "design_pressure_bar": {"type": "number", "description": "Design pressure in bar"},
                "design_temp_C": {"type": "number", "description": "Design temperature in °C"},
                "material": {"type": "string", "description": "ASME specification material"},
                "corrosion_allowance_mm": {"type": "number", "description": "Corrosion allowance in mm"}
            },
            "required": ["vessel_id_mm", "shell_thickness_mm", "nozzle_od_mm", "nozzle_thickness_mm", "design_pressure_bar"]
        }
    },
    {
        "name": "pv_asme_ug99_hydro",
        "description": "Computes mandatory proof hydrostatic test pressure per ASME Section VIII Division 1 UG-99(b).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "design_pressure_bar": {"type": "number", "description": "Design pressure in bar"},
                "design_temp_C": {"type": "number", "description": "Design temperature in °C (default: 100.0)"},
                "material": {"type": "string", "description": "Vessel material (default: 'SA-240 316L')"}
            },
            "required": ["design_pressure_bar"]
        }
    }
]

