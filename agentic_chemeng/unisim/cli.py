"""
Agentic ChemEng - Honeywell UniSim Command Line Interface
"""

import argparse
import json
import sys

from .controller import UniSimController


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        prog="unisim-cli",
        description="Autonomous CLI for Honeywell UniSim Design Process Simulation"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    subparsers.add_parser("status", help="Check UniSim COM server connectivity")

    inspect_p = subparsers.add_parser("inspect", help="Inspect UniSim simulation case (.usc, .hsc)")
    inspect_p.add_argument("filepath", help="Path to UniSim case file")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    controller = UniSimController()

    try:
        if args.command == "status":
            res = controller.get_status()
        elif args.command == "inspect":
            res = controller.inspect_case(args.filepath)
        else:
            res = {"error": f"Unknown command: {args.command}"}

        print(json.dumps(res, indent=2))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()

