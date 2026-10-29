"""
Unit tests for Process Hydraulics Engine
"""

import pytest
from agentic_chemeng.hydraulics.equations import (
    get_pipe_dimensions,
    calculate_friction_factor,
    calculate_pressure_drop,
    calculate_pump_tdh_and_npsha
)


def test_pipe_dimensions_dn100():
    dims = get_pipe_dimensions(100, schedule="sch40")
    assert dims["nominal_diameter_DN"] == 100
    assert dims["outside_diameter_mm"] == 114.3
    assert dims["wall_thickness_mm"] == 6.02
    assert abs(dims["inside_diameter_mm"] - 102.26) < 0.05
    assert dims["flow_area_m2"] > 0.008


def test_friction_factor():
    # Laminar flow Re = 1000 => f = 64 / 1000 = 0.064
    f_lam = calculate_friction_factor(1000, roughness_m=0.000045, inside_diameter_m=0.1)
    assert abs(f_lam - 0.064) < 1e-4

    # Turbulent flow Re = 100000
    f_turb = calculate_friction_factor(100000, roughness_m=0.000045, inside_diameter_m=0.1)
    assert 0.015 <= f_turb <= 0.025


def test_pressure_drop():
    res = calculate_pressure_drop(
        flow_m3_h=50.0,
        pipe_dn_mm=100,
        length_m=100.0,
        fluid="water",
        density_kg_m3=998.2,
        viscosity_cp=1.002
    )
    assert res["flow_regime"] == "TURBULENT"
    assert 1.4 <= res["velocity_m_s"] <= 1.8
    assert res["pressure_drop_bar"] > 0.01


def test_pump_tdh_and_npsha():
    res = calculate_pump_tdh_and_npsha(
        flow_m3_h=50.0,
        static_head_m=15.0,
        discharge_press_barg=3.0,
        suction_press_barg=0.2,
        suction_loss_m=0.5,
        discharge_loss_m=2.5,
        suction_static_lift_m=2.0
    )
    assert res["total_dynamic_head_m"] > 35.0
    assert res["npsh_available_m"] > 5.0
    assert res["npsh_satisfactory"] is True
    assert res["hydraulic_power_kW"] > 0.0
    assert res["recommended_motor_rating_kW"] >= res["brake_power_BHP_kW"]

