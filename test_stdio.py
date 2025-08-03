#!/usr/bin/env python3
"""
Test client for STDIO MCP Server
This simulates how Claude Desktop would connect to your server.
"""

import asyncio
from fastmcp import Client

async def test_stdio_server():
    """Test the MCP server using STDIO transport (like Claude Desktop does)"""
    print("🚀 Testing MCP Server via STDIO (Claude Desktop style)")
    print("=" * 60)
    
    try:
        # Connect to the server using STDIO (starts subprocess)
        # Try absolute path with poetry
        async with Client([
            "poetry", 
            "run", 
            "python", 
            "/Users/kiryl/projects/agi_house_hack/server.py"
        ]) as client:
            print("✅ Connected to MCP server via STDIO")
            
            # List available tools
            print("\n📋 Available tools:")
            tools = await client.list_tools()
            for tool in tools:
                print(f"  - {tool.name}: {tool.description}")
            
            # Test hello_world tool
            print("\n🌍 Testing hello_world tool:")
            result = await client.call_tool("hello_world", {})
            print(f"  Result: {result.content[0].text}")
            
            # Test echo tool
            print("\n📢 Testing echo tool:")
            result = await client.call_tool("echo", {"message": "from Claude Desktop test"})
            print(f"  Result: {result.content[0].text}")
            
            # Test get_status tool
            print("\n📊 Testing get_status tool:")
            result = await client.call_tool("get_status", {})
            print(f"  Result: {result.content[0].text}")
            
            print("\n✅ All tests completed! Server is ready for Claude Desktop!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure Poetry and FastMCP are installed properly")

if __name__ == "__main__":
    asyncio.run(test_stdio_server()) 