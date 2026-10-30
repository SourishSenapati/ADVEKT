"""
Agentic ChemEng - Example: Industrial MVR Falling-Film Evaporator Simulation
Lead Chemical & Process Engineer: Sourish Senapati
"""

import json
from agentic_chemeng.thermal.equations import design_mvr_evaporator
from agentic_chemeng.thermo.equations import calculate_steam_properties


def run_mvr_case_study():
    print("=" * 70)
    print("AGENTIC CHEMENG: MVR FALLING-FILM EVAPORATOR DESIGN STUDY")
    print("=" * 70)

    # 1. Thermal Design of Evaporator
    evap_result = design_mvr_evaporator(
        feed_flow_kg_h=2500.0,
        feed_solids_pct=5.5,
        product_solids_pct=35.0,
        evaporator_temp_C=78.0,
        compressor_temp_rise_C=8.5,
        overall_U_W_m2_K=2250.0
    )

    print("\n[Evaporator Mass & Energy Balance]")
    print(f"Feed Flow Rate:            {evap_result['feed_rate_kg_h']} kg/h (at 5.5% solids)")
    print(f"Evaporation Rate:          {evap_result['evaporation_rate_kg_h']} kg/h of pure water vapor")
    print(f"Concentrated Product:      {evap_result['product_rate_kg_h']} kg/h (at 35.0% solids)")
    print(f"Concentration Factor:      {evap_result['concentration_factor']}x")
    print(f"Required Heat Duty:        {evap_result['thermal_duty_kW']} kW")
    print(f"Heat Transfer Area:        {evap_result['heat_transfer_area_m2']} m2")

    print("\n[Vapor Compression & Energy Efficiency]")
    print(f"Compressor Shaft Power:    {evap_result['compressor_shaft_power_kW']} kW")
    print(f"Electrical Motor Draw:     {evap_result['compressor_electrical_draw_kW']} kW")
    print(f"Specific Energy:           {evap_result['specific_energy_kWh_per_tonne_water']} kWh / tonne water evaporated")
    print(f"Steam Savings vs Direct:   {evap_result['steam_savings_vs_direct_steam_percent']}%")

    # 2. Thermodynamic Properties of Compressed Vapor
    steam_props = calculate_steam_properties(temperature_C=78.0 + 8.5)
    print("\n[Recompressed Motive Vapor Properties (at Calandria Shell)]")
    print(f"Saturation Pressure:       {steam_props['saturation_pressure_bar']} bar absolute")
    print(f"Latent Heat of Condens.:   {steam_props['latent_heat_hfg_kJ_kg']} kJ/kg")
    print(f"Specific Volume of Vapor:  {steam_props['specific_volume_vapor_m3_kg']} m3/kg")
    print("=" * 70)


if __name__ == "__main__":
    run_mvr_case_study()

