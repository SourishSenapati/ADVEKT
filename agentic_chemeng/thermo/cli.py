"""
Agentic ChemEng - Thermodynamics Command Line Interface
"""

import argparse
import json
import sys

from .equations import calculate_steam_properties, peng_robinson_eos


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        prog="thermo-cli",
        description="Autonomous CLI for Chemical Engineering Thermodynamics (ASME Steam Tables & Peng-Robinson EOS)"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    steam_p = subparsers.add_parser("steam", help="Calculate ASME STEAM-TA steam/water properties")
    steam_p.add_argument("--temp", "-t", type=float, default=None, help="Temperature in °C")
    steam_p.add_argument("--pressure", "-p", type=float, default=None, help="Pressure in bar absolute")

    pr_p = subparsers.add_parser("pr-eos", help="Calculate Peng-Robinson Equation of State (Z and fugacities)")
    pr_p.add_argument("--compounds", "-c", default="methane,ethane,propane", help="Comma-separated component names")
    pr_p.add_argument("--fractions", "-z", default="0.7,0.2,0.1", help="Comma-separated mole fractions")
    pr_p.add_argument("--temp", "-t", type=float, default=25.0, help="Temperature in °C")
    pr_p.add_argument("--pressure", "-p", type=float, default=30.0, help="Pressure in bar")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == "steam":
            res = calculate_steam_properties(temperature_C=args.temp, pressure_bar=args.pressure)
        elif args.command == "pr-eos":
            comps = [c.strip() for c in args.compounds.split(",") if c.strip()]
            fracs = [float(f.strip()) for f in args.fractions.split(",") if f.strip()]
            res = peng_robinson_eos(
                compounds=comps,
                mole_fractions=fracs,
                temperature_C=args.temp,
                pressure_bar=args.pressure
            )
        else:
            res = {"error": f"Unknown command: {args.command}"}

        print(json.dumps(res, indent=2))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()

