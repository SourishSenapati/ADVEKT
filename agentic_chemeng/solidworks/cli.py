#!/usr/bin/env python
"""
Agentic ChemEng - SolidWorks 2025 Autonomous CLI
Command-line interface empowering AI agents and engineers to programmatically
inspect, rebuild, render, export, and automate Dassault Systèmes SOLIDWORKS 2025 SP1.2.
"""

import argparse
import json
import os
import sys

from .controller import SolidWorksController


def print_json(data):
    print(json.dumps(data, indent=2, default=str))


def main():
    parser = argparse.ArgumentParser(
        description="SolidWorks 2025 Autonomous Agentic CLI (Agentic ChemEng)"
    )
    subparsers = parser.add_subparsers(dest="command", help="CAD Command")

    subparsers.add_parser("status", help="Query SolidWorks connection status, revision, and open documents")

    open_p = subparsers.add_parser("open", help="Open a .SLDPRT, .SLDASM, .SLDDRW, or .STEP document")
    open_p.add_argument("filepath", help="Path to CAD file")
    open_p.add_argument("--readonly", action="store_true", help="Open as read-only")
    open_p.add_argument("--visible", action="store_true", help="Make SolidWorks window visible")

    close_p = subparsers.add_parser("close", help="Close document(s)")
    close_p.add_argument("--title", help="Title of document to close")
    close_p.add_argument("--all", action="store_true", dest="all_docs", help="Close all open documents")

    inspect_p = subparsers.add_parser("inspect", help="Inspect features, bodies, custom properties, bounding box, and mass props")
    inspect_p.add_argument("filepath", nargs="?", help="Optional file path (defaults to active doc)")

    mp_p = subparsers.add_parser("mass-props", help="Compute exact mass, volume, surface area, and center of gravity")
    mp_p.add_argument("filepath", nargs="?", help="Optional file path (defaults to active doc)")

    rebuild_p = subparsers.add_parser("rebuild", help="Force parametric rebuild and save")
    rebuild_p.add_argument("filepath", nargs="?", help="Optional file path (defaults to active doc)")
    rebuild_p.add_argument("--no-save", action="store_true", help="Do not save after rebuild")

    render_p = subparsers.add_parser("render", help="Render viewport to high-resolution PNG image")
    render_p.add_argument("filepath", nargs="?", help="Optional file path (defaults to active doc)")
    render_p.add_argument("--view", default="iso", choices=["iso", "isometric", "front", "top", "right", "left", "back"], help="View orientation")
    render_p.add_argument("--out", help="Output PNG path")

    export_p = subparsers.add_parser("export", help="Export CAD model to multiple formats (STEP, PDF, PNG)")
    export_p.add_argument("filepath", nargs="?", help="Optional file path (defaults to active doc)")
    export_p.add_argument("--formats", default="step,png", help="Comma-separated formats: step,pdf,png")
    export_p.add_argument("--out-dir", help="Output directory")

    exec_p = subparsers.add_parser("exec-code", help="Execute Python code snippet directly in SolidWorks COM environment")
    exec_p.add_argument("code", help="Python code string to execute")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    controller = SolidWorksController(visible=getattr(args, "visible", False))

    try:
        if args.command == "status":
            print_json(controller.get_status())
        elif args.command == "open":
            print_json(controller.open_document(args.filepath, read_only=args.readonly, silent=True))
        elif args.command == "close":
            print_json(controller.close_document(title=args.title, all_docs=args.all_docs))
        elif args.command == "inspect":
            print_json(controller.inspect_model(filepath=args.filepath))
        elif args.command == "mass-props":
            print_json(controller.get_mass_properties(filepath=args.filepath))
        elif args.command == "rebuild":
            print_json(controller.force_rebuild(filepath=args.filepath, save=not args.no_save))
        elif args.command == "render":
            print_json(controller.render_view(filepath=args.filepath, view=args.view, out_path=args.out))
        elif args.command == "export":
            fmt_list = [f.strip() for f in args.formats.split(",") if f.strip()]
            print_json(controller.export_cad(filepath=args.filepath, formats=fmt_list, out_dir=args.out_dir))
        elif args.command == "exec-code":
            print_json(controller.execute_agent_code(args.code))
    except Exception as e:
        print_json({"status": "error", "error_type": type(e).__name__, "message": str(e)})
        sys.exit(1)


if __name__ == "__main__":
    main()

