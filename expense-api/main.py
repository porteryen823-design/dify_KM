import sys
import io

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime, timezone, timedelta
import sqlite3
import os

# ------------------------------
# App setup
# ------------------------------
app = FastAPI(title="Expense Tracker API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = os.environ.get("DB_PATH", "/app/data/expenses.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
TW_TZ = timezone(timedelta(hours=8))

# ------------------------------
# Database
# ------------------------------
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            amount    REAL    NOT NULL,
            store     TEXT    NOT NULL,
            item      TEXT    NOT NULL,
            datetime  TEXT    NOT NULL,
            memo      TEXT
        )
    """)
    conn.commit()
    conn.close()


init_db()

# ------------------------------
# Schemas
# ------------------------------
class ExpenseCreate(BaseModel):
    amount: float
    store: str
    item: str
    datetime: Optional[str] = None  # 新增日期欄位
    memo: Optional[str] = None

    @field_validator("amount")
    @classmethod
    def amount_must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Amount must be greater than 0")
        return v

    @field_validator("store", "item")
    @classmethod
    def must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Field must not be empty")
        return v.strip()


class ExpenseOut(BaseModel):
    id: int
    amount: float
    store: str
    item: str
    datetime: str
    memo: Optional[str]


# ------------------------------
# Routes
# ------------------------------
@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/expenses", response_model=ExpenseOut, status_code=201)
def create_expense(payload: ExpenseCreate):
    # 修改：不再自動補全現在時間，以便觀察 Dify 是否有傳值
    if not payload.datetime or payload.datetime.strip() == "":
        final_dt = "DATE_MISSING_FROM_DIFY"
    else:
        final_dt = payload.datetime
    
    conn = get_db()
    try:
        cursor = conn.execute(
            "INSERT INTO expenses (amount, store, item, datetime, memo) VALUES (?, ?, ?, ?, ?)",
            (payload.amount, payload.store, payload.item, final_dt, payload.memo),
        )
        conn.commit()
        row = conn.execute(
            "SELECT * FROM expenses WHERE id = ?", (cursor.lastrowid,)
        ).fetchone()
        return dict(row)
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


@app.get("/expenses", response_model=list[ExpenseOut])
def list_expenses(limit: int = 50):
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM expenses ORDER BY id DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]
