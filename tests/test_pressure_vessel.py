"""
Unit tests for ASME BPVC Section VIII Div 1 Pressure Vessel Engine
"""

import pytest
from agentic_chemeng.pressure_vessel.equations import (
    calculate_shell_thickness_ug27,
    calculate_dished_head_ug32,
    calculate_nozzle_reinforcement_ug37,
    calculate_hydrostatic_test_ug99,
    get_allowable_stress
)


def test_allowable_stress_lookup():
    s_316L = get_allowable_stress("SA-240 316L", 100.0)
    assert s_316L == 115.0

    s_cs = get_allowable_stress("SA-516 Gr 70", 100.0)
    assert s_cs == 138.0


def test_ug27_shell_thickness():
    res = calculate_shell_thickness_ug27(
        design_pressure_bar=10.0,
        inside_diameter_mm=1200.0,
        design_temp_C=100.0,
        material="SA-240 316L",
        weld_joint_efficiency=1.0,
        corrosion_allowance_mm=1.5
    )
    # P = 1.0 MPa, R = 600 mm, S = 115 MPa, E = 1.0
    # t_calc = 1.0 * 600 / (115 - 0.6) = 600 / 114.4 = 5.245 mm
    # t_min = 5.245 + 1.5 = 6.745 mm -> Recommended plate = 8.0 mm
    assert abs(res["pressure_calc_thickness_mm"] - 5.245) < 0.05
    assert abs(res["minimum_required_thickness_mm"] - 6.745) < 0.05
    assert res["recommended_plate_thickness_mm"] == 8.0
    assert res["mawp_corroded_bar"] > 10.0


def test_ug32_dished_head():
    res = calculate_dished_head_ug32(
        design_pressure_bar=10.0,
        inside_diameter_mm=1200.0,
        head_type="ellipsoidal_2_1",
        design_temp_C=100.0,
        material="SA-240 316L",
        corrosion_allowance_mm=1.5
    )
    assert res["minimum_required_thickness_mm"] > 0.0
    assert res["recommended_head_plate_mm"] >= res["minimum_required_thickness_mm"]


def test_ug37_nozzle_reinforcement():
    res = calculate_nozzle_reinforcement_ug37(
        vessel_id_mm=1200.0,
        shell_thickness_mm=10.0,
        nozzle_od_mm=168.3,
        nozzle_thickness_mm=7.11,
        design_pressure_bar=10.0,
        design_temp_C=100.0,
        material="SA-240 316L"
    )
    assert res["area_required_A_req_mm2"] > 0.0
    assert "is_reinforcement_adequate" in res


def test_ug99_hydrotest():
    res = calculate_hydrostatic_test_ug99(
        design_pressure_bar=10.0,
        design_temp_C=100.0,
        material="SA-240 316L"
    )
    # S_test at 20°C is 115, S_design at 100°C is 115 -> ratio = 1.0
    # P_hydro = 1.3 * 10 = 13.0 bar
    assert abs(res["minimum_hydrotest_pressure_bar"] - 13.0) < 0.05

