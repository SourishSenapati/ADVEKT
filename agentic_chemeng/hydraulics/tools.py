"""
Agentic ChemEng - Hydraulics Tool Definitions & Schemas for MCP & Agent Suites
"""

HYDRAULICS_TOOLS = [
    {
        "name": "hydraulics_pipe_dimensions",
        "description": "Retrieves ASME B36.10M / B36.19M standard pipe dimensions (OD, wall thickness, ID, internal area) for given DN and schedule.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "dn_mm": {"type": "integer", "description": "Nominal diameter DN in mm (15, 20, 25, 40, 50, 80, 100, 150, 200, 250, 300, 400, 500, 600)"},
                "schedule": {"type": "string", "description": "Pipe schedule: 'sch10', 'sch40', or 'sch80' (default: 'sch40')"}
            },
            "required": ["dn_mm"]
        }
    },
    {
        "name": "hydraulics_pressure_drop",
        "description": "Computes line velocity, Reynolds number, Colebrook-White friction factor, and Darcy-Weisbach pressure drop with fittings minor losses.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "flow_m3_h": {"type": "number", "description": "Volumetric flow rate in m3/h"},
                "pipe_dn_mm": {"type": "integer", "description": "Nominal diameter DN in mm"},
                "length_m": {"type": "number", "description": "Equivalent or straight pipe length in meters"},
                "fluid": {"type": "string", "description": "Fluid identifier (default: 'water')"},
                "density_kg_m3": {"type": "number", "description": "Fluid density in kg/m3 (default: 998.2)"},
                "viscosity_cp": {"type": "number", "description": "Dynamic viscosity in cP (default: 1.002)"},
                "schedule": {"type": "string", "description": "Pipe schedule (default: 'sch40')"},
                "fittings": {"type": "object", "description": "Dict of fitting types and counts, e.g. {'elbow_90_lr': 4, 'gate_valve_full_open': 2}"}
            },
            "required": ["flow_m3_h", "pipe_dn_mm", "length_m"]
        }
    },
    {
        "name": "hydraulics_pump_head_npsha",
        "description": "Computes Centrifugal Pump Total Dynamic Head (TDH), NPSHa, hydraulic power, brake power (BHP), and recommended IEC motor rating.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "flow_m3_h": {"type": "number", "description": "Operating flow rate in m3/h"},
                "static_head_m": {"type": "number", "description": "Static elevation difference between source and destination in meters"},
                "discharge_press_barg": {"type": "number", "description": "Discharge vessel pressure in barg"},
                "suction_press_barg": {"type": "number", "description": "Suction vessel pressure in barg"},
                "suction_loss_m": {"type": "number", "description": "Total head loss in suction piping in meters"},
                "discharge_loss_m": {"type": "number", "description": "Total head loss in discharge piping in meters"},
                "fluid_density_kg_m3": {"type": "number", "description": "Fluid density in kg/m3 (default: 998.2)"},
                "vapor_press_bara": {"type": "number", "description": "Fluid vapor pressure at pumping temperature in bara (default: 0.0234)"},
                "suction_static_lift_m": {"type": "number", "description": "Suction static liquid level above pump centerline in meters (positive for flooded suction)"},
                "pump_eff": {"type": "number", "description": "Pump hydraulic efficiency (default: 0.72)"}
            },
            "required": ["flow_m3_h", "static_head_m", "discharge_press_barg", "suction_press_barg", "suction_loss_m", "discharge_loss_m"]
        }
    }
]

