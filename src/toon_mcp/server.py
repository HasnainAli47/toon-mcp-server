 """
 MCP server exposing TOON conversion tools.
 
 This server is designed to be run over stdio so that MCP-compatible hosts
 (such as IDEs or orchestrators) can invoke it as a subprocess.
 """
 
 from __future__ import annotations
 
 import asyncio
 
from mcp.server import Server
from mcp.server.stdio import stdio_server

from .codec import json_to_toon, toon_to_json, system_prompt_to_toon


server = Server("toon-mcp-server")


@server.tool()
async def convert_json_to_toon(payload: object) -> str:
     """
     Convert JSON-compatible data into TOON text.
 
     Parameters
     ----------
     payload:
         Any JSON-serialisable structure (usually provided by the MCP host).
    """

    try:
        return json_to_toon(payload)
    except (TypeError, ValueError) as exc:
        # Tool error messages should be explicit so the MCP host can surface
        # them directly to the user.
        raise ValueError(f"convert_json_to_toon: {exc}") from exc


@server.tool()
async def convert_toon_to_json(toon_text: object):
     """
     Convert TOON text back into JSON-compatible data.
 
     Parameters
     ----------
     toon_text:
         String containing TOON-formatted data.
    """

    try:
        # The codec layer will validate that this is a string and raise
        # a clear error if not.
        return toon_to_json(toon_text)  # type: ignore[arg-type]
    except (TypeError, ValueError) as exc:
        raise ValueError(f"convert_toon_to_json: {exc}") from exc


@server.tool()
async def convert_system_prompt_to_toon(prompt: object) -> str:
     """
     Convert a plain system prompt string into TOON format.
 
     Parameters
     ----------
     prompt:
         The system prompt text to be wrapped in a minimal TOON document.
    """

    try:
        return system_prompt_to_toon(prompt)  # type: ignore[arg-type]
    except TypeError as exc:
        raise ValueError(f"convert_system_prompt_to_toon: {exc}") from exc
 
 
 async def _run() -> None:
     """
     Entry point used by :func:`main` and by the console script.
     """
 
     async with stdio_server() as (read_stream, write_stream):
         await server.run(read_stream, write_stream)
 
 
 def main() -> None:
     """
     Console-script entry point for ``toon-mcp-server``.
     """
 
     asyncio.run(_run())
 
 
 if __name__ == "__main__":
     main()
 

