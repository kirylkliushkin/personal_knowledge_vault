# Hello World MCP Server

A simple Model Context Protocol (MCP) server built with FastMCP that responds with "hello world" messages. This server can be connected to by other agents and MCP clients.

## Features

- **hello_world**: Returns a simple "hello world" message
- **echo**: Echoes back a message with "hello world" prefix
- **get_status**: Returns server status and available tools

## Setup

1. **Install dependencies**:
   ```bash
   poetry install
   ```

2. **Test the server for Claude Desktop**:
   ```bash
   poetry run python test_stdio.py
   ```

This tests the STDIO transport that Claude Desktop uses.

## Usage

### Connecting with MCP Clients

Other agents can connect to this server using the MCP protocol. The server exposes three tools:

1. `hello_world()` - Returns "hello world"
2. `echo(message: str)` - Returns "hello world: {message}"
3. `get_status()` - Returns server information

### Connecting to Claude Desktop

**Step 1: Test your server first**
```bash
poetry run python test_stdio.py
```

**Step 2: Locate Claude Desktop config file**
On macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`

**Step 3: Add your server to the config**
Copy the contents of `claude_desktop_config.json` to Claude's config file, or merge it if you already have other servers:

```json
{
  "mcpServers": {
    "hello-world-server": {
      "command": "poetry",
      "args": [
        "run", 
        "python", 
        "/Users/kiryl/projects/agi_house_hack/server.py"
      ],
      "env": {}
    }
  }
}
```

**Step 4: Restart Claude Desktop**
- Quit Claude Desktop completely
- Reopen it
- Your "hello world" tools should now be available!

### Testing with FastMCP Client

You can test the server programmatically:

```python
import asyncio
from fastmcp import Client

async def test_server():
    async with Client("poetry run python server.py") as client:
        # List available tools
        tools = await client.list_tools()
        print(f"Available tools: {tools}")
        
        # Call hello_world tool
        result = await client.call_tool("hello_world", {})
        print(f"Result: {result.content}")
        
        # Call echo tool
        result = await client.call_tool("echo", {"message": "from client"})
        print(f"Echo result: {result.content}")

if __name__ == "__main__":
    asyncio.run(test_server())
```

## Server Transports

### For Claude Desktop (Recommended)
- **File**: `server.py` 
- **Transport**: STDIO (default)
- **Usage**: Claude Desktop starts the server automatically
- **Test**: `poetry run python test_stdio.py`

### For Other Agents (HTTP connections)
- **File**: `server_streamable.py`
- **Transport**: Streamable HTTP 
- **Usage**: Multiple agents can connect to running server
- **Test**: Start server, then `poetry run python test_client_local.py`

```bash
# For multiple agents over HTTP
poetry run python server_streamable.py

# For Claude Desktop (no need to run manually)
# Claude Desktop will start server.py automatically
```

## Development

The server is built using [FastMCP](https://github.com/jlowin/fastmcp), a high-level Python framework for building MCP servers and clients.

### Project Structure
```
.
├── server.py           # Main MCP server implementation
├── pyproject.toml      # Poetry dependencies and project config
├── test_client.py      # Example test client
└── README.md          # This file
```

## Next Steps

This is a basic example. You can extend it by:

- Adding more sophisticated tools
- Integrating with external APIs
- Adding authentication
- Implementing resources and prompts
- Creating more complex business logic

For more information about MCP and FastMCP, visit:
- [FastMCP Documentation](https://gofastmcp.com)
- [Model Context Protocol](https://modelcontextprotocol.io) 