"""
Agentic ChemEng - Example: AI Agent JSON-RPC MCP Client
Lead Chemical & Process Engineer: Sourish Senapati
"""

import json
from agentic_chemeng.mcp.server import process_message


def run_agentic_mcp_session():
    print("=" * 70)
    print("AGENTIC CHEMENG: MODEL CONTEXT PROTOCOL (MCP) SESSION DEMO")
    print("=" * 70)

    # 1. MCP Initialize Handshake
    init_msg = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
    init_res = json.loads(process_message(init_msg))
    print("\n[Step 1: MCP Server Initialize]")
    print(json.dumps(init_res, indent=2))

    # 2. Query Available Tools (tools/list)
    list_msg = json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
    list_res = json.loads(process_message(list_msg))
    tools = list_res["result"]["tools"]
    print(f"\n[Step 2: MCP Tools List] - Total Registered Tools: {len(tools)}")
    for t in tools[:10]:
        print(f" - {t['name']}: {t['description'][:65]}...")
    print(f"   ... and {len(tools) - 10} more tools.")

    # 3. Autonomous Tool Execution: thermo_steam_properties
    tool_msg = json.dumps({
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "thermo_steam_properties",
            "arguments": {"pressure_bar": 4.0}
        }
    })
    tool_res = json.loads(process_message(tool_msg))
    content_text = tool_res["result"]["content"][0]["text"]
    print("\n[Step 3: Autonomous Tool Execution - thermo_steam_properties]")
    print(content_text)

    # 4. Autonomous Tool Execution: pv_asme_ug27_shell
    vessel_msg = json.dumps({
        "jsonrpc": "2.0",
        "id": 4,
        "method": "tools/call",
        "params": {
            "name": "pv_asme_ug27_shell",
            "arguments": {
                "design_pressure_bar": 12.0,
                "inside_diameter_mm": 1500.0,
                "material": "SA-240 316L",
                "corrosion_allowance_mm": 2.0
            }
        }
    })
    vessel_res = json.loads(process_message(vessel_msg))
    vessel_content = vessel_res["result"]["content"][0]["text"]
    print("\n[Step 4: Autonomous Tool Execution - pv_asme_ug27_shell]")
    print(vessel_content)
    print("=" * 70)


if __name__ == "__main__":
    run_agentic_mcp_session()

