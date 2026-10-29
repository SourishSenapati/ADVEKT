```
    ___     ____ _    __ ______ __ __ ______
   /   |   / __ \ |  / // ____// //_//_  __/
  / /| |  / / / / | / // __/  / ,<    / /   
 / ___ | / /_/ /| |/ // /___ / /| |  / /    
/_/  |_|/_____/ |___//_____//_/ |_| /_/     
```

# ADVEKT (`advekt`)

**Autonomous Multi-Discipline Chemical & Mechanical Engineering CAE Suite with Native RAEBYES Circuit Breaking**  
*The Invariant Velocity Field of Continuous Matter*  

[![Python 3.10+](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue.svg?style=flat-square)](https://www.python.org/)
[![MCP Server](https://img.shields.io/badge/MCP-60%20Tools%20(JSON--RPC%202.0)-8A2BE2.svg?style=flat-square)](https://modelcontextprotocol.io/)
[![CLI Binaries](https://img.shields.io/badge/CLI-21%20Executables-00bcd4.svg?style=flat-square)](https://github.com/SourishSenapati/ADVEKT)
[![Tests Passing](https://img.shields.io/badge/tests-60%2F60%20passed%20(100%25)-brightgreen.svg?style=flat-square)](https://github.com/SourishSenapati/ADVEKT)
[![Circuit Breaker](https://img.shields.io/badge/RAEBYES-Invariant%20Protected-orange.svg?style=flat-square)](https://github.com/SourishSenapati/RAEBYES)
[![License](https://img.shields.io/badge/license-Commercial%20%26%20IP%20Protection%20v1.0-red.svg?style=flat-square)](LICENSE)
[![Monetization Protected](https://img.shields.io/badge/monetization-IP%20Reserved%20(Sourish%20Senapati)-blueviolet.svg?style=flat-square)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg?style=flat-square)](https://github.com/SourishSenapati/ADVEKT)

*Project Ref:* `FNQ-PR-2026-001`  
*Lead Chemical & Process Engineer:* **Sourish Senapati** (*FinnoaQ Agro-Industrial Technologies Ltd.*)  
*License:* ADVEKT Source-Available Commercial & IP Protection License v1.0 (Non-Commercial/Academic Free; Commercial License Required)    

---

## 1. The Cryptic Philosophy & Physical Cipher

**ADVEKT** (/ædˈvɛkt/) is named after the fundamental **advection operator** of continuum mechanics and transport phenomena:

$$\mathbf{u} \cdot \nabla c \quad \text{and} \quad \rho (\mathbf{u} \cdot \nabla) \mathbf{u}$$

In physical fluid dynamics, **advection** is the immutable velocity field that transports continuous matter, momentum, and enthalpy across physical boundaries. It is the realization of Heraclitus's continuum flux (*Panta Rhei*) strictly constrained by the conservation laws (*The Logos*). Continuous matter cannot be forged; mass cannot be hallucinated.

In autonomous artificial intelligence, **ADVEKT** is the deterministic velocity field that propels AI coding agents (Claude, Cursor, Antigravity, Gemini) through rigorous chemical and mechanical engineering tasks without permitting them to drift into superficial "vibe coding," synthetic mock arrays, or unverified hallucinations.

### The Anti-Hallucination Mandate
Superficial AI coding assistants frequently fabricate plausible-sounding chemical yields, random pipe wall thicknesses, and synthetic temperature arrays. In industrial chemical plants, boiler islands, and high-pressure reactors, unverified numbers lead to catastrophic physical failure. 

**ADVEKT eliminates hallucination through three inviolable architectural principles:**
1. **Direct Software COM Automation:** On Windows, ADVEKT directly controls authentic, licensed CAD/CAE software (SolidWorks, Aspen Plus, Aspen HYSYS, AutoCAD, CHEMCAD, PRO/II) via official OLE/COM APIs.
2. **Headless Linux Physics Solvers:** On Linux and cloud containers where COM is absent, ADVEKT dispatches exact, analytical, first-principles solvers (ASME Section VIII Div 1, Darcy-Weisbach Colebrook-White, ASME STEAM-TA steam tables, Peng-Robinson Cubic EOS, TEMA Kern shell-and-tube rating).
3. **Hardwired Invariant Circuit Breaking:** Integrated natively with [`SourishSenapati/RAEBYES`](https://github.com/SourishSenapati/RAEBYES). If any AI-generated stream table violates conservation of mass ($\delta_{\text{mass}} \ge 10^{-4}$) or outputs flat synthetic arrays ($\operatorname{Var} < 10^{-6}$), the circuit breaker trips instantly, preventing corrupted data from entering downstream CAD models or fabrication drawings.

---

## 2. System Architecture & Dual Interfaces

```
                    ┌────────────────────────────────────────────────────────┐
                    │                      A D V E K T                       │
                    └───────────────────────────┬────────────────────────────┘
                                                │
                 ┌──────────────────────────────┴──────────────────────────────┐
                 ▼                                                             ▼
   ┌───────────────────────────┐                                 ┌───────────────────────────┐
   │    HIGH-PERFORMANCE CLI   │                                 │     MCP SERVER ENGINE     │
   │      (21 Executables)     │                                 │     (60 Tools JSON-RPC)   │
   ├───────────────────────────┤                                 ├───────────────────────────┤
   │  • advekt status (<0.2s)  │                                 │  • Claude Desktop         │
   │  • solidworks-cli         │                                 │  • Cursor / Antigravity   │
   │  • aspen-plus-cli / hysys │                                 │  • Gemini CLI / Copilot   │
   │  • thermo-cli / pv-cli    │                                 │  • Stdio non-blocking     │
   │  • hydraulics / thermal   │                                 │  • Zero zombie processes  │
   └─────────────┬─────────────┘                                 └─────────────┬─────────────┘
                 │                                                             │
                 └──────────────────────────────┬──────────────────────────────┘
                                                ▼
     ┌──────────────────────────────────────────────────────────────────────────────────┐
     │                     THE 17 ENGINEERING DISCIPLINES & SOLVERS                     │
     ├────────────────────────────────────────┬─────────────────────────────────────────┤
     │  Windows COM Automation (Live Apps):   │  Native Linux / POSIX Solvers (No COM): │
     │  • Dassault Systèmes SOLIDWORKS 2025   │  • ASME STEAM-TA / PR-EOS Thermo        │
     │  • Aspen Technology Aspen Plus V14     │  • ASME B36.10M / Crane TP 410 Flow     │
     │  • Aspen Technology Aspen HYSYS        │  • TEMA / Kern Heat Exchanger Rating    │
     │  • Chemstations CHEMCAD v7/v8          │  • ASME BPVC Section VIII Div 1 PV      │
     │  • AVEVA SimSci PRO/II                 │  • Cantera Reaction Kinetics (Arrhenius)│
     │  • Autodesk AutoCAD 2025               │  • DWSIM Open-Source Flowsheet XML      │
     │  • Honeywell UniSim Design             │  • COMSOL & Ansys Fluent Headless Audits│
     └────────────────────────────────────────┴─────────────────────────────────────────┘
                                                │
                                                ▼
     ┌──────────────────────────────────────────────────────────────────────────────────┐
     │                     NATIVE RAEBYES CIRCUIT BREAKER INTEGRATION                   │
     │       Strict Invariant Enforcement: Zero Mass & Energy Closure Error (< 1e-4)    │
     │       Non-Blocking Diagnostics: ROT inspection in < 0.2s | Memory-Leak Free      │
     └──────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Subsystem Matrix & Supported Standards

| Subsystem | Underlying Engine | Key Capabilities | Standards / Formats | Platform Support |
| :--- | :--- | :--- | :--- | :--- |
| **SolidWorks** | Dassault Systèmes SOLIDWORKS 2025 SP1.2 (`SldWorks.Application`) | Parametric 3D solid modeling, feature tree traversal, assembly constraints, mass properties, high-res viewport rendering, STEP/PDF export | `.SLDPRT`, `.SLDASM`, `.SLDDRW`, `.STEP`, B-Rep solid math | Windows (COM Automation) |
| **Aspen Plus** | Aspen Technology Aspen Plus V14 (`Apwn.Document` OLE Services) | Rigorous flowsheet topology inspection, stream balance extraction, unit block duty schedules, live solver execution (`Run2`), offline converged audit | `.bkp`, `.apw`, `.inp`, ASME STEAM-TA, NRTL, ELECNRTL | Windows (COM) + Linux (Offline Audit) |
| **Aspen HYSYS** | Aspen Technology Aspen HYSYS (`HYSYS.Application` COM) | Dynamic & steady-state hydrocarbon/chemical flowsheets, material/energy streams, unit operations, property packages | `.hsc`, Peng-Robinson, Sour PR, SRK, Glycol, Amines | Windows (COM) + Linux (Offline Case Parsing) |
| **CHEMCAD** | Chemstations CHEMCAD v7/v8 (`CHEMCAD.Application` COM) | Chemical process flowsheet inspection, unit operations, streams, and batch distillation modeling | `.ccx`, `.cc5`, `.cc6`, NRTL, UNIQUAC, Peng-Robinson | Windows (COM) + Linux (Offline XML/CCX) |
| **PRO/II** | AVEVA SimSci PRO/II (`PROII.Application` COM) | Refinery, gas processing, and petrochemical flowsheet simulation and archive inspection | `.prz`, `.pr2`, `.inp`, SRK, Peng-Robinson, Grayson-Streed | Windows (COM) + Linux (Offline PRZ Parsing) |
| **Cantera** | Cantera Chemical Physics Suite (Open-Source) | Chemical reaction kinetics (Arrhenius law), multi-component gas transport properties (Sutherland viscosity, thermal conductivity), Gibbs equilibrium | Cantera YAML / XML / CTI, Kinetic Theory of Gases | **Native Cross-Platform (Linux, macOS, Windows)** |
| **UniSim Design** | Honeywell UniSim Design (`UniSimDesign.Application` COM) | Refining, gas processing, and petrochemical flowsheet inspection and property packages | `.usc`, `.hsc`, Peng-Robinson, Kabadi-Danner | Windows (COM) + Linux (Offline Inspection) |
| **Siemens gPROMS** | Siemens / PSE gPROMS ProcessBuilder & ModelBuilder | Advanced equation-oriented process modeling, distributed systems (PDEs/DAEs), dynamic simulation, parameter estimation | `.gPJ`, `.gPA`, `.xml`, Custom DAEs, Catalytic / Polymer Systems | Windows (COM/CLI) + Linux (Offline Parsing) |
| **COMSOL Multiphysics** | COMSOL Multiphysics Suite | Chemical reaction engineering (`cheq`), transport of diluted/concentrated species (`tds`/`tcs`), heat transfer in fluids (`ht`), laminar flow (`spf`) | `.mph`, Finite Element Analysis, Multiphysics Coupling | **Native Headless Inspection (Linux, macOS, Windows)** + Batch CLI |
| **Ansys Fluent & CFX** | Ansys Fluent & CFX Fluid Dynamics | Reacting flow CFD, finite-rate combustion kinetics, multi-component species transport, multiphase Eulerian/VOF/DPM | `.cas`, `.cas.gz`, `.cas.h5`, `.def`, `.cfx`, `.jou` | **Native Headless Inspection (Linux & Windows)** + Batch Journal Solver |
| **DWSIM** | DWSIM Open-Source Simulator (v8/v9) | Open-source process simulation, CAPE-OPEN thermodynamics, XML flowsheet inspection, Rachford-Rice VLE flash | `.dwsim`, `.dwxml`, CoolProp, UNIFAC, IAPWS-IF97 | **Native Cross-Platform (Linux & Windows)** |
| **AutoCAD** | Autodesk AutoCAD 2025 (`AutoCAD.Application` & `accoreconsole.exe`) | Automated P&ID and General Arrangement drafting, title block verification, layer auditing, headless DWG-to-PDF/DXF batch conversion | `.dwg`, `.dxf`, Vector PDF, ANSI/ISO title blocks | Windows (COM & accoreconsole) |
| **Thermodynamics** | First-Principles Thermodynamics Engine | High-precision steam tables (ASME STEAM-TA / IAPWS-95 6-term), Peng-Robinson Cubic Equation of State (PR-EOS), analytical Cardano cubic root solver, fugacity coefficients, Wagner/Antoine vapor pressure | ASME 1967 Steam Tables, IAPWS Industrial Formulation, PR (1976) | **Native Cross-Platform (Pure Python / No COM Required)** |
| **Process Hydraulics** | First-Principles Hydraulics Engine | Darcy-Weisbach head loss, Colebrook-White friction factor (Newton-Raphson), ASME B36.10M standard pipe schedules, Crane TP 410 minor losses, Pump TDH, NPSHa, motor sizing | ASME B36.10M, Crane TP 410, Hydraulic Institute (HI) | **Native Cross-Platform (Pure Python / No COM Required)** |
| **Thermal Design** | Industrial Heat Transfer Engine | TEMA E shell-and-tube heat exchanger rating (Kern method), LMTD & $F_T$ configuration correction, MVR falling-film evaporator mass/energy balances, compressor power & specific energy | TEMA 10th Ed Class C/R, Kern Method, MVR Industrial Design | **Native Cross-Platform (Pure Python / No COM Required)** |
| **Pressure Vessels** | ASME Section VIII Div 1 Mechanical Engine | UG-27(c)(1) cylindrical shell thickness under internal pressure, UG-32(d) 2:1 ellipsoidal heads, UG-32(e) torispherical heads, UG-37 nozzle opening area replacement, UG-99 hydrostatic test pressure | ASME BPVC Section VIII Div 1, ASME Section II Part D | **Native Cross-Platform (Pure Python / No COM Required)** |
| **RAEBYES Protocol** | Invariant Circuit Breaker Daemon | Strict mass/energy conservation enforcement ($\delta < 10^{-4}$), array/tensor variance floor auditing ($\operatorname{Var} > 10^{-6}$), process crash recovery | Circuit breaker tripping, tamper-evident JSON audit trail | **Native Cross-Platform (Pure Python / No COM Required)** |

---

## 4. The 60 Registered Model Context Protocol (MCP) Tools

`advekt` exposes an exhaustive suite of **60 MCP tools** conforming strictly to the Model Context Protocol JSON-RPC 2.0 specification:

### Mechanical CAD & Automated Drafting (12 Tools)
* **SolidWorks 2025** (9 tools):
  1. `solidworks_get_status`: Inspect COM registration, ROT running instance, and version.
  2. `solidworks_open_document`: Open `.SLDPRT`, `.SLDASM`, or `.SLDDRW` with silent configuration options.
  3. `solidworks_close_document`: Close active document with optional save.
  4. `solidworks_inspect_model`: Extract feature tree, solid bodies, custom metadata, and units.
  5. `solidworks_get_mass_properties`: Compute mass (kg), volume ($m^3$), surface area ($m^2$), and Center of Gravity (CoG).
  6. `solidworks_force_rebuild`: Trigger top-level parametric assembly/part rebuild.
  7. `solidworks_render_view`: Render high-resolution isometric, front, or top viewport to PNG.
  8. `solidworks_export_cad`: Export native geometry to `.STEP` (AP203/AP214) or drawing to vector `.PDF`.
  9. `solidworks_execute_script`: Dispatch custom VBScript / VBA macro into SolidWorks kernel.
* **Autodesk AutoCAD 2025** (3 tools):
  10. `autocad_get_status`: Inspect AutoCAD COM server and `accoreconsole.exe` availability.
  11. `autocad_plot_pdf`: Headless batch vector plot of `.DWG` layout to PDF.
  12. `autocad_run_script`: Execute batch AutoLISP (`.lsp`) or command script (`.scr`).

### Chemical Process Simulation & Flowsheeting (23 Tools)
* **Aspen Plus V14** (6 tools):
  13. `aspen_plus_get_status`: Verify Aspen Plus COM registration and active licenses.
  14. `aspen_plus_open_simulation`: Load `.bkp`, `.apw`, or `.inp` case.
  15. `aspen_plus_inspect_flowsheet`: Extract complete flowsheet topology, streams, and unit blocks.
  16. `aspen_plus_get_stream_table`: Extract converged stream balance table (T, P, mass flow, vapor fraction).
  17. `aspen_plus_get_block_data`: Extract block-level duty schedules, heat transfer rates, and separation parameters.
  18. `aspen_plus_run_simulation`: Dispatch flowsheet solver calculation run.
* **Aspen HYSYS** (4 tools):
  19. `aspen_hysys_get_status`: Check HYSYS COM server connection.
  20. `aspen_hysys_open_case`: Open `.hsc` simulation archive.
  21. `aspen_hysys_inspect_case`: Extract streams, property packages, and flowsheet structure.
  22. `aspen_hysys_solve`: Trigger steady-state or dynamic case solve.
* **Chemstations CHEMCAD v7/v8** (3 tools):
  23. `chemcad_get_status`: Verify CHEMCAD COM server availability.
  24. `chemcad_inspect_flowsheet`: Inspect unit operations, streams, and batch distillation setups.
  25. `chemcad_run_simulation`: Trigger flowsheet convergence run.
* **AVEVA SimSci PRO/II** (3 tools):
  26. `proii_get_status`: Verify PRO/II COM registration.
  27. `proii_inspect_flowsheet`: Inspect flowsheet and thermodynamic components.
  28. `proii_run_simulation`: Execute PRO/II batch calculation.
* **Honeywell UniSim Design** (2 tools):
  29. `unisim_get_status`: Check UniSim COM server registration.
  30. `unisim_inspect_case`: Inspect simulation case (`.usc`, `.hsc`).
* **DWSIM Simulator** (3 tools):
  31. `dwsim_get_status`: Verify DWSIM executable, CAPE-OPEN libraries, and CoolProp bindings.
  32. `dwsim_inspect_flowsheet`: Parse `.dwsim` / `.dwxml` XML topology without running GUI.
  33. `dwsim_flash_calculation`: Perform isothermal/isobaric Rachford-Rice vapor-liquid flash.
* **Cantera Chemical Kinetics** (3 tools):
  34. `cantera_get_status`: Verify Cantera chemical physics environment.
  35. `cantera_arrhenius_kinetics`: Calculate forward/reverse rate coefficients via Arrhenius parameters.
  36. `cantera_gas_transport_properties`: Calculate multi-component Sutherland viscosity and thermal conductivity.

### Advanced Multiphysics & CFD Solvers (9 Tools)
* **Siemens gPROMS** (3 tools):
  37. `gproms_get_status`: Verify gPROMS ProcessBuilder/ModelBuilder CLI.
  38. `gproms_inspect_project`: Inspect `.gPJ`, `.gPA`, or `.xml` project hierarchy and DAE/PDE equations.
  39. `gproms_run_simulation`: Dispatch dynamic simulation or parameter estimation run.
* **COMSOL Multiphysics** (3 tools):
  40. `comsol_get_status`: Check COMSOL batch engine and license.
  41. `comsol_inspect_model`: Extract physics interfaces (`cheq`, `tds`, `ht`, `spf`), meshes, and study nodes from `.mph`.
  42. `comsol_run_study`: Dispatch headless batch parametric sweep or study solve.
* **Ansys Fluent & CFX** (3 tools):
  43. `ansys_get_status`: Inspect Ansys environment variables (`AWP_ROOT`) and fluent solvers.
  44. `ansys_inspect_case`: Inspect `.cas` / `.cas.gz` mesh dimensions and boundary conditions.
  45. `ansys_run_journal`: Dispatch headless CFD calculation via `.jou` journal script.

### First-Principles Engineering & Invariants (15 Tools)
* **Thermodynamics Engine** (2 tools):
  46. `thermo_steam_properties`: High-precision ASME STEAM-TA / IAPWS steam tables (T, P, h, s, v, $\rho$, latent heat).
  47. `thermo_peng_robinson_eos`: Peng-Robinson Cubic EOS (Cardano analytical root solver, Z factor, fugacity coefficients).
* **Process Hydraulics** (3 tools):
  48. `hydraulics_pipe_dimensions`: Query ASME B36.10M / B36.19M pipe dimensional schedules (DN, OD, ID, thickness).
  49. `hydraulics_pressure_drop`: Darcy-Weisbach head loss with Colebrook-White friction factor (Newton-Raphson).
  50. `hydraulics_pump_head_npsha`: Total Dynamic Head (TDH), NPSHa, hydraulic power, and motor rating.
* **Industrial Thermal Design** (3 tools):
  51. `thermal_lmtd_calculation`: Logarithmic Mean Temperature Difference with multi-pass $F_T$ configuration correction.
  52. `thermal_rate_tema_shell_and_tube`: Kern method rating for TEMA E shell-and-tube heat exchangers.
  53. `thermal_mvr_evaporator_design`: Mechanical Vapor Recompression falling-film evaporator mass/energy balances and compressor power.
* **ASME Pressure Vessels** (4 tools):
  54. `pv_asme_ug27_shell`: ASME BPVC Section VIII Div 1 UG-27(c)(1) cylindrical shell thickness & MAWP under internal pressure.
  55. `pv_asme_ug32_head`: ASME Section VIII Div 1 UG-32 2:1 ellipsoidal and torispherical formed heads.
  56. `pv_asme_ug37_nozzle`: ASME Section VIII Div 1 UG-37 nozzle opening area replacement & reinforcement limits.
  57. `pv_asme_ug99_hydro`: ASME Section VIII Div 1 UG-99(b) hydrostatic proof test pressure.
* **RAEBYES Invariant Circuit Breaker** (3 tools):
  58. `raebyes_verify_simulation_variance`: Guard against synthetic flat arrays ($\operatorname{Var}(\mathbf{X}) \ge \sigma^2_{\text{min}}$).
  59. `raebyes_verify_conservation_invariants`: Enforce mass balance closure ($\delta_{\text{mass}} < 10^{-4}$).
  60. `raebyes_get_circuit_breaker_status`: Read circuit breaker state, trip history, and diagnostic logs.

---

## 5. Governing Equations & Mathematical Formulations

### 1. ASME Section VIII Division 1 Pressure Vessel Mechanics
Under internal design pressure $P$, nominal design stress $S$, joint efficiency $E$, inside radius $R$, and corrosion allowance $t_c$:

* **Cylindrical Shell (UG-27(c)(1)):**
  $$t = \frac{P R}{S E - 0.6 P} + t_c, \quad \text{MAWP} = \frac{S E t}{R + 0.6 t}$$

* **2:1 Ellipsoidal Formed Head (UG-32(d)):**
  $$t = \frac{P D K}{2 S E - 0.2 P} + t_c \quad \text{where } K = \frac{1}{6}\left[2 + \left(\frac{D}{2h}\right)^2\right] = 1.0 \text{ for } \frac{D}{2h} = 2.0$$

* **Torispherical Head (UG-32(e)):**
  $$t = \frac{0.885 P L}{S E - 0.1 P} + t_c \quad (L = \text{inside crown radius})$$

* **Nozzle Opening Reinforcement (UG-37):**
  $$A_{\text{req}} = d \cdot t_r \cdot F$$
  $$A_{\text{avail}} = A_1 (\text{excess shell}) + A_2 (\text{excess nozzle neck}) + A_4 (\text{weld fillets})$$
  $$\text{Enforced Constraint: } A_{\text{avail}} \ge A_{\text{req}}$$

* **Hydrostatic Proof Test Pressure (UG-99(b)):**
  $$P_{\text{test}} = 1.3 \cdot P_{\text{design}} \cdot \left(\frac{S_{\text{test}}}{S_{\text{design}}}\right)$$

### 2. Fluid Dynamics & Process Hydraulics
* **Darcy-Weisbach Formulation:**
  $$\Delta h_f = f \frac{L}{D} \frac{v^2}{2g}, \quad \Delta P_f = \rho g \Delta h_f$$

* **Implicit Colebrook-White Friction Factor:**
  $$\frac{1}{\sqrt{f}} = -2.0 \log_{10} \left( \frac{\epsilon / D}{3.7} + \frac{2.51}{\text{Re} \sqrt{f}} \right)$$
  *Solved via 6-iteration Newton-Raphson down to $|f_{k+1} - f_k| < 10^{-8}$.*

* **Total Dynamic Head (TDH) & Net Positive Suction Head Available (NPSHa):**
  $$\text{TDH} = (z_{\text{disch}} - z_{\text{suct}}) + \frac{P_{\text{disch}} - P_{\text{suct}}}{\rho g} + \Delta h_{f,\text{total}}$$
  $$\text{NPSHa} = \frac{P_{\text{suct,abs}} - P_v}{\rho g} + z_{\text{suct}} - h_{f,\text{suction}}$$
  $$P_{\text{elec}} = \frac{\rho g Q \cdot \text{TDH}}{\eta_{\text{pump}} \eta_{\text{motor}}}$$

### 3. High-Precision Thermodynamics
* **Peng-Robinson Cubic Equation of State (1976):**
  $$P = \frac{R T}{v - b} - \frac{a(T)}{v(v + b) + b(v - b)}$$
  In cubic polynomial form for compressibility factor $Z$:
  $$Z^3 - (1 - B) Z^2 + (A - 3B^2 - 2B) Z - (AB - B^2 - B^3) = 0$$
  *Solved via closed-form analytical Cardano cubic root algorithm. Identifies liquid roots ($Z_L = \min Z$), vapor roots ($Z_V = \max Z$), and calculates component fugacity coefficients $\ln \phi_i$.*

### 4. Industrial Thermal Design
* **TEMA E Shell-and-Tube Exchanger (Kern Method):**
  $$Q = U_o A_o \Delta T_{lm} F_T$$
  $$\Delta T_{lm} = \frac{(T_{h,\text{in}} - T_{c,\text{out}}) - (T_{h,\text{out}} - T_{c,\text{in}})}{\ln\left(\frac{T_{h,\text{in}} - T_{c,\text{out}}}{T_{h,\text{out}} - T_{c,\text{in}}}\right)}$$

* **Mechanical Vapor Recompression (MVR) Evaporator Balances:**
  $$\dot{m}_{\text{evap}} = \dot{m}_{\text{feed}} \left(1 - \frac{x_{\text{feed}}}{x_{\text{prod}}}\right)$$
  $$W_{\text{comp}} = \frac{\dot{m}_{\text{evap}} R T_1}{\eta_{\text{isen}} \frac{\gamma - 1}{\gamma}} \left[ \left(\frac{P_2}{P_1}\right)^{\frac{\gamma - 1}{\gamma}} - 1 \right]$$

### 5. RAEBYES Invariant Circuit Breaker Criteria
* **Mass Balance Conservation Invariant:**
  $$\delta_{\text{mass}} = \frac{\left|\sum \dot{m}_{\text{in}} - \sum \dot{m}_{\text{out}}\right|}{\sum \dot{m}_{\text{in}}} < \epsilon_{\text{tol}} \quad (\epsilon_{\text{tol}} = 10^{-4})$$

* **Synthetic Variance Floor Check (Flat Array Detection):**
  $$\operatorname{Var}(\mathbf{X}) = \frac{1}{N} \sum_{i=1}^N (x_i - \bar{x})^2 \ge \sigma^2_{\text{min}} \quad (\sigma^2_{\text{min}} = 10^{-6})$$

---

## 6. Installation

```bash
# Clone the repository
git clone https://github.com/SourishSenapati/ADVEKT.git
cd ADVEKT

# Install in editable mode
pip install -e .

# Or install with developer test dependencies
pip install -e ".[dev]"
```

---

## 7. Command-Line Interface (CLI) Guide

ADVEKT provides **21 dedicated high-performance CLI executables** designed for headless scripts, CI/CD pipelines, and fast engineering terminals:

### 1. Master Subsystem Gateway (`advekt`)
```bash
# Execute sub-200ms non-blocking status inquiry across all 17 engineering subsystems
advekt status

# Start Model Context Protocol (MCP) JSON-RPC 2.0 stdio server
advekt mcp
```

### 2. High-Precision Thermodynamics (`thermo-cli`)
```bash
# Saturated steam properties at 160.0°C (ASME STEAM-TA / IAPWS Formulation)
thermo-cli steam --temp 160.0

# Superheated steam properties at 40 bar, 500°C
thermo-cli steam --pressure 40.0 --temp 500.0

# Peng-Robinson Cubic EOS flash for hydrocarbon mixture
thermo-cli pr-eos --compounds methane,ethane,propane --fractions 0.7,0.2,0.1 --temp 30.0 --pressure 45.0
```

### 3. Process Hydraulics & Pumps (`hydraulics-cli`)
```bash
# Query ASME B36.10M standard pipe dimensions (DN 100 Sch 40)
hydraulics-cli pipe-dims 100 --schedule sch40

# Darcy-Weisbach pressure drop across 120m carbon steel line
hydraulics-cli pressure-drop --flow 45.0 --dn 100 --length 120.0 --roughness 0.045

# Centrifugal pump Total Dynamic Head (TDH), NPSHa, and motor rating
hydraulics-cli pump --flow 45.0 --static-head 15.0 --p-disch 3.5 --p-suct 0.2
```

### 4. Industrial Thermal Design (`thermal-cli`)
```bash
# Calculate LMTD and multi-pass configuration correction factor FT
thermal-cli lmtd --th-in 120.0 --th-out 80.0 --tc-in 30.0 --tc-out 60.0 --passes 2

# Rate TEMA E Shell-and-Tube heat exchanger via Kern method
thermal-cli shell-and-tube --duty 450.0 --th-in 120.0 --th-out 80.0 --tc-in 30.0 --tc-out 60.0 --tubes 240 --length 4.0

# Design MVR Falling Film Evaporator (area, compressor power, specific energy)
thermal-cli mvr --feed-flow 1500.0 --feed-solids 5.0 --product-solids 35.0 --temp 80.0
```

### 5. ASME Section VIII Div 1 Pressure Vessels (`pv-cli`)
```bash
# Cylindrical shell wall thickness & MAWP (UG-27)
pv-cli shell --pressure 10.0 --diameter 1200.0 --temp 120.0 --material "SA-240 316L" --joint-eff 1.0 --corrosion 1.5

# 2:1 Ellipsoidal dished head thickness (UG-32)
pv-cli head --pressure 10.0 --diameter 1200.0 --type ellipsoidal_2_1 --material "SA-240 316L"

# Nozzle opening reinforcement check (UG-37)
pv-cli nozzle --vessel-id 1200.0 --shell-t 10.0 --nozzle-od 168.3 --nozzle-t 7.11 --pressure 10.0

# Hydrostatic proof test pressure calculation (UG-99)
pv-cli hydro --pressure 10.0 --temp 120.0 --material "SA-240 316L"
```

### 6. RAEBYES Invariant Circuit Breaker (`raebyes-chemeng-cli`)
```bash
# Inspect circuit breaker trip state and telemetry
raebyes-chemeng-cli status

# Verify strict mass conservation invariant (< 1e-4 closure error)
raebyes-chemeng-cli check-mass --inflow 1500.0 --outflow 1500.02 --tol 1e-4

# Audit numerical array against flat synthetic mock detection
raebyes-chemeng-cli check-variance --values "10.2, 12.5, 14.8, 18.2, 22.0" --min-var 1e-6
```

### 7. Dassault Systèmes SOLIDWORKS (`solidworks-cli`)
```bash
# Check SolidWorks connection status
solidworks-cli status

# Inspect 3D CAD model (features, bodies, custom properties, mass)
solidworks-cli inspect "path/to/vessel.sldprt"

# Compute mass properties (mass, volume, center of gravity)
solidworks-cli mass-props "path/to/assembly.sldasm"

# Render high-resolution isometric view to PNG
solidworks-cli render "path/to/part.sldprt" --view iso --out render.png

# Export CAD model to STEP and PDF
solidworks-cli export "path/to/part.sldprt" --formats step,pdf
```

### 8. Aspen Plus V14 (`aspen-plus-cli`)
```bash
# Check Aspen Plus COM registration and licensing state
aspen-plus-cli status

# Open simulation case
aspen-plus-cli open "path/to/plant.bkp"

# Inspect flowsheet topology, streams, and unit blocks
aspen-plus-cli inspect

# Retrieve converged stream balance table (T, P, mass flow, vapor fraction)
aspen-plus-cli streams
```

---

## 8. Python SDK Usage

In addition to CLI and MCP, `advekt` can be imported directly into Python applications:

```python
import advekt

# 1. High-Precision ASME Steam Tables
steam = advekt.thermo.calculate_steam_properties(temperature_C=160.0, pressure_bar=6.18)
print(f"Saturation Enthalpy (h_fg): {steam['latent_heat_hfg_kJ_kg']} kJ/kg")
print(f"Liquid Density: {steam['liquid_density_kg_m3']} kg/m³")

# 2. Process Hydraulics (Darcy-Weisbach & Colebrook-White)
hyd = advekt.hydraulics.calculate_pressure_drop(
    flow_m3_h=45.0,
    dn_mm=100,
    length_m=120.0,
    roughness_mm=0.045
)
print(f"Friction Factor (f): {hyd['darcy_friction_factor']:.5f}")
print(f"Total Pressure Drop: {hyd['pressure_drop_bar']:.3f} bar")

# 3. ASME Section VIII Div 1 Cylindrical Shell
shell = advekt.pressure_vessel.calculate_ug27_shell(
    design_pressure_bar=10.0,
    inside_diameter_mm=1200.0,
    design_temp_C=120.0,
    material="SA-240 316L",
    joint_efficiency=1.0,
    corrosion_allowance_mm=1.5
)
print(f"Required Shell Thickness: {shell['required_thickness_mm']:.2f} mm")
print(f"Calculated MAWP: {shell['mawp_bar']:.2f} bar")

# 4. RAEBYES Invariant Check
guard = advekt.raebyes.verify_conservation_invariants(
    total_inflow_kg_h=1500.0,
    total_outflow_kg_h=1500.02,
    tolerance=1e-4
)
assert guard["passed"] is True, "Circuit breaker tripped on mass balance closure error!"
```

---

## 9. Model Context Protocol (MCP) Configuration

Configure your AI coding assistant to use `advekt-mcp`:

### Claude Desktop (`claude_desktop_config.json`)
```json
{
  "mcpServers": {
    "advekt": {
      "command": "advekt-mcp",
      "args": []
    }
  }
}
```

### Cursor (`.cursor/settings.json`)
```json
{
  "cursor.mcpServers": {
    "advekt": {
      "command": "python",
      "args": ["-m", "agentic_chemeng.mcp.server"]
    }
  }
}
```

---

## 10. Low-Spec Optimization & Linux Resilience

`advekt` is engineered to operate reliably across **Linux, macOS, Windows**, and **legacy low-spec machines**:

1. **Full Linux / POSIX Compatibility:**
   - Detects `sys.platform == 'win32'` dynamically. Windows COM (`pywin32`) imports are conditionally bypassed on Linux without crashes.
   - All first-principles modules (Thermodynamics, Hydraulics, Thermal Design, ASME Pressure Vessels, DWSIM XML parsing, Cantera kinetics) run **100% natively on Linux**.
2. **Sub-200ms Non-Blocking Status Inquiries:**
   - Querying system status (`advekt status`) tests active Running Object Table (ROT) registrations and OS registry keys in `< 0.2s` without launching heavy CAD/CAE applications into RAM.
3. **Wall-Clock Timeout Guardians:**
   - All external processes are wrapped in `run_with_timeout()`. If a slow HDD or hung application freezes, execution terminates cleanly after a configurable threshold (default: 20s).
4. **Memory Management & Zero Process Leaks:**
   - Explicit `gc.collect()` and COM pointer releases prevent memory accumulation.
   - `cleanup_stale_processes()` kills orphan background workers on both Windows (`taskkill`) and Linux (`pkill`).

---

## 11. Intellectual Property Ownership, Commercial Licensing & Monetization Covenant

`ADVEKT` is released under the **ADVEKT Source-Available Commercial & Intellectual Property Protection License v1.0** ([`LICENSE`](LICENSE)).

### 1. 100% Retained Intellectual Property
All intellectual property, copyrights, patent rights, trade dress, trademarks, and trade secrets in `ADVEKT` (`advekt`), its 60 MCP tools, 21 CLI executables, and mathematical solvers are exclusively and solely owned by **Sourish Senapati** (*FinnoaQ Agro-Industrial Technologies Ltd.*). No title or transfer of IP is granted.

### 2. Free for Personal, Non-Commercial & Academic Research
You are free to inspect, download, test, benchmark, and evaluate `ADVEKT` for individual personal projects, non-profit academic research, and classroom education without charge.

### 3. Strict Commercial & Paid Product Restriction (Monetization Protection)
* **Anti-Parasitic & Paid Wrapper Clause:** If any third party, startup, corporation, or individual launches, sells, markets, hosts, or monetizes any paid product, commercial software bundle, SaaS platform, agent-as-a-service, paid API wrapper, or consulting deliverable that incorporates, embeds, or derives from `ADVEKT` (in whole or in part), **you are legally required to obtain a Commercial License and execute a formal revenue-sharing / royalty agreement with Sourish Senapati prior to launch or commercial distribution**.
* **Remedies for Unlicensed Commercial Exploitation:** Willful commercial infringement entitles Sourish Senapati to immediate injunctive relief, full disgorgement of all gross commercial revenues and subscriber proceeds, statutory damages, and mandatory legal fee reimbursement.

### 4. Commercial & Enterprise Licensing Inquiries
For commercial licensing, enterprise multi-seat deployment, OEM bundling, proprietary process bindings, or revenue-sharing agreements, contact:
* **Lead Engineer & IP Owner:** Sourish Senapati
* **Email:** `sourishsenapati791@gmail.com` / `engineering@finnoaq.com`
* **Entity:** FinnoaQ Agro-Industrial Technologies Ltd.
* **Project Reference:** `FNQ-PR-2026-001`

---

## 12. Technical Standards Attribution

- **Lead Chemical & Process Engineer:** Sourish Senapati (*FinnoaQ Agro-Industrial Technologies Ltd.*)
- **Governing Project Reference:** `FNQ-PR-2026-001`
- **Thermodynamic Standards:** ASME STEAM-TA (1967 Formulation), IAPWS Industrial Formulation (1997), Peng-Robinson Cubic Equation of State (1976).
- **Hydraulic Standards:** ASME B36.10M / B36.19M Welded and Seamless Wrought Steel Pipe, Crane Technical Paper No. 410, Hydraulic Institute (HI) Standards.
- **Thermal Standards:** Tubular Exchanger Manufacturers Association (TEMA 10th Edition), Kern Method.
- **Mechanical Standards:** ASME Boiler and Pressure Vessel Code (BPVC) Section VIII Division 1 (Rules for Construction of Pressure Vessels), Section II Part D (Materials - Properties).
- **Circuit Breaker Protocol:** [`SourishSenapati/RAEBYES`](https://github.com/SourishSenapati/RAEBYES).
