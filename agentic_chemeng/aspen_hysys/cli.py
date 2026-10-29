"""
Agentic ChemEng - Aspen HYSYS Command Line Interface
"""

import argparse
import json
import sys

from .controller import AspenHysysController


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        prog="aspen-hysys-cli",
        description="Autonomous CLI for Aspen HYSYS (HYSYS.Application COM Automation)"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    subparsers.add_parser("status", help="Check HYSYS COM server connectivity and active case")

    open_parser = subparsers.add_parser("open", help="Open a HYSYS .hsc case file")
    open_parser.add_argument("filepath", help="Path to .hsc case file")

    inspect_parser = subparsers.add_parser("inspect", help="Inspect flowsheet streams and operations")
    inspect_parser.add_argument("--filepath", "-f", default=None, help="Path to .hsc case file")

    subparsers.add_parser("solve", help="Trigger active HYSYS flowsheet solver")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    controller = AspenHysysController()

    try:
        if args.command == "status":
            res = controller.get_status()
        elif args.command == "open":
            res = controller.open_case(args.filepath)
        elif args.command == "inspect":
            res = controller.inspect_case(args.filepath)
        elif args.command == "solve":
            res = controller.solve()
        else:
            res = {"error": f"Unknown command: {args.command}"}

        print(json.dumps(res, indent=2))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()

