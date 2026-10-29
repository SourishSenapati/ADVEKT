"""
Agentic ChemEng - AutoCAD Tool Definitions & Schemas for MCP & Agent Suites
"""

AUTOCAD_TOOLS = [
    {
        "name": "autocad_get_status",
        "description": "Checks connectivity with Autodesk AutoCAD 2025 COM automation and accoreconsole.exe console availability.",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "autocad_plot_pdf",
        "description": "Headlessly plots a native DWG or DXF engineering drawing to a vector PDF using DWG To PDF.pc3.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "drawing_path": {"type": "string", "description": "Path to DWG or DXF file"},
                "out_pdf_path": {"type": "string", "description": "Optional destination PDF path"}
            },
            "required": ["drawing_path"]
        }
    },
    {
        "name": "autocad_run_script",
        "description": "Executes AutoCAD command script (.scr) headlessly using accoreconsole.exe.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "drawing_path": {"type": "string", "description": "Path to DWG or DXF file"},
                "script_commands": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of AutoCAD command strings to execute sequentially"
                }
            },
            "required": ["drawing_path", "script_commands"]
        }
    }
]


def dispatch_autocad_tool(controller, tool_name, arguments):
    if tool_name == "autocad_get_status":
        return controller.get_status()
    elif tool_name == "autocad_plot_pdf":
        return controller.plot_pdf(arguments.get("drawing_path"), out_pdf_path=arguments.get("out_pdf_path"))
    elif tool_name == "autocad_run_script":
        return controller.run_script(arguments.get("drawing_path"), arguments.get("script_commands"))
    else:
        raise ValueError(f"Unknown autocad tool: {tool_name}")

