#!/usr/bin/env python3
"""
MCP Server for Claude Desktop using FastMCP
Uses STDIO transport for Claude Desktop integration.
"""
import os
from zep_cloud.client import Zep
from fastmcp import FastMCP
import dotenv

dotenv.load_dotenv()

API_KEY = os.environ.get('ZEP_API_KEY')


client = Zep(
    api_key=API_KEY,
)
# new_user = client.user.delete(
#     user_id="ikliuger@gmail.com",
# )

# new_user = client.user.add(
#     user_id="ikliuger@gmail.com",

# )


# Create MCP server instance
mcp = FastMCP("Knowledge Vault")

@mcp.tool
def hello_world() -> str:
    """Returns a simple hello world message"""
    return "hello world"

@mcp.tool
def echo(message: str) -> str:
    """Echo back a message with hello world prefix"""
    return f"hello world: {message}"

@mcp.tool
def get_status() -> dict:
    """Get server status information"""
    return {
        "status": "running",
        "message": "hello world",
        "server": "FastMCP Hello World Server",
        "available_tools": ["hello_world", "echo", "get_status", "add_user_message", "get_user_information"]
    }

@mcp.tool
def add_user_message(user_id: str, message: str) -> dict:
    """
    Add user message to the knowledge graph
    
    Args:
        user_id: User ID or email address
        message: The user's message to store in the graph
    
    Returns:
        dict: Result of the operation including success status and any relevant info
    """
    try:
        # Add the message data to the graph using the user_id as group_id
        # This allows organizing messages by user
        result = client.graph.add(
            user_id=user_id,
            type="text",
            data=message
        )
        
        return {
            "success": True,
            "message": "User message successfully added to knowledge graph",
            "user_id": user_id,
            "data_added": message[:100] + "..." if len(message) > 100 else message,
            "result": str(result) if result else "Added successfully"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to add user message to knowledge graph",
            "user_id": user_id
        }

@mcp.tool
def get_user_information(user_id: str, request: str) -> dict:
    """
    Retrieve user knowledge and contextual information from the knowledge graph.
    
    This tool searches through a user's stored knowledge, conversations, preferences, 
    and contextual information to find content relevant to the specific request. 
    Use this to get user-specific context, recall past interactions, understand 
    user preferences, or find any information previously stored about the user.
    
    Args:
        user_id: User ID or email address to search knowledge for
        request: Natural language query describing what information you need 
                (e.g., "user preferences", "past conversations about travel", 
                "personal information", "recent interests")
    
    Returns:
        dict: Retrieved user knowledge including relevant facts, entities, and 
              contextual information that matches the request
    """
    try:
        # Search the graph for information related to the user and request
        search_results = client.graph.search(
            query=request,
            user_id=user_id,
            limit=10  # Limit results to top 10 most relevant
        )
        
        # Extract facts and entities from search results
        facts = []
        entities = []
        
        # Process edges (facts/relationships)
        if hasattr(search_results, 'edges') and search_results.edges:
            for edge in search_results.edges:
                if hasattr(edge, 'fact'):
                    facts.append({
                        "fact": edge.fact,
                        "uuid": getattr(edge, 'uuid', None),
                        "created_at": str(getattr(edge, 'created_at', None))
                    })
        
        # Process nodes (entities)
        if hasattr(search_results, 'nodes') and search_results.nodes:
            for node in search_results.nodes:
                entities.append({
                    "name": getattr(node, 'name', 'Unknown'),
                    "uuid": getattr(node, 'uuid', None),
                    "summary": getattr(node, 'summary', None),
                    "created_at": str(getattr(node, 'created_at', None))
                })
        
        return {
            "success": True,
            "message": "Information retrieved successfully",
            "user_id": user_id,
            "request": request,
            "results": {
                "facts": facts,
                "entities": entities,
                "total_facts": len(facts),
                "total_entities": len(entities)
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to retrieve information from knowledge graph",
            "user_id": user_id,
            "request": request,
            "results": {
                "facts": [],
                "entities": [],
                "total_facts": 0,
                "total_entities": 0
            }
        }

if __name__ == "__main__":
    # Run with STDIO transport (default) for Claude Desktop
    print("Starting MCP server...")
    mcp.run() 