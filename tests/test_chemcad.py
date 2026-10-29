"""
Unit tests for CHEMCAD Autonomous Process Simulation Subsystem
"""

import pytest
from agentic_chemeng.chemcad.controller import ChemcadController


def test_chemcad_status():
    controller = ChemcadController()
    status = controller.get_status()
    assert "status" in status
    assert "chemcad_version" in status
    assert ".ccx" in status["supported_formats"]
    assert status["lead_process_engineer"] == "Sourish Senapati (FinnoaQ Agro-Industrial Technologies Ltd.)"

