"""
Agentic ChemEng - Example: ASME Section VIII Div 1 Pressure Vessel Design
Project Ref: FNQ-PR-2026-001 | Lead Engineer: Sourish Senapati (FinnoaQ Agro-Industrial Technologies Ltd.)
"""

import json
from agentic_chemeng.pressure_vessel.equations import (
    calculate_shell_thickness_ug27,
    calculate_dished_head_ug32,
    calculate_nozzle_reinforcement_ug37,
    calculate_hydrostatic_test_ug99
)


def run_vessel_case_study():
    print("=" * 70)
    print("AGENTIC CHEMENG: ASME BPVC SECTION VIII DIV 1 VESSEL CALCULATION")
    print("=" * 70)

    # Vessel specifications
    P_design_bar = 10.0
    ID_mm = 1200.0
    T_design_C = 120.0
    mat = "SA-240 316L"
    ca = 1.5

    # 1. Shell Thickness per UG-27(c)(1)
    shell = calculate_shell_thickness_ug27(
        design_pressure_bar=P_design_bar,
        inside_diameter_mm=ID_mm,
        design_temp_C=T_design_C,
        material=mat,
        weld_joint_efficiency=1.0,
        corrosion_allowance_mm=ca
    )

    print("\n[ASME UG-27(c)(1) Cylindrical Shell]")
    print(f"Material:                  {shell['material']} (Allowable Stress: {shell['allowable_stress_S_MPa']} MPa)")
    print(f"Pressure Thickness:        {shell['pressure_calc_thickness_mm']} mm")
    print(f"Min Required (+ CA):       {shell['minimum_required_thickness_mm']} mm")
    print(f"Recommended Plate:         {shell['recommended_plate_thickness_mm']} mm")
    print(f"MAWP Corroded:             {shell['mawp_corroded_bar']} bar")

    # 2. Formed Head per UG-32(d)
    head = calculate_dished_head_ug32(
        design_pressure_bar=P_design_bar,
        inside_diameter_mm=ID_mm,
        head_type="ellipsoidal_2_1",
        design_temp_C=T_design_C,
        material=mat,
        corrosion_allowance_mm=ca
    )

    print("\n[ASME UG-32(d) 2:1 Ellipsoidal Formed Head]")
    print(f"Min Required Head Thick:   {head['minimum_required_thickness_mm']} mm")
    print(f"Recommended Head Plate:    {head['recommended_head_plate_mm']} mm")

    # 3. Nozzle Opening Area Replacement per UG-37
    nozzle = calculate_nozzle_reinforcement_ug37(
        vessel_id_mm=ID_mm,
        shell_thickness_mm=shell['recommended_plate_thickness_mm'],
        nozzle_od_mm=168.3,  # DN 150 nozzle
        nozzle_thickness_mm=7.11,
        design_pressure_bar=P_design_bar,
        design_temp_C=T_design_C,
        material=mat,
        corrosion_allowance_mm=ca
    )

    print("\n[ASME UG-37 Nozzle Reinforcement Check (DN 150)]")
    print(f"Area Required (A_req):     {nozzle['area_required_A_req_mm2']} mm2")
    print(f"Total Area Available:      {nozzle['total_area_available_mm2']} mm2")
    print(f"Area Ratio (Avail / Req):  {nozzle['area_ratio']}")
    print(f"Reinforcement Adequate:    {nozzle['is_reinforcement_adequate']}")

    # 4. Hydrostatic Proof Test per UG-99(b)
    hydro = calculate_hydrostatic_test_ug99(
        design_pressure_bar=P_design_bar,
        design_temp_C=T_design_C,
        material=mat
    )

    print("\n[ASME UG-99(b) Hydrostatic Test Pressure]")
    print(f"Minimum Test Pressure:     {hydro['minimum_hydrotest_pressure_bar']} bar abs ({hydro['minimum_hydrotest_pressure_barg']} barg)")
    print("=" * 70)


if __name__ == "__main__":
    run_vessel_case_study()

