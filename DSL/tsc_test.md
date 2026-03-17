# TSC Assigner 測試流程說明

### 📌 測試目標
驗證 Dify 1.13.0 中，使用 **Code 節點** 產出的常數值，是否能透過 **Variable Assigner** 成功寫入 `conversation.language` 對話變數中。

### 🔧 節點邏輯描述

1.  **Start 節點**: 流程起點。
2.  **Code 節點 (1.產生字串)**:
    *   **語言**: Python3
    *   **程式碼**:
        ```python
        def main():
            return {"result": "English"}
        ```
    *   **輸出變數**: `result` (String)
3.  **Variable Assigner 節點 (2.變數指派)**:
    *   **寫入目標**: `conversation.language`
    *   **值來源**: 引用自 `1.產生字串(Code)` 的輸出變數 `result`。
4.  **Answer 節點 (3.結果確認)**:
    *   輸出一段文字，確認流程已成功走完。

### 🚀 使用方式
1. 將 `tsc_test.yml` 匯入 Dify。
2. 在預覽視窗隨便輸入任何內容。
3. 觀察流程是否能順利走到最後一個 Answer 節點。

**整理人：** Antigravity AI & Porter
