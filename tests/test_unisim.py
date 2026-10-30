"""
Unit tests for Honeywell UniSim Design Subsystem
"""

import pytest
from agentic_chemeng.unisim.controller import UniSimController


def test_unisim_status():
    controller = UniSimController()
    status = controller.get_status()
    assert "status" in status
    assert "unisim_version" in status
    assert ".usc" in status["supported_formats"]
    assert status["lead_process_engineer"] == "Sourish Senapati"

