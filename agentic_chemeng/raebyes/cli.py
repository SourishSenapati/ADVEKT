"""
Agentic ChemEng - RAEBYES Command Line Interface
"""

import argparse
import json
import sys

from .circuit_breaker import CIRCUIT_BREAKER


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        prog="raebyes-chemeng-cli",
        description="RAEBYES Deterministic Circuit Breaker & Invariant Verifier for Chemical & Mechanical Engineering"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    subparsers.add_parser("status", help="Check RAEBYES circuit-breaker and raebyesd daemon status")

    mass_p = subparsers.add_parser("check-mass", help="Verify conservation of mass")
    mass_p.add_argument("--inflow", type=float, required=True, help="Total mass inflow (kg/h)")
    mass_p.add_argument("--outflow", type=float, required=True, help="Total mass outflow (kg/h)")
    mass_p.add_argument("--tol", type=float, default=1e-4, help="Relative closure tolerance (default: 1e-4)")

    var_p = subparsers.add_parser("check-variance", help="Audit numerical array/tensor variance against flat mock detection")
    var_p.add_argument("--values", required=True, help="Comma-separated numerical values or JSON array")
    var_p.add_argument("--min-var", type=float, default=1e-6, help="Minimum acceptable variance")
    var_p.add_argument("--exec-time-ms", type=float, default=None, help="Execution latency in ms")
    var_p.add_argument("--min-exec-time-ms", type=float, default=0.0, help="Minimum expected execution latency in ms")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == "status":
            res = {
                "circuit_breaker_state": CIRCUIT_BREAKER.state,
                "call_history_count": len(CIRCUIT_BREAKER.call_history),
                "breach_count": CIRCUIT_BREAKER.breach_count,
                "daemon": CIRCUIT_BREAKER.check_daemon_status(),
                "governing_protocol": "SourishSenapati/RAEBYES",
                "lead_engineer": "Sourish Senapati (FinnoaQ Agro-Industrial Technologies Ltd.)"
            }
        elif args.command == "check-mass":
            res = CIRCUIT_BREAKER.verify_mass_conservation(
                mass_in_kg_h=args.inflow,
                mass_out_kg_h=args.outflow,
                tolerance=args.tol
            )
        elif args.command == "check-variance":
            try:
                vals = json.loads(args.values)
            except Exception:
                vals = [float(x.strip()) for x in args.values.split(",") if x.strip()]

            res = CIRCUIT_BREAKER.verify_numerical_variance(
                data=vals,
                min_variance=args.min_var,
                execution_time_ms=args.exec_time_ms,
                min_execution_time_ms=args.min_exec_time_ms
            )
        else:
            res = {"error": f"Unknown command: {args.command}"}

        print(json.dumps(res, indent=2))
        if isinstance(res, dict) and not res.get("passed", True):
            sys.exit(1)
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()

