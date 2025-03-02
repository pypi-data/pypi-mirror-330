import asyncio
from typing import Any
import httpx
from mcp import stdio_server
from mcp.server.fastmcp import FastMCP
from tabaka_core import Tabaka


app = FastMCP("tabaka")
sandbox = Tabaka()


@app.tool(name="execute_code")
def execute_code(code: str) -> str:
    return sandbox.execute_code(code)


async def main():
    async with stdio_server() as streams:
        await app.run(
            streams[0],
            streams[1],
            app.create_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(main())
