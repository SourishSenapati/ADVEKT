"""
Unit tests for Thermal Engineering Engine
"""

import pytest
from agentic_chemeng.thermal.equations import (
    calculate_lmtd,
    rate_tema_shell_and_tube,
    design_mvr_evaporator
)


def test_lmtd_counter_current():
    res = calculate_lmtd(th_in=120.0, th_out=80.0, tc_in=30.0, tc_out=60.0, shell_passes=1, tube_passes=1)
    # d1 = 120 - 60 = 60, d2 = 80 - 30 = 50 => LMTD = (60 - 50) / ln(60/50) = 54.85°C
    assert abs(res["lmtd_counter_current_C"] - 54.85) < 0.2
    assert res["FT_correction_factor"] == 1.0


def test_rate_tema_shell_and_tube():
    res = rate_tema_shell_and_tube(
        duty_kW=500.0,
        th_in=120.0,
        th_out=80.0,
        tc_in=30.0,
        tc_out=60.0,
        tube_count=240,
        tube_length_m=4.0
    )
    assert res["duty_kW"] == 500.0
    assert res["actual_area_m2"] > 40.0
    assert res["overall_U_fouled_W_m2_K"] > 500.0
    assert "is_adequately_sized" in res


def test_design_mvr_evaporator():
    res = design_mvr_evaporator(
        feed_flow_kg_h=2000.0,
        feed_solids_pct=5.0,
        product_solids_pct=35.0,
        evaporator_temp_C=80.0
    )
    # Mass balance: P = 2000 * 5 / 35 = 285.71 kg/h, W = 1714.29 kg/h
    assert abs(res["product_rate_kg_h"] - 285.71) < 0.1
    assert abs(res["evaporation_rate_kg_h"] - 1714.29) < 0.1
    assert res["heat_transfer_area_m2"] > 40.0
    assert res["compressor_electrical_draw_kW"] > 0.0

