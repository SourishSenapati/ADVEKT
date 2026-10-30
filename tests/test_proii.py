"""
Unit tests for AVEVA SimSci PRO/II Process Simulation Subsystem
"""

import pytest
from agentic_chemeng.proii.controller import ProIIController


def test_proii_status():
    controller = ProIIController()
    status = controller.get_status()
    assert "status" in status
    assert "proii_version" in status
    assert ".prz" in status["supported_formats"]
    assert status["lead_process_engineer"] == "Sourish Senapati"

