import json
import os
from typing import Optional

import pymysql
import pymysql.cursors
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="LINE Flex Template API")


def get_conn() -> pymysql.connections.Connection:
    return pymysql.connect(
        host=os.getenv("MYSQL_HOST", "db_mysql"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.getenv("MYSQL_USER", "flex_api"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        database=os.getenv("MYSQL_DATABASE", "line_flex"),
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )


class FlexIn(BaseModel):
    id: str
    description: Optional[str] = None
    contents: dict


class FlexOut(BaseModel):
    id: str
    description: Optional[str] = None
    contents: dict


class FlexSummary(BaseModel):
    id: str
    description: Optional[str] = None


class LineChannelOut(BaseModel):
    name: str
    channel_access_token: str
    default_user_id: str
    description: Optional[str] = None


def _normalize_contents(raw) -> dict:
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, (bytes, bytearray)):
        raw = raw.decode("utf-8")
    return json.loads(raw)


@app.get("/")
def health():
    return {"status": "flex_api running"}


@app.get("/flex", response_model=list[FlexSummary])
def list_flex():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT id, description FROM flex_message_templates ORDER BY id")
        return cur.fetchall()


@app.get("/flex/{flex_id}", response_model=FlexOut)
def get_flex(flex_id: str):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            "SELECT id, description, contents FROM flex_message_templates WHERE id=%s",
            (flex_id,),
        )
        row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail=f"flex_id '{flex_id}' not found")

    # 正規化 contents
    raw_contents = _normalize_contents(row["contents"])

    # 若 contents 是完整 Flex Message（type=flex），提取其 contents 欄位
    # 這樣 assemble 節點可以直接用它來組裝
    if isinstance(raw_contents, dict) and raw_contents.get("type") == "flex":
        row["contents"] = raw_contents.get("contents", raw_contents)
    else:
        row["contents"] = raw_contents

    return FlexOut(**row)


@app.post("/flex", response_model=FlexOut)
def upsert_flex(payload: FlexIn):
    contents_json = json.dumps(payload.contents, ensure_ascii=False)
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO flex_message_templates (id, description, contents)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE
              description = VALUES(description),
              contents    = VALUES(contents)
            """,
            (payload.id, payload.description, contents_json),
        )
    return FlexOut(id=payload.id, description=payload.description, contents=payload.contents)


@app.delete("/flex/{flex_id}")
def delete_flex(flex_id: str):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("DELETE FROM flex_message_templates WHERE id=%s", (flex_id,))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"flex_id '{flex_id}' not found")
    return {"deleted": flex_id}


@app.get("/line/channel/{name}", response_model=LineChannelOut)
def get_line_channel(name: str):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            "SELECT name, channel_access_token, default_user_id, description "
            "FROM line_channels WHERE name=%s",
            (name,),
        )
        row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail=f"line channel '{name}' not found")
    return row
