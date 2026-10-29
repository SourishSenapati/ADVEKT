"""
Agentic ChemEng - Siemens gPROMS Advanced Process Modeling & Digital Twin Controller
Project Ref: FNQ-PR-2026-001 | Lead Engineer: Sourish Senapati (FinnoaQ Agro-Industrial Technologies Ltd.)

Interfaces with Siemens / PSE gPROMS ProcessBuilder & ModelBuilder via COM/API,
batch CLI dispatch (gproms.exe -batch), and headless .gPJ / .gPA project archive inspection.
Specialized in equation-oriented modeling, dynamic simulations, crystallizers, catalytic
reactors, fuel cells, and distributed parameter systems (PDEs/DAEs).
Cross-platform: Windows COM/CLI + Linux headless project archive parsing.
"""

import json
import os
import re
import shutil
import subprocess
import sys
import zipfile
import xml.etree.ElementTree as ET

from ..resilience import (
    ensure_com_initialized,
    validate_file_path,
    run_with_timeout,
    build_response,
    IS_WINDOWS,
    EngineeringValidationError
)

if IS_WINDOWS:
    try:
        import win32com.client
    except ImportError:
        win32com = None
else:
    win32com = None


class GpromsController:
    """Autonomous controller for Siemens / PSE gPROMS ProcessBuilder & ModelBuilder."""

    def __init__(self):
        self._app = None
        self._active_project = None

    def get_status(self):
        """Returns non-blocking connectivity, registry, and license status (<0.2s)."""
        installed = False
        version_str = "gPROMS Not Registered in Environment"
        gproms_exe = shutil.which("gproms") or shutil.which("gproms.exe")

        # Check standard Windows paths if not in PATH
        if not gproms_exe and IS_WINDOWS:
            candidates = [
                r"C:\Program Files\PSE\gPROMS\gproms.exe",
                r"C:\Program Files\Siemens\gPROMS\gproms.exe",
                r"C:\Program Files (x86)\PSE\gPROMS\gproms.exe"
            ]
            for c in candidates:
                if os.path.exists(c):
                    gproms_exe = c
                    break

        if gproms_exe:
            installed = True
            version_str = f"gPROMS CLI Found ({gproms_exe})"

        com_active = False
        if IS_WINDOWS and win32com is not None:
            ensure_com_initialized()
            try:
                # Fast check for COM registration without launching full UI
                app = win32com.client.GetActiveObject("PSE.gPROMS")
                com_active = True
                version_str = "Siemens gPROMS (Active Instance Connected via COM)"
            except Exception:
                try:
                    # Check registry ProgID without full cold start
                    import winreg
                    with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, "PSE.gPROMS"):
                        installed = True
                        version_str = "Siemens gPROMS COM Server Registered"
                except Exception:
                    pass

        status_flag = "connected" if (com_active or gproms_exe) else ("offline_mode" if not IS_WINDOWS else "ready_on_demand")

        return {
            "status": status_flag,
            "platform": sys.platform,
            "executable_found": bool(gproms_exe),
            "executable_path": gproms_exe,
            "com_registered": com_active,
            "gproms_version": version_str,
            "supported_formats": [".gPJ", ".gPA", ".xml", ".txt"],
            "lead_process_engineer": "Sourish Senapati (FinnoaQ Agro-Industrial Technologies Ltd.)",
            "governing_project": "FNQ-PR-2026-001"
        }

    def inspect_project(self, filepath):
        """
        Parses and inspects a gPROMS project file (.gPJ, .gPA, .xml, .txt).
        Extracts equation-oriented models, processes, scheduled tasks,
        variable types, parameters, and distributed domain specifications.
        """
        abs_path = validate_file_path(
            filepath,
            allowed_extensions=[".gpj", ".gpa", ".xml", ".txt", ".zip"],
            must_exist=True
        )

        models = []
        processes = []
        tasks = []
        variable_types = []
        parameter_estimations = []
        equation_count = 0

        # Inspect if .gPJ is a ZIP archive container
        if zipfile.is_zipfile(abs_path):
            with zipfile.ZipFile(abs_path, "r") as z:
                for name in z.namelist():
                    content_lower = name.lower()
                    if content_lower.endswith(".xml") or content_lower.endswith(".txt") or content_lower.endswith(".gmd"):
                        raw_data = z.read(name).decode("utf-8", errors="ignore")
                        self._parse_gproms_text_or_xml(
                            raw_data, models, processes, tasks, variable_types, parameter_estimations
                        )
                        equation_count += raw_data.count("=")
        else:
            # Parse as direct text/XML project
            with open(abs_path, "r", encoding="utf-8", errors="ignore") as f:
                raw_data = f.read()
                self._parse_gproms_text_or_xml(
                    raw_data, models, processes, tasks, variable_types, parameter_estimations
                )
                equation_count = raw_data.count("=")

        return build_response(
            status="success",
            filepath=abs_path,
            filename=os.path.basename(abs_path),
            size_bytes=os.path.getsize(abs_path),
            models=list(set(models)),
            processes=list(set(processes)),
            tasks=list(set(tasks)),
            variable_types=list(set(variable_types)),
            parameter_estimations=list(set(parameter_estimations)),
            estimated_equations_count=equation_count,
            solver_architecture="Siemens gPROMS Equation-Oriented DAE/PDE Solver",
            epistemic_classification="OFFLINE_AUDIT",
            lead_process_engineer="Sourish Senapati (FinnoaQ Agro-Industrial Technologies Ltd.)",
            project_ref="FNQ-PR-2026-001"
        )

    def _parse_gproms_text_or_xml(self, content, models, processes, tasks, var_types, param_ests):
        """Helper to extract gPROMS language constructs and XML elements."""
        # 1. Regex parse standard gPROMS syntax keywords
        model_matches = re.findall(r"\bMODEL\s+([A-Za-z0-9_]+)", content, re.IGNORECASE)
        models.extend(model_matches)

        process_matches = re.findall(r"\bPROCESS\s+([A-Za-z0-9_]+)", content, re.IGNORECASE)
        processes.extend(process_matches)

        task_matches = re.findall(r"\bTASK\s+([A-Za-z0-9_]+)", content, re.IGNORECASE)
        tasks.extend(task_matches)

        vtype_matches = re.findall(r"\bVARIABLE_TYPE\s+([A-Za-z0-9_]+)", content, re.IGNORECASE)
        var_types.extend(vtype_matches)

        pest_matches = re.findall(r"\bESTIMATION\s+([A-Za-z0-9_]+)", content, re.IGNORECASE)
        param_ests.extend(pest_matches)

        # 2. XML parse if structured
        if "<" in content and ">" in content:
            try:
                root = ET.fromstring(content)
                for elem in root.iter():
                    tag = elem.tag.lower()
                    name = elem.get("name") or elem.get("id")
                    if name:
                        if "model" in tag:
                            models.append(name)
                        elif "process" in tag:
                            processes.append(name)
                        elif "task" in tag:
                            tasks.append(name)
                        elif "variable" in tag or "vartype" in tag:
                            var_types.append(name)
            except Exception:
                pass

    def run_simulation(self, filepath=None, process_name=None, timeout_sec=60.0):
        """Dispatches batch simulation of a gPROMS model or process."""
        status = self.get_status()
        gproms_exe = status.get("executable_path")

        if not gproms_exe:
            return build_response(
                status="unlicensed_or_missing",
                message=(
                    "Siemens gPROMS executable was not detected in PATH or standard installation directories. "
                    "In compliance with FinnoaQ operational rules (AGENTS.md Track A), synthetic mock execution "
                    "is strictly prohibited. Offline project topology auditing is fully operational."
                ),
                epistemic_classification="BLOCKED",
                project_path=filepath,
                lead_process_engineer="Sourish Senapati (FinnoaQ Agro-Industrial Technologies Ltd.)"
            )

        if filepath:
            abs_path = validate_file_path(filepath, must_exist=True)
            cmd = [gproms_exe, "-batch", abs_path]
            if process_name:
                cmd.extend(["-process", process_name])

            try:
                proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_sec)
                return build_response(
                    status="success" if proc.returncode == 0 else "solver_error",
                    exit_code=proc.returncode,
                    stdout=proc.stdout,
                    stderr=proc.stderr,
                    project_path=abs_path
                )
            except subprocess.TimeoutExpired:
                return build_response(
                    status="timeout_exceeded",
                    timeout_sec=timeout_sec,
                    error="gPROMS simulation exceeded runtime threshold."
                )
        return build_response(
            status="ready",
            message="gPROMS batch dispatcher is configured and ready."
        )
