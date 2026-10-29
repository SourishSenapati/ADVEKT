"""
Agentic ChemEng - Industrial Thermal Design Command Line Interface
"""

import argparse
import json
import sys

from .equations import (
    calculate_lmtd,
    rate_tema_shell_and_tube,
    design_mvr_evaporator
)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        prog="thermal-cli",
        description="Autonomous CLI for Heat Transfer & Thermal Design (TEMA Shell-and-Tube & MVR Evaporators)"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    lmtd_p = subparsers.add_parser("lmtd", help="Calculate LMTD and FT correction factor")
    lmtd_p.add_argument("--th-in", type=float, required=True, help="Hot fluid inlet temp (°C)")
    lmtd_p.add_argument("--th-out", type=float, required=True, help="Hot fluid outlet temp (°C)")
    lmtd_p.add_argument("--tc-in", type=float, required=True, help="Cold fluid inlet temp (°C)")
    lmtd_p.add_argument("--tc-out", type=float, required=True, help="Cold fluid outlet temp (°C)")

    tema_p = subparsers.add_parser("shell-and-tube", help="Rate TEMA Shell-and-Tube heat exchanger")
    tema_p.add_argument("--duty", type=float, required=True, help="Heat duty in kW")
    tema_p.add_argument("--th-in", type=float, required=True, help="Hot inlet temp (°C)")
    tema_p.add_argument("--th-out", type=float, required=True, help="Hot outlet temp (°C)")
    tema_p.add_argument("--tc-in", type=float, required=True, help="Cold inlet temp (°C)")
    tema_p.add_argument("--tc-out", type=float, required=True, help="Cold outlet temp (°C)")
    tema_p.add_argument("--tubes", type=int, default=240, help="Number of tubes")
    tema_p.add_argument("--length", type=float, default=4.0, help="Tube length in meters")

    mvr_p = subparsers.add_parser("mvr", help="Design MVR falling film evaporator")
    mvr_p.add_argument("--feed-flow", type=float, required=True, help="Feed flow rate in kg/h")
    mvr_p.add_argument("--feed-solids", type=float, required=True, help="Feed solids % (e.g. 5)")
    mvr_p.add_argument("--product-solids", type=float, required=True, help="Product solids % (e.g. 35)")
    mvr_p.add_argument("--temp", type=float, default=80.0, help="Evaporator boiling temp (°C)")
    mvr_p.add_argument("--temp-rise", type=float, default=8.0, help="Compressor temp lift (°C)")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == "lmtd":
            res = calculate_lmtd(args.th_in, args.th_out, args.tc_in, args.tc_out)
        elif args.command == "shell-and-tube":
            res = rate_tema_shell_and_tube(
                duty_kW=args.duty,
                th_in=args.th_in,
                th_out=args.th_out,
                tc_in=args.tc_in,
                tc_out=args.tc_out,
                tube_count=args.tubes,
                tube_length_m=args.length
            )
        elif args.command == "mvr":
            res = design_mvr_evaporator(
                feed_flow_kg_h=args.feed_flow,
                feed_solids_pct=args.feed_solids,
                product_solids_pct=args.product_solids,
                evaporator_temp_C=args.temp,
                compressor_temp_rise_C=args.temp_rise
            )
        else:
            res = {"error": f"Unknown command: {args.command}"}

        print(json.dumps(res, indent=2))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()

