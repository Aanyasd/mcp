from fastmcp import FastMCP
import json
import requests

server = FastMCP("My MCP Server")

@server.tool
def generate_model(config_type, action, params):
    """
    Generate MCP JSON model for a given config type and action.
    Args:
        config_type (str): 'sonic', 'fmcli', or 'onesfm'
        action (str): e.g. 'shutdown', 'add_vlan', 'add_route'
        params (dict): parameters for the action
    Returns:
        dict: JSON model
    """
    model = {
        "type": config_type,
        "action": action,
        "params": params
    }
    return model


capabilities = [
    {
        "name": "shutdown_interface",
        "description": "Shutdown or startup an interface",
        "supported_on": ["sonic", "fmcli", "onesfm"],
        "params": ["interface", "state"]
    },
    {
        "name": "vlan_config",
        "description": "Add or delete VLAN",
        "supported_on": ["sonic", "fmcli", "onesfm"],
        "params": ["vlan_id", "action"]
    },
    {
        "name": "vlan_member",
        "description": "Add or remove member to VLAN",
        "supported_on": ["sonic", "fmcli", "onesfm"],
        "params": ["vlan_id", "interface", "action", "tagged"]
    },
    {
        "name": "static_route",
        "description": "Add static route",
        "supported_on": ["sonic", "fmcli", "onesfm"],
        "params": ["prefix", "nexthop"]
    }
]

@server.tool
def get_capabilities(request):
    return {"capabilities": capabilities}

@server.tool
def generate_model_endpoint(request):
    data = request.json
    config_type = data.get("type")
    action = data.get("action")
    params = data.get("params", {})
    model = generate_model(config_type, action, params)
    return {"model": model}

if __name__ == "__main__":
    server.run(transport = "http", host = "0.0.0.0")  
    # using host 0.0.0.0 to allow All available interfaces - can change
    # default port (8000), and path (/mcp/)
    # can customise as needed
