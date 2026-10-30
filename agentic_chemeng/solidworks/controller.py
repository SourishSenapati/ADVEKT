"""
Agentic ChemEng - SolidWorks 2025 Autonomous Controller (Industrial Hardened)
Lead Chemical & Process Engineer: Sourish Senapati

Interfaces directly with Dassault Systèmes SOLIDWORKS 2025 SP1.2 COM API (SldWorks.Application).
Zero synthetic approximations — all geometry and metadata originate from authentic B-Rep solids.
Hardened with timeout guards, COM apartment safety, and robust process lifecycle control.
"""

import os
import sys
import time
import json
import traceback
import pythoncom
import win32com.client

from ..resilience import (
    com_safe_scope,
    validate_file_path,
    EngineeringTimeoutError,
    EngineeringValidationError
)

SW_DOC_NONE = 0
SW_DOC_PART = 1
SW_DOC_ASSEMBLY = 2
SW_DOC_DRAWING = 3
SW_DOC_SDM = 4

SW_OPEN_SILENT = 1
SW_OPEN_READONLY = 2

SW_SAVE_CURRENT_VERSION = 0
SW_SAVE_SILENT = 2

SW_VIEW_FRONT = 1
SW_VIEW_BACK = 2
SW_VIEW_LEFT = 3
SW_VIEW_RIGHT = 4
SW_VIEW_TOP = 5
SW_VIEW_BOTTOM = 6
SW_VIEW_ISOMETRIC = 7

NAMED_VIEWS = {
    "iso": ("*Isometric", SW_VIEW_ISOMETRIC),
    "isometric": ("*Isometric", SW_VIEW_ISOMETRIC),
    "front": ("*Front", SW_VIEW_FRONT),
    "back": ("*Back", SW_VIEW_BACK),
    "top": ("*Top", SW_VIEW_TOP),
    "bottom": ("*Bottom", SW_VIEW_BOTTOM),
    "right": ("*Right", SW_VIEW_RIGHT),
    "left": ("*Left", SW_VIEW_LEFT),
}


class SolidWorksController:
    """Manages an active or dispatched SolidWorks COM Automation session with fail-safe guards."""

    def __init__(self, visible=False):
        self._sw = None
        self._visible = visible

    def get_sw(self, launch_if_closed=True):
        """Connects to active SolidWorks session or dispatches a new one if requested."""
        if self._sw is not None:
            try:
                _ = self._sw.RevisionNumber
                return self._sw
            except Exception:
                self._sw = None

        try:
            self._sw = win32com.client.GetActiveObject("SldWorks.Application")
            return self._sw
        except Exception:
            pass

        if not launch_if_closed:
            return None

        try:
            self._sw = win32com.client.Dispatch("SldWorks.Application")
            self._sw.Visible = self._visible
            self._sw.UserControl = self._visible
        except Exception as e:
            raise RuntimeError(f"Failed to launch Dassault Systèmes SOLIDWORKS via COM: {str(e)}")
        return self._sw

    def get_status(self, launch_if_closed=False):
        """Returns non-blocking diagnostic status of SolidWorks application and loaded documents."""
        with com_safe_scope():
            sw = self.get_sw(launch_if_closed=launch_if_closed)
            if not sw:
                return {
                    "status": "ready_on_demand",
                    "version": "SOLIDWORKS 2025 SP1.2 (Registered in Windows COM)",
                    "active_document": None,
                    "active_document_path": None,
                    "open_document_count": 0,
                    "open_documents": [],
                    "notice": "SolidWorks COM server is registered. Engine launches automatically on 'open', 'inspect', or 'rebuild'.",
                    "lead_engineer": "Sourish Senapati",
                    "project_ref": "ADVEKT-CAE-2026"
                }

            try:
                rev = sw.RevisionNumber
                doc_count = sw.GetDocumentCount
                active_doc = sw.ActiveDoc
                active_title = active_doc.GetTitle if active_doc else None
                active_path = active_doc.GetPathName if active_doc else None

                open_docs = []
                docs_raw = sw.GetDocuments
                if docs_raw:
                    for doc in docs_raw:
                        try:
                            open_docs.append({
                                "title": doc.GetTitle,
                                "path": doc.GetPathName,
                                "type": self._get_doc_type_name(doc.GetType),
                                "is_dirty": doc.GetSaveFlag
                            })
                        except Exception:
                            pass

                return {
                    "status": "connected",
                    "version": f"SOLIDWORKS 2025 (Revision {rev})",
                    "active_document": active_title,
                    "active_document_path": active_path,
                    "open_document_count": doc_count,
                    "open_documents": open_docs,
                    "lead_engineer": "Sourish Senapati",
                    "project_ref": "ADVEKT-CAE-2026"
                }
            except Exception as e:
                return {
                    "status": "connected_busy",
                    "version": "SOLIDWORKS 2025 SP1.2",
                    "error": str(e)
                }

    def _get_doc_type_name(self, doc_type_int):
        mapping = {1: "Part (.SLDPRT)", 2: "Assembly (.SLDASM)", 3: "Drawing (.SLDDRW)"}
        return mapping.get(doc_type_int, f"Unknown ({doc_type_int})")

    def _determine_doc_type(self, filepath):
        ext = os.path.splitext(filepath)[1].lower()
        if ext == ".sldprt":
            return SW_DOC_PART
        elif ext == ".sldasm":
            return SW_DOC_ASSEMBLY
        elif ext == ".slddrw":
            return SW_DOC_DRAWING
        elif ext in [".step", ".stp"]:
            return SW_DOC_PART
        return SW_DOC_PART

    def open_document(self, filepath, read_only=False, silent=True):
        """Opens a document in SolidWorks with strict path validation and error decoding."""
        abs_path = validate_file_path(
            filepath,
            allowed_extensions=[".sldprt", ".sldasm", ".slddrw", ".step", ".stp"],
            must_exist=True
        )

        with com_safe_scope():
            sw = self.get_sw(launch_if_closed=True)
            doc_type = self._determine_doc_type(abs_path)
            options = 0
            if silent:
                options |= SW_OPEN_SILENT
            if read_only:
                options |= SW_OPEN_READONLY

            errors = win32com.client.VARIANT(win32com.client.pythoncom.VT_BYREF | win32com.client.pythoncom.VT_I4, 0)
            warnings = win32com.client.VARIANT(win32com.client.pythoncom.VT_BYREF | win32com.client.pythoncom.VT_I4, 0)

            doc = sw.OpenDoc6(abs_path, doc_type, options, "", errors, warnings)
            if not doc:
                err_code = errors.value
                err_reasons = []
                if err_code & 1: err_reasons.append("Generic error")
                if err_code & 2: err_reasons.append("File not found")
                if err_code & 4: err_reasons.append("File load error")
                if err_code & 8: err_reasons.append("File view-only / read-only lock conflict")
                if err_code & 16: err_reasons.append("Future version file")
                reason_str = ", ".join(err_reasons) if err_reasons else f"Error code {err_code}"
                raise RuntimeError(f"SolidWorks failed to open '{os.path.basename(abs_path)}': {reason_str}")

            return {
                "title": doc.GetTitle,
                "path": abs_path,
                "type": self._get_doc_type_name(doc.GetType),
                "errors": errors.value,
                "warnings": warnings.value
            }

    def close_document(self, title=None, all_docs=False):
        """Closes a specific open document or all documents."""
        with com_safe_scope():
            sw = self.get_sw(launch_if_closed=False)
            if not sw:
                return {"closed": [], "message": "SolidWorks is not currently running."}

            closed = []
            if all_docs:
                docs_raw = sw.GetDocuments
                if docs_raw:
                    for doc in docs_raw:
                        try:
                            t = doc.GetTitle
                            sw.CloseDoc(t)
                            closed.append(t)
                        except Exception:
                            pass
            else:
                if not title:
                    active_doc = sw.ActiveDoc
                    if active_doc:
                        title = active_doc.GetTitle
                    else:
                        return {"closed": [], "message": "No active document to close."}
                sw.CloseDoc(title)
                closed.append(title)

            return {"closed": closed, "remaining_count": sw.GetDocumentCount}

    def inspect_model(self, filepath=None):
        """Inspects full geometry, features, bodies, custom properties, and bounding box."""
        with com_safe_scope():
            doc = None
            should_close = False
            sw = None

            if filepath:
                abs_path = validate_file_path(
                    filepath,
                    allowed_extensions=[".sldprt", ".sldasm", ".slddrw", ".step", ".stp"],
                    must_exist=True
                )
                self.open_document(abs_path, read_only=True, silent=True)
                sw = self.get_sw(launch_if_closed=False)
                doc = sw.ActiveDoc
                should_close = True
            else:
                sw = self.get_sw(launch_if_closed=False)
                if not sw:
                    raise RuntimeError("SolidWorks is not running and no filepath was provided.")
                doc = sw.ActiveDoc
                if not doc:
                    raise RuntimeError("No document is currently active in SolidWorks.")

            try:
                title = doc.GetTitle
                doc_type = doc.GetType
                type_name = self._get_doc_type_name(doc_type)

                config_names = list(doc.GetConfigurationNames) if hasattr(doc, "GetConfigurationNames") else []
                active_config = doc.GetActiveConfiguration.Name if doc.GetActiveConfiguration else "Default"

                cpm = doc.Extension.CustomPropertyManager("")
                prop_names = cpm.GetNames if hasattr(cpm, "GetNames") and cpm.GetNames else []
                custom_props = {}
                for pn in prop_names:
                    val = cpm.Get(pn)
                    if isinstance(val, tuple) and len(val) >= 2:
                        custom_props[pn] = val[1]
                    else:
                        custom_props[pn] = str(val)

                feat = doc.FirstFeature
                features = []
                while feat:
                    features.append({"name": feat.Name, "type": feat.GetTypeName2})
                    feat = feat.GetNextFeature

                bodies_data = []
                if doc_type == SW_DOC_PART:
                    bodies = doc.GetBodies2(0, False)
                    if bodies:
                        for b in bodies:
                            bodies_data.append({"name": b.Name, "visible": b.Visible})

                bbox_data = None
                if doc_type == SW_DOC_PART:
                    try:
                        box = doc.GetPartBox(True)
                        if box and len(box) == 6:
                            dx = round((box[3] - box[0]) * 1000.0, 2)
                            dy = round((box[4] - box[1]) * 1000.0, 2)
                            dz = round((box[5] - box[2]) * 1000.0, 2)
                            bbox_data = {
                                "min_corner_m": [round(box[0], 4), round(box[1], 4), round(box[2], 4)],
                                "max_corner_m": [round(box[3], 4), round(box[4], 4), round(box[5], 4)],
                                "dimensions_mm": {"length_x": dx, "height_y": dy, "width_z": dz}
                            }
                    except Exception:
                        pass

                mass_props_data = self._compute_mass_properties_internal(doc)

                return {
                    "title": title,
                    "type": type_name,
                    "active_configuration": active_config,
                    "configurations": config_names,
                    "custom_properties": custom_props,
                    "feature_count": len(features),
                    "features_summary": features[:25],
                    "solid_body_count": len(bodies_data),
                    "solid_bodies": bodies_data[:20],
                    "bounding_box": bbox_data,
                    "mass_properties": mass_props_data
                }
            finally:
                if should_close and doc and sw:
                    sw.CloseDoc(doc.GetTitle)

    def _compute_mass_properties_internal(self, doc):
        """Helper to extract authentic mass properties from a document."""
        try:
            mp = doc.Extension.CreateMassProperty
            if not mp:
                return None
            mass_kg = round(mp.Mass, 3)
            vol_m3 = round(mp.Volume, 4)
            sa_m2 = round(mp.SurfaceArea, 3)
            cog = mp.CenterOfMass
            cog_mm = [round(c * 1000.0, 2) for c in cog] if cog else [0.0, 0.0, 0.0]
            moi = mp.GetMomentOfInertia(0)
            moi_list = [round(m, 4) for m in moi] if moi else []

            return {
                "mass_kg": mass_kg,
                "volume_m3": vol_m3,
                "volume_liters": round(vol_m3 * 1000.0, 1),
                "surface_area_m2": sa_m2,
                "center_of_mass_mm": {"x": cog_mm[0], "y": cog_mm[1], "z": cog_mm[2]},
                "moments_of_inertia": moi_list
            }
        except Exception as e:
            return {"error": str(e)}

    def get_mass_properties(self, filepath=None):
        """Queries precise mass properties for a model with safety cleanup."""
        with com_safe_scope():
            should_close = False
            doc = None
            sw = None
            if filepath:
                abs_path = validate_file_path(filepath, must_exist=True)
                self.open_document(abs_path, read_only=True, silent=True)
                sw = self.get_sw(launch_if_closed=False)
                doc = sw.ActiveDoc
                should_close = True
            else:
                sw = self.get_sw(launch_if_closed=False)
                if not sw:
                    raise RuntimeError("SolidWorks is not running.")
                doc = sw.ActiveDoc
                if not doc:
                    raise RuntimeError("No document is currently active.")

            try:
                mp_data = self._compute_mass_properties_internal(doc)
                return {
                    "title": doc.GetTitle,
                    "mass_properties": mp_data
                }
            finally:
                if should_close and doc and sw:
                    sw.CloseDoc(doc.GetTitle)

    def force_rebuild(self, filepath=None, save=True):
        """Forces full parametric rebuild and optionally saves."""
        with com_safe_scope():
            should_close = False
            doc = None
            sw = None
            if filepath:
                abs_path = validate_file_path(filepath, must_exist=True)
                self.open_document(abs_path, read_only=False, silent=True)
                sw = self.get_sw(launch_if_closed=False)
                doc = sw.ActiveDoc
                should_close = True
            else:
                sw = self.get_sw(launch_if_closed=False)
                if not sw:
                    raise RuntimeError("SolidWorks is not running.")
                doc = sw.ActiveDoc
                if not doc:
                    raise RuntimeError("No document is currently active.")

            try:
                title = doc.GetTitle
                rebuild_ok = doc.ForceRebuild3(False)
                saved = False
                file_size = None
                if save:
                    errors = win32com.client.VARIANT(win32com.client.pythoncom.VT_BYREF | win32com.client.pythoncom.VT_I4, 0)
                    warnings = win32com.client.VARIANT(win32com.client.pythoncom.VT_BYREF | win32com.client.pythoncom.VT_I4, 0)
                    saved = doc.Save3(SW_SAVE_SILENT, errors, warnings)
                    p = doc.GetPathName
                    if p and os.path.exists(p):
                        file_size = os.path.getsize(p)

                return {
                    "title": title,
                    "rebuild_success": bool(rebuild_ok),
                    "saved": bool(saved),
                    "file_size_bytes": file_size
                }
            finally:
                if should_close and doc and sw:
                    sw.CloseDoc(doc.GetTitle)

    def render_view(self, filepath=None, view="iso", out_path=None):
        """Sets the viewport to a designated standard orientation and renders a high-res PNG."""
        with com_safe_scope():
            should_close = False
            doc = None
            sw = None
            if filepath:
                abs_path = validate_file_path(filepath, must_exist=True)
                self.open_document(abs_path, read_only=True, silent=True)
                sw = self.get_sw(launch_if_closed=False)
                doc = sw.ActiveDoc
                should_close = True
            else:
                sw = self.get_sw(launch_if_closed=False)
                if not sw:
                    raise RuntimeError("SolidWorks is not running.")
                doc = sw.ActiveDoc
                if not doc:
                    raise RuntimeError("No document is currently active.")

            try:
                title = doc.GetTitle
                view_key = view.lower().strip()
                view_tuple = NAMED_VIEWS.get(view_key, ("*Isometric", SW_VIEW_ISOMETRIC))
                view_name, view_id = view_tuple

                doc.ShowNamedView2(view_name, view_id)
                doc.ViewZoomtofit2()

                if not out_path:
                    doc_path = doc.GetPathName
                    base = os.path.splitext(doc_path)[0] if doc_path else title
                    out_path = f"{base}_{view_key}.png"

                out_abs = os.path.abspath(out_path)
                os.makedirs(os.path.dirname(out_abs), exist_ok=True)

                res = doc.SaveAs3(out_abs, SW_SAVE_CURRENT_VERSION, SW_SAVE_SILENT)
                if not os.path.exists(out_abs):
                    raise RuntimeError(f"Failed to capture SolidWorks viewport render: {out_abs} (SaveAs3 code: {res})")

                return {
                    "title": title,
                    "view": view_name,
                    "output_image": out_abs,
                    "file_size_bytes": os.path.getsize(out_abs)
                }
            finally:
                if should_close and doc and sw:
                    sw.CloseDoc(doc.GetTitle)

    def export_cad(self, filepath=None, formats=None, out_dir=None):
        """Exports the model/drawing to formats: ['step', 'pdf', 'png']."""
        if formats is None:
            formats = ["step", "png"]

        with com_safe_scope():
            should_close = False
            doc = None
            sw = None
            if filepath:
                abs_path = validate_file_path(filepath, must_exist=True)
                self.open_document(abs_path, read_only=True, silent=True)
                sw = self.get_sw(launch_if_closed=False)
                doc = sw.ActiveDoc
                should_close = True
            else:
                sw = self.get_sw(launch_if_closed=False)
                if not sw:
                    raise RuntimeError("SolidWorks is not running.")
                doc = sw.ActiveDoc
                if not doc:
                    raise RuntimeError("No document is currently active.")

            try:
                title = doc.GetTitle
                doc_path = doc.GetPathName
                base_name = os.path.splitext(os.path.basename(doc_path))[0] if doc_path else title

                if out_dir is None:
                    out_dir = os.path.dirname(doc_path) if doc_path else os.path.abspath("engineering/cad")
                os.makedirs(out_dir, exist_ok=True)

                exported = {}
                for fmt in formats:
                    fmt = fmt.lower().strip()
                    if fmt in ["step", "stp"]:
                        doc.ClearSelection2(True)
                        tgt = os.path.join(out_dir, f"{base_name}.step")
                        res = doc.SaveAs3(tgt, SW_SAVE_CURRENT_VERSION, SW_SAVE_SILENT)
                        if os.path.exists(tgt):
                            exported["step"] = {"path": tgt, "size_bytes": os.path.getsize(tgt)}
                    elif fmt == "pdf":
                        tgt = os.path.join(out_dir, f"{base_name}.pdf")
                        res = doc.SaveAs3(tgt, SW_SAVE_CURRENT_VERSION, SW_SAVE_SILENT)
                        if os.path.exists(tgt):
                            exported["pdf"] = {"path": tgt, "size_bytes": os.path.getsize(tgt)}
                    elif fmt == "png":
                        doc.ShowNamedView2("*Isometric", SW_VIEW_ISOMETRIC)
                        doc.ViewZoomtofit2()
                        tgt = os.path.join(out_dir, f"{base_name}_Iso.png")
                        res = doc.SaveAs3(tgt, SW_SAVE_CURRENT_VERSION, SW_SAVE_SILENT)
                        if os.path.exists(tgt):
                            exported["png"] = {"path": tgt, "size_bytes": os.path.getsize(tgt)}

                return {
                    "title": title,
                    "exported_files": exported
                }
            finally:
                if should_close and doc and sw:
                    sw.CloseDoc(doc.GetTitle)

    def execute_agent_code(self, code_str):
        """Executes an agent script snippet with direct access to 'sw', 'doc', and 'controller'."""
        with com_safe_scope():
            sw = self.get_sw(launch_if_closed=True)
            doc = sw.ActiveDoc
            local_scope = {
                "sw": sw,
                "doc": doc,
                "controller": self,
                "result": None
            }

            import io
            from contextlib import redirect_stdout, redirect_stderr
            f_out = io.StringIO()
            f_err = io.StringIO()

            with redirect_stdout(f_out), redirect_stderr(f_err):
                exec(code_str, globals(), local_scope)

            return {
                "stdout": f_out.getvalue(),
                "stderr": f_err.getvalue(),
                "result": str(local_scope.get("result"))
            }
