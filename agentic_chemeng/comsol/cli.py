"""
Agentic ChemEng - COMSOL Multiphysics Command Line Interface
"""

import argparse
import json
import sys

from .controller import ComsolController


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        prog="comsol-cli",
        description="Autonomous CLI for COMSOL Multiphysics Chemical & Transport Modeling"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    subparsers.add_parser("status", help="Check COMSOL Multiphysics installation and license status")

    inspect_p = subparsers.add_parser("inspect", help="Inspect COMSOL model file (.mph)")
    inspect_p.add_argument("filepath", help="Path to COMSOL model file (.mph)")

    run_p = subparsers.add_parser("run", help="Run batch simulation for a COMSOL model")
    run_p.add_argument("filepath", help="Path to COMSOL model file (.mph)")
    run_p.add_argument("--study", dest="study_tag", default=None, help="Study tag to solve (e.g. std1)")
    run_p.add_argument("--output", dest="output_path", default=None, help="Output solved model path")
    run_p.add_argument("--timeout", type=float, default=120.0, help="Timeout in seconds")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    controller = ComsolController()

    try:
        if args.command == "status":
            res = controller.get_status()
        elif args.command == "inspect":
            res = controller.inspect_model(args.filepath)
        elif args.command == "run":
            res = controller.run_study(
                args.filepath,
                study_tag=args.study_tag,
                output_path=args.output_path,
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

