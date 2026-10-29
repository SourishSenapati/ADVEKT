"""
Unit tests for CAD/CAE Controllers non-blocking COM status inquiries
"""

import pytest
from agentic_chemeng.solidworks.controller import SolidWorksController
from agentic_chemeng.aspen_plus.controller import AspenPlusController
from agentic_chemeng.aspen_hysys.controller import AspenHysysController
from agentic_chemeng.autocad.controller import AutoCADController


def test_solidworks_controller_status():
    sw = SolidWorksController(visible=False)
    status = sw.get_status(launch_if_closed=False)
    assert "status" in status
    assert status["status"] in ["ready_on_demand", "connected", "connected_busy"]
    assert "version" in status


def test_aspen_plus_controller_status():
    ap = AspenPlusController()
    status = ap.get_status()
    assert "com_registered" in status
    assert status["lead_process_engineer"] == "Sourish Senapati (FinnoaQ Agro-Industrial Technologies Ltd.)"


def test_aspen_hysys_controller_status():
    ah = AspenHysysController()
    status = ah.get_status()
    assert "status" in status
    assert "supported_formats" in status
    assert ".hsc" in status["supported_formats"]


def test_autocad_controller_status():
    ac = AutoCADController(visible=False)
    status = ac.get_status()
    assert "status" in status
    assert "accoreconsole_path" in status

