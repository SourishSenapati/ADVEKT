"""
Unit tests for Cantera Chemical Kinetics, Thermodynamics & Transport Subsystem
"""

import pytest
from agentic_chemeng.cantera.controller import CanteraController


def test_cantera_status():
    controller = CanteraController()
    status = controller.get_status()
    assert "status" in status
    assert "supported_capabilities" in status
    assert len(status["supported_capabilities"]) >= 5
    assert status["lead_process_engineer"] == "Sourish Senapati"


def test_cantera_arrhenius_kinetics():
    controller = CanteraController()
    # Hydrolysis of pectin / ester: A = 1e8, Ea = 80 kJ/mol, T = 100°C, t = 600s
    res = controller.calculate_arrhenius_kinetics(
        A_pre_exponential=1e8,
        Ea_kJ_mol=80.0,
        temperature_C=100.0,
        order=1.0,
        initial_conc_mol_m3=50.0,
        time_seconds=600.0
    )
    assert res["temperature_K"] == 373.15
    assert res["rate_constant_k"] > 0.0
    assert 0.0 <= res["fractional_conversion_X"] <= 1.0
    assert res["final_concentration_mol_m3"] <= res["initial_concentration_mol_m3"]


def test_cantera_gas_transport_properties():
    controller = CanteraController()
    res = controller.calculate_gas_transport_properties(
        gas_species="air",
        temperature_C=20.0,
        pressure_bar=1.01325
    )
    assert 1.15 <= res["density_kg_m3"] <= 1.25
    # Air viscosity at 20°C is ~1.8e-5 Pa.s (0.018 cP)
    assert 0.017 <= res["dynamic_viscosity_cP"] <= 0.019
    # Thermal conductivity ~ 0.025 W/m.K
    assert 0.020 <= res["thermal_conductivity_W_m_K"] <= 0.030
    assert 0.65 <= res["prandtl_number"] <= 0.75

