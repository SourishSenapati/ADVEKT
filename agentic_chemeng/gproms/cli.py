"""
Agentic ChemEng - Siemens gPROMS Command Line Interface
"""

import argparse
import json
import sys

from .controller import GpromsController


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        prog="gproms-cli",
        description="Autonomous CLI for Siemens / PSE gPROMS Advanced Process Modeling"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    subparsers.add_parser("status", help="Check Siemens gPROMS installation and environment status")

    inspect_p = subparsers.add_parser("inspect", help="Inspect gPROMS project file (.gPJ, .gPA, .xml)")
    inspect_p.add_argument("filepath", help="Path to gPROMS project file")

    run_p = subparsers.add_parser("run", help="Run batch simulation for a gPROMS project")
    run_p.add_argument("filepath", help="Path to gPROMS project file")
    run_p.add_argument("--process", dest="process_name", default=None, help="Process name to simulate")
    run_p.add_argument("--timeout", type=float, default=60.0, help="Timeout in seconds")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    controller = GpromsController()

    try:
        if args.command == "status":
            res = controller.get_status()
        elif args.command == "inspect":
            res = controller.inspect_project(args.filepath)
        elif args.command == "run":
            res = controller.run_simulation(args.filepath, process_name=args.process_name, timeout_sec=args.timeout)
        else:
            res = {"error": f"Unknown command: {args.command}"}

        print(json.dumps(res, indent=2))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()

