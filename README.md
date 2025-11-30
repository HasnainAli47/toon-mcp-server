 ## toon-mcp-server
 
 **An MCP server and Python utility library for converting JSON data and system prompts to and from TOON format.**
 
 TOON (Token‑Oriented Object Notation) is a compact, human‑readable serialization format designed to reduce token usage when interacting with Large Language Models (LLMs). It preserves the structure of your data while using a syntax that is often **30–60% more token‑efficient than JSON**, especially for tabular or repetitive data.
 
 This project provides:
 
 - **A small, well‑typed Python library** for:
   - JSON ↔ TOON conversion.
   - Wrapping system prompts in TOON format.
 - **An MCP stdio server** that exposes these capabilities as tools, ready to be used from MCP‑compatible hosts (e.g. editors or orchestration layers).
 - **PyPI‑ready packaging and clear documentation**, so you can confidently share this with the wider Python community.
 
 ---
 
 ## Features
 
 - **JSON → TOON conversion**: Convert any JSON‑serialisable Python object into TOON text using the `toons` library.
 - **TOON → JSON conversion**: Parse TOON back into Python objects that you can serialise as JSON.
 - **System prompt TOON wrapper**: Wrap your system prompt in a minimal, explicit TOON structure to keep prompts structured and token‑efficient.
 - **MCP stdio server**:
   - Tool: `convert_json_to_toon`
   - Tool: `convert_toon_to_json`
   - Tool: `convert_system_prompt_to_toon`
 - **Clean, simple API** with type hints and docstrings suitable for library use.
 
 ---
 
 ## Installation
 
 Once published to PyPI, you will be able to install it with:
 
 ```bash
 pip install toon-mcp-server
 ```
 
 For local development (in this repository), you can install in editable mode:
 
 ```bash
 cd path/to/this/repo
 pip install -e .
 ```
 
 This will install:
 
 - The `toon_mcp` Python package.
 - The `toon-mcp-server` console script, which runs the MCP stdio server.
 
 ---
 
 ## Library Usage
 
 The main public API lives in `toon_mcp` and is re‑exported from `__init__.py` for convenience.
 
 ```python
 from toon_mcp import (
     json_to_toon,
     toon_to_json,
     system_prompt_to_toon,
     toon_to_system_prompt,
 )
 ```
 
 ### JSON → TOON
 
 ```python
 from toon_mcp import json_to_toon
 
 data = {
     "user": {"id": 123, "name": "Alice"},
     "messages": [
         {"role": "system", "content": "You are a helpful assistant."},
         {"role": "user", "content": "Explain TOON format in simple terms."},
     ],
 }
 
 toon_text = json_to_toon(data)
 print(toon_text)
 ```
 
 - **Input**: Any JSON‑serialisable Python object (`dict`, `list`, `str`, etc.).
 - **Output**: A TOON string that can be sent to an LLM or stored on disk.
 
 You can optionally request a specific indentation level for readability:
 
 ```python
 toon_text = json_to_toon(data, indent=2)
 ```
 
 ### TOON → JSON
 
 ```python
 from toon_mcp import toon_to_json
 
 obj = toon_to_json(toon_text)
 # `obj` is now a standard Python structure that can be serialised as JSON
 ```
 
 - **Input**: TOON text (string).
 - **Output**: Python object (typically `dict` or `list`) that you can then pass to `json.dumps`, your LLM client, or other logic.
 
 ### System prompt → TOON
 
 System prompts are often large and repeated for many requests. This helper wraps your system prompt in a minimal TOON document:
 
 ```python
 from toon_mcp import system_prompt_to_toon
 
 system_prompt = (
     "You are a senior Python engineer. "
     "Answer clearly, use type hints, and explain important design decisions."
 )
 
 toon_prompt = system_prompt_to_toon(system_prompt)
 print(toon_prompt)
 ```
 
 Conceptually, this is equivalent to serialising a structure like:
 
 ```python
 {"system_prompt": system_prompt}
 ```
 
 but in TOON form, which tends to be more compact than raw JSON for larger prompts.
 
 ### TOON → system prompt
 
 ```python
 from toon_mcp import toon_to_system_prompt
 
 original_prompt = toon_to_system_prompt(toon_prompt)
 assert original_prompt == system_prompt
 ```
 
 - **Input**: TOON text that was produced by `system_prompt_to_toon`.
 - **Output**: The original system prompt string.
 
 ---
 
 ## MCP Server
 
 The MCP server is implemented in `toon_mcp.server` and is installed as the `toon-mcp-server` console script.
 
 Under the hood it uses the official `mcp` Python library and runs over stdio:
 
 - It exposes three tools:
   - **`convert_json_to_toon`**
   - **`convert_toon_to_json`**
   - **`convert_system_prompt_to_toon`**
 - It is meant to be launched by an MCP‑compatible host (e.g. an editor, a CLI orchestrator, or other tooling).
 
 ### Tools
 
 - **`convert_json_to_toon`**
   - **Input**: `payload` – JSON‑serialisable structure (MCP will usually send this as a JSON object).
   - **Output**: TOON string.
 
 - **`convert_toon_to_json`**
   - **Input**: `toon_text` – TOON‑formatted string.
   - **Output**: Decoded Python structure (serialisable back to JSON by the host).
 
 - **`convert_system_prompt_to_toon`**
   - **Input**: `prompt` – plain text system prompt.
   - **Output**: TOON string wrapping the prompt (compatible with `toon_to_system_prompt` in the library).
 
 ### Running the server manually
 
 After installing the package:
 
 ```bash
 toon-mcp-server
 ```
 
 This will start the MCP server on stdio (it is meant to be started by an MCP host, not usually by hand).
 
 ### Example host configuration (conceptual)
 
 Exact configuration varies per host, but a typical configuration might look like:
 
 ```json
 {
   "mcpServers": {
     "toon-mcp-server": {
       "command": "toon-mcp-server",
       "args": []
     }
   }
 }
 ```
 
 Consult your MCP host's documentation to see where and how to specify this configuration.
 
 ---
 
 ## Project Layout
 
 - **`pyproject.toml`**: Build configuration and metadata for PyPI.
 - **`src/toon_mcp/__init__.py`**: Public API exports.
 - **`src/toon_mcp/codec.py`**: Core conversion functions.
 - **`src/toon_mcp/server.py`**: MCP stdio server and tool definitions.
 - **`tests/`**: Basic tests for conversions and prompt handling.
 
 ---
 
 ## Design Notes
 
 - **Official TOON implementation**: This project deliberately delegates TOON parsing and serialisation to the `toons` library, which is implemented in Rust and mirrors the standard `json` module API. This keeps the implementation small, predictable, and performant.
 - **Simple, explicit API**:
   - `json_to_toon` / `toon_to_json` operate on arbitrary JSON‑serialisable structures.
   - `system_prompt_to_toon` / `toon_to_system_prompt` focus on the system prompt use‑case, keeping the structure obvious (`{"system_prompt": ...}`) while benefitting from TOON syntax.
 - **MCP first‑class**: The MCP server is implemented once, in `toon_mcp.server`, and exported through the `toon-mcp-server` console script so hosts can launch it easily.
 
 ---
 
 ## Testing
 
 After installing development dependencies, you can run tests with:
 
 ```bash
 pytest
 ```
 
 Basic tests cover:
 
 - Round‑trip JSON → TOON → JSON.
 - Round‑trip system prompt → TOON → system prompt.
 
 You are encouraged to add more tests for your specific use‑cases and data shapes.
 
 ---
 
 ## Versioning
 
 This project follows **semantic versioning**:
 
 - **MAJOR**: Breaking changes.
 - **MINOR**: Backwards‑compatible feature additions.
 - **PATCH**: Backwards‑compatible bug fixes and small improvements.
 
 ---
 
 ## Contributing
 
 Contributions are welcome!
 
 - **Issues**: Use GitHub Issues to report bugs or request features.
 - **Pull Requests**:
   - Keep changes focused and well‑documented.
   - Add or update tests for new behaviour.
   - Maintain type hints and docstrings.
 
 ---
 
 ## License
 
 This project is licensed under the **MIT License**. See the `LICENSE` file for details.
 

