"""
update_knowledge.py
====================
功能：將 update/ 目錄中的 .md 檔案，透過 Dify Dataset API
      自動更新對應的知識庫文件，成功後移至 uploaded/ 目錄。

使用方式：
    python update_knowledge.py

前置條件：
    1. 在同目錄建立 .env，填入 DIFY_API_KEY / DIFY_BASE_URL / DATASET_ID
    2. 將待更新的 .md 檔案放入 update/ 目錄（檔名須與知識庫文件名稱相同）
"""

import sys
import io
import os
import shutil
from datetime import datetime
from pathlib import Path

# Windows UTF-8 輸出修正
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

import requests
from dotenv import load_dotenv

# ─────────────────────────────────────────────
# 環境設定
# ─────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
UPDATE_DIR = BASE_DIR / "update"
UPLOADED_DIR = BASE_DIR / "uploaded"

load_dotenv(BASE_DIR / ".env")
API_KEY    = os.getenv("DIFY_API_KEY", "")
BASE_URL   = os.getenv("DIFY_BASE_URL", "http://localhost:8080").rstrip("/")
DATASET_ID = os.getenv("DATASET_ID", "")

HEADERS = {"Authorization": f"Bearer {API_KEY}"}


# ─────────────────────────────────────────────
# 輔助函式
# ─────────────────────────────────────────────
def fetch_all_documents() -> list[dict]:
    """取得知識庫中所有文件清單（支援分頁）"""
    docs = []
    page = 1
    while True:
        url = f"{BASE_URL}/v1/datasets/{DATASET_ID}/documents"
        resp = requests.get(url, headers=HEADERS, params={"page": page, "limit": 100}, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        items = data.get("data", [])
        docs.extend(items)
        if not data.get("has_more", False):
            break
        page += 1
    return docs


def find_document_id(docs: list[dict], filename: str) -> str | None:
    """依檔名在文件清單中尋找 document_id"""
    for doc in docs:
        if doc.get("name") == filename:
            return doc.get("id")
    return None


def safe_move(src: Path, dest_dir: Path) -> None:
    """將檔案移到目標目錄；若已存在則加上 _YYYYMMDD_HHMMSS 後綴"""
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / src.name
    if dest.exists():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        stem = src.stem
        suffix = src.suffix
        dest = dest_dir / f"{stem}_{timestamp}{suffix}"
    shutil.move(str(src), str(dest))
    print(f"  -> 已移至：{dest.name}")


def update_document(document_id: str, file_path: Path) -> bool:
    """呼叫 Dify update_by_file API 更新文件"""
    url = f"{BASE_URL}/v1/datasets/{DATASET_ID}/documents/{document_id}/update_by_file"
    data_payload = (
        '{"indexing_technique":"high_quality",'
        '"process_rule":{"mode":"automatic"}}'
    )
    with open(file_path, "rb") as f:
        files = {
            "file": (file_path.name, f, "text/markdown"),
        }
        form_data = {
            "data": (None, data_payload, "text/plain"),
        }
        # requests multipart：data 和 file 合併傳送
        resp = requests.post(
            url,
            headers=HEADERS,
            files={**form_data, **files},
            timeout=60,
        )
    if resp.status_code == 200:
        return True
    else:
        print(f"  [ERROR] HTTP {resp.status_code}：{resp.text}")
        return False


# ─────────────────────────────────────────────
# 主程式
# ─────────────────────────────────────────────
def main():
    print("=" * 55)
    print(" Dify 知識庫文件更新工具")
    print("=" * 55)

    # 基本驗證
    if not API_KEY:
        print("[ERROR] 請在 .env 設定 DIFY_API_KEY")
        sys.exit(1)
    if not DATASET_ID:
        print("[ERROR] 請在 .env 設定 DATASET_ID")
        sys.exit(1)

    # 取得待上傳檔案清單
    md_files = list(UPDATE_DIR.glob("*.md"))
    if not md_files:
        print(f"[INFO] update/ 目錄中沒有 .md 檔案，結束。")
        return

    print(f"\n[INFO] 找到 {len(md_files)} 個待更新檔案，正在查詢知識庫文件清單...")

    # 取得遠端文件清單
    try:
        docs = fetch_all_documents()
    except requests.RequestException as e:
        print(f"[ERROR] 無法取得文件清單：{e}")
        sys.exit(1)

    print(f"[INFO] 遠端共有 {len(docs)} 份文件\n")

    # 逐一處理
    success_count = 0
    skip_count = 0

    for file_path in md_files:
        filename = file_path.name
        print(f"[處理] {filename}")

        doc_id = find_document_id(docs, filename)
        if not doc_id:
            print(f"  [SKIP] 知識庫中找不到名稱為「{filename}」的文件，跳過。")
            skip_count += 1
            continue

        print(f"  Document ID：{doc_id}")
        ok = update_document(doc_id, file_path)
        if ok:
            print(f"  [OK] 更新成功！")
            safe_move(file_path, UPLOADED_DIR)
            success_count += 1
        else:
            print(f"  [FAIL] 更新失敗，檔案保留在 update/ 目錄。")

    # 結果摘要
    print("\n" + "=" * 55)
    print(f" 完成！成功：{success_count}，跳過：{skip_count}，"
          f"失敗：{len(md_files) - success_count - skip_count}")
    print("=" * 55)


if __name__ == "__main__":
    main()
