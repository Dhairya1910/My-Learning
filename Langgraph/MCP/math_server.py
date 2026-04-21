from fastmcp import FastMCP

mcp = FastMCP("math_server")


@mcp.tool()
def add(a: int, b: int) -> int:
    """
    Add two numbers
    """
    return a + b


@mcp.tool()
def sub(a: int, b: int) -> int:
    """
    subtract two numbers
    """
    return a - b


@mcp.tool()
def weather_report(city: str) -> str:
    """
    This tool is to see the weather reports.
    """
    return "Sunny he weather in Surat"


if __name__ == "__main__":
    mcp.run(transport="stdio")
