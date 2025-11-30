 """
 Core conversion utilities for TOON <-> JSON and system prompt handling.
 
 This module is intentionally small and dependency-light: it relies on the
 `toons` library, which implements the official TOON format with an API that
 mirrors Python's standard `json` module.
 """
 
from __future__ import annotations

import json
from typing import Any

import toons


def json_to_toon(data: Any, *, indent: int | None = None) -> str:
     """
     Convert a Python object (typically parsed from JSON) into TOON text.
 
     Parameters
     ----------
     data:
         Any JSON-serialisable Python object (dict, list, str, int, float, bool, None).
     indent:
         Optional indentation level to pass through to `toons.dumps`. Using a small
         non-zero indent (for example 2) can make the output more readable while still
         remaining token-efficient. If ``None`` (the default), `toons` chooses its
         own compact representation.
 
    Returns
    -------
    str
        TOON representation of the input data.

    Raises
    ------
    TypeError
        If ``data`` cannot be serialised as JSON (e.g. contains non‑serialisable
        objects such as open file handles, sets, or custom classes).
    """

    # Validate that the object is at least JSON-serialisable. This provides
    # a clear and familiar error message instead of letting lower-level
    # TOON errors surface directly.
    try:
        json.dumps(data)
    except (TypeError, ValueError) as exc:  # pragma: no cover - message is what's important
        raise TypeError(
            "json_to_toon expected a JSON-serialisable object "
            "(dict, list, str, int, float, bool, or None). "
            f"Got {type(data).__name__}: {exc}"
        ) from exc

    if indent is not None and not isinstance(indent, int):
        raise TypeError(
            "json_to_toon 'indent' must be an int number of spaces or None, "
            f"got {type(indent).__name__}."
        )

    return toons.dumps(data, indent=indent)
 
 
def toon_to_json(text: str) -> Any:
     """
     Parse TOON text into a Python object that can be serialised as JSON.
 
     Parameters
     ----------
     text:
         TOON-formatted string, as produced by :func:`json_to_toon` or any other
         TOON-compliant producer.
 
    Returns
    -------
    Any
        Python object representation of the input TOON.

    Raises
    ------
    TypeError
        If ``text`` is not a string.
    ValueError
        If the TOON text is invalid and cannot be parsed.
    """

    if not isinstance(text, str):
        raise TypeError(
            "toon_to_json expected 'text' to be a str containing TOON data, "
            f"got {type(text).__name__}."
        )

    try:
        return toons.loads(text)
    except Exception as exc:  # pragma: no cover - error type may vary by toons version
        raise ValueError(f"Failed to parse TOON text: {exc}") from exc
 
 
def system_prompt_to_toon(prompt: str) -> str:
     """
     Wrap a system prompt in a minimal TOON structure.
 
     The prompt is represented as a small TOON document with a single field
     named ``system_prompt``. This keeps things simple and explicit while
     still benefiting from TOON's compact syntax for larger prompts.
 
     Example output (schematic)::
 
         system_prompt: You are a helpful assistant...
 
     Parameters
     ----------
     prompt:
         Raw system prompt text.
 
    Returns
    -------
    str
        TOON-formatted representation of the prompt.

    Raises
    ------
    TypeError
        If ``prompt`` is not a string.
    """

    if not isinstance(prompt, str):
        raise TypeError(
            "system_prompt_to_toon expected 'prompt' to be a string, "
            f"got {type(prompt).__name__}."
        )

    payload = {"system_prompt": prompt}
    return json_to_toon(payload)
 
 
 def toon_to_system_prompt(text: str) -> str:
     """
     Extract a system prompt from TOON text produced by :func:`system_prompt_to_toon`.
 
     Parameters
     ----------
     text:
         TOON-formatted string previously created by :func:`system_prompt_to_toon`,
         or a compatible structure that contains a ``system_prompt`` field.
 
     Returns
     -------
     str
         The system prompt text.
 
     Raises
     ------
     KeyError
         If the decoded structure does not contain a ``system_prompt`` key.
     TypeError
         If the decoded structure is not a mapping.
     """
 
     obj = toon_to_json(text)
     if not isinstance(obj, dict):
         raise TypeError("Expected TOON structure to decode to a mapping with 'system_prompt' key.")
     if "system_prompt" not in obj:
         raise KeyError("Decoded TOON structure does not contain a 'system_prompt' field.")
     value = obj["system_prompt"]
     if not isinstance(value, str):
         raise TypeError("Field 'system_prompt' is not a string in decoded TOON structure.")
     return value
 

