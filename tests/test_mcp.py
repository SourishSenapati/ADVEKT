"""
Unit tests for Unified MCP Server & Tool Protocol
"""

import json
import pytest
from agentic_chemeng.mcp.server import ALL_TOOLS, process_message, handle_tool_call


def test_mcp_all_tools_count():
    assert len(ALL_TOOLS) == 37
    tool_names = [t["name"] for t in ALL_TOOLS]
    # Check key representative tools from each subsystem
    assert "solidworks_get_status" in tool_names
    assert "aspen_plus_get_status" in tool_names
    assert "aspen_hysys_get_status" in tool_names
    assert "dwsim_get_status" in tool_names
    assert "autocad_get_status" in tool_names
    assert "thermo_steam_properties" in tool_names
    assert "hydraulics_pressure_drop" in tool_names
    assert "thermal_rate_tema_shell_and_tube" in tool_names
    assert "pv_asme_ug27_shell" in tool_names


def test_mcp_initialize():
    req = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
    resp = json.loads(process_message(req))
    assert resp["id"] == 1
    assert "serverInfo" in resp["result"]
    assert resp["result"]["serverInfo"]["lead_engineer"] == "Sourish Senapati (FinnoaQ Agro-Industrial Technologies Ltd.)"


def test_mcp_tools_list():
    req = json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
    resp = json.loads(process_message(req))
    assert resp["id"] == 2
    assert "tools" in resp["result"]
    assert len(resp["result"]["tools"]) == 37


def test_mcp_tool_call_thermo():
    req = json.dumps({
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "thermo_steam_properties",
            "arguments": {"temperature_C": 120.0}
        }
    })
    resp = json.loads(process_message(req))
    assert resp["id"] == 3
    content_text = resp["result"]["content"][0]["text"]
    data = json.loads(content_text)
    assert data["temperature_C"] == 120.0
    assert 1.9 <= data["saturation_pressure_bar"] <= 2.1


def test_mcp_tool_call_pressure_vessel():
    req = json.dumps({
        "jsonrpc": "2.0",
        "id": 4,
        "method": "tools/call",
        "params": {
            "name": "pv_asme_ug27_shell",
            "arguments": {
                "design_pressure_bar": 10.0,
                "inside_diameter_mm": 1000.0,
                "material": "SA-240 316L"
            }
        }
    })
    resp = json.loads(process_message(req))
    assert resp["id"] == 4
    content_text = resp["result"]["content"][0]["text"]
    data = json.loads(content_text)
    assert data["inside_diameter_mm"] == 1000.0
    assert data["recommended_plate_thickness_mm"] >= 6.0

