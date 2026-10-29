"""
Agentic ChemEng - Process Hydraulics Command Line Interface
"""

import argparse
import json
import sys

from .equations import (
    get_pipe_dimensions,
    calculate_pressure_drop,
    calculate_pump_tdh_and_npsha
)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        prog="hydraulics-cli",
        description="Autonomous CLI for Process Hydraulics (Darcy-Weisbach, Colebrook-White, Pump TDH, NPSHa)"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    dim_p = subparsers.add_parser("pipe-dims", help="Get ASME B36.10M pipe schedule dimensions")
    dim_p.add_argument("dn", type=int, help="Nominal diameter DN (mm)")
    dim_p.add_argument("--schedule", "-s", default="sch40", help="Pipe schedule (sch10, sch40, sch80)")

    dp_p = subparsers.add_parser("pressure-drop", help="Calculate line velocity, friction factor, and head loss")
    dp_p.add_argument("--flow", "-q", type=float, required=True, help="Flow rate in m3/h")
    dp_p.add_argument("--dn", type=int, required=True, help="Pipe DN (mm)")
    dp_p.add_argument("--length", "-l", type=float, required=True, help="Pipe length in meters")
    dp_p.add_argument("--density", type=float, default=998.2, help="Density in kg/m3")
    dp_p.add_argument("--viscosity", type=float, default=1.002, help="Viscosity in cP")
    dp_p.add_argument("--schedule", default="sch40", help="Schedule (sch10, sch40, sch80)")

    pump_p = subparsers.add_parser("pump", help="Calculate Centrifugal Pump TDH, NPSHa, and Power")
    pump_p.add_argument("--flow", "-q", type=float, required=True, help="Flow rate in m3/h")
    pump_p.add_argument("--static-head", type=float, required=True, help="Static head in meters")
    pump_p.add_argument("--p-disch", type=float, required=True, help="Discharge pressure in barg")
    pump_p.add_argument("--p-suct", type=float, required=True, help="Suction pressure in barg")
    pump_p.add_argument("--hf-suct", type=float, default=0.5, help="Suction head loss in meters")
    pump_p.add_argument("--hf-disch", type=float, default=3.0, help="Discharge head loss in meters")
    pump_p.add_argument("--suct-lift", type=float, default=2.0, help="Suction liquid head above pump (m)")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == "pipe-dims":
            res = get_pipe_dimensions(args.dn, schedule=args.schedule)
        elif args.command == "pressure-drop":
            res = calculate_pressure_drop(
                flow_m3_h=args.flow,
                pipe_dn_mm=args.dn,
                length_m=args.length,
                density_kg_m3=args.density,
                viscosity_cp=args.viscosity,
                schedule=args.schedule
            )
        elif args.command == "pump":
            res = calculate_pump_tdh_and_npsha(
                flow_m3_h=args.flow,
                static_head_m=args.static_head,
                discharge_press_barg=args.p_disch,
                suction_press_barg=args.p_suct,
                suction_loss_m=args.hf_suct,
                discharge_loss_m=args.hf_disch,
                suction_static_lift_m=args.suct_lift
            )
        else:
            res = {"error": f"Unknown command: {args.command}"}

        print(json.dumps(res, indent=2))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
