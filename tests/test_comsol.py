"""
Tests for COMSOL Multiphysics controller, tools, and CLI.
"""

import os
import tempfile
import zipfile
import pytest

from agentic_chemeng.comsol.controller import ComsolController
from agentic_chemeng.comsol.tools import COMSOL_TOOLS


def test_comsol_status():
    controller = ComsolController()
    status = controller.get_status()
    assert "status" in status
    assert "platform" in status
    assert "supported_physics_modules" in status
    assert any("Chemical Reaction" in m for m in status["supported_physics_modules"])
    assert "Sourish Senapati" in status["lead_process_engineer"]


def test_comsol_tools_schema():
    assert len(COMSOL_TOOLS) == 3
    names = [t["name"] for t in COMSOL_TOOLS]
    assert "comsol_get_status" in names
    assert "comsol_inspect_model" in names
    assert "comsol_run_study" in names


def test_comsol_inspect_model_archive():
    controller = ComsolController()
    # Create mock .mph (zip archive containing model.xml)
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
    <comsolModel version="6.2">
        <component name="comp1">
            <physics type="cheq" name="Reaction Engineering" tag="cheq1"/>
            <physics type="tds" name="Transport of Diluted Species" tag="tds1"/>
            <physics type="ht" name="Heat Transfer in Fluids" tag="ht1"/>
            <geom tag="geom1" dim="3"/>
        </component>
        <study type="std_stationary" tag="std1" name="Stationary Solver"/>
        <param name="c_feed" value="1500[mol/m^3]"/>
        <param name="T_inlet" value="350[K]"/>
    </comsolModel>
    """
    with tempfile.NamedTemporaryFile(suffix=".mph", delete=False) as f:
        tmp_mph = f.name

    with zipfile.ZipFile(tmp_mph, "w") as z:
        z.writestr("model.xml", xml_content)

    try:
        res = controller.inspect_model(tmp_mph)
        assert res["status"] == "success"
        assert any("cheq" in p for p in res["physics_interfaces"])
        assert any("tds" in p for p in res["physics_interfaces"])
        assert any("ht" in p for p in res["physics_interfaces"])
        assert "c_feed" in res["parameters"]
        assert res["epistemic_classification"] == "OFFLINE_AUDIT"
    finally:
        if os.path.exists(tmp_mph):
            os.remove(tmp_mph)


def test_comsol_run_study_missing_exe():
    controller = ComsolController()
    res = controller.run_study("dummy.mph")
    assert res["status"] in ["unlicensed_or_missing", "ready"]
    if res["status"] == "unlicensed_or_missing":
        assert res["epistemic_classification"] == "BLOCKED"
