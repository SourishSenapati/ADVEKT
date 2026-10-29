#!/usr/bin/env python
"""
Agentic ChemEng - AutoCAD Autonomous CLI
Command-line interface empowering AI agents and draftspersons to headlessly plot,
audit, and script Autodesk AutoCAD 2025 drawings.
"""

import argparse
import json
import os
import sys

from .controller import AutoCADController


def print_json(data):
    print(json.dumps(data, indent=2, default=str))


def main():
    parser = argparse.ArgumentParser(
        description="AutoCAD 2025 Autonomous Agentic CLI (Agentic ChemEng)"
    )
    subparsers = parser.add_subparsers(dest="command", help="AutoCAD Command")

    subparsers.add_parser("status", help="Check AutoCAD COM registration and accoreconsole.exe path")

    plot_p = subparsers.add_parser("plot", help="Headlessly plot DWG or DXF to vector PDF")
    plot_p.add_argument("drawing_path", help="Path to DWG or DXF file")
    plot_p.add_argument("--out", help="Output PDF file path")

    script_p = subparsers.add_parser("script", help="Execute script commands headlessly via accoreconsole")
    script_p.add_argument("drawing_path", help="Path to DWG or DXF file")
    script_p.add_argument("commands", nargs="+", help="AutoCAD commands to execute")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    controller = AutoCADController()

    try:
        if args.command == "status":
            print_json(controller.get_status())
        elif args.command == "plot":
            print_json(controller.plot_pdf(args.drawing_path, out_pdf_path=args.out))
        elif args.command == "script":
            print_json(controller.run_script(args.drawing_path, args.commands))
    except Exception as e:
        print_json({"status": "error", "error_type": type(e).__name__, "message": str(e)})
        sys.exit(1)


if __name__ == "__main__":
    main()

