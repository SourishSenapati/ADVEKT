"""
Agentic ChemEng - Autonomous Multi-Discipline Chemical & Mechanical Engineering CLI
Project Ref: FNQ-PR-2026-001 | Lead Engineer: Sourish Senapati (FinnoaQ Agro-Industrial Technologies Ltd.)

Unified command-line gateway coordinating:
1. solidworks       : Dassault Systèmes SOLIDWORKS 2025 B-Rep CAD automation
2. aspen-plus       : Aspen Plus V14 flowsheet inspection and OLE simulation
3. aspen-hysys      : Aspen HYSYS COM simulation and property package solver
4. dwsim            : DWSIM open-source process simulator & flowsheet inspection
5. autocad          : Autodesk AutoCAD 2025 DWG/DXF/PDF vector pipelines
6. thermo           : ASME STEAM-TA steam properties & Peng-Robinson Cubic EOS
7. hydraulics       : Darcy-Weisbach, Colebrook-White, ASME B36.10M, Pump TDH/NPSHa
8. thermal          : TEMA Shell-and-Tube heat exchangers & MVR evaporators
9. pressure-vessel  : ASME BPVC Section VIII Div 1 (UG-27, UG-32, UG-37, UG-99)
10. mcp             : Model Context Protocol (MCP) JSON-RPC 2.0 stdio server
"""

import argparse
import json
import sys

from .solidworks.controller import SolidWorksController
from .aspen_plus.controller import AspenPlusController
from .aspen_hysys.controller import AspenHysysController
from .dwsim.controller import DwsimController
from .autocad.controller import AutoCADController
from .chemcad.controller import ChemcadController
from .proii.controller import ProIIController
from .cantera.controller import CanteraController
from .unisim.controller import UniSimController
from .mcp.server import ALL_TOOLS, main as mcp_main


def get_system_status():
    """Performs fast non-blocking diagnostic inspection of all registered engineering engines."""
    sw = SolidWorksController(visible=False).get_status(launch_if_closed=False)
    ap = AspenPlusController().get_status()
    ah = AspenHysysController().get_status()
    dw = DwsimController().get_status()
    ac = AutoCADController(visible=False).get_status()
    cc = ChemcadController().get_status()
    pr = ProIIController().get_status()
    ct = CanteraController().get_status()
    us = UniSimController().get_status()

    return {
        "suite": "Agentic ChemEng Multi-Discipline Engineering Architecture",
        "version": "1.0.0",
        "lead_engineer": "Sourish Senapati (FinnoaQ Agro-Industrial Technologies Ltd.)",
        "project_ref": "FNQ-PR-2026-001",
        "registered_mcp_tools_count": len(ALL_TOOLS),
        "subsystems": {
            "solidworks_cad": sw,
            "aspen_plus_simulation": ap,
            "aspen_hysys_simulation": ah,
            "dwsim_open_source_simulation": dw,
            "chemcad_simulation": cc,
            "proii_simulation": pr,
            "cantera_kinetics_transport": ct,
            "unisim_simulation": us,
            "autocad_drafting": ac,
            "thermo_engine": {"status": "operational", "standards": ["ASME STEAM-TA", "Peng-Robinson EOS"]},
            "hydraulics_engine": {"status": "operational", "standards": ["Darcy-Weisbach", "ASME B36.10M", "Crane TP 410"]},
            "thermal_engine": {"status": "operational", "standards": ["TEMA 10th Ed", "Kern Method", "MVR Evaporation"]},
            "pressure_vessel_engine": {"status": "operational", "standards": ["ASME BPVC Section VIII Div 1", "Section II Part D"]}
        }
    }


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        prog="agentic-chemeng",
        description="Autonomous Multi-Discipline Chemical & Mechanical Engineering CLI Suite"
    )
    subparsers = parser.add_subparsers(dest="subsystem", help="Engineering Subsystems")

    # Overall status command
    subparsers.add_parser("status", help="Query comprehensive health status across all engineering software")

    # MCP server command
    subparsers.add_parser("mcp", help="Run the Model Context Protocol (MCP) JSON-RPC 2.0 stdio server")

    # Subsystem forwarders
    subparsers.add_parser("solidworks", help="SolidWorks 2025 CAD automation")
    subparsers.add_parser("aspen-plus", help="Aspen Plus V14 chemical simulation")
    subparsers.add_parser("aspen-hysys", help="Aspen HYSYS simulation & thermodynamic packages")
    subparsers.add_parser("dwsim", help="DWSIM open-source process simulator")
    subparsers.add_parser("chemcad", help="Chemstations CHEMCAD process simulation")
    subparsers.add_parser("proii", help="AVEVA SimSci PRO/II refinery & chemical simulation")
    subparsers.add_parser("cantera", help="Cantera chemical kinetics, thermodynamics & transport")
    subparsers.add_parser("unisim", help="Honeywell UniSim Design process simulation")
    subparsers.add_parser("autocad", help="Autodesk AutoCAD 2025 drafting & vector tools")
    subparsers.add_parser("thermo", help="Rigorous thermodynamics (ASME Steam & Peng-Robinson)")
    subparsers.add_parser("hydraulics", help="Process hydraulics (Darcy-Weisbach, Pump TDH, NPSHa)")
    subparsers.add_parser("thermal", help="Industrial thermal design (TEMA Shell & Tube, MVR)")
    subparsers.add_parser("pressure-vessel", help="ASME BPVC Section VIII Div 1 pressure vessels")

    # Handle remaining arguments
    args, remaining = parser.parse_known_args()

    if not args.subsystem or args.subsystem == "status":
        print(json.dumps(get_system_status(), indent=2))
        return

    if args.subsystem == "mcp":
        mcp_main()
        return

    # Forward to subsystem CLIs
    sys.argv = [f"agentic-chemeng {args.subsystem}"] + remaining

    if args.subsystem == "solidworks":
        from .solidworks.cli import main as sw_cli
        sw_cli()
    elif args.subsystem == "aspen-plus":
        from .aspen_plus.cli import main as ap_cli
        ap_cli()
    elif args.subsystem == "aspen-hysys":
        from .aspen_hysys.cli import main as ah_cli
        ah_cli()
    elif args.subsystem == "dwsim":
        from .dwsim.cli import main as dw_cli
        dw_cli()
    elif args.subsystem == "chemcad":
        from .chemcad.cli import main as cc_cli
        cc_cli()
    elif args.subsystem == "proii":
        from .proii.cli import main as pr_cli
        pr_cli()
    elif args.subsystem == "cantera":
        from .cantera.cli import main as ct_cli
        ct_cli()
    elif args.subsystem == "unisim":
        from .unisim.cli import main as us_cli
        us_cli()
    elif args.subsystem == "autocad":
        from .autocad.cli import main as ac_cli
        ac_cli()
    elif args.subsystem == "thermo":
        from .thermo.cli import main as th_cli
        th_cli()
    elif args.subsystem == "hydraulics":
        from .hydraulics.cli import main as hyd_cli
        hyd_cli()
    elif args.subsystem == "thermal":
        from .thermal.cli import main as thm_cli
        thm_cli()
    elif args.subsystem in ["pressure-vessel", "pv"]:
        from .pressure_vessel.cli import main as pv_cli
        pv_cli()
    else:
        print(f"Unknown subsystem: {args.subsystem}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

