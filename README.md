# Knowledge Vault MCP Server

A Model Context Protocol (MCP) server built with FastMCP that provides intelligent knowledge storage and retrieval using Zep's knowledge graph. This server can store user messages and retrieve contextual information, making it perfect for building personalized AI experiences.

## Features

- **add_user_message**: Store user messages in the knowledge graph
- **get_user_information**: Retrieve user-specific knowledge and context based on natural language queries
- **hello_world**: Returns a simple "hello world" message (for testing)
- **echo**: Echoes back a message with "hello world" prefix (for testing)
- **get_status**: Returns server status and available tools

## Setup

1. **Install dependencies**:
   ```bash
   poetry install
   ```

2. **Configure Zep API**:
   Create a `.env` file in the project root with your Zep API key:
   ```bash
   ZEP_API_KEY=your_zep_api_key_here
   ```

3. **Test the server for Claude Desktop**:
   ```bash
   poetry run python test_stdio.py
   ```

This tests the STDIO transport that Claude Desktop uses.

## Usage

### Main Knowledge Management Tools

The server provides two powerful knowledge management tools:

1. **`add_user_message(user_id: str, message: str)`** - Stores user messages in the knowledge graph
   - Associates messages with specific users
   - Builds a personalized knowledge base for each user

2. **`get_user_information(user_id: str, request: str)`** - Retrieves relevant user knowledge
   - Uses natural language queries to find information
   - Returns facts, entities, and contextual information
   - Examples: "user preferences", "past conversations about travel", "personal information"

### Example Usage

```python
# Store a user message
add_user_message("user@example.com", "I love hiking and prefer mountain trails over beach walks")

# Later, retrieve user preferences
get_user_information("user@example.com", "user's outdoor activity preferences")
```

### Connecting to Claude Desktop

**Step 1: Test your server first**
```bash
poetry run python test_stdio.py
```

**Step 2: Locate Claude Desktop config file**
On macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`

**Step 3: Add your server to the config**
```json
{
  "mcpServers": {
    "knowledge-vault": {
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
- Your Knowledge Vault tools should now be available!

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
        
        # Store user information
        result = await client.call_tool("add_user_message", {
            "user_id": "test@example.com",
            "message": "I'm interested in machine learning and AI"
        })
        print(f"Storage result: {result.content}")
        
        # Retrieve user information
        result = await client.call_tool("get_user_information", {
            "user_id": "test@example.com",
            "request": "What are the user's interests?"
        })
        print(f"Retrieved info: {result.content}")

if __name__ == "__main__":
    asyncio.run(test_server())
```

## Dependencies

This project uses:
- **FastMCP**: High-level Python framework for MCP servers
- **Zep Cloud**: Knowledge graph and memory management
- **python-dotenv**: Environment variable management

## Development

### Project Structure
```
.
├── server.py           # Main MCP server implementation
├── pyproject.toml      # Poetry dependencies and project config
├── test_stdio.py       # STDIO transport test
├── run_server.sh       # Server startup script
├── .env               # Environment variables (create this)
└── README.md          # This file
```

### Environment Variables

Required environment variables:
- `ZEP_API_KEY`: Your Zep Cloud API key for knowledge graph access

## Use Cases

This Knowledge Vault is perfect for:

- **Personalized AI Assistants**: Remember user preferences and context across conversations
- **Customer Support**: Store and retrieve customer interaction history
- **Learning Systems**: Track user progress and adapt to learning patterns
- **Content Recommendation**: Build user profiles for personalized recommendations
- **Research Assistance**: Organize and retrieve research notes and findings

## Next Steps

Extend the server by:

- Adding more sophisticated knowledge retrieval queries
- Implementing user authentication and authorization
- Adding data export/import capabilities
- Creating specialized tools for different domains
- Integrating with other knowledge sources
- Adding analytics and insights about stored knowledge

For more information about MCP and FastMCP, visit:
- [FastMCP Documentation](https://gofastmcp.com)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [Zep Cloud Documentation](https://docs.getzep.com) 