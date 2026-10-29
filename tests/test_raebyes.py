"""
Unit tests for RAEBYES Deterministic Invariant Circuit Breaker & Protocol.
Inspired by SourishSenapati/RAEBYES.
"""

import pytest
from agentic_chemeng.raebyes.circuit_breaker import RaebyesCircuitBreaker, RaebyesInvariantError
from agentic_chemeng.raebyes.tools import RAEBYES_TOOLS, dispatch_raebyes_tool


def test_raebyes_variance_guard_flat_array():
    cb = RaebyesCircuitBreaker()
    # A synthetic flat array [10.0, 10.0, 10.0, 10.0] has zero variance
    res = cb.verify_numerical_variance([10.0, 10.0, 10.0, 10.0])
    assert res["passed"] is False
    assert "Synthetic flat mock detected" in res["error"]
    assert res["variance"] < 1e-9


def test_raebyes_variance_guard_valid_physical_array():
    cb = RaebyesCircuitBreaker()
    # Genuine numerical values with physical gradient
    res = cb.verify_numerical_variance([10.2, 12.5, 14.8, 18.2, 22.0])
    assert res["passed"] is True
    assert res["variance"] > 1e-4
    assert res["count"] == 5


def test_raebyes_variance_guard_nan_and_inf():
    cb = RaebyesCircuitBreaker()
    res_nan = cb.verify_numerical_variance([1.0, 2.0, float("nan")])
    assert res_nan["passed"] is False
    assert "NaN" in res_nan["error"]

    res_inf = cb.verify_numerical_variance([1.0, 2.0, float("inf")])
    assert res_inf["passed"] is False
    assert "infinite values" in res_inf["error"]


def test_raebyes_mass_conservation_pass():
    cb = RaebyesCircuitBreaker()
    # 1000 kg/h in, 999.98 kg/h out -> closure error 2e-5 (within 1e-4)
    res = cb.verify_mass_conservation(mass_in_kg_h=1000.0, mass_out_kg_h=999.98)
    assert res["passed"] is True
    assert res["status"] == "CONSERVED"
    assert res["closure_error_relative"] < 1e-4


def test_raebyes_mass_conservation_fail():
    cb = RaebyesCircuitBreaker()
    # 1000 kg/h in, 950 kg/h out -> 5% closure error (violation)
    res = cb.verify_mass_conservation(mass_in_kg_h=1000.0, mass_out_kg_h=950.0)
    assert res["passed"] is False
    assert res["status"] == "VIOLATED"
    assert res["closure_error_relative"] > 0.01


def test_raebyes_energy_conservation():
    cb = RaebyesCircuitBreaker()
    # Nominal duty 500 kW, calculated sensible heat 500.1 kW
    res = cb.verify_energy_conservation(duty_kW=500.0, calculated_heat_kW=500.1)
    assert res["passed"] is True
    assert res["status"] == "CONSERVED"

    res_fail = cb.verify_energy_conservation(duty_kW=500.0, calculated_heat_kW=450.0)
    assert res_fail["passed"] is False
    assert res_fail["status"] == "VIOLATED"


def test_raebyes_loop_trap_spasm():
    cb = RaebyesCircuitBreaker()
    tool = "test_solver"
    args = {"tolerance": 1e-5}

    # 1st call: OK
    ok, err = cb.record_and_check_loop(tool, args)
    assert ok is True
    assert err is None

    # 2nd call: OK
    ok, err = cb.record_and_check_loop(tool, args)
    assert ok is True

    # 3rd identical call: TRIPPED (ERR_IDENTICAL_LOOP)
    ok, err = cb.record_and_check_loop(tool, args)
    assert ok is False
    assert "ERR_IDENTICAL_LOOP" in err
    assert cb.state == "OPEN"


def test_raebyes_tools_schema():
    assert len(RAEBYES_TOOLS) == 3
    names = [t["name"] for t in RAEBYES_TOOLS]
    assert "raebyes_verify_simulation_variance" in names
    assert "raebyes_verify_conservation_invariants" in names
    assert "raebyes_get_circuit_breaker_status" in names


def test_raebyes_mcp_dispatch():
    res = dispatch_raebyes_tool(
        "raebyes_verify_conservation_invariants",
        {"mass_in_kg_h": 1500.0, "mass_out_kg_h": 1500.01}
    )
    assert res["passed"] is True
    assert res["status"] == "CONSERVED"

