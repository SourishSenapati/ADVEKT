"""
Unit tests for DWSIM Open-Source Process Simulation Subsystem
"""

import pytest
from agentic_chemeng.dwsim.controller import DwsimController


def test_dwsim_get_status():
    controller = DwsimController()
    status = controller.get_status()
    assert "supported_property_packages" in status
    assert len(status["supported_property_packages"]) >= 5
    assert "supported_unit_operations" in status
    assert status["lead_process_engineer"] == "Sourish Senapati"


def test_dwsim_flash_calculation():
    controller = DwsimController()
    # Flash of Water-Ethanol at 90°C and 1.01325 bar (mixture should boil between 78.4°C and 100°C)
    res = controller.flash_calculation(
        flash_type="TP",
        temperature_C=90.0,
        pressure_bar=1.01325,
        compounds=["Water", "Ethanol"],
        mole_fractions=[0.8, 0.2]
    )
    assert "thermodynamic_state" in res
    assert 0.0 <= res["vapor_fraction_beta"] <= 1.0
    assert "liquid_mole_fractions_x" in res
    assert "vapor_mole_fractions_y" in res

