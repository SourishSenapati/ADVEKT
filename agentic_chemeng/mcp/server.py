"""
Agentic ChemEng - Unified Chemical & Mechanical Engineering MCP Server (Industrial Hardened)
Project Ref: FNQ-PR-2026-001 | Lead Engineer: Sourish Senapati (FinnoaQ Agro-Industrial Technologies Ltd.)

Exposes a comprehensive Model Context Protocol (MCP) JSON-RPC 2.0 server across:
1. Dassault Systèmes SOLIDWORKS 2025 (Parametric 3D B-Rep CAD, assemblies, BPE, mass properties).
2. Aspen Technology Aspen Plus V14 (Apwn.Document OLE flowsheet automation & converged streams).
3. Aspen Technology Aspen HYSYS (HYSYS.Application COM automation & property packages).
4. DWSIM (Open-source chemical process simulation & CAPE-OPEN thermodynamics).
5. Autodesk AutoCAD 2025 (P&ID, General Arrangement drawings, DWG/DXF/PDF vector pipelines).
6. Thermodynamics Engine (ASME STEAM-TA steam properties, Peng-Robinson Cubic EOS).
7. Process Hydraulics (Darcy-Weisbach, Colebrook-White, ASME B36.10M pipe schedules, Pump TDH, NPSHa).
8. Industrial Thermal Design (TEMA Shell-and-Tube rating via Kern method, MVR Falling-Film Evaporator sizing).
9. ASME BPVC Section VIII Div 1 (UG-27 shell thickness, UG-32 formed heads, UG-37 nozzle reinforcement, UG-99 hydro test).
"""

import json
import os
import signal
import sys
import traceback

from ..solidworks.controller import SolidWorksController
from ..solidworks.tools import SOLIDWORKS_TOOLS, dispatch_solidworks_tool
from ..aspen_plus.controller import AspenPlusController
from ..aspen_plus.tools import ASPEN_PLUS_TOOLS
from ..aspen_hysys.controller import AspenHysysController
from ..aspen_hysys.tools import ASPEN_HYSYS_TOOLS
from ..dwsim.controller import DwsimController
from ..dwsim.tools import DWSIM_TOOLS
from ..autocad.controller import AutoCADController
from ..autocad.tools import AUTOCAD_TOOLS, dispatch_autocad_tool

from ..thermo.equations import calculate_steam_properties, peng_robinson_eos
from ..thermo.tools import THERMO_TOOLS
from ..hydraulics.equations import get_pipe_dimensions, calculate_pressure_drop, calculate_pump_tdh_and_npsha
from ..hydraulics.tools import HYDRAULICS_TOOLS
from ..thermal.equations import calculate_lmtd, rate_tema_shell_and_tube, design_mvr_evaporator
from ..thermal.tools import THERMAL_TOOLS
from ..pressure_vessel.equations import (
    calculate_shell_thickness_ug27,
    calculate_dished_head_ug32,
    calculate_nozzle_reinforcement_ug37,
    calculate_hydrostatic_test_ug99
)
from ..pressure_vessel.tools import PRESSURE_VESSEL_TOOLS

from .protocol import (
    MCP_VERSION,
    SERVER_NAME,
    SERVER_VERSION,
    format_response,
    format_error,
    format_tool_content
)

# Global controller singletons
sw_controller = SolidWorksController(visible=False)
aspen_plus_controller = AspenPlusController()
aspen_hysys_controller = AspenHysysController()
dwsim_controller = DwsimController()
autocad_controller = AutoCADController()

ALL_TOOLS = (
    SOLIDWORKS_TOOLS +
    ASPEN_PLUS_TOOLS +
    ASPEN_HYSYS_TOOLS +
    DWSIM_TOOLS +
    AUTOCAD_TOOLS +
    THERMO_TOOLS +
    HYDRAULICS_TOOLS +
    THERMAL_TOOLS +
    PRESSURE_VESSEL_TOOLS
)


def dispatch_aspen_plus_tool(controller, tool_name, args):
    if tool_name == "aspen_plus_get_status":
        return controller.get_status()
    elif tool_name == "aspen_plus_open_simulation":
        return controller.open_simulation(args["filepath"])
    elif tool_name == "aspen_plus_inspect_flowsheet":
        return controller.inspect_flowsheet(args.get("filepath"))
    elif tool_name == "aspen_plus_get_stream_table":
        return controller.get_stream_table(args.get("filepath"))
    elif tool_name == "aspen_plus_get_block_data":
        return controller.get_block_data(args.get("filepath"), args.get("block_id"))
    elif tool_name == "aspen_plus_run_simulation":
        return controller.run_simulation()
    raise ValueError(f"Unknown Aspen Plus tool: {tool_name}")


def dispatch_aspen_hysys_tool(controller, tool_name, args):
    if tool_name == "aspen_hysys_get_status":
        return controller.get_status()
    elif tool_name == "aspen_hysys_open_case":
        return controller.open_case(args["filepath"])
    elif tool_name == "aspen_hysys_inspect_case":
        return controller.inspect_case(args.get("filepath"))
    elif tool_name == "aspen_hysys_solve":
        return controller.solve()
    raise ValueError(f"Unknown Aspen HYSYS tool: {tool_name}")


def dispatch_dwsim_tool(controller, tool_name, args):
    if tool_name == "dwsim_get_status":
        return controller.get_status()
    elif tool_name == "dwsim_inspect_flowsheet":
        return controller.inspect_flowsheet(args["filepath"])
    elif tool_name == "dwsim_flash_calculation":
        return controller.flash_calculation(
            temperature_C=args["temperature_C"],
            pressure_bar=args["pressure_bar"],
            compounds=args["compounds"],
            mole_fractions=args["mole_fractions"]
        )
    raise ValueError(f"Unknown DWSIM tool: {tool_name}")


def dispatch_thermo_tool(tool_name, args):
    if tool_name == "thermo_steam_properties":
        return calculate_steam_properties(
            temperature_C=args.get("temperature_C"),
            pressure_bar=args.get("pressure_bar")
        )
    elif tool_name == "thermo_peng_robinson_eos":
        return peng_robinson_eos(
            compounds=args["compounds"],
            mole_fractions=args["mole_fractions"],
            temperature_C=args["temperature_C"],
            pressure_bar=args["pressure_bar"]
        )
    raise ValueError(f"Unknown Thermo tool: {tool_name}")


def dispatch_hydraulics_tool(tool_name, args):
    if tool_name == "hydraulics_pipe_dimensions":
        return get_pipe_dimensions(
            dn_mm=args["dn_mm"],
            schedule=args.get("schedule", "sch40")
        )
    elif tool_name == "hydraulics_pressure_drop":
        return calculate_pressure_drop(
            flow_m3_h=args["flow_m3_h"],
            pipe_dn_mm=args["pipe_dn_mm"],
            length_m=args["length_m"],
            fluid=args.get("fluid", "water"),
            density_kg_m3=args.get("density_kg_m3", 998.2),
            viscosity_cp=args.get("viscosity_cp", 1.002),
            schedule=args.get("schedule", "sch40"),
            fittings=args.get("fittings")
        )
    elif tool_name == "hydraulics_pump_head_npsha":
        return calculate_pump_tdh_and_npsha(
            flow_m3_h=args["flow_m3_h"],
            static_head_m=args["static_head_m"],
            discharge_press_barg=args["discharge_press_barg"],
            suction_press_barg=args["suction_press_barg"],
            suction_loss_m=args["suction_loss_m"],
            discharge_loss_m=args["discharge_loss_m"],
            fluid_density_kg_m3=args.get("fluid_density_kg_m3", 998.2),
            vapor_press_bara=args.get("vapor_press_bara", 0.0234),
            suction_static_lift_m=args.get("suction_static_lift_m", 0.0),
            pump_eff=args.get("pump_eff", 0.72)
        )
    raise ValueError(f"Unknown Hydraulics tool: {tool_name}")


def dispatch_thermal_tool(tool_name, args):
    if tool_name == "thermal_lmtd_calculation":
        return calculate_lmtd(
            th_in=args["th_in"],
            th_out=args["th_out"],
            tc_in=args["tc_in"],
            tc_out=args["tc_out"],
            shell_passes=args.get("shell_passes", 1),
            tube_passes=args.get("tube_passes", 2)
        )
    elif tool_name == "thermal_rate_tema_shell_and_tube":
        return rate_tema_shell_and_tube(
            duty_kW=args["duty_kW"],
            th_in=args["th_in"],
            th_out=args["th_out"],
            tc_in=args["tc_in"],
            tc_out=args["tc_out"],
            shell_id_mm=args.get("shell_id_mm", 600),
            tube_od_mm=args.get("tube_od_mm", 19.05),
            tube_wt_mm=args.get("tube_wt_mm", 1.65),
            tube_length_m=args.get("tube_length_m", 4.0),
            tube_count=args.get("tube_count", 240)
        )
    elif tool_name == "thermal_mvr_evaporator_design":
        return design_mvr_evaporator(
            feed_flow_kg_h=args["feed_flow_kg_h"],
            feed_solids_pct=args["feed_solids_pct"],
            product_solids_pct=args["product_solids_pct"],
            evaporator_temp_C=args.get("evaporator_temp_C", 80.0),
            compressor_temp_rise_C=args.get("compressor_temp_rise_C", 8.0)
        )
    raise ValueError(f"Unknown Thermal tool: {tool_name}")


def dispatch_pv_tool(tool_name, args):
    if tool_name == "pv_asme_ug27_shell":
        return calculate_shell_thickness_ug27(
            design_pressure_bar=args["design_pressure_bar"],
            inside_diameter_mm=args["inside_diameter_mm"],
            design_temp_C=args.get("design_temp_C", 100.0),
            material=args.get("material", "SA-240 316L"),
            weld_joint_efficiency=args.get("weld_joint_efficiency", 1.0),
            corrosion_allowance_mm=args.get("corrosion_allowance_mm", 1.5)
        )
    elif tool_name == "pv_asme_ug32_head":
        return calculate_dished_head_ug32(
            design_pressure_bar=args["design_pressure_bar"],
            inside_diameter_mm=args["inside_diameter_mm"],
            head_type=args.get("head_type", "ellipsoidal_2_1"),
            design_temp_C=args.get("design_temp_C", 100.0),
            material=args.get("material", "SA-240 316L"),
            weld_joint_efficiency=args.get("weld_joint_efficiency", 1.0),
            corrosion_allowance_mm=args.get("corrosion_allowance_mm", 1.5)
        )
    elif tool_name == "pv_asme_ug37_nozzle":
        return calculate_nozzle_reinforcement_ug37(
            vessel_id_mm=args["vessel_id_mm"],
            shell_thickness_mm=args["shell_thickness_mm"],
            nozzle_od_mm=args["nozzle_od_mm"],
            nozzle_thickness_mm=args["nozzle_thickness_mm"],
            design_pressure_bar=args["design_pressure_bar"],
            design_temp_C=args.get("design_temp_C", 100.0),
            material=args.get("material", "SA-240 316L"),
            corrosion_allowance_mm=args.get("corrosion_allowance_mm", 1.5)
        )
    elif tool_name == "pv_asme_ug99_hydro":
        return calculate_hydrostatic_test_ug99(
            design_pressure_bar=args["design_pressure_bar"],
            design_temp_C=args.get("design_temp_C", 100.0),
            material=args.get("material", "SA-240 316L")
        )
    raise ValueError(f"Unknown Pressure Vessel tool: {tool_name}")


def handle_tool_call(tool_name, arguments):
    """Routes tool execution to the appropriate engineering subsystem."""
    if not tool_name or not isinstance(tool_name, str):
        raise ValueError(f"Invalid tool name: {tool_name}")

    if tool_name.startswith("solidworks_"):
        return dispatch_solidworks_tool(sw_controller, tool_name, arguments or {})
    elif tool_name.startswith("aspen_plus_"):
        return dispatch_aspen_plus_tool(aspen_plus_controller, tool_name, arguments or {})
    elif tool_name.startswith("aspen_hysys_"):
        return dispatch_aspen_hysys_tool(aspen_hysys_controller, tool_name, arguments or {})
    elif tool_name.startswith("dwsim_"):
        return dispatch_dwsim_tool(dwsim_controller, tool_name, arguments or {})
    elif tool_name.startswith("autocad_"):
        return dispatch_autocad_tool(autocad_controller, tool_name, arguments or {})
    elif tool_name.startswith("thermo_"):
        return dispatch_thermo_tool(tool_name, arguments or {})
    elif tool_name.startswith("hydraulics_"):
        return dispatch_hydraulics_tool(tool_name, arguments or {})
    elif tool_name.startswith("thermal_"):
        return dispatch_thermal_tool(tool_name, arguments or {})
    elif tool_name.startswith("pv_"):
        return dispatch_pv_tool(tool_name, arguments or {})
    else:
        raise ValueError(f"Unknown tool name: {tool_name}. Registered tools: {len(ALL_TOOLS)}")


def process_message(line):
    """Processes a single incoming JSON-RPC 2.0 message."""
    if not line or not line.strip():
        return None

    try:
        req = json.loads(line)
    except json.JSONDecodeError as e:
        return format_error(None, -32700, f"Parse error: {str(e)}")

    if not isinstance(req, dict):
        return format_error(None, -32600, "Invalid Request: Expected JSON object")

    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if req_id is None:
        # Notification - no reply needed
        return None

    if method == "initialize":
        return format_response(req_id, {
            "protocolVersion": MCP_VERSION,
            "capabilities": {
                "tools": {
                    "listChanged": False
                }
            },
            "serverInfo": {
                "name": SERVER_NAME,
                "version": SERVER_VERSION,
                "lead_engineer": "Sourish Senapati (FinnoaQ Agro-Industrial Technologies Ltd.)",
                "project_ref": "FNQ-PR-2026-001"
            }
        })

    elif method == "tools/list":
        return format_response(req_id, {
            "tools": ALL_TOOLS
        })

    elif method == "tools/call":
        tool_name = params.get("name")
        arguments = params.get("arguments", {})

        if not tool_name:
            return format_error(req_id, -32602, "Missing parameter: 'name'")

        try:
            tool_result = handle_tool_call(tool_name, arguments)
            return format_response(req_id, format_tool_content(tool_result))
        except Exception as e:
            return format_response(req_id, {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps({
                            "status": "error",
                            "error_type": type(e).__name__,
                            "message": str(e),
                            "traceback": traceback.format_exc()
                        }, indent=2)
                    }
                ],
                "isError": True
            })

    elif method == "ping":
        return format_response(req_id, {})

    else:
        return format_error(req_id, -32601, f"Method '{method}' not found")


def run_stdio_server():
    """Runs the MCP server over standard input and output."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stdin, "reconfigure"):
        sys.stdin.reconfigure(encoding="utf-8")

    # Graceful SIGINT / SIGTERM handling
    def sig_handler(sig, frame):
        sys.exit(0)

    try:
        signal.signal(signal.SIGINT, sig_handler)
        signal.signal(signal.SIGTERM, sig_handler)
    except Exception:
        pass

    for line in sys.stdin:
        try:
            response_json = process_message(line)
            if response_json:
                sys.stdout.write(response_json + "\n")
                sys.stdout.flush()
        except Exception as e:
            err_resp = format_error(None, -32603, f"Internal server error: {str(e)}")
            sys.stdout.write(err_resp + "\n")
            sys.stdout.flush()


def main():
    run_stdio_server()


if __name__ == "__main__":
    main()

