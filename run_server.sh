#!/bin/bash
# Wrapper script to run MCP server with Poetry environment
# This ensures FastMCP is available when Claude Desktop starts the server

cd "/Users/kiryl/projects/agi_house_hack"
exec poetry run python server.py 