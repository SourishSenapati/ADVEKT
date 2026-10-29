"""
Agentic ChemEng - RAEBYES Circuit Breaker Tool Definitions & Schemas for MCP
"""

from typing import Any, Dict
from .circuit_breaker import CIRCUIT_BREAKER

RAEBYES_TOOLS = [
    {
        "name": "raebyes_verify_simulation_variance",
        "description": "Applies RAEBYES VarianceGuard to output numerical arrays/tensors to detect flat synthetic mock arrays, NaN values, infinite divergence, and suspicious instant solver bypasses.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "data": {"description": "Numerical array, list, dictionary, or scalar values to audit"},
                "min_variance": {"type": "number", "description": "Minimum required variance for non-scalar data (default: 1e-6)"},
                "execution_time_ms": {"type": "number", "description": "Reported execution latency in milliseconds"},
                "min_execution_time_ms": {"type": "number", "description": "Minimum expected physical solver runtime in milliseconds"}
            },
            "required": ["data"]
        }
    },
    {
        "name": "raebyes_verify_conservation_invariants",
        "description": "Verifies First-Principles conservation of mass (closure error < 1e-4) and thermal energy (closure error < 1e-3) across chemical unit operations.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "mass_in_kg_h": {"type": "number", "description": "Inlet total mass flow (kg/h)"},
                "mass_out_kg_h": {"type": "number", "description": "Outlet total mass flow (kg/h)"},
                "nominal_duty_kW": {"type": "number", "description": "Specified or duty rating in kW (optional)"},
                "calculated_heat_kW": {"type": "number", "description": "Enthalpy or sensible heat balance in kW (optional)"},
                "tolerance": {"type": "number", "description": "Allowable relative tolerance (default: 1e-4)"}
            },
            "required": ["mass_in_kg_h", "mass_out_kg_h"]
        }
    },
    {
        "name": "raebyes_get_circuit_breaker_status",
        "description": "Queries the active RAEBYES circuit-breaker state, loop-detection ledger, and raebyesd daemon socket/pipe connectivity.",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
]


def dispatch_raebyes_tool(tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
    """Dispatches RAEBYES circuit-breaker tool calls."""
    if tool_name == "raebyes_verify_simulation_variance":
        return CIRCUIT_BREAKER.verify_numerical_variance(
            data=args["data"],
            min_variance=args.get("min_variance", 1e-6),
            execution_time_ms=args.get("execution_time_ms"),
            min_execution_time_ms=args.get("min_execution_time_ms", 0.0)
        )
    elif tool_name == "raebyes_verify_conservation_invariants":
        mass_res = CIRCUIT_BREAKER.verify_mass_conservation(
            mass_in_kg_h=args["mass_in_kg_h"],
            mass_out_kg_h=args["mass_out_kg_h"],
            tolerance=args.get("tolerance", 1e-4)
        )
        if "nominal_duty_kW" in args and "calculated_heat_kW" in args:
            energy_res = CIRCUIT_BREAKER.verify_energy_conservation(
                duty_kW=args["nominal_duty_kW"],
                calculated_heat_kW=args["calculated_heat_kW"],
                tolerance=args.get("tolerance", 1e-3)
            )
            mass_res["energy_audit"] = energy_res
            mass_res["all_passed"] = mass_res["passed"] and energy_res["passed"]
        else:
            mass_res["all_passed"] = mass_res["passed"]
        return mass_res
    elif tool_name == "raebyes_get_circuit_breaker_status":
        daemon_status = CIRCUIT_BREAKER.check_daemon_status()
        return {
            "status": "operational",
            "circuit_breaker_state": CIRCUIT_BREAKER.state,
            "call_history_count": len(CIRCUIT_BREAKER.call_history),
            "breach_count": CIRCUIT_BREAKER.breach_count,
            "daemon": daemon_status,
            "lead_engineer": "Sourish Senapati (FinnoaQ Agro-Industrial Technologies Ltd.)",
            "project_ref": "FNQ-PR-2026-001"
        }
    raise ValueError(f"Unknown RAEBYES tool: {tool_name}")

