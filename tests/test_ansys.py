"""
Tests for Ansys Fluent & CFX controller, tools, and CLI.
"""

import gzip
import os
import tempfile
import pytest

from agentic_chemeng.ansys.controller import AnsysController
from agentic_chemeng.ansys.tools import ANSYS_TOOLS


def test_ansys_status():
    controller = AnsysController()
    status = controller.get_status()
    assert "status" in status
    assert "platform" in status
    assert "supported_models" in status
    assert any("Species Transport" in m for m in status["supported_models"])
    assert "Sourish Senapati" in status["lead_process_engineer"]


def test_ansys_tools_schema():
    assert len(ANSYS_TOOLS) == 3
    names = [t["name"] for t in ANSYS_TOOLS]
    assert "ansys_get_status" in names
    assert "ansys_inspect_case" in names
    assert "ansys_run_journal" in names


def test_ansys_inspect_case_file():
    controller = AnsysController()
    case_content = """(0 "Fluent Case File")
(2 3)
(12 (1 1 50000 1 3))
(37 (2 velocity-inlet inlet-gas))
(37 (3 pressure-outlet outlet-flue))
(37 (4 wall reactor-wall))
(37 (1 fluid gas-domain))
models: species-transport, energy, k-omega
"""
    with tempfile.NamedTemporaryFile("w", suffix=".cas", delete=False) as f:
        f.write(case_content)
        tmp_cas = f.name

    try:
        res = controller.inspect_case(tmp_cas)
        assert res["status"] == "success"
        assert res["dimension"] == "3D"
        assert res["estimated_mesh_cells"] == 50000
        bc_names = [bc["name"] for bc in res["boundary_conditions"]]
        assert "inlet-gas" in bc_names
        assert "outlet-flue" in bc_names
        assert any("Species Transport" in m for m in res["physical_models"])
        assert res["epistemic_classification"] == "OFFLINE_AUDIT"
    finally:
        if os.path.exists(tmp_cas):
            os.remove(tmp_cas)


def test_ansys_inspect_case_gzipped():
    controller = AnsysController()
    case_content = b"""(0 "Fluent Case File")
(2 2)
(12 (1 1 20000 1 2))
(37 (5 velocity-inlet air-inlet))
(37 (6 outflow outlet))
models: reaction, eulerian
"""
    with tempfile.NamedTemporaryFile(suffix=".cas.gz", delete=False) as f:
        tmp_gz = f.name

    with gzip.open(tmp_gz, "wb") as gz:
        gz.write(case_content)

    try:
        res = controller.inspect_case(tmp_gz)
        assert res["status"] == "success"
        assert res["dimension"] == "2D"
        assert res["estimated_mesh_cells"] == 20000
        bc_types = [bc["type"] for bc in res["boundary_conditions"]]
        assert "velocity-inlet" in bc_types
        assert "outflow" in bc_types
    finally:
        if os.path.exists(tmp_gz):
            os.remove(tmp_gz)


def test_ansys_run_journal_missing_exe():
    controller = AnsysController()
    res = controller.run_journal("dummy.jou")
    assert res["status"] in ["unlicensed_or_missing", "ready"]
    if res["status"] == "unlicensed_or_missing":
        assert res["epistemic_classification"] == "BLOCKED"
