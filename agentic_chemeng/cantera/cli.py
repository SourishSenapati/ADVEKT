"""
Agentic ChemEng - Cantera Chemical Kinetics & Transport Command Line Interface
"""

import argparse
import json
import sys

from .controller import CanteraController


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        prog="cantera-cli",
        description="Autonomous CLI for Cantera Chemical Kinetics, Thermodynamics & Transport Properties"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    subparsers.add_parser("status", help="Check Cantera engine status")

    kin_p = subparsers.add_parser("kinetics", help="Compute Arrhenius reaction rate and conversion")
    kin_p.add_argument("--A", "-a", type=float, required=True, help="Pre-exponential factor A")
    kin_p.add_argument("--Ea", "-e", type=float, required=True, help="Activation energy in kJ/mol")
    kin_p.add_argument("--temp", "-t", type=float, required=True, help="Temperature in °C")
    kin_p.add_argument("--order", "-n", type=float, default=1.0, help="Reaction order")
    kin_p.add_argument("--c0", type=float, default=100.0, help="Initial concentration in mol/m3")
    kin_p.add_argument("--time", type=float, default=60.0, help="Reaction time in seconds")

    trans_p = subparsers.add_parser("transport", help="Compute gas transport properties (viscosity, conductivity)")
    trans_p.add_argument("--gas", "-g", default="air", help="Gas species: air, n2, o2, co2, h2, ch4, steam")
    trans_p.add_argument("--temp", "-t", type=float, default=25.0, help="Temperature in °C")
    trans_p.add_argument("--pressure", "-p", type=float, default=1.01325, help="Pressure in bar")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    controller = CanteraController()

    try:
        if args.command == "status":
            res = controller.get_status()
        elif args.command == "kinetics":
            res = controller.calculate_arrhenius_kinetics(
                A_pre_exponential=args.A,
                Ea_kJ_mol=args.Ea,
                temperature_C=args.temp,
                order=args.order,
                initial_conc_mol_m3=args.c0,
                time_seconds=args.time
            )
        elif args.command == "transport":
            res = controller.calculate_gas_transport_properties(
                gas_species=args.gas,
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

