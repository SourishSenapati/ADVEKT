"""
Agentic ChemEng - ASME BPVC Section VIII Division 1 Pressure Vessel Engine
Lead Chemical & Process Engineer: Sourish Senapati

Provides rigorous mechanical engineering derivations:
1. UG-27(c)(1): Cylindrical Shell Thickness under Internal Pressure.
2. UG-32(d): 2:1 Ellipsoidal Formed Heads Thickness.
3. UG-32(e): Torispherical (ASME Flanged & Dished) Heads Thickness.
4. UG-37: Nozzle Opening Area Replacement & Reinforcement Verification.
5. UG-99: Minimum Hydrostatic Proof Test Pressure.
6. ASME Section II Part D Maximum Allowable Stress Material Database.
"""

import math
from ..resilience import EngineeringValidationError

# Maximum Allowable Stress S (MPa) per ASME BPVC Section II Part D Table 1A
# Material Key: {temp_C: S_MPa}
MATERIAL_STRESS_DB = {
    "SA-240 316L": {40: 115.0, 100: 115.0, 150: 108.0, 200: 101.0, 250: 96.0, 300: 92.0},
    "SA-240 316":  {40: 138.0, 100: 138.0, 150: 130.0, 200: 124.0, 250: 119.0, 300: 115.0},
    "SA-240 304L": {40: 115.0, 100: 115.0, 150: 104.0, 200: 96.0, 250: 90.0, 300: 86.0},
    "SA-240 304":  {40: 138.0, 100: 138.0, 150: 125.0, 200: 117.0, 250: 112.0, 300: 108.0},
    "SA-516 Gr 70":{40: 138.0, 100: 138.0, 150: 138.0, 200: 138.0, 250: 138.0, 300: 135.0},
    "SA-106 Gr B": {40: 118.0, 100: 118.0, 150: 118.0, 200: 118.0, 250: 118.0, 300: 115.0},
}


def get_allowable_stress(material_name, design_temp_C):
    """Retrieves ASME Section II Part D allowable stress S (MPa) with temperature interpolation."""
    mat_key = material_name.strip()
    if mat_key not in MATERIAL_STRESS_DB:
        # Search case-insensitive
        match = next((k for k in MATERIAL_STRESS_DB if k.lower() == mat_key.lower()), None)
        if match:
            mat_key = match
        else:
            # Default to SA-240 316L
            mat_key = "SA-240 316L"

    temps = sorted(MATERIAL_STRESS_DB[mat_key].keys())
    t_c = float(design_temp_C)

    if t_c <= temps[0]:
        return MATERIAL_STRESS_DB[mat_key][temps[0]]
    if t_c >= temps[-1]:
        return MATERIAL_STRESS_DB[mat_key][temps[-1]]

    # Linear interpolation
    for i in range(len(temps) - 1):
        t1, t2 = temps[i], temps[i + 1]
        if t1 <= t_c <= t2:
            s1, s2 = MATERIAL_STRESS_DB[mat_key][t1], MATERIAL_STRESS_DB[mat_key][t2]
            return round(s1 + (s2 - s1) * (t_c - t1) / (t2 - t1), 2)

    return 115.0


def calculate_shell_thickness_ug27(
    design_pressure_bar,
    inside_diameter_mm,
    design_temp_C=100.0,
    material="SA-240 316L",
    weld_joint_efficiency=1.0,  # 1.0 = Full RT (UW-11(a)), 0.85 = Spot RT (UW-11(b)), 0.70 = No RT
    corrosion_allowance_mm=1.5
):
    """
    Computes minimum required cylindrical shell thickness per ASME Section VIII Div 1 UG-27(c)(1).
    t = (P * R) / (S * E - 0.6 * P) + CA
    """
    P_mpa = float(design_pressure_bar) * 0.1  # bar to MPa
    R_mm = float(inside_diameter_mm) / 2.0
    E = float(weld_joint_efficiency)
    CA = float(corrosion_allowance_mm)
    S_mpa = get_allowable_stress(material, design_temp_C)

    denom = (S_mpa * E) - (0.6 * P_mpa)
    if denom <= 0:
        raise EngineeringValidationError("Design pressure exceeds material allowable stress limit.")

    t_calc_mm = (P_mpa * R_mm) / denom
    t_min_mm = t_calc_mm + CA

    # Standard nominal plate commercial thicknesses (mm): 3, 4, 5, 6, 8, 10, 12, 14, 16, 18, 20, 22, 25
    standard_plates = [3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0, 18.0, 20.0, 22.0, 25.0, 30.0, 35.0, 40.0]
    rec_plate_mm = next((p for p in standard_plates if p >= t_min_mm), math.ceil(t_min_mm))

    # Maximum Allowable Working Pressure (MAWP) in corroded condition
    t_corroded = rec_plate_mm - CA
    mawp_mpa = (S_mpa * E * t_corroded) / (R_mm + 0.6 * t_corroded)
    mawp_bar = mawp_mpa * 10.0

    return {
        "design_pressure_bar": design_pressure_bar,
        "inside_diameter_mm": inside_diameter_mm,
        "design_temperature_C": design_temp_C,
        "material": material,
        "allowable_stress_S_MPa": S_mpa,
        "joint_efficiency_E": E,
        "corrosion_allowance_mm": CA,
        "pressure_calc_thickness_mm": round(t_calc_mm, 3),
        "minimum_required_thickness_mm": round(t_min_mm, 3),
        "recommended_plate_thickness_mm": rec_plate_mm,
        "mawp_corroded_bar": round(mawp_bar, 2),
        "code_clause": "ASME BPVC Section VIII Div 1 UG-27(c)(1) Cylindrical Shells"
    }


def calculate_dished_head_ug32(
    design_pressure_bar,
    inside_diameter_mm,
    head_type="ellipsoidal_2_1",  # "ellipsoidal_2_1" or "torispherical"
    design_temp_C=100.0,
    material="SA-240 316L",
    weld_joint_efficiency=1.0,
    corrosion_allowance_mm=1.5
):
    """
    Computes minimum required formed head thickness per ASME Section VIII Div 1 UG-32.
    UG-32(d) 2:1 Ellipsoidal Head: t = (P * D) / (2 * S * E - 0.2 * P) + CA
    UG-32(e) Torispherical Head:   t = (0.885 * P * L) / (S * E - 0.1 * P) + CA
    """
    P_mpa = float(design_pressure_bar) * 0.1
    D_mm = float(inside_diameter_mm)
    E = float(weld_joint_efficiency)
    CA = float(corrosion_allowance_mm)
    S_mpa = get_allowable_stress(material, design_temp_C)

    if head_type.lower() in ["ellipsoidal", "ellipsoidal_2_1", "2:1"]:
        code_clause = "ASME Section VIII Div 1 UG-32(d) 2:1 Ellipsoidal Head"
        denom = (2.0 * S_mpa * E) - (0.2 * P_mpa)
        t_calc_mm = (P_mpa * D_mm) / denom
    else:
        # Torispherical (ASME F&D: crown L = D)
        code_clause = "ASME Section VIII Div 1 UG-32(e) Torispherical Head"
        denom = (S_mpa * E) - (0.1 * P_mpa)
        t_calc_mm = (0.885 * P_mpa * D_mm) / denom

    t_min_mm = t_calc_mm + CA
    standard_plates = [3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0, 18.0, 20.0, 22.0, 25.0, 30.0]
    rec_plate_mm = next((p for p in standard_plates if p >= t_min_mm), math.ceil(t_min_mm))

    return {
        "head_type": head_type,
        "design_pressure_bar": design_pressure_bar,
        "inside_diameter_mm": inside_diameter_mm,
        "material": material,
        "allowable_stress_S_MPa": S_mpa,
        "joint_efficiency_E": E,
        "corrosion_allowance_mm": CA,
        "pressure_calc_thickness_mm": round(t_calc_mm, 3),
        "minimum_required_thickness_mm": round(t_min_mm, 3),
        "recommended_head_plate_mm": rec_plate_mm,
        "code_clause": code_clause
    }


def calculate_nozzle_reinforcement_ug37(
    vessel_id_mm,
    shell_thickness_mm,
    nozzle_od_mm,
    nozzle_thickness_mm,
    design_pressure_bar,
    design_temp_C=100.0,
    material="SA-240 316L",
    corrosion_allowance_mm=1.5,
    weld_leg_outer_mm=6.0
):
    """
    Computes nozzle opening reinforcement area replacement per ASME Section VIII Div 1 UG-37.
    Evaluates Area Required (A_req) vs Area Available in Shell (A1), Nozzle Neck (A2), and Welds (A4).
    """
    P_mpa = float(design_pressure_bar) * 0.1
    R_mm = float(vessel_id_mm) / 2.0
    CA = float(corrosion_allowance_mm)
    S_mpa = get_allowable_stress(material, design_temp_C)

    # Corroded dimensions
    t_shell_act = float(shell_thickness_mm)
    t_shell_corr = t_shell_act - CA
    t_nozzle_act = float(nozzle_thickness_mm)
    t_nozzle_corr = t_nozzle_act - CA

    d_opening_corr = float(nozzle_od_mm) - 2.0 * t_nozzle_corr  # Inside finished opening in corroded condition
    r_nozzle_corr = d_opening_corr / 2.0

    # Required thicknesses (t_r for shell, t_rn for nozzle)
    tr_shell = (P_mpa * R_mm) / ((S_mpa * 1.0) - (0.6 * P_mpa))
    tr_nozzle = (P_mpa * r_nozzle_corr) / ((S_mpa * 1.0) - (0.6 * P_mpa))

    # Required Area: A_req = d * tr_shell * F (F=1.0 for all planes)
    A_req = d_opening_corr * tr_shell

    # Area available in shell (A1)
    # A1 = max( d * (E1*t - F*tr) - 2*tn*(E1*t - F*tr)*(1-fr1), 2*(t + tn)*(E1*t - F*tr) - 2*tn*(E1*t - F*tr)*(1-fr1) )
    # Assuming full weld efficiency E1=1.0, fr1=1.0
    excess_shell_t = max(0.0, t_shell_corr - tr_shell)
    A1 = max(d_opening_corr * excess_shell_t, 2.0 * (t_shell_corr + t_nozzle_corr) * excess_shell_t)

    # Area available in nozzle neck (A2)
    # Limit of reinforcement along nozzle wall h = min(2.5 * t_shell_corr, 2.5 * t_nozzle_corr)
    h_limit = min(2.5 * t_shell_corr, 2.5 * t_nozzle_corr)
    excess_nozzle_t = max(0.0, t_nozzle_corr - tr_nozzle)
    A2 = 2.0 * h_limit * excess_nozzle_t

    # Area available in outward fillet welds (A4)
    leg = float(weld_leg_outer_mm)
    A4 = 2.0 * 0.5 * (leg**2)

    total_avail = A1 + A2 + A4
    is_adequate = total_avail >= A_req
    pad_area_needed = max(0.0, A_req - total_avail)

    return {
        "nozzle_opening_diameter_d_mm": round(d_opening_corr, 2),
        "shell_required_thickness_tr_mm": round(tr_shell, 3),
        "nozzle_required_thickness_trn_mm": round(tr_nozzle, 3),
        "area_required_A_req_mm2": round(A_req, 2),
        "area_available_shell_A1_mm2": round(A1, 2),
        "area_available_nozzle_A2_mm2": round(A2, 2),
        "area_available_welds_A4_mm2": round(A4, 2),
        "total_area_available_mm2": round(total_avail, 2),
        "area_ratio": round(total_avail / max(A_req, 1e-4), 3),
        "is_reinforcement_adequate": is_adequate,
        "reinforcement_pad_required": not is_adequate,
        "pad_area_needed_mm2": round(pad_area_needed, 2),
        "code_clause": "ASME BPVC Section VIII Div 1 UG-37 Nozzle Openings"
    }


def calculate_hydrostatic_test_ug99(design_pressure_bar, design_temp_C=100.0, material="SA-240 316L"):
    """
    Computes Standard Hydrostatic Test Pressure per ASME Section VIII Div 1 UG-99(b).
    P_hydro = 1.3 * MAWP * (S_test / S_design)
    Where S_test is allowable stress at ambient test temperature (20°C).
    """
    S_test = get_allowable_stress(material, 20.0)
    S_design = get_allowable_stress(material, design_temp_C)
    stress_ratio = S_test / S_design

    P_hydro_bar = 1.3 * float(design_pressure_bar) * stress_ratio

    return {
        "design_pressure_bar": design_pressure_bar,
        "design_temperature_C": design_temp_C,
        "material": material,
        "allowable_stress_ambient_S_test_MPa": S_test,
        "allowable_stress_design_S_design_MPa": S_design,
        "stress_ratio_Stest_over_Sdesign": round(stress_ratio, 3),
        "hydrotest_multiplier": 1.3,
        "minimum_hydrotest_pressure_bar": round(P_hydro_bar, 2),
        "minimum_hydrotest_pressure_barg": round(P_hydro_bar - 1.01325, 2),
        "code_clause": "ASME BPVC Section VIII Div 1 UG-99(b) Hydrostatic Test"
    }

