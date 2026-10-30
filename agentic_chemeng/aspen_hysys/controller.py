"""
Agentic ChemEng - Aspen HYSYS Autonomous Simulation Controller
Lead Chemical & Process Engineer: Sourish Senapati

Interfaces directly with Aspen Technology Aspen HYSYS via COM Automation (HYSYS.Application).
Provides programmatic inspection of dynamic & steady-state hydrocarbon/chemical flowsheets,
material/energy streams, unit operations, and property packages (Peng-Robinson, NRTL).
"""

import json
import os
import sys
import win32com.client

from ..resilience import (
    ensure_com_initialized,
    validate_file_path,
    EngineeringValidationError
)


class AspenHysysController:
    """Manages an active or offline Aspen HYSYS simulation session."""

    def __init__(self):
        self._app = None
        self._active_case = None

    def get_status(self):
        """Tests HYSYS COM registration and active simulation state without cold-locking."""
        ensure_com_initialized()
        com_active = False
        version_str = "Unknown"
        active_case_name = None

        try:
            # Check active running instance first
            app = win32com.client.GetActiveObject("HYSYS.Application")
            com_active = True
            version_str = f"Aspen HYSYS (Active Instance: {app.Version})"
            try:
                active_case_name = app.ActiveDocument.Title
            except Exception:
                pass
        except Exception:
            try:
                # Check COM class registration
                app = win32com.client.Dispatch("HYSYS.Application")
                com_active = True
                version_str = f"Aspen HYSYS {app.Version} (Registered in Windows COM)"
            except Exception:
                com_active = False

        return {
            "status": "connected" if com_active else "disconnected",
            "com_registered": com_active,
            "hysys_version": version_str,
            "active_case": active_case_name,
            "prog_id": "HYSYS.Application",
            "supported_formats": [".hsc"],
            "lead_process_engineer": "Sourish Senapati",
            "governing_project": "ADVEKT-CAE-2026"
        }

    def open_case(self, filepath):
        """Opens a native .hsc simulation case in Aspen HYSYS."""
        abs_path = validate_file_path(
            filepath,
            allowed_extensions=[".hsc"],
            must_exist=True
        )

        ensure_com_initialized()
        live_opened = False
        err_msg = None

        try:
            app = win32com.client.Dispatch("HYSYS.Application")
            sim_case = app.SimulationCases.Open(abs_path)
            self._app = app
            self._active_case = sim_case
            live_opened = True
        except Exception as e:
            err_msg = str(e)

        return {
            "simulation_case": os.path.basename(abs_path),
            "file_path": abs_path,
            "file_size_bytes": os.path.getsize(abs_path),
            "live_hysys_opened": live_opened,
            "solver_state": "ACTIVE" if live_opened else "OFFLINE_INSPECTION",
            "notice": err_msg if not live_opened else "Active HYSYS simulation session established"
        }

    def inspect_case(self, filepath=None):
        """Inspects flowsheet streams, operations, and fluid packages."""
        if filepath:
            open_res = self.open_case(filepath)
        elif not self._active_case:
            # Return baseline capabilities
            return {
                "active_case": None,
                "supported_packages": [
                    "Peng-Robinson (PR)",
                    "Sour PR",
                    "Soave-Redlich-Kwong (SRK)",
                    "NRTL",
                    "UNIQUAC",
                    "Glycol Package",
                    "Amines Package"
                ],
                "operations_supported": [
                    "Separators (2-phase, 3-phase)",
                    "Distillation Columns",
                    "Heat Exchangers / Coolers",
                    "Centrifugal & Reciprocating Compressors",
                    "Expansion Turbines",
                    "Control Valves & Relief Valves"
                ]
            }

        try:
            case = self._active_case
            fs = case.Flowsheet
            mat_streams = [s.Name for s in fs.MaterialStreams] if hasattr(fs, "MaterialStreams") else []
            operations = [op.Name for op in fs.Operations] if hasattr(fs, "Operations") else []
            can_solve = bool(case.Solver.CanSolve) if hasattr(case, "Solver") else True

            return {
                "case_name": case.Title,
                "can_solve": can_solve,
                "material_streams_count": len(mat_streams),
                "material_streams": mat_streams[:20],
                "operations_count": len(operations),
                "operations": operations[:20]
            }
        except Exception as e:
            return {"error": str(e)}

    def solve(self):
        """Triggers the HYSYS flowsheet solver."""
        if not self._active_case:
            return {"status": "error", "message": "No active simulation case loaded in HYSYS."}

        try:
            self._active_case.Solver.CanSolve = True
            return {"status": "success", "solver_state": "ACTIVE_SOLVING"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

