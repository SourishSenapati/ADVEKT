"""
Agentic ChemEng - CHEMCAD Command Line Interface
"""

import argparse
import json
import sys

from .controller import ChemcadController


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        prog="chemcad-cli",
        description="Autonomous CLI for Chemstations CHEMCAD Process Simulation"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    subparsers.add_parser("status", help="Check CHEMCAD COM server connectivity")

    inspect_p = subparsers.add_parser("inspect", help="Inspect CHEMCAD flowsheet file (.ccx, .cc5)")
    inspect_p.add_argument("filepath", help="Path to CHEMCAD case file")

    subparsers.add_parser("run", help="Run active CHEMCAD simulation solver")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    controller = ChemcadController()

    try:
        if args.command == "status":
            res = controller.get_status()
        elif args.command == "inspect":
            res = controller.inspect_flowsheet(args.filepath)
        elif args.command == "run":
            res = controller.run_simulation()
        else:
            res = {"error": f"Unknown command: {args.command}"}

        print(json.dumps(res, indent=2))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()

