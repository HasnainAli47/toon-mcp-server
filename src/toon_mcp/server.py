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
 async def convert_json_to_toon(payload: dict) -> str:
     """
     Convert JSON-compatible data into TOON text.
 
     Parameters
     ----------
     payload:
         Any JSON-serialisable structure (usually provided by the MCP host).
     """
 
     return json_to_toon(payload)
 
 
 @server.tool()
 async def convert_toon_to_json(toon_text: str):
     """
     Convert TOON text back into JSON-compatible data.
 
     Parameters
     ----------
     toon_text:
         String containing TOON-formatted data.
     """
 
     return toon_to_json(toon_text)
 
 
 @server.tool()
 async def convert_system_prompt_to_toon(prompt: str) -> str:
     """
     Convert a plain system prompt string into TOON format.
 
     Parameters
     ----------
     prompt:
         The system prompt text to be wrapped in a minimal TOON document.
     """
 
     return system_prompt_to_toon(prompt)
 
 
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
 

