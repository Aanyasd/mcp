# import asyncio
# from fastmcp import Client
# import requests
# import json

# try:
#     client = Client("http://127.0.0.1:4321/mcp/") # mcp-server for docker, 0.0.0.0 for local testing
# except:
#     print("Failed to connect to the MCP server. Please ensure the server is running and accessible.")

# async def main():         
#     async with client:
#         # print("Sending ping to MCP server...")
#         response = await client.ping()
#         print("Established connection with MCP server:", response)
#         tools = await client.list_tools()
#         cap = await client.call_tool("get_capabilities")
#         req ={
#                 "type": "sonic",         # or "fmcli", "onesfm"
#                 "action": "add_vlan",    # or any supported action
#                 "params": {"vlan_id": 10, "action": "add"}
#             }
#         result = await client.call_tool("generate_model_endpoint", req)
#         print(result)



# if __name__ == "__main__":
#     asyncio.run(main())
    

import asyncio
from logging import info
from unittest import result
from fastmcp import Client
import uuid
# from fastmcp.client.transports import StreamableHTTPTransport
from fastmcp.client.transports import StreamableHttpTransport
import json
    
class StreamableMCPClient:
    # def __init__(self, endpoint: str):
    #     self.endpoint = endpoint
    #     self.session_id = None

    #     # Create transport for Streamable HTTP
    #     self.transport = StreamableHttpTransport(self.endpoint)
    #     self.client = Client(self.transport)

    # async def initialize_session(self):
    #     """Initialize MCP session and store session ID."""
    #     async with self.client as c:
    #         self.session_id = self.transport.session_id
    #         print(f"[INFO] Session initialized: {self.session_id}")

    async def call_tool(self, tool_name: str, **params):
        """Send JSON-RPC request (POST) to call a tool."""
        async with self.client as c:
            try:
                response = await c.call_tool(tool_name, **params)
                print(f"[RESPONSE] {response}")
                return response
            except Exception as e:
                print(f"[ERROR] Tool call failed: {e}")

    async def list_tools(self):
        """List available tools."""
        async with self.client as c:
            try:
                tools = await c.list_tools()
                # print(f"[INFO] Available tools: {tools}")
                return tools
            except Exception as e:
                print(f"[ERROR] Failed to list tools: {e}")

    async def send_request(self, tool_name: str, params: dict = None):
        """Send a JSON-RPC tool call."""
        async with self.client as c:
            try:
                response = await c.call_tool(tool_name, params or {})
                # print(f"[INFO] Tool `{tool_name}` response: {response}")
                return response
            except Exception as e:
                print(f"[ERROR] Tool call failed: {e}")

    async def listen_for_server_messages(self, last_event_id=None):
        """GET SSE stream for server-initiated messages."""
        async with self.client as c:
            print("[INFO] Listening for server-initiated SSE messages...")
            async for message in c.listen(last_event_id=last_event_id):
                print(f"[SERVER SSE] {message}")

    async def terminate_session(self):
        """Send DELETE to terminate session."""
        async with self.client as c:
            if not self.session_id:
                print("[INFO] No active session to terminate.")
                return
            try:
                await c.terminate_session()
                print(f"[INFO] Session {self.session_id} terminated.")
                self.session_id = None
            except Exception as e:
                print(f"[WARN] Termination failed: {e}")


# Example usage
# async def main():
    

    # Step 1: Initialize session
    # await mcp_client.initialize_session()

    # Step 2: Send a tool request
    # await mcp_client.call_tool("get_capabilities", mcp_client.session_id)

    # Step 3: Listen for messages from the server
    # await mcp_client.listen_for_server_messages()

    # Step 4: Terminate session
    # await mcp_client.terminate_session()

async def main():  
    endpoint = "http://0.0.0.0:4321/mcp"             # mcp-server or 0.0.0.0
    mcp_client = Client(endpoint)       
    async with mcp_client:
        response = await mcp_client.call_tool("initialize")
        print("Established connection with MCP server:", response)
    
    #list tools
    # print("\n Available tools:")
    # tools = await mcp_client.list_tools()
    # for tool in tools:
    #     print(tool.name)

    # cap = await mcp_client.call_tool("get_capabilities")
    req ={
            "type": "sonic",         # or "fmcli", "onesfm"
            "action": "add_vlan",    # or any supported action
            "params": {"vlan_id": 10, "action": "add"}
        }
    
    # print(result)
    async with mcp_client as c:
        info = await c.call_tool("request_info")
        print("Request info:", info)
        result = await mcp_client.call_tool("generate_model_endpoint", req)

    x =(result.content[0]).text
    print(type(x))

    data = json.loads(x)

    # Write to file with pretty formatting
    with open("client_file.json", "w") as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    asyncio.run(main())