#!/usr/bin/env python3
"""
Scan LineFlexMessage directory, extract Flex Message contents,
and insert/update into MySQL line_flex.flex_message_templates.

Maps filename to id, extracts contents, uses filename as description.
"""
import json
import pathlib
import sys
from typing import Optional

import pymysql

# Connect to DB
conn = pymysql.connect(
    host="127.0.0.1",
    port=13366,
    user="flex_api",
    password="flex_api_pwd_change_me",
    database="line_flex",
    charset="utf8mb4",
    autocommit=True,
)

root = pathlib.Path(__file__).resolve().parents[3] / "Dify" / "LineFlexMessage"
print(f"Scanning {root}...")

cursor = conn.cursor()

# Scan all .json files
for i, json_file in enumerate(sorted(root.glob("*.json")), 1):
    print(f"\n[{i}] {json_file.name}")

    text = json_file.read_text(encoding="utf-8")
    # Try to parse; if it fails, attempt to salvage by finding last valid }
    try:
        raw = json.loads(text)
    except json.JSONDecodeError:
        print(f"  [!] JSON parse error, attempting recovery...")
        for end_idx in range(len(text) - 1, -1, -1):
            if text[end_idx] == "}":
                try:
                    raw = json.loads(text[: end_idx + 1])
                    print(f"  [OK] Recovered from position {end_idx}")
                    break
                except json.JSONDecodeError:
                    pass
        else:
            print(f"  [SKIP] Could not recover, skipping")
            continue

    # Extract filename as id (sans .json)
    flex_id = json_file.stem

    # Extract description from filename (clean up underscores/dashes)
    description = json_file.stem.replace("_", " ").replace("-", " ")

    # Extract contents based on structure
    contents: Optional[dict] = None

    if isinstance(raw, dict):
        # Case 1: Direct Flex Message with nested "contents"
        if "contents" in raw:
            contents = raw["contents"]
            # If altText exists, use it for description
            if "altText" in raw and raw["altText"]:
                description = raw["altText"]
        # Case 2: Raw contents object (bubble/carousel/etc)
        elif raw.get("type") in ("bubble", "carousel"):
            contents = raw
        else:
            print(f"  [!] Skipping: unrecognized structure")
            continue

    elif isinstance(raw, list):
        # Case 3: Array of Flex Messages, extract first one
        if raw and isinstance(raw[0], dict):
            first = raw[0]
            if "contents" in first:
                contents = first["contents"]
                if "altText" in first and first["altText"]:
                    description = first["altText"]
            else:
                print(f"  [!] Skipping: array item has no contents")
                continue
        else:
            print(f"  [!] Skipping: empty array or malformed")
            continue
    else:
        print(f"  [!] Skipping: root is neither dict nor list")
        continue

    if not contents:
        print(f"  [!] Skipping: could not extract contents")
        continue

    contents_json = json.dumps(contents, ensure_ascii=False)
    print(f"  id={flex_id}")
    print(f"  desc={description[:60]}{'…' if len(description) > 60 else ''}")
    print(f"  contents size: {len(contents_json)} bytes")

    # Upsert
    try:
        cursor.execute(
            """
            INSERT INTO flex_message_templates (id, description, contents)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE
              description = VALUES(description),
              contents = VALUES(contents)
            """,
            (flex_id, description, contents_json),
        )
        print(f"  [OK] Inserted/updated")
    except Exception as e:
        print(f"  [ERR] {e}")

cursor.close()
conn.close()

print("\nDone!")
