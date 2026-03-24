"""
tsc_md_clean.py
────────────────────────────────────────────────────────────────────
批次清理 Doc_tsc/*.md 中「孤立 ## 章節標題行」問題。

問題說明：
  在 Q/A 格式文件中，## 章節標題（如 ## 繞路與恢復機制）
  位於 --- 分隔線和 ### Q: 問答對之間，被 Dify 單獨切成
  僅 7 個字元的無意義段落（如截圖中的 Chunk-45）。

修正策略：
  移除「僅作為分類用途、後面緊跟 ### Q: 的 ## 標題行」。
  保留所有 ### Q: / **A:** 問答對（這是核心內容，絕對不刪）。
  文章格式文件（無 Q/A 標記）則略過不處理。

整理人：Antigravity AI & Porter
────────────────────────────────────────────────────────────────────
"""

import sys
import io
import re
import shutil
from pathlib import Path
from datetime import datetime

# ── Windows 環境 Unicode 輸出修正 (Rules 8-1) ──────────────────────
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# ── 設定區 ─────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
DOC_DIR    = SCRIPT_DIR                   # 清理腳本所在資料夾
BACKUP_DIR = SCRIPT_DIR / "_backup_md"   # 修改前先備份至此
DRY_RUN    = False                        # True=僅預覽, False=實際寫入

# ── 判斷文件格式 ────────────────────────────────────────────────────
def is_qa_format(text: str) -> bool:
    """判斷文件是否為 Q/A 格式（含 ### Q: 或 ### Q：標記）。"""
    return bool(re.search(r"^#{1,3}\s+Q[：:]", text, re.MULTILINE))

# ── 核心清理邏輯 ────────────────────────────────────────────────────
def clean_orphan_section_headers(text: str) -> tuple[str, list[str]]:
    """
    移除「孤立的 ## 章節標題行」。

    定義「孤立 ## 標題」（必須同時滿足以下條件）：
      1. 以 ## 開頭（非 ### 或更深），即一級或二級主題標題。
      2. 該標題行之後，跳過空行，緊接著是 ### Q: 開頭的問答對。
      3. 這類標題只做分類用途，對 RAG 無額外資訊貢獻。

    【注意】絕對不移除 ### Q: / **A:** 行，這些是正式問答內容。

    回傳：(已清理文字, [被移除的標題清單])
    """
    lines   = text.splitlines(keepends=True)
    result  = []
    removed = []
    i       = 0

    while i < len(lines):
        line = lines[i]

        # 只偵測 ## 開頭（恰好兩個 #），不含 ### 或更深
        if re.match(r"^##\s+\S", line) and not re.match(r"^###", line):
            # 往後掃描，跳過空行，看下一個非空行是否為 ### Q:
            j = i + 1
            while j < len(lines) and lines[j].strip() == "":
                j += 1

            next_non_blank = lines[j].strip() if j < len(lines) else ""

            # 下一個有內容的行是 ### Q: 開頭 → 判定為孤立標題
            is_next_qa_block = bool(re.match(r"^###\s+Q[：:]", next_non_blank))

            if is_next_qa_block:
                # 移除此孤立標題行，並嘗試移除前面的 --- 分隔線
                title_text = line.rstrip()
                removed.append(title_text)
                print(f"  ✂️  移除孤立標題: {title_text}")

                # 同時移除標題前緊靠的 --- 行（及其前的空白行）
                while result and result[-1].strip() == "":
                    result.pop()
                if result and result[-1].strip() == "---":
                    result.pop()
                    # 清掉 --- 前可能殘留的空行
                    while result and result[-1].strip() == "":
                        result.pop()
                    # 在前一段 Q/A 結束後保留分隔線
                    result.append("\n---\n")

                i += 1  # 跳過此標題行
                continue

        result.append(line)
        i += 1

    cleaned = "".join(result)
    # 清理產生的連續 --- 分隔線
    cleaned = re.sub(r"(\n---\n){2,}", "\n---\n", cleaned)
    # 清理多餘的連續空行（超過 2 行）
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)

    return cleaned, removed

# ── 主程序 ──────────────────────────────────────────────────────────
def main():
    md_files = sorted(DOC_DIR.glob("*.md"))

    if not md_files:
        print("❌ 找不到任何 .md 檔案，請確認執行目錄是否正確。")
        return

    print("=" * 62)
    print(" TSC Markdown 孤立標題清理工具 v2")
    print(f" 檔案路徑：{DOC_DIR}")
    print(f" 模式：{'[DRY RUN 預覽模式]' if DRY_RUN else '[實際寫入模式]'}")
    print("=" * 62)

    if not DRY_RUN:
        BACKUP_DIR.mkdir(exist_ok=True)

    total_removed   = 0
    files_modified  = 0
    files_skipped   = 0
    files_article   = 0

    for md_file in md_files:
        print(f"\n📄 處理: {md_file.name}")
        text = md_file.read_text(encoding="utf-8", errors="replace")

        # ① 文章格式 → 跳過
        if not is_qa_format(text):
            print(f"   ℹ️  文章格式（無 Q/A 標記），跳過修改。")
            files_article += 1
            continue

        # ② 執行清理
        cleaned, removed_list = clean_orphan_section_headers(text)

        if not removed_list:
            print(f"   ✅ 無孤立 ## 標題，無需修改。")
            files_skipped += 1
            continue

        print(f"   📊 移除孤立 ## 標題：{len(removed_list)} 個")

        if not DRY_RUN:
            # 備份
            ts          = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = BACKUP_DIR / f"{md_file.stem}_{ts}.md"
            shutil.copy2(md_file, backup_path)
            print(f"   💾 備份至：{backup_path.name}")

            # 寫回
            md_file.write_text(cleaned, encoding="utf-8")
            print(f"   ✅ 已覆寫儲存：{md_file.name}")
        else:
            print(f"   [DRY RUN] 實際寫入已略過。")

        total_removed  += len(removed_list)
        files_modified += 1

    print("\n" + "=" * 62)
    print(f"🎯 清理完成摘要")
    print(f"   - 修改檔案數     : {files_modified}")
    print(f"   - 跳過無變更     : {files_skipped}")
    print(f"   - 文章格式跳過   : {files_article}")
    print(f"   - 移除孤立 ## 標題: {total_removed} 個")
    if not DRY_RUN and total_removed > 0:
        print(f"   - 備份目錄       : {BACKUP_DIR}")
    print("=" * 62)

    if DRY_RUN:
        print("\n⚠️  目前為 DRY RUN 預覽模式，設定 DRY_RUN = False 後重新執行以實際修改。")

if __name__ == "__main__":
    main()
