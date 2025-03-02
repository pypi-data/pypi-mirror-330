import asyncio
from typing import Any, Optional
import signal
import httpx
import typer
from typer import Typer
import subprocess
import os
import sys
from pathlib import Path
from mcp.server.fastmcp import FastMCP
from mcp import types

from pydantic import BaseModel, Field

from mcp.server.fastmcp.utilities.types import Image

from tabaka_core import Tabaka


app = FastMCP("tabaka")
cli = Typer(
    name="tabaka",
    help="Tabaka MCP Server CLI",
    add_completion=False,
    no_args_is_help=True,
)
sandbox: Tabaka = Tabaka()


@app.tool()
def execute_code(
    code: str = Field(..., description="The code to execute"),
    language_id: str = Field(
        "python", description="Language to execute the code in, e.g. 'python' etc."
    ),
    required_packages: list[str] = Field(
        default_factory=list,
        description="Packages to install before execution, non-standard library packages, e.g. 'requests', 'numpy', 'pandas', etc.",
    ),
    timeout: Optional[int] = Field(
        180, description="Maximum execution time in seconds"
    ),
) -> str:
    return sandbox.execute_code(
        code, language_id, required_packages, timeout
    ).model_dump_json()


@cli.command()
def start():
    """Start the Tabaka MCP server."""
    # Start the server as a detached process
    script_path = Path(__file__).resolve()
    cmd = [sys.executable, str(script_path), "run"]
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    typer.echo(f"Started the Tabaka server")


@cli.command()
def run():
    """Run the server in the foreground."""

    def handle_interrupt(sig, frame):
        """Custom interrupt handler to ensure clean shutdown"""
        typer.echo("Interrupt received, shutting down gracefully...")
        try:
            # See: https://github.com/encode/uvicorn/discussions/1103
            signal.raise_signal(signal.SIGINT)
        except Exception:
            pass

        sandbox.cleanup()
        sys.exit(0)

    # Register custom signal handler for graceful shutdown
    signal.signal(signal.SIGINT, handle_interrupt)
    signal.signal(signal.SIGTERM, handle_interrupt)

    try:
        app.run(transport="sse")
    except KeyboardInterrupt:
        handle_interrupt(None, None)
    except Exception as e:
        typer.echo(f"Error: {e}")
        handle_interrupt(None, None)


@cli.command()
def stop():
    """Stop the Tabaka server and clean up any Docker containers."""
    typer.echo("Stopping Tabaka server and cleaning up Docker containers...")

    # Find processes that match our server pattern
    server_stopped = False

    try:
        if sys.platform == "win32":
            # Windows approach
            subprocess.run(
                ["taskkill", "/F", "/FI", "WINDOWTITLE eq *tabaka*"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )
            server_stopped = True
        else:
            # Unix approach - find processes with "tabaka-mcp" in command line
            # More elegant solution using pkill
            result = subprocess.run(
                ["pkill", "-f", "tabaka"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )
            server_stopped = result.returncode == 0
    except Exception as e:
        typer.echo(f"Note: Process termination attempt: {e}")

    # Clean up Docker containers
    clean_containers()

    if server_stopped:
        typer.echo("Server processes stopped successfully.")
    else:
        typer.echo("No running server processes found or unable to stop them.")


def clean_containers():
    """Clean up Docker containers related to Tabaka."""
    try:
        # Stop and remove containers in one command using docker compose
        containers = (
            subprocess.run(
                [
                    "docker",
                    "ps",
                    "-a",
                    "--filter",
                    "name=tabaka",
                    "--format",
                    "{{.ID}}",
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            .stdout.strip()
            .split("\n")
        )

        if containers and containers[0]:
            typer.echo(f"Found {len(containers)} Docker containers to clean up")

            # Stop all containers at once
            container_ids = [c for c in containers if c]
            if container_ids:
                subprocess.run(
                    ["docker", "stop"] + container_ids,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=False,
                )
                subprocess.run(
                    ["docker", "rm"] + container_ids,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=False,
                )

            typer.echo("Docker containers cleaned up successfully.")
        else:
            typer.echo("No Docker containers found to clean up.")
    except Exception as e:
        typer.echo(f"Error cleaning up Docker containers: {e}")


if __name__ == "__main__":
    cli()
