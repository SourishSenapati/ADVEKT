"""
Agentic ChemEng - RAEBYES Deterministic Invariant Circuit Breaker & Daemon Protocol
Project Ref: FNQ-PR-2026-001 | Lead Engineer: Sourish Senapati (FinnoaQ Agro-Industrial Technologies Ltd.)
Specification: SourishSenapati/RAEBYES (https://github.com/SourishSenapati/RAEBYES)

Implements the RAEBYES protocol to make AI coding and scientific agents physically
allergic to synthetic shortcuts, flat mock tensors, deleted test assertions, phantom runs,
and circular reward-hacking loops across all 16 chemical, mechanical, and CAE subsystems.
"""

import datetime
import hashlib
import json
import math
import os
import sys
from typing import Any, Dict, List, Optional, Tuple, Union

try:
    from raebyes.variance import VarianceGuard as BaseVarianceGuard
    from raebyes.spasm import RaebyesSpasmError, trigger_spasm, record_breach
    HAVE_RAEBYES_SDK = True
except ImportError:
    HAVE_RAEBYES_SDK = False


class RaebyesInvariantError(ValueError):
    """Raised when an engineering output violates physical conservation laws or contains synthetic mocks."""
    pass


class RaebyesCircuitBreaker:
    """
    Stateful circuit breaker tracking agent tool call hashes and enforcing
    physical invariants and non-synthetic computation.
    """

    def __init__(self, workspace_dir: Optional[str] = None):
        self.workspace_dir = workspace_dir or os.getcwd()
        self.call_history: List[str] = []
        self.max_history = 50
        self.state = "CLOSED"  # CLOSED (Normal) -> HALF_OPEN (Anomalous) -> OPEN (Tripped)
        self.breach_count = 0

    def compute_call_hash(self, tool_name: str, args: Dict[str, Any]) -> str:
        """Computes deterministic SHA-256 fingerprint for a tool execution."""
        sorted_args = json.dumps(args, sort_keys=True, default=str)
        raw = f"{tool_name}:{sorted_args}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def record_and_check_loop(self, tool_name: str, args: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Detects runaway loops and cyclic convergence:
        1. ERR_IDENTICAL_LOOP: 3 consecutive calls with identical arguments.
        2. ERR_CYCLIC_CONVERGENCE: Alternating 2-cycle state flips (A -> B -> A -> B).
        """
        chash = self.compute_call_hash(tool_name, args)
        self.call_history.append(chash)
        if len(self.call_history) > self.max_history:
            self.call_history.pop(0)

        # 1. Check identical loop (3x repeat)
        if len(self.call_history) >= 3:
            if self.call_history[-1] == self.call_history[-2] == self.call_history[-3]:
                self.state = "OPEN"
                self.breach_count += 1
                return False, (
                    f"ERR_IDENTICAL_LOOP: Tool '{tool_name}' invoked 3 consecutive times "
                    f"with identical arguments ({chash[:12]}). Runaway agent loop halted."
                )

        # 2. Check 2-cycle oscillation (A-B-A-B)
        if len(self.call_history) >= 4:
            if (self.call_history[-1] == self.call_history[-3] and
                self.call_history[-2] == self.call_history[-4] and
                self.call_history[-1] != self.call_history[-2]):
                self.state = "OPEN"
                self.breach_count += 1
                return False, (
                    f"ERR_CYCLIC_CONVERGENCE: 2-cycle alternating state flip detected "
                    f"between {self.call_history[-2][:8]} and {self.call_history[-1][:8]}. "
                    "Oscillating agent edit loop halted."
                )

        return True, None

    @staticmethod
    def verify_numerical_variance(
        data: Any,
        execution_time_ms: Optional[float] = None,
        min_variance: float = 1e-6,
        min_execution_time_ms: float = 0.0,
        allow_scalars: bool = True
    ) -> Dict[str, Any]:
        """
        Audits output numerical arrays/tensors against the RAEBYES VarianceGuard.
        Detects flat constant mock arrays, NaN values, infinite divergence,
        and suspicious sub-millisecond execution times.
        """
        # Flatten numerical data
        numbers: List[float] = []

        def walk(val: Any):
            if isinstance(val, (int, float)) and not isinstance(val, bool):
                numbers.append(float(val))
            elif isinstance(val, (list, tuple)):
                for item in val:
                    walk(item)
            elif hasattr(val, "tolist") and callable(getattr(val, "tolist")):
                try:
                    walk(val.tolist())
                except Exception:
                    pass
            elif isinstance(val, dict):
                for v in val.values():
                    walk(v)

        walk(data)

        if not numbers:
            return {
                "passed": False,
                "error": "Output contains zero numerical values.",
                "variance": 0.0
            }

        # Check for NaN / Infinity
        if any(math.isnan(n) for n in numbers):
            return {
                "passed": False,
                "error": "Numerical output contains NaN (unstable or uncomputed state).",
                "variance": 0.0
            }
        if any(math.isinf(n) for n in numbers):
            return {
                "passed": False,
                "error": "Numerical output contains infinite values (diverged calculation).",
                "variance": 0.0
            }

        if len(numbers) == 1 and allow_scalars:
            return {
                "passed": True,
                "is_scalar": True,
                "value": numbers[0],
                "variance": None
            }

        # Calculate sample variance
        mean = sum(numbers) / len(numbers)
        variance = sum((n - mean) ** 2 for n in numbers) / len(numbers)

        if len(numbers) > 1 and variance < min_variance:
            return {
                "passed": False,
                "error": f"Output variance ({variance:.4e}) is below safety threshold ({min_variance:.4e}). Synthetic flat mock detected.",
                "variance": variance,
                "mean": mean
            }

        if execution_time_ms is not None and min_execution_time_ms > 0:
            if execution_time_ms < min_execution_time_ms:
                return {
                    "passed": False,
                    "error": f"Execution time ({execution_time_ms:.2f}ms) is below minimum threshold ({min_execution_time_ms:.2f}ms). Mock simulation detected.",
                    "variance": variance,
                    "execution_time_ms": execution_time_ms
                }

        return {
            "passed": True,
            "variance": variance,
            "mean": mean,
            "count": len(numbers),
            "execution_time_ms": execution_time_ms
        }

    @staticmethod
    def verify_mass_conservation(
        mass_in_kg_h: float,
        mass_out_kg_h: float,
        tolerance: float = 1e-4
    ) -> Dict[str, Any]:
        """
        Enforces strict First-Principles Conservation of Mass.
        Relative closure error must not exceed tolerance (default 0.01%).
        """
        if mass_in_kg_h <= 0.0:
            raise RaebyesInvariantError(f"Invalid feed mass flow: {mass_in_kg_h} kg/h")

        delta = abs(mass_in_kg_h - mass_out_kg_h)
        rel_error = delta / mass_in_kg_h

        passed = rel_error <= tolerance
        return {
            "passed": passed,
            "mass_in_kg_h": mass_in_kg_h,
            "mass_out_kg_h": mass_out_kg_h,
            "closure_error_relative": rel_error,
            "tolerance": tolerance,
            "error_percentage": rel_error * 100.0,
            "status": "CONSERVED" if passed else "VIOLATED"
        }

    @staticmethod
    def verify_energy_conservation(
        duty_kW: float,
        calculated_heat_kW: float,
        tolerance: float = 1e-3
    ) -> Dict[str, Any]:
        """
        Enforces strict First-Principles Conservation of Thermal Energy (Q = m * Cp * dT).
        """
        ref = max(abs(duty_kW), 1e-3)
        delta = abs(duty_kW - calculated_heat_kW)
        rel_error = delta / ref

        passed = rel_error <= tolerance
        return {
            "passed": passed,
            "nominal_duty_kW": duty_kW,
            "calculated_heat_kW": calculated_heat_kW,
            "energy_closure_error": rel_error,
            "tolerance": tolerance,
            "status": "CONSERVED" if passed else "VIOLATED"
        }

    def check_daemon_status(self) -> Dict[str, Any]:
        """
        Probes local operating system for active RAEBYES daemon (raebyesd).
        POSIX: ~/.cache/raebyes/raebyesd.sock
        Windows: \\\\.\\pipe\\raebyesd.sock
        """
        if sys.platform == "win32":
            pipe_path = r"\\.\pipe\raebyesd.sock"
            pipe_active = os.path.exists(pipe_path)
            return {
                "daemon": "raebyesd",
                "platform": "win32",
                "named_pipe": pipe_path,
                "active": pipe_active,
                "protocol": "SourishSenapati/RAEBYES",
                "circuit_breaker_state": self.state
            }
        else:
            sock_path = os.path.expanduser("~/.cache/raebyes/raebyesd.sock")
            sock_active = os.path.exists(sock_path)
            return {
                "daemon": "raebyesd",
                "platform": sys.platform,
                "socket_path": sock_path,
                "active": sock_active,
                "protocol": "SourishSenapati/RAEBYES",
                "circuit_breaker_state": self.state
            }


# Global singleton instance
CIRCUIT_BREAKER = RaebyesCircuitBreaker()
