"""
Agentic ChemEng - DWSIM Command Line Interface
"""

import argparse
import json
import sys

from .controller import DwsimController


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        prog="dwsim-cli",
        description="Autonomous CLI for DWSIM Open-Source Process Simulation & CAPE-OPEN Thermodynamics"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    subparsers.add_parser("status", help="Check DWSIM installation and supported thermodynamic packages")

    inspect_parser = subparsers.add_parser("inspect", help="Inspect a DWSIM flowsheet file (.dwsim, .dwxml)")
    inspect_parser.add_argument("filepath", help="Path to flowsheet file")

    flash_parser = subparsers.add_parser("flash", help="Perform isothermal/isobaric VLE flash calculation")
    flash_parser.add_argument("--temp", "-t", type=float, default=100.0, help="Temperature in °C")
    flash_parser.add_argument("--pressure", "-p", type=float, default=1.01325, help="Pressure in bar")
    flash_parser.add_argument("--compounds", "-c", default="Water,Ethanol", help="Comma-separated compounds")
    flash_parser.add_argument("--fractions", "-z", default="0.8,0.2", help="Comma-separated mole fractions")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    controller = DwsimController()

    try:
        if args.command == "status":
            res = controller.get_status()
        elif args.command == "inspect":
            res = controller.inspect_flowsheet(args.filepath)
        elif args.command == "flash":
            comps = [c.strip() for c in args.compounds.split(",") if c.strip()]
            fracs = [float(f.strip()) for f in args.fractions.split(",") if f.strip()]
            res = controller.flash_calculation(
                temperature_C=args.temp,
                pressure_bar=args.pressure,
                compounds=comps,
                mole_fractions=fracs
            )
        else:
            res = {"error": f"Unknown command: {args.command}"}

        print(json.dumps(res, indent=2))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()

