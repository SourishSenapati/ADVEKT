"""
Agentic ChemEng - Autodesk AutoCAD 2025 Autonomous Controller (Industrial Hardened)
Project Ref: FNQ-PR-2026-001 | Lead Engineer: Sourish Senapati (FinnoaQ Agro-Industrial Technologies Ltd.)

Interfaces directly with Autodesk AutoCAD 2025 via COM API (AutoCAD.Application)
and the high-speed headless console engine (accoreconsole.exe).
Hardened with timeout guards, temp file cleanup, and defensive path checking.
"""

import os
import subprocess
import sys
import tempfile
import win32com.client

from ..resilience import (
    com_safe_scope,
    validate_file_path,
    EngineeringTimeoutError,
    EngineeringValidationError
)

ACCORECONSOLE_CANDIDATES = [
    r"C:\Program Files\Autodesk\AutoCAD 2025\accoreconsole.exe",
    r"C:\Program Files\Autodesk\AutoCAD 2024\accoreconsole.exe",
    r"C:\Program Files\Autodesk\AutoCAD 2023\accoreconsole.exe",
]


class AutoCADController:
    """Manages an active AutoCAD session or headless accoreconsole execution with fail-safe guards."""

    def __init__(self, visible=False):
        self._acad = None
        self._visible = visible
        self._accoreconsole_path = None

    def find_accoreconsole(self):
        if self._accoreconsole_path and os.path.exists(self._accoreconsole_path):
            return self._accoreconsole_path

        for p in ACCORECONSOLE_CANDIDATES:
            if os.path.exists(p):
                self._accoreconsole_path = p
                return p
        return None

    def get_status(self):
        """Checks AutoCAD COM connectivity and accoreconsole binary availability without cold launch."""
        with com_safe_scope():
            com_active = False
            com_version = "AutoCAD 2025 (accoreconsole engine)"
            active_doc = None

            try:
                acad = win32com.client.GetActiveObject("AutoCAD.Application")
                com_active = True
                com_version = acad.Version
                try:
                    active_doc = acad.ActiveDocument.Name
                except Exception:
                    pass
            except Exception:
                com_active = False

            console_path = self.find_accoreconsole()

            return {
                "status": "connected" if (com_active or console_path) else "disconnected",
                "com_active": com_active,
                "autocad_version": com_version,
                "active_document": active_doc,
                "accoreconsole_available": bool(console_path),
                "accoreconsole_path": console_path,
                "lead_engineer": "Sourish Senapati (FinnoaQ Agro-Industrial Technologies Ltd.)",
                "project_ref": "FNQ-PR-2026-001"
            }

    def run_script(self, drawing_path, script_commands, timeout_sec=60):
        """Executes AutoCAD command script headlessly using accoreconsole.exe with timeout guard."""
        console = self.find_accoreconsole()
        if not console:
            raise RuntimeError("accoreconsole.exe was not found on this system.")

        drawing_abs = validate_file_path(
            drawing_path,
            allowed_extensions=[".dwg", ".dxf"],
            must_exist=True
        )

        with tempfile.NamedTemporaryFile("w", suffix=".scr", delete=False) as f:
            scr_path = f.name
            if isinstance(script_commands, list):
                f.write("\n".join(script_commands) + "\n")
            else:
                f.write(script_commands + "\n")

        try:
            cmd = [console, "/i", drawing_abs, "/s", scr_path]
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_sec)
            return {
                "drawing": drawing_abs,
                "script_path": scr_path,
                "return_code": proc.returncode,
                "stdout": proc.stdout[-1500:] if proc.stdout else "",
                "success": proc.returncode == 0
            }
        except subprocess.TimeoutExpired:
            raise EngineeringTimeoutError(f"accoreconsole timed out after {timeout_sec}s executing script on {drawing_abs}")
        finally:
            try:
                if os.path.exists(scr_path):
                    os.remove(scr_path)
            except Exception:
                pass

    def plot_pdf(self, drawing_path, out_pdf_path=None):
        """Plots a DWG or DXF drawing headlessly to vector PDF via DWG To PDF.pc3."""
        drawing_abs = validate_file_path(
            drawing_path,
            allowed_extensions=[".dwg", ".dxf"],
            must_exist=True
        )

        if not out_pdf_path:
            base = os.path.splitext(drawing_abs)[0]
            out_pdf_path = f"{base}.pdf"

        pdf_abs = os.path.abspath(out_pdf_path)
        os.makedirs(os.path.dirname(pdf_abs), exist_ok=True)

        scr_commands = [
            "-PLOT",
            "Y",
            "Model",
            "DWG To PDF.pc3",
            "ANSI expand B (11.00 x 17.00 Inches)",
            "Millimeters",
            "Landscape",
            "N",
            "Extents",
            "Fit",
            "Center",
            "Y",
            "acad.ctb",
            "Y",
            "N",
            "N",
            "N",
            pdf_abs,
            "Y",
            "Y",
            "QUIT_Y"
        ]

        res = self.run_script(drawing_abs, scr_commands)
        res["output_pdf"] = pdf_abs
        res["pdf_exists"] = os.path.exists(pdf_abs)
        if os.path.exists(pdf_abs):
            res["pdf_size_bytes"] = os.path.getsize(pdf_abs)
        return res

