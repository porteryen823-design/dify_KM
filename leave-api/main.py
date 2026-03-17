import sqlite3
import os
from datetime import datetime, timezone, timedelta
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Leave Request API")

DB_PATH = "data/leaves.db"
os.makedirs("data", exist_ok=True)

# 台灣時區設定
TW_TZ = timezone(timedelta(hours=8))

# 資料庫初始化
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS leaves (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                duration REAL NOT NULL,
                date_start TEXT NOT NULL,
                date_end TEXT NOT NULL,
                reason TEXT,
                created_at TEXT NOT NULL
            )
        """)

init_db()

# Pydantic 模型
class LeaveCreate(BaseModel):
    category: str
    duration: float
    date_start: str
    date_end: str
    reason: Optional[str] = None

class LeaveOut(LeaveCreate):
    id: int
    created_at: str

@app.get("/")
def read_root():
    return {"status": "Leave API is running"}

@app.post("/leaves", response_model=LeaveOut, status_code=201)
def create_leave(payload: LeaveCreate):
    now_tw = datetime.now(TW_TZ).isoformat(timespec="seconds")
    
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            "INSERT INTO leaves (category, duration, date_start, date_end, reason, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (payload.category, payload.duration, payload.date_start, payload.date_end, payload.reason, now_tw),
        )
        leave_id = cursor.lastrowid
        conn.commit()
        
        return {
            "id": leave_id,
            "created_at": now_tw,
            **payload.model_dump()
        }

@app.get("/leaves", response_model=List[LeaveOut])
def list_leaves():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute("SELECT * FROM leaves ORDER BY id DESC")
        return [dict(row) for row in cursor.fetchall()]
