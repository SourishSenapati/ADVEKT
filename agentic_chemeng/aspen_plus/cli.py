"""
Agentic ChemEng - Aspen Plus Command Line Interface
"""

import argparse
import json
import sys

from .controller import AspenPlusController


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        prog="aspen-plus-cli",
        description="Autonomous CLI for Aspen Plus Process Simulation (Apwn.Document COM Automation)"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    subparsers.add_parser("status", help="Check Aspen Plus COM registration and licensing state")

    open_parser = subparsers.add_parser("open", help="Open a simulation file (.bkp, .apw)")
    open_parser.add_argument("filepath", help="Path to simulation file")

    inspect_parser = subparsers.add_parser("inspect", help="Inspect flowsheet topology and unit blocks")
    inspect_parser.add_argument("--filepath", "-f", default=None, help="Path to simulation file")

    streams_parser = subparsers.add_parser("streams", help="Get rigorous stream balance table")
    streams_parser.add_argument("--filepath", "-f", default=None, help="Path to simulation file")

    blocks_parser = subparsers.add_parser("blocks", help="Get unit block duty and thermal data")
    blocks_parser.add_argument("--filepath", "-f", default=None, help="Path to simulation file")
    blocks_parser.add_argument("--block-id", "-b", default=None, help="Specific block identifier")

    subparsers.add_parser("run", help="Execute simulation run")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    controller = AspenPlusController()

    try:
        if args.command == "status":
            res = controller.get_status()
        elif args.command == "open":
            res = controller.open_simulation(args.filepath)
        elif args.command == "inspect":
            res = controller.inspect_flowsheet(args.filepath)
        elif args.command == "streams":
            res = controller.get_stream_table(args.filepath)
        elif args.command == "blocks":
            res = controller.get_block_data(args.filepath, args.block_id)
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

