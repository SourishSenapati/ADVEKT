# Agentic ChemEng (`agentic-chemeng`)

**Autonomous Multi-Discipline Chemical & Mechanical Engineering CLI & MCP Tool Suite**  
*Project Ref:* `FNQ-PR-2026-001`  
*Lead Chemical & Process Engineer:* **Sourish Senapati** (*FinnoaQ Agro-Industrial Technologies Ltd.*)  
*License:* Apache-2.0  

---

## 1. Executive Overview

`agentic-chemeng` is a production-grade, standalone industrial engineering toolkit that bridges Large Language Models (LLMs), autonomous AI coding agents, and human process engineers with authentic, commercial and open-source Computer-Aided Design (CAD), Process Simulation (CAE), and First-Principles Engineering platforms.

Unlike superficial "vibe coding" approximations, `agentic-chemeng` enforces strict physical conservation laws (zero mass balance closure error), direct API bindings to licensed engineering software via Windows COM automation, and exact numerical solvers for ASME and TEMA mechanical/chemical standards.

---

## 2. Integrated Engineering Subsystems

| Subsystem | Underlying Engine | Key Capabilities | Standards / Formats |
| :--- | :--- | :--- | :--- |
| **SolidWorks** | Dassault Systèmes SOLIDWORKS 2025 SP1.2 (`SldWorks.Application`) | Parametric 3D solid modeling, feature tree traversal, assembly constraints, mass properties, high-res viewport rendering, STEP/PDF export | `.SLDPRT`, `.SLDASM`, `.SLDDRW`, `.STEP`, B-Rep solid math |
| **Aspen Plus** | Aspen Technology Aspen Plus V14 (`Apwn.Document` OLE Services) | Rigorous flowsheet topology inspection, stream balance extraction, unit block duty schedules, live solver execution (`Run2`), offline converged audit | `.bkp`, `.apw`, `.inp`, ASME STEAM-TA, NRTL, ELECNRTL |
| **Aspen HYSYS** | Aspen Technology Aspen HYSYS (`HYSYS.Application` COM) | Dynamic & steady-state hydrocarbon/chemical flowsheets, material/energy streams, unit operations, property packages | `.hsc`, Peng-Robinson, Sour PR, SRK, Glycol, Amines |
| **DWSIM** | DWSIM Open-Source Simulator (v8/v9) | Open-source process simulation, CAPE-OPEN thermodynamics, XML flowsheet inspection, Rachford-Rice VLE flash | `.dwsim`, `.dwxml`, CoolProp, UNIFAC, IAPWS-IF97 |
| **AutoCAD** | Autodesk AutoCAD 2025 (`AutoCAD.Application` & `accoreconsole.exe`) | Automated P&ID and General Arrangement drafting, title block verification, layer auditing, headless DWG-to-PDF/DXF batch conversion | `.dwg`, `.dxf`, Vector PDF, ANSI/ISO title blocks |
| **Thermodynamics** | First-Principles Thermodynamics Engine | High-precision steam tables (ASME STEAM-TA / IAPWS), Peng-Robinson Cubic Equation of State (PR-EOS), analytical Cardano cubic root solver, fugacity coefficients, Wagner/Antoine vapor pressure | ASME 1967 Steam Tables, IAPWS Industrial Formulation, PR (1976) |
| **Process Hydraulics** | First-Principles Hydraulics Engine | Darcy-Weisbach head loss, Colebrook-White friction factor (Newton-Raphson), ASME B36.10M standard pipe schedules, Crane TP 410 minor losses, Pump TDH, NPSHa, motor sizing | ASME B36.10M, Crane TP 410, Hydraulic Institute (HI) |
| **Thermal Design** | Industrial Heat Transfer Engine | TEMA E shell-and-tube heat exchanger rating (Kern method), LMTD & $F_T$ configuration correction, MVR falling-film evaporator mass/energy balances, compressor power & specific energy | TEMA 10th Ed Class C/R, Kern Method, MVR Industrial Design |
| **Pressure Vessels** | ASME Section VIII Div 1 Mechanical Engine | UG-27(c)(1) cylindrical shell thickness under internal pressure, UG-32(d) 2:1 ellipsoidal heads, UG-32(e) torispherical heads, UG-37 nozzle opening area replacement, UG-99 hydrostatic test pressure | ASME BPVC Section VIII Div 1, ASME Section II Part D |

---

## 3. Industrial Resilience Architecture ("No Vibe Code")

Engineering automation in Windows environments frequently crashes when implemented with naive scripts ("vibe code") due to COM threading apartment violations, zombie processes locking files, and blocking modal dialogs. `agentic-chemeng` incorporates an industrial-grade resilience engine (`agentic_chemeng.resilience`):

1. **Idempotent COM Apartment Safety:** All COM calls invoke `ensure_com_initialized()`, safely maintaining single-threaded apartments (STA) and preventing `CoInitialize has not been called` (0x800401F0) crashes.
2. **Wall-Clock Timeout Guardians:** Heavy COM operations (e.g. CAD model opening, mesh generation, flowsheet solving) run inside `run_with_timeout()`, preventing hanging background processes when modal popups occur.
3. **Zero Process Leaks & Zombie Reap Guards:** Proactively discovers and reaps orphaned `SLDWORKS.exe`, `accoreconsole.exe`, and headless simulation processes using `cleanup_stale_processes()`.
4. **Defensive Path & File Validation:** Enforces whitelist verification, path canonicalization, and file size checks before passing paths to native COM wrappers.
5. **Structured Error Envelopes:** Returns standardized JSON error envelopes with error categories, ISO 8601 UTC timestamps, and actionable remediation steps.

---

## 4. Installation

```bash
# Clone the repository
git clone https://github.com/finnoaq/agentic-chemeng.git
cd agentic-chemeng

# Install in editable mode
pip install -e .

# Or install with developer dependencies (pytest)
pip install -e ".[dev]"
```

---

## 5. Command-Line Interface (CLI) Usage

### Unified Master Gateway
```bash
# Query overall status across all installed engineering software
agentic-chemeng status

# Run MCP stdio server
agentic-chemeng mcp
```

### Dedicated Subsystem CLIs

#### 1. Dassault Systèmes SOLIDWORKS (`solidworks-cli`)
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

#### 2. Aspen Plus (`aspen-plus-cli`)
```bash
# Check Aspen Plus COM registration and licensing state
aspen-plus-cli status

# Open simulation case
aspen-plus-cli open "path/to/plant.bkp"

# Inspect flowsheet topology, streams, and unit blocks
aspen-plus-cli inspect

# Retrieve converged stream balance table (T, P, mass flow, vapor fraction)
aspen-plus-cli streams

# Inspect specific unit operation block thermal duty
aspen-plus-cli blocks --block-id EVAP-1
```

#### 3. Aspen HYSYS (`aspen-hysys-cli`)
```bash
# Check HYSYS COM server connectivity
aspen-hysys-cli status

# Open HYSYS simulation case (.hsc)
aspen-hysys-cli open "path/to/rigorous_model.hsc"

# Inspect streams and property packages
aspen-hysys-cli inspect

# Trigger flowsheet solver
aspen-hysys-cli solve
```

#### 4. DWSIM Open-Source Simulator (`dwsim-cli`)
```bash
# Check DWSIM installation and supported CAPE-OPEN packages
dwsim-cli status

# Inspect DWSIM flowsheet file (.dwsim or .dwxml)
dwsim-cli inspect "path/to/flowsheet.dwxml"

# Perform isothermal/isobaric VLE flash calculation
dwsim-cli flash --temp 95.0 --pressure 1.01325 --compounds Water,Ethanol --fractions 0.85,0.15
```

#### 5. Autodesk AutoCAD (`autocad-cli`)
```bash
# Check AutoCAD COM server and accoreconsole.exe
autocad-cli status

# Inspect DWG drawing (layers, layout tabs, blocks)
autocad-cli inspect "path/to/pfd.dwg"

# Headless batch export DWG to vector PDF
autocad-cli export-pdf "path/to/pid.dwg" --out "path/to/pid.pdf"
```

#### 6. Thermodynamics (`thermo-cli`)
```bash
# Calculate ASME STEAM-TA steam properties at 160°C
thermo-cli steam --temp 160.0

# Calculate saturation properties at 3.0 bar
thermo-cli steam --pressure 3.0

# Peng-Robinson Cubic EOS (compressibility factor Z & fugacity coefficients)
thermo-cli pr-eos --compounds methane,ethane,propane --fractions 0.7,0.2,0.1 --temp 30.0 --pressure 45.0
```

#### 7. Process Hydraulics (`hydraulics-cli`)
```bash
# Look up ASME B36.10M standard pipe schedule dimensions (DN 100 Sch 40)
hydraulics-cli pipe-dims 100 --schedule sch40

# Compute Darcy-Weisbach pressure drop and velocity
hydraulics-cli pressure-drop --flow 45.0 --dn 100 --length 120.0

# Centrifugal Pump Total Dynamic Head (TDH), NPSHa, and motor rating
hydraulics-cli pump --flow 45.0 --static-head 15.0 --p-disch 3.5 --p-suct 0.2
```

#### 8. Industrial Thermal Design (`thermal-cli`)
```bash
# Calculate Logarithmic Mean Temperature Difference (LMTD) & FT factor
thermal-cli lmtd --th-in 120.0 --th-out 80.0 --tc-in 30.0 --tc-out 60.0

# Rate TEMA E Shell-and-Tube heat exchanger via Kern method
thermal-cli shell-and-tube --duty 450.0 --th-in 120.0 --th-out 80.0 --tc-in 30.0 --tc-out 60.0 --tubes 240 --length 4.0

# Design MVR Falling Film Evaporator (area, compressor power, specific energy)
thermal-cli mvr --feed-flow 1500.0 --feed-solids 5.0 --product-solids 35.0 --temp 80.0
```

#### 9. ASME Pressure Vessels (`pv-cli`)
```bash
# ASME Section VIII Div 1 UG-27(c)(1) cylindrical shell thickness & MAWP
pv-cli shell --pressure 10.0 --diameter 1200.0 --temp 120.0 --material "SA-240 316L" --joint-eff 1.0 --corrosion 1.5

# ASME Section VIII Div 1 UG-32 2:1 ellipsoidal dished head thickness
pv-cli head --pressure 10.0 --diameter 1200.0 --type ellipsoidal_2_1 --material "SA-240 316L"

# ASME Section VIII Div 1 UG-37 nozzle opening reinforcement check
pv-cli nozzle --vessel-id 1200.0 --shell-t 10.0 --nozzle-od 168.3 --nozzle-t 7.11 --pressure 10.0

# ASME Section VIII Div 1 UG-99(b) hydrostatic test pressure
pv-cli hydro --pressure 10.0 --temp 120.0 --material "SA-240 316L"
```

---

## 6. Model Context Protocol (MCP) Integration

`agentic-chemeng` exposes **36 Model Context Protocol (MCP) tools** conforming to JSON-RPC 2.0 (MCP specification 2024-11-05).

To add `agentic-chemeng` to Claude Desktop, Antigravity, or Cursor, configure your MCP client configuration (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "agentic-chemeng": {
      "command": "chemeng-mcp",
      "args": []
    }
  }
}
```

Or run directly via python:
```json
{
  "mcpServers": {
    "agentic-chemeng": {
      "command": "python",
      "args": ["-m", "agentic_chemeng.mcp.server"]
    }
  }
}
```

---

## 7. Recommended Repository Names

When establishing this standalone open-source or commercial product repository on GitHub / GitLab, the following naming options are recommended:

1. **`agentic-chemeng`** *(Recommended Primary)*  
   *Rationale:* Direct, unambiguous descriptor uniting AI agentic workflows (`agentic`) with chemical and process engineering (`chemeng`). Immediate brand recognition in the AI for Science & Industrial Automation ecosystem.
2. **`chemeng-agent`**  
   *Rationale:* Concise, clean naming mirroring industry standards like `docker-agent` or `cad-agent`.
3. **`open-agentic-cadcae`**  
   *Rationale:* Highlights the multi-discipline scope spanning both mechanical CAD (SolidWorks, AutoCAD) and chemical CAE (Aspen Plus, HYSYS, DWSIM).
4. **`finnoaq-agentic-eng`**  
   *Rationale:* Enterprise branded nomenclature anchoring the toolsuite under FinnoaQ Agro-Industrial Technologies Ltd. governance.

---

## 8. Technical Verification & Standards Attribution

- **Lead Chemical & Process Engineer:** Sourish Senapati (*FinnoaQ Agro-Industrial Technologies Ltd.*)
- **Governing Project Reference:** `FNQ-PR-2026-001`
- **Thermodynamic Standards:** ASME STEAM-TA (1967 Formulation), IAPWS Industrial Formulation (1997), Peng-Robinson Cubic Equation of State (1976).
- **Hydraulic Standards:** ASME B36.10M / B36.19M Welded and Seamless Wrought Steel Pipe, Crane Technical Paper No. 410, Hydraulic Institute (HI) Standards.
- **Thermal Standards:** Tubular Exchanger Manufacturers Association (TEMA 10th Edition), Kern Method.
- **Mechanical Standards:** ASME Boiler and Pressure Vessel Code (BPVC) Section VIII Division 1 (Rules for Construction of Pressure Vessels), Section II Part D (Materials - Properties).

