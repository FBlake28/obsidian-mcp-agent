from mcp.server.fastmcp import FastMCP

mcp = FastMCP("obsidian-mcp-agent")


@mcp.tool()
def ping() -> str:
    """Test tool to verify the server is working."""
    return "pong"


if __name__ == "__main__":
    mcp.run(transport="stdio")
