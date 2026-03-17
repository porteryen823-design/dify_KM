from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import os

app = FastAPI(title="AUTOMAT Prompt Library API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "prompt_library.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/prompts", summary="取得所有 Prompt 或依分類篩選")
def get_prompts(category: str = Query(None, description="依分類篩選 (e.g., HR, Marketing, IT, Ops, Strategy, Sales)")):
    conn = get_db()
    cursor = conn.cursor()
    if category:
        cursor.execute("SELECT * FROM PromptLibrary WHERE category = ?", (category,))
    else:
        cursor.execute("SELECT * FROM PromptLibrary")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.get("/prompts/search", summary="全文搜尋 Prompt")
def search_prompts(q: str = Query(..., description="搜尋關鍵字 (支援 name, description, tags 等欄位)")):
    if not q.strip():
        return []
        
    conn = get_db()
    cursor = conn.cursor()
    query = f"%{q}%"
    cursor.execute('''
        SELECT * FROM PromptLibrary 
        WHERE name LIKE ? OR description LIKE ? OR tags LIKE ? OR category LIKE ?
        ORDER BY id ASC
    ''', (query, query, query, query))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.get("/prompts/{prompt_id}", summary="取得單一 Prompt 詳細資訊")
def get_prompt_by_id(prompt_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PromptLibrary WHERE id = ?", (prompt_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    raise HTTPException(status_code=404, detail="Prompt not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
