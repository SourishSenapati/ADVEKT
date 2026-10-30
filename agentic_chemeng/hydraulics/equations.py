"""
Agentic ChemEng - First-Principles Process Hydraulics Engine
Lead Chemical & Process Engineer: Sourish Senapati

Provides rigorous industrial calculations:
1. ASME B36.10M / B36.19M standard pipe schedule dimension lookup (DN15 - DN600).
2. Darcy-Weisbach head loss & Colebrook-White friction factor via Newton-Raphson.
3. Fitting minor losses (Crane Technical Paper No. 410).
4. Centrifugal pump Total Dynamic Head (TDH) & Net Positive Suction Head Available (NPSHa).
5. Pump hydraulic power, brake horsepower (BHP), and motor sizing.
"""

import math
from ..resilience import EngineeringValidationError

G_ACCEL = 9.80665  # m/s^2

# Pipe Schedule Database per ASME B36.10M (Dimensions in mm)
# Keys: DN (mm) -> {"OD": mm, "sch40_wt": mm, "sch80_wt": mm, "sch10_wt": mm}
PIPE_SCHEDULES = {
    15:  {"OD": 21.34, "sch40_wt": 2.77, "sch80_wt": 3.73, "sch10_wt": 1.65},
    20:  {"OD": 26.67, "sch40_wt": 2.87, "sch80_wt": 3.91, "sch10_wt": 1.65},
    25:  {"OD": 33.40, "sch40_wt": 3.38, "sch80_wt": 4.55, "sch10_wt": 1.65},
    40:  {"OD": 48.26, "sch40_wt": 3.68, "sch80_wt": 5.08, "sch10_wt": 1.65},
    50:  {"OD": 60.33, "sch40_wt": 3.91, "sch80_wt": 5.54, "sch10_wt": 2.77},
    80:  {"OD": 88.90, "sch40_wt": 5.49, "sch80_wt": 7.62, "sch10_wt": 3.05},
    100: {"OD": 114.30, "sch40_wt": 6.02, "sch80_wt": 8.56, "sch10_wt": 3.05},
    150: {"OD": 168.28, "sch40_wt": 7.11, "sch80_wt": 10.97, "sch10_wt": 3.40},
    200: {"OD": 219.08, "sch40_wt": 8.18, "sch80_wt": 12.70, "sch10_wt": 3.76},
    250: {"OD": 273.05, "sch40_wt": 9.27, "sch80_wt": 15.09, "sch10_wt": 4.19},
    300: {"OD": 323.85, "sch40_wt": 10.31, "sch80_wt": 17.48, "sch10_wt": 4.57},
    400: {"OD": 406.40, "sch40_wt": 12.70, "sch80_wt": 21.44, "sch10_wt": 4.78},
    500: {"OD": 508.00, "sch40_wt": 15.09, "sch80_wt": 26.19, "sch10_wt": 5.54},
    600: {"OD": 610.00, "sch40_wt": 17.48, "sch80_wt": 30.96, "sch10_wt": 6.35},
}

# Crane TP 410 Resistance Coefficients (K-factors)
FITTING_K = {
    "elbow_90_std": 0.75,
    "elbow_90_lr": 0.45,
    "elbow_45_std": 0.35,
    "tee_through_run": 0.40,
    "tee_through_branch": 1.50,
    "gate_valve_full_open": 0.17,
    "globe_valve_full_open": 6.00,
    "swing_check_valve": 2.00,
    "ball_valve_full_bore": 0.05,
    "butterfly_valve": 0.30,
    "entrance_sharp": 0.50,
    "exit_pipe_to_tank": 1.00
}


def get_pipe_dimensions(dn_mm, schedule="sch40"):
    """Returns pipe outside diameter, wall thickness, inside diameter, and area in mm / m."""
    dn = int(dn_mm)
    if dn not in PIPE_SCHEDULES:
        valid_dns = sorted(list(PIPE_SCHEDULES.keys()))
        raise EngineeringValidationError(f"Nominal diameter DN {dn} not found. Available DN: {valid_dns}")

    spec = PIPE_SCHEDULES[dn]
    od = spec["OD"]
    sch_key = schedule.lower()
    if sch_key not in ["sch10", "sch40", "sch80"]:
        sch_key = "sch40"

    wt = spec[f"{sch_key}_wt"]
    id_mm = od - 2.0 * wt
    id_m = id_mm / 1000.0
    area_m2 = math.pi * (id_m / 2.0)**2

    return {
        "nominal_diameter_DN": dn,
        "schedule": sch_key.upper(),
        "outside_diameter_mm": round(od, 2),
        "wall_thickness_mm": round(wt, 2),
        "inside_diameter_mm": round(id_mm, 2),
        "inside_diameter_m": round(id_m, 5),
        "flow_area_m2": round(area_m2, 6)
    }


def calculate_friction_factor(reynolds_number, roughness_m, inside_diameter_m):
    """
    Computes Darcy friction factor using Colebrook-White equation for turbulent flow
    or f = 64/Re for laminar flow.
    """
    Re = float(reynolds_number)
    D = float(inside_diameter_m)
    eps = float(roughness_m)

    if Re <= 0:
        return 0.0
    if Re < 2300:
        return round(64.0 / Re, 5)

    # Turbulent: Colebrook-White implicit equation solved via Newton-Raphson
    # 1/sqrt(f) = -2 * log10( eps/(3.7*D) + 2.51/(Re*sqrt(f)) )
    # Initial guess via Haaland equation
    rel_rough = eps / D
    inv_sqrt_f_guess = -1.8 * math.log10((rel_rough / 3.7)**1.11 + 6.9 / Re)
    f = 1.0 / (inv_sqrt_f_guess**2)

    for _ in range(25):
        sqrt_f = math.sqrt(f)
        arg = (rel_rough / 3.7) + (2.51 / (Re * sqrt_f))
        if arg <= 0:
            break
        F = (1.0 / sqrt_f) + 2.0 * math.log10(arg)
        # Derivative dF/df
        dF_df = -0.5 * (f**(-1.5)) + (2.0 / (math.log(10.0) * arg)) * (-1.255 / (Re * (f**1.5)))
        if abs(dF_df) < 1e-12:
            break
        df = F / dF_df
        f -= df
        f = max(0.005, min(0.1, f))
        if abs(df) < 1e-6:
            break

    return round(f, 5)


def calculate_pressure_drop(flow_m3_h, pipe_dn_mm, length_m, fluid="water", density_kg_m3=998.2, viscosity_cp=1.002, roughness_mm=0.045, schedule="sch40", fittings=None):
    """
    Computes rigorous pipe pressure drop and velocity per Darcy-Weisbach & Crane TP 410.
    """
    pipe_dim = get_pipe_dimensions(pipe_dn_mm, schedule=schedule)
    D_m = pipe_dim["inside_diameter_m"]
    A_m2 = pipe_dim["flow_area_m2"]

    Q_m3_s = float(flow_m3_h) / 3600.0
    v_m_s = Q_m3_s / A_m2

    rho = float(density_kg_m3)
    mu_pa_s = float(viscosity_cp) * 1e-3  # cP to Pa.s
    Re = (rho * v_m_s * D_m) / max(mu_pa_s, 1e-6)

    eps_m = float(roughness_mm) * 1e-3
    f = calculate_friction_factor(Re, eps_m, D_m)

    # Major head loss (Darcy-Weisbach)
    L_m = float(length_m)
    vel_head = (v_m_s**2) / (2.0 * G_ACCEL)
    hf_major_m = f * (L_m / D_m) * vel_head

    # Minor losses
    total_K = 0.0
    fittings_detail = {}
    if fittings and isinstance(fittings, dict):
        for ftype, count in fittings.items():
            k_val = FITTING_K.get(ftype, 0.5)
            sub_k = k_val * count
            total_K += sub_k
            fittings_detail[ftype] = {"count": count, "K_each": k_val, "K_total": round(sub_k, 3)}

    hf_minor_m = total_K * vel_head
    hf_total_m = hf_major_m + hf_minor_m

    dp_pa = rho * G_ACCEL * hf_total_m
    dp_bar = dp_pa / 1e5

    return {
        "flow_m3_h": flow_m3_h,
        "pipe_dn": pipe_dn_mm,
        "inside_diameter_mm": pipe_dim["inside_diameter_mm"],
        "velocity_m_s": round(v_m_s, 3),
        "reynolds_number": round(Re, 1),
        "flow_regime": "LAMINAR" if Re < 2300 else ("TRANSITIONAL" if Re < 4000 else "TURBULENT"),
        "friction_factor": f,
        "velocity_head_m": round(vel_head, 3),
        "major_loss_m": round(hf_major_m, 3),
        "minor_loss_m": round(hf_minor_m, 3),
        "total_head_loss_m": round(hf_total_m, 3),
        "pressure_drop_bar": round(dp_bar, 4),
        "pressure_drop_kPa": round(dp_bar * 100.0, 2),
        "pressure_drop_per_100m_bar": round((dp_bar / max(L_m, 0.1)) * 100.0, 4),
        "fittings_breakdown": fittings_detail
    }


def calculate_pump_tdh_and_npsha(flow_m3_h, static_head_m, discharge_press_barg, suction_press_barg, suction_loss_m, discharge_loss_m, fluid_density_kg_m3=998.2, vapor_press_bara=0.0234, suction_static_lift_m=0.0, pump_eff=0.72, motor_eff=0.92):
    """
    Computes Centrifugal Pump Total Dynamic Head (TDH), NPSHa, hydraulic power, and motor rating.
    """
    rho = float(fluid_density_kg_m3)
    p_disch_pa = (float(discharge_press_barg) + 1.01325) * 1e5
    p_suct_pa = (float(suction_press_barg) + 1.01325) * 1e5

    # Head difference from pressure
    head_press_m = (p_disch_pa - p_suct_pa) / (rho * G_ACCEL)
    total_hf_m = float(suction_loss_m) + float(discharge_loss_m)
    tdh_m = float(static_head_m) + head_press_m + total_hf_m

    # NPSHa = (P_suct_abs - P_vap) / (rho*g) + z_suct - hf_suct
    p_vap_pa = float(vapor_press_bara) * 1e5
    npsha_m = (p_suct_pa - p_vap_pa) / (rho * G_ACCEL) + float(suction_static_lift_m) - float(suction_loss_m)

    # Power calculations
    Q_m3_s = float(flow_m3_h) / 3600.0
    p_hyd_w = rho * G_ACCEL * Q_m3_s * tdh_m
    p_hyd_kw = p_hyd_w / 1000.0
    p_brake_kw = p_hyd_kw / float(pump_eff)
    p_motor_kw = p_brake_kw / float(motor_eff)

    # Standard IEC motor frame sizing (kW): 0.75, 1.1, 1.5, 2.2, 3, 4, 5.5, 7.5, 11, 15, 18.5, 22, 30, 37, 45, 55, 75
    standard_motors = [0.75, 1.1, 1.5, 2.2, 3.0, 4.0, 5.5, 7.5, 11.0, 15.0, 18.5, 22.0, 30.0, 37.0, 45.0, 55.0, 75.0, 90.0, 110.0]
    rec_motor = next((m for m in standard_motors if m >= p_brake_kw * 1.15), round(p_brake_kw * 1.25, 1))

    return {
        "flow_m3_h": flow_m3_h,
        "total_dynamic_head_m": round(tdh_m, 2),
        "pressure_rise_bar": round((tdh_m * rho * G_ACCEL) / 1e5, 3),
        "npsh_available_m": round(npsha_m, 2),
        "npsh_satisfactory": npsha_m >= 3.0,
        "hydraulic_power_kW": round(p_hyd_kw, 2),
        "brake_power_BHP_kW": round(p_brake_kw, 2),
        "motor_power_draw_kW": round(p_motor_kw, 2),
        "recommended_motor_rating_kW": rec_motor,
        "pump_efficiency": pump_eff,
        "governing_standard": "Hydraulic Institute (HI) & ISO 9906 Rotodynamic Pumps"
    }

