 import textwrap
 
 from toon_mcp import (
     json_to_toon,
     toon_to_json,
     system_prompt_to_toon,
     toon_to_system_prompt,
 )
 
 
 def test_json_toon_roundtrip_simple():
     data = {"a": 1, "b": [1, 2, 3], "c": {"nested": True}}
     toon_text = json_to_toon(data)
     result = toon_to_json(toon_text)
     assert result == data
 
 
 def test_json_toon_roundtrip_with_strings():
     data = {
         "user": {"id": 42, "name": "Alice"},
         "messages": [
             {"role": "system", "content": "You are a helpful assistant."},
             {"role": "user", "content": "Hello!"},
         ],
     }
     toon_text = json_to_toon(data)
     result = toon_to_json(toon_text)
     assert result == data
 
 
 def test_system_prompt_roundtrip():
     prompt = textwrap.dedent(
         """
         You are a careful assistant.
         - Respond concisely.
         - Use Python examples when relevant.
         """
     ).strip()
 
     toon_prompt = system_prompt_to_toon(prompt)
     recovered = toon_to_system_prompt(toon_prompt)
     assert recovered == prompt
 

