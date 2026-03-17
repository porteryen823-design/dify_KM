---
description: 將原始文檔內容（txt, md, pdf）優化為適合 Dify RAG 的格式
---

# /rag-optimize 執行步驟

1. **讀取源文件**：利用 `view_file` 讀取使用者指定的原始文檔。
2. **清理與預處理**：
   - 移除文件中不必要的行號（如 `1:`, `2:`）。
   - 統一使用 UTF-8 編碼，將中文標點統整為全形。
3. **結構化標註 (Structure)**：
   - 根據文件層級加入 Markdown 標題（`##`, `###`）。
   - 加入 YAML Front-Matter（`title`, `description`, `tags`）。
4. **分段與塊化 (Chunking Optimization)**：
   - 使用 `---` 分隔不相關的語意塊，確保 Dify 切塊時語意完整。
   - 將條列式內容整理為有序或無序列表。
5. **產生目標文件**：
   - 將結果存至使用者指定的目標路徑（如 `xxx.md`）。
6. **回報差異**：描述優化了哪些部分（如格式、標點、結構等）。

---
// turbo-all
// 執行指令範例：
// /rag-optimize @[source.txt] 優化並存入 target.md
