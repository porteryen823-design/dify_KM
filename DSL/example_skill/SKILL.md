---
name: Text Analyzer Skill
description: 分析上傳的文字檔案，計算字數、行數及高頻詞彙。
---

# Text Analyzer Skill 說明書

此技能可以協助使用者分析純文字檔案 (.txt)。

## 使用流程
1. 讀取使用者提供的檔案內容。
2. 執行 `process.py` 來計算統計數據。
3. 輸出分析結果。

## 執行指令
```bash
python3 process.py [檔案名稱]
```

## 輸出規格
- 總字數
- 總行數
- 前 5 個高頻詞彙
