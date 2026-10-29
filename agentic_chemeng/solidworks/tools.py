"""
Agentic ChemEng - SolidWorks Tool Definitions & Schemas for MCP & Agent Suites
"""

SOLIDWORKS_TOOLS = [
    {
        "name": "solidworks_get_status",
        "description": "Checks connectivity with Dassault Systèmes SOLIDWORKS 2025 SP1.2, reports software revision, active document, and open document list.",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "solidworks_open_document",
        "description": "Opens a native CAD file (.SLDPRT, .SLDASM, .SLDDRW, or .STEP) in SolidWorks.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "filepath": {"type": "string", "description": "Absolute or relative path to the CAD file"},
                "read_only": {"type": "boolean", "description": "Whether to open in read-only mode (default: false)"},
                "silent": {"type": "boolean", "description": "Whether to suppress interactive UI dialogs (default: true)"}
            },
            "required": ["filepath"]
        }
    },
    {
        "name": "solidworks_close_document",
        "description": "Closes a specific document by title or closes all open documents.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Title or filename of document to close. If omitted, closes active document."},
                "all_docs": {"type": "boolean", "description": "Set to true to close all currently loaded documents."}
            },
            "required": []
        }
    },
    {
        "name": "solidworks_inspect_model",
        "description": "Extracts complete engineering metadata, custom properties, feature tree, solid body list, B-Rep bounding box dimensions, and exact mass properties.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "filepath": {"type": "string", "description": "Optional path to CAD file. If omitted, inspects the active document."}
            },
            "required": []
        }
    },
    {
        "name": "solidworks_get_mass_properties",
        "description": "Computes exact mass (kg), volume (m3, L), surface area (m2), center of mass (mm), and moments of inertia.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "filepath": {"type": "string", "description": "Optional path to CAD file. If omitted, calculates for active document."}
            },
            "required": []
        }
    },
    {
        "name": "solidworks_force_rebuild",
        "description": "Forces full parametric rebuild of the active or designated model/assembly and saves the updated geometry.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "filepath": {"type": "string", "description": "Optional path to CAD file. If omitted, rebuilds active document."},
                "save": {"type": "boolean", "description": "Whether to save after rebuilding (default: true)"}
            },
            "required": []
        }
    },
    {
        "name": "solidworks_render_view",
        "description": "Orients the model to a standard engineering viewpoint (isometric, front, top, right, etc.) and renders a high-resolution PNG image directly from the B-Rep viewport.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "filepath": {"type": "string", "description": "Optional path to CAD file. If omitted, renders active document."},
                "view": {"type": "string", "enum": ["iso", "isometric", "front", "top", "right", "left", "back"], "description": "Standard viewpoint to set (default: iso)"},
                "out_path": {"type": "string", "description": "Destination PNG file path"}
            },
            "required": []
        }
    },
    {
        "name": "solidworks_export_cad",
        "description": "Exports CAD geometry or drawings into STEP AP214, PDF, or high-res PNG.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "filepath": {"type": "string", "description": "Optional path to CAD file. If omitted, exports active document."},
                "formats": {"type": "array", "items": {"type": "string", "enum": ["step", "pdf", "png"]}, "description": "List of target export formats"},
                "out_dir": {"type": "string", "description": "Target directory for exported artifacts"}
            },
            "required": []
        }
    },
    {
        "name": "solidworks_execute_script",
        "description": "Executes an autonomous Python automation script directly in the live SolidWorks COM environment (with access to 'sw', 'doc', and 'controller').",
        "inputSchema": {
            "type": "object",
            "properties": {
                "code": {"type": "string", "description": "Python code snippet to execute"}
            },
            "required": ["code"]
        }
    }
]


def dispatch_solidworks_tool(controller, tool_name, arguments):
    if tool_name == "solidworks_get_status":
        return controller.get_status()
    elif tool_name == "solidworks_open_document":
        return controller.open_document(arguments.get("filepath"), read_only=arguments.get("read_only", False), silent=arguments.get("silent", True))
    elif tool_name == "solidworks_close_document":
        return controller.close_document(title=arguments.get("title"), all_docs=arguments.get("all_docs", False))
    elif tool_name == "solidworks_inspect_model":
        return controller.inspect_model(filepath=arguments.get("filepath"))
    elif tool_name == "solidworks_get_mass_properties":
        return controller.get_mass_properties(filepath=arguments.get("filepath"))
    elif tool_name == "solidworks_force_rebuild":
        return controller.force_rebuild(filepath=arguments.get("filepath"), save=arguments.get("save", True))
    elif tool_name == "solidworks_render_view":
        return controller.render_view(filepath=arguments.get("filepath"), view=arguments.get("view", "iso"), out_path=arguments.get("out_path"))
    elif tool_name == "solidworks_export_cad":
        return controller.export_cad(filepath=arguments.get("filepath"), formats=arguments.get("formats", ["step", "png"]), out_dir=arguments.get("out_dir"))
    elif tool_name == "solidworks_execute_script":
        return controller.execute_agent_code(arguments.get("code", ""))
    else:
        raise ValueError(f"Unknown solidworks tool: {tool_name}")

