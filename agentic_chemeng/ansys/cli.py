"""
Agentic ChemEng - Ansys Fluent & CFX Command Line Interface
"""

import argparse
import json
import sys

from .controller import AnsysController


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        prog="ansys-cli",
        description="Autonomous CLI for Ansys Fluent & CFX Reacting Flow & Chemical CFD"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    subparsers.add_parser("status", help="Check Ansys Fluent / CFX installation and license status")

    inspect_p = subparsers.add_parser("inspect", help="Inspect Ansys case file (.cas, .cas.gz, .msh)")
    inspect_p.add_argument("filepath", help="Path to Ansys case file")

    run_p = subparsers.add_parser("run", help="Run batch CFD simulation via Fluent journal")
    run_p.add_argument("journal_path", help="Path to Fluent journal file (.jou, .txt)")
    run_p.add_argument("--dimensions", default="3ddp", help="Solver precision & dimensions (default: 3ddp)")
    run_p.add_argument("--timeout", type=float, default=180.0, help="Timeout in seconds")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    controller = AnsysController()

    try:
        if args.command == "status":
            res = controller.get_status()
        elif args.command == "inspect":
            res = controller.inspect_case(args.filepath)
        elif args.command == "run":
            res = controller.run_journal(
                args.journal_path,
                dimensions=args.dimensions,
                timeout_sec=args.timeout
            )
        else:
            res = {"error": f"Unknown command: {args.command}"}

        print(json.dumps(res, indent=2))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
