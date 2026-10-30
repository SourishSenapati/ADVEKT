"""
Agentic ChemEng - Example: Process Hydraulics & Pumping Loop Design
Lead Chemical & Process Engineer: Sourish Senapati
"""

import json
from agentic_chemeng.hydraulics.equations import (
    get_pipe_dimensions,
    calculate_pressure_drop,
    calculate_pump_tdh_and_npsha
)


def run_hydraulics_case_study():
    print("=" * 70)
    print("AGENTIC CHEMENG: PROCESS HYDRAULICS & PUMP SIZING STUDY")
    print("=" * 70)

    # 1. Pipe Geometry Lookup per ASME B36.10M
    dn = 100  # 4-inch nominal pipe
    pipe_spec = get_pipe_dimensions(dn, schedule="sch40")
    print("\n[ASME B36.10M Pipe Dimensions - DN 100 Sch 40]")
    print(f"Outside Diameter:          {pipe_spec['outside_diameter_mm']} mm")
    print(f"Wall Thickness:            {pipe_spec['wall_thickness_mm']} mm")
    print(f"Inside Diameter:           {pipe_spec['inside_diameter_mm']} mm")
    print(f"Flow Area:                 {pipe_spec['flow_area_m2']} m2")

    # 2. Piping Line Pressure Drop Calculation (Darcy-Weisbach)
    fittings = {
        "elbow_90_lr": 6,
        "gate_valve_full_open": 2,
        "swing_check_valve": 1,
        "entrance_sharp": 1,
        "exit_pipe_to_tank": 1
    }

    dp_result = calculate_pressure_drop(
        flow_m3_h=60.0,
        pipe_dn_mm=100,
        length_m=85.0,
        fluid="water",
        density_kg_m3=998.2,
        viscosity_cp=1.002,
        fittings=fittings
    )

    print("\n[Darcy-Weisbach & Colebrook-White Pressure Drop]")
    print(f"Flow Rate:                 {dp_result['flow_m3_h']} m3/h")
    print(f"Line Velocity:             {dp_result['velocity_m_s']} m/s (Recommended: 1.5 - 2.5 m/s)")
    print(f"Reynolds Number:           {dp_result['reynolds_number']} ({dp_result['flow_regime']})")
    print(f"Darcy Friction Factor:     {dp_result['friction_factor']}")
    print(f"Major Pipe Loss:           {dp_result['major_loss_m']} m")
    print(f"Minor Fitting Loss:        {dp_result['minor_loss_m']} m")
    print(f"Total Piping Head Loss:    {dp_result['total_head_loss_m']} m ({dp_result['pressure_drop_bar']} bar)")

    # 3. Centrifugal Pump Sizing
    pump_result = calculate_pump_tdh_and_npsha(
        flow_m3_h=60.0,
        static_head_m=18.0,
        discharge_press_barg=2.5,
        suction_press_barg=0.1,
        suction_loss_m=0.8,
        discharge_loss_m=dp_result['total_head_loss_m'],
        suction_static_lift_m=3.0,
        pump_eff=0.74,
        motor_eff=0.93
    )

    print("\n[Centrifugal Pump Total Dynamic Head & NPSHa]")
    print(f"Total Dynamic Head (TDH):  {pump_result['total_dynamic_head_m']} m ({pump_result['pressure_rise_bar']} bar rise)")
    print(f"NPSH Available (NPSHa):    {pump_result['npsh_available_m']} m (Adequate: {pump_result['npsh_satisfactory']})")
    print(f"Hydraulic Power:           {pump_result['hydraulic_power_kW']} kW")
    print(f"Brake Horsepower (BHP):    {pump_result['brake_power_BHP_kW']} kW")
    print(f"Electrical Motor Draw:     {pump_result['motor_power_draw_kW']} kW")
    print(f"Recommended Motor Frame:   {pump_result['recommended_motor_rating_kW']} kW standard IEC frame")
    print("=" * 70)


if __name__ == "__main__":
    run_hydraulics_case_study()

