"""
Unit tests for Chemical Engineering Thermodynamics Engine
"""

import pytest
from agentic_chemeng.thermo.equations import calculate_steam_properties, peng_robinson_eos


def test_steam_properties_saturation_at_100C():
    res = calculate_steam_properties(temperature_C=100.0)
    assert res["temperature_C"] == 100.0
    # Saturation pressure at 100°C should be ~1.013 bar
    assert 0.99 <= res["saturation_pressure_bar"] <= 1.03
    assert res["thermodynamic_region"] == "SATURATED_VAPOR_LIQUID"
    # Latent heat at 100°C is ~2257 kJ/kg
    assert 2200.0 <= res["latent_heat_hfg_kJ_kg"] <= 2300.0
    # Liquid density ~ 958 kg/m3 at 100°C
    assert 940.0 <= res["liquid_density_kg_m3"] <= 980.0


def test_steam_properties_pressure_input():
    res = calculate_steam_properties(pressure_bar=3.0)
    assert res["pressure_bar"] == 3.0
    # Saturation temperature at 3 bar is ~133.5°C
    assert 130.0 <= res["temperature_C"] <= 136.0


def test_peng_robinson_eos_gas_mixture():
    res = peng_robinson_eos(
        compounds=["methane", "ethane", "propane"],
        mole_fractions=[0.7, 0.2, 0.1],
        temperature_C=25.0,
        pressure_bar=30.0
    )
    assert res["Z_vapor"] > 0.7
    assert "methane" in res["fugacity_coeff_vapor_phi_V"]
    assert 0.5 <= res["fugacity_coeff_vapor_phi_V"]["methane"] <= 1.1

