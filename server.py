from fastmcp import FastMCP, Context
import uuid
import json
# from fastmcp.server.context import ToolContext

server = FastMCP("My MCP Server")
print(Context(server).session_id)  # Print the session ID for debugging
with open("sonic.json", "r") as f:
    sonic = json.load(f)


# print(server.context)  # Print the session ID for debugging
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

@server.tool
def initialize(context: Context = None):
    session_id = str(uuid.uuid4())
    print(f"[INFO] Assigned session: {session_id}")
    return {"status": "initialized", "session_id": session_id}

cap = {
  "capabilities": [
    {
      "name": "interface_state",
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
    },
    {
      "name": "get_config",
      "description": "Retrieve current configuration",
      "supported_on": ["sonic", "fmcli", "onesfm"],
      "params": []
    }

  ],
  "model_types": [
    { "type": "sonic", "versions": ["1.0", "2.0"] },
    { "type": "fmcli", "versions": ["1.0"] },
    { "type": "onesfm", "versions": ["1.0", "1.1"] }
  ]
}

# print (type(cap))

@server.tool
def get_capabilities(context: Context = None):
    sid = context.session_id() if context else None
    print("Session ID:", sid)
    return cap

@server.tool
async def request_info(ctx: Context) -> dict:
    """Return information about the current request."""
    return {
        "request_id": ctx.request_id,
        "client_id": ctx.client_id or "Unknown client",
        "session_id": ctx.session_id or "No session id",
    }

def json_response(request):
    """
    Example tool that returns a JSON response.
    """
    data = request.json
    print("Received data:", data)
    return {"status": "success", "data": data}

@server.tool
def generate_model_endpoint(type: str, action: str, params: dict):
    """
    Receives a request from client and returns a generated model.
    Matches client payload keys: type, action, params.
    """
    print(f"[REQUEST] type={type}, action={action}, params={params}")

    if (type == "sonic"):
        print("forwarding sonic json")
        return sonic
    model = {
        "type": type,
        "action": action,
        "params": params
    }

    response = {"status": "success", "model": model}
    print(f"[RESPONSE] {response}")
    return response

if __name__ == "__main__":
    # print(sonic)
    server.run(transport = "http", host = "0.0.0.0", port = 4321)  
    # using host 0.0.0.0 to allow All available interfaces - can change
    # default port (8000), and path (/mcp/)
    # can customise as needed


# from fastmcp import FastMCP, Context
# from typing import Dict, Any

# server = FastMCP("My MCP Server")

# capabilities = {
#     "capabilities": [
#         {
#             "name": "xyz",
#             "description": "Shutdown or startup an interface",
#             "supported_on": ["sonic", "fmcli", "onesfm"],
#             "params": ["interface", "state"]
#         },
#         {
#             "name": "vlan_config",
#             "description": "Add or delete VLAN",
#             "supported_on": ["sonic", "fmcli", "onesfm"],
#             "params": ["vlan_id", "action"]
#         }
#     ]
# }

# @server.tool
# def get_capabilities(context: Context = None) -> Dict[str, Any]:
#     sid = context.session_id() if context else None
#     print(f"[DEBUG] Session ID: {sid}")
#     return capabilities

# @server.tool
# def initialize(context: Context = None) -> Dict[str, Any]:
#     sid = context.session_id() if context else None
#     print(f"[DEBUG] Initialize called, Session ID: {sid}")
#     return {"status": "initialized", "session": sid}

# @server.tool
# def generate_model(config_type: str, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
#     """Generate a config model."""
#     return {"type": config_type, "action": action, "params": params}

# @server.tool
# async def notify_client(context: Context = None):
#     """Send async server-side message."""
#     sid = context.session_id() if context else None
#     await context.send_notification("serverMessage", {"info": f"Hello Session {sid}"})
#     return {"status": "notified"}

# if __name__ == "__main__":
#     server.run(
#         transport="http",   # Streamable HTTP transport
#         host="0.0.0.0",              # Bind to localhost for security
#         port=4321
#     )