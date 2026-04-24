"""One-off sanity check: parse init.sql, unescape MySQL string literal,
validate that the seed JSON is proper JSON.
"""
import json
import pathlib
import re

sql = pathlib.Path(__file__).with_name("init.sql").read_text(encoding="utf-8")

m = re.search(r"'all_elements_demo',\s*'[^']*',\s*'(.*)'\)\s*ON DUPLICATE", sql, re.DOTALL)
assert m, "seed JSON literal not located"
raw = m.group(1)

# Reverse sql_escape: '' -> '  ; \\ -> \
unescaped = raw.replace("''", "'").replace("\\\\", "\\")

obj = json.loads(unescaped)
print(f"seed JSON length: {len(unescaped)}")
print(f"seed root keys : {list(obj.keys())}")
print(f"seed type      : {obj['type']}")
print(f"seed size      : {obj['size']}")
print(f"body contents  : {len(obj['body']['contents'])} items")
