"""
Tests for Siemens gPROMS controller, tools, and CLI.
"""

import os
import tempfile
import pytest

from agentic_chemeng.gproms.controller import GpromsController
from agentic_chemeng.gproms.tools import GPROMS_TOOLS


def test_gproms_status():
    controller = GpromsController()
    status = controller.get_status()
    assert "status" in status
    assert "platform" in status
    assert "supported_formats" in status
    assert ".gPJ" in status["supported_formats"]
    assert "Sourish Senapati" in status["lead_process_engineer"]


def test_gproms_tools_schema():
    assert len(GPROMS_TOOLS) == 3
    names = [t["name"] for t in GPROMS_TOOLS]
    assert "gproms_get_status" in names
    assert "gproms_inspect_project" in names
    assert "gproms_run_simulation" in names


def test_gproms_inspect_project_text():
    controller = GpromsController()
    sample_gproms = """
    # Siemens gPROMS Process Model
    VARIABLE_TYPE
        Concentration = 0.0 : 100.0 UNIT = "mol/m3"
        Temperature = 250.0 : 600.0 UNIT = "K"

    MODEL CSTR_Reactor
        PARAMETER
            Volume AS REAL
        VARIABLE
            C_A AS Concentration
            T AS Temperature
        EQUATION
            $C_A = (C_Ain - C_A)/tau - k * C_A;
            $T = (T_in - T)/tau + dH_rxn * k * C_A / (rho * Cp);
    END

    PROCESS ContinuousReaction
        UNIT
            R101 AS CSTR_Reactor
        SCHEDULE
            CONTINUE FOR 3600.0
    END
    """
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
        f.write(sample_gproms)
        tmp_path = f.name

    try:
        res = controller.inspect_project(tmp_path)
        assert res["status"] == "success"
        assert "CSTR_Reactor" in res["models"]
        assert "ContinuousReaction" in res["processes"]
        assert "Concentration" in res["variable_types"]
        assert res["estimated_equations_count"] > 0
        assert res["epistemic_classification"] == "OFFLINE_AUDIT"
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_gproms_run_simulation_missing_exe():
    controller = GpromsController()
    res = controller.run_simulation("dummy.gpj")
    # In unlicensed/test environments without gproms.exe, should fail closed cleanly
    assert res["status"] in ["unlicensed_or_missing", "ready"]
    if res["status"] == "unlicensed_or_missing":
        assert res["epistemic_classification"] == "BLOCKED"
