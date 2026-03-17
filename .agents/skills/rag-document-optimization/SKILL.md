---
name: rag-document-optimization
description: 處理、優化並結構化原始文檔，使其適合 Dify RAG 檢索。適用於處理含有行號、結構混亂、或標點不統一的 txt/md/pdf 轉檔內容。
---

# RAG Document Optimization Skill

當需要準備或修復 Dify 知識庫的原始文件時，請遵循此 Skill 進行處理。

## 1. 處理原則 (Core Principles)

### A. 清理噪聲 (Noise Reduction)
- **移除行號**：原始文件常帶有 IDE 或編輯器產生的行號（如 `1:`, `2:`），必須使用正則表達式 `^\d+:\s*` 移除。
- **統一標點**：中文內容一律使用全形標點（`，` `。` `？` `：` `！`），並移除多餘的半形空白。
- **編碼格式**：強制使用 **UTF-8** 編碼，避免 Windows 環境常見的 ANSI 亂碼。

### B. 結構化升級 (Structural Enhancement)
- **Front-Matter**：檔案開頭必須包含 YAML 區塊：
  ```yaml
  ---
  title: [文件標題]
  description: [簡短描述文件內容，幫助 RAG 理解背景]
  tags: [標籤1, 標籤2]
  ---
  ```
- **語意分塊 (Semantic Chunking)**：
  - 使用 `##` 或 `###` 標定主題。
  - 不同主題間使用 `---` 分隔，這能提示 Dify 在進行自動切片時保持語意區塊的完整性。

## 2. 操作工作流 (Optimization Workflow)

1. **初步清理**：執行正則替換，將純文字轉為乾淨的 Markdown。
2. **主題識別**：識別內容中的 Q&A、步驟說明、或是參數定義，並給予對應的標題。
3. **優化列表**：將密集的描述文字改寫為清爽的列表（無序 `-` 或有序 `1.`）。
4. **驗證與存檔**：確認目標檔案路徑（如 `Doc_tsc/xxx.md`）並執行寫入。

## 3. RAG 最佳實踐指令 (Prompts)

- **優化指令**：「請幫我優化 @[file.txt]，移除行號並轉為具備 Front-Matter 的 Markdown 格式，適合 Dify RAG 使用。」
- **FAQ 轉換**：「請將 @[file.md] 的內容轉換為 20 個精準的 FAQ，存入 tsc_FAQ.md，嚴禁幻覺。」

## 4. 相關工具與 Workflow
- 搭配 `/rag-optimize` 工作流進行自動化處理。
- 搭配 `/gen-faq` 工作流進行後續問答對生成。
