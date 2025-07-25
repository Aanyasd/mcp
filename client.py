import asyncio
from fastmcp import Client
import requests

client = Client("http://mcp-server:8000/mcp/") # mcp-server for docker, 0.0.0.0 for local testing
print(client.transport)
async def main():          # dummy function to test connection
    async with client:
        # print("Sending ping to MCP server...")
        response = await client.ping()
        print("Established connection with MCP server:", response)
        tools = await client.list_tools()

        for t in tools:
            print(t)



# async def discover_capabilities():
#     async with client:
#         result = await client.call_tool("list_tools")
#         print(result)
#         print("🔍 Available tools exposed by server:")
#         for tool in result.get("tools", []):
#             print(f" - {tool}")

if __name__ == "__main__":
    asyncio.run(main())
    