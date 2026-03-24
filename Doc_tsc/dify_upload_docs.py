"""
dify_upload_docs.py
────────────────────────────────────────────────────────────────────
將本地 .md 文件更新至 Dify 知識庫（datasets）。

流程：
  1. 呼叫 GET /v1/datasets/{dataset_id}/documents 查詢所有文件清單
  2. 依照本地文件名稱比對 Dify 中的 document.name
  3. 找到對應文件後，呼叫 POST .../update-by-text 更新內容
  4. 若找不到對應文件，則改呼叫 POST .../document/create-by-text 新增

整理人：Antigravity AI & Porter
────────────────────────────────────────────────────────────────────
"""

import sys
import io
import os
import requests
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# ── Windows 環境 Unicode 輸出修正 (Rules 8-1) ──────────────────────
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# ── 載入 .env 金鑰設定 ─────────────────────────────────────────────
env_path = Path(__file__).parent.parent / "dify" / ".agents" / "skills" / "dify-api-testing" / "examples" / ".env"
load_dotenv(dotenv_path=env_path)

API_KEY    = os.getenv("DIFY_KNOWLEDGE_API_KEY", "")
BASE_URL   = os.getenv("DIFY_API_BASE", "http://localhost:8080/v1")
DATASET_ID = os.getenv("DIFY_DATASET_ID", "3296d37b-804b-4e58-86d3-e20121eda16e")

# ── 目標文件（本地路徑）────────────────────────────────────────────
SCRIPT_DIR   = Path(__file__).parent
TARGET_FILES = [
    SCRIPT_DIR / "tsc_张俊贤.md",
    SCRIPT_DIR / "tsc交管问答_kimroy 金正阳.md",
]

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}


import re

# ── 工具函式 ───────────────────────────────────────────────────────
def list_all_documents() -> dict[str, str]:
    """
    查詢知識庫內所有文件，回傳 {document_name: document_id} 的字典。
    支援分頁（page_size 最大 100）。
    """
    doc_map: dict[str, str] = {}
    page = 1
    while True:
        url    = f"{BASE_URL}/datasets/{DATASET_ID}/documents"
        params = {"page": page, "limit": 100}
        resp   = requests.get(url, headers=HEADERS, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        for doc in data.get("data", []):
            doc_map[doc["name"]] = doc["id"]

        if not data.get("has_more", False):
            break
        page += 1

    return doc_map


def update_document(document_id: str, doc_name: str, text: str) -> dict:
    """
    呼叫 update-by-text 更新現有文件內容。
    """
    url     = f"{BASE_URL}/datasets/{DATASET_ID}/documents/{document_id}/update-by-text"
    payload = {
        "name": doc_name,
        "text": text,
        "process_rule": {"mode": "automatic"},
    }
    resp = requests.post(url, headers=HEADERS, json=payload, timeout=60)
    resp.raise_for_status()
    return resp.json()


def create_document(doc_name: str, text: str) -> dict:
    """
    若知識庫中找不到對應文件，則新增文件。
    """
    url     = f"{BASE_URL}/datasets/{DATASET_ID}/document/create-by-text"
    payload = {
        "name": doc_name,
        "text": text,
        "process_rule": {"mode": "automatic"},
        "doc_form": "text_model",
        "doc_language": "Chinese",
    }
    resp = requests.post(url, headers=HEADERS, json=payload, timeout=60)
    resp.raise_for_status()
    return resp.json()


# ── 主程序 ──────────────────────────────────────────────────────────
def main():
    print("=" * 62)
    print(" Dify 知識庫文件批次更新工具")
    print(f" 目標知識庫 ID: {DATASET_ID}")
    print(f" Base URL     : {BASE_URL}")
    print("=" * 62)

    # 前置檢查
    if not API_KEY or API_KEY == "your_dataset_api_key_here":
        print("❌ 錯誤：請先在 .env 中設定正確的 DIFY_KNOWLEDGE_API_KEY (dataset-xxx)")
        return

    for f in TARGET_FILES:
        if not f.exists():
            print(f"❌ 找不到本地文件：{f}")
            return

    # Step 1：取得知識庫中所有文件清單
    print("\n📋 Step 1：查詢知識庫文件清單...")
    try:
        doc_map = list_all_documents()
        print(f"   共找到 {len(doc_map)} 個文件，已建立名稱索引。")
    except requests.exceptions.RequestException as e:
        print(f"❌ 無法查詢文件清單: {e}")
        if hasattr(e, "response") and e.response is not None:
            print(f"   伺服器回應: {e.response.text}")
        return

    # Step 2：逐一更新/新增文件
    print("\n🚀 Step 2：開始更新文件...\n")
    for local_file in TARGET_FILES:
        doc_name = local_file.name                             # 例如 tsc_张俊贤.md
        text     = local_file.read_text(encoding="utf-8")
        
        # [預處理] 移除 Markdown 中的 --- 分隔線，避免成為無效的檢索字元
        # 使用正則表達式過濾掉僅包含 --- (3個以上橫切線) 的整行
        text = re.sub(r'(?m)^-{3,}\s*$', '', text)

        ts       = datetime.now().strftime("%H:%M:%S")

        print(f"[{ts}] 📄 處理：{doc_name}")
        print(f"         本地大小：{len(text):,} 字元 (已移除 --- 雜訊)")

        try:
            if doc_name in doc_map:
                # ── 更新 ──────────────────────────────────────────
                document_id = doc_map[doc_name]
                print(f"         Dify Doc ID：{document_id}")
                print(f"         操作：UPDATE（update-by-text）")
                result = update_document(document_id, doc_name, text)
                batch  = result.get("batch", "N/A")
                new_id = result.get("document", {}).get("id", "N/A")
                print(f"         ✅ 更新成功！Batch: {batch}  New Doc ID: {new_id}")
            else:
                # ── 新增 ──────────────────────────────────────────
                print(f"         ⚠️  知識庫中找不到此文件，將執行 CREATE（create-by-text）")
                result = create_document(doc_name, text)
                batch  = result.get("batch", "N/A")
                new_id = result.get("document", {}).get("id", "N/A")
                print(f"         ✅ 新增成功！Batch: {batch}  Doc ID: {new_id}")

        except requests.exceptions.RequestException as e:
            print(f"         ❌ 失敗: {e}")
            if hasattr(e, "response") and e.response is not None:
                print(f"            伺服器回應: {e.response.text}")

        print()

    print("=" * 62)
    print("🎯 批次更新完成，請至 Dify 知識庫確認文件狀態（索引中→完成）")
    print("=" * 62)


if __name__ == "__main__":
    main()
