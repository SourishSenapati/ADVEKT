"""
Agentic ChemEng - ASME Pressure Vessel Command Line Interface
"""

import argparse
import json
import sys

from .equations import (
    calculate_shell_thickness_ug27,
    calculate_dished_head_ug32,
    calculate_nozzle_reinforcement_ug37,
    calculate_hydrostatic_test_ug99
)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        prog="pv-cli",
        description="Autonomous CLI for ASME Section VIII Div 1 Pressure Vessel Design (UG-27, UG-32, UG-37, UG-99)"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    shell_p = subparsers.add_parser("shell", help="Calculate UG-27 cylindrical shell thickness")
    shell_p.add_argument("--pressure", "-p", type=float, required=True, help="Design pressure in bar")
    shell_p.add_argument("--diameter", "-d", type=float, required=True, help="Inside diameter in mm")
    shell_p.add_argument("--temp", "-t", type=float, default=100.0, help="Design temp in °C")
    shell_p.add_argument("--material", "-m", default="SA-240 316L", help="ASME material name")
    shell_p.add_argument("--joint-eff", "-e", type=float, default=1.0, help="Weld joint efficiency E (1.0, 0.85, 0.7)")
    shell_p.add_argument("--corrosion", "-ca", type=float, default=1.5, help="Corrosion allowance in mm")

    head_p = subparsers.add_parser("head", help="Calculate UG-32 formed head thickness")
    head_p.add_argument("--pressure", "-p", type=float, required=True, help="Design pressure in bar")
    head_p.add_argument("--diameter", "-d", type=float, required=True, help="Inside diameter in mm")
    head_p.add_argument("--type", default="ellipsoidal_2_1", choices=["ellipsoidal_2_1", "torispherical"], help="Head type")
    head_p.add_argument("--temp", "-t", type=float, default=100.0, help="Design temp in °C")
    head_p.add_argument("--material", "-m", default="SA-240 316L", help="ASME material name")
    head_p.add_argument("--corrosion", "-ca", type=float, default=1.5, help="Corrosion allowance in mm")

    nozzle_p = subparsers.add_parser("nozzle", help="Calculate UG-37 nozzle reinforcement area replacement")
    nozzle_p.add_argument("--vessel-id", type=float, required=True, help="Vessel shell inside diameter in mm")
    nozzle_p.add_argument("--shell-t", type=float, required=True, help="Shell nominal thickness in mm")
    nozzle_p.add_argument("--nozzle-od", type=float, required=True, help="Nozzle neck outside diameter in mm")
    nozzle_p.add_argument("--nozzle-t", type=float, required=True, help="Nozzle neck thickness in mm")
    nozzle_p.add_argument("--pressure", "-p", type=float, required=True, help="Design pressure in bar")
    nozzle_p.add_argument("--temp", "-t", type=float, default=100.0, help="Design temp in °C")
    nozzle_p.add_argument("--material", "-m", default="SA-240 316L", help="ASME material name")

    hydro_p = subparsers.add_parser("hydro", help="Calculate UG-99 hydrostatic test pressure")
    hydro_p.add_argument("--pressure", "-p", type=float, required=True, help="Design pressure in bar")
    hydro_p.add_argument("--temp", "-t", type=float, default=100.0, help="Design temp in °C")
    hydro_p.add_argument("--material", "-m", default="SA-240 316L", help="ASME material name")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == "shell":
            res = calculate_shell_thickness_ug27(
                design_pressure_bar=args.pressure,
                inside_diameter_mm=args.diameter,
                design_temp_C=args.temp,
                material=args.material,
                weld_joint_efficiency=args.joint_eff,
                corrosion_allowance_mm=args.corrosion
            )
        elif args.command == "head":
            res = calculate_dished_head_ug32(
                design_pressure_bar=args.pressure,
                inside_diameter_mm=args.diameter,
                head_type=args.type,
                design_temp_C=args.temp,
                material=args.material,
                corrosion_allowance_mm=args.corrosion
            )
        elif args.command == "nozzle":
            res = calculate_nozzle_reinforcement_ug37(
                vessel_id_mm=args.vessel_id,
                shell_thickness_mm=args.shell_t,
                nozzle_od_mm=args.nozzle_od,
                nozzle_thickness_mm=args.nozzle_t,
                design_pressure_bar=args.pressure,
                design_temp_C=args.temp,
                material=args.material
            )
        elif args.command == "hydro":
            res = calculate_hydrostatic_test_ug99(
                design_pressure_bar=args.pressure,
                design_temp_C=args.temp,
                material=args.material
            )
        else:
            res = {"error": f"Unknown command: {args.command}"}

        print(json.dumps(res, indent=2))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()

