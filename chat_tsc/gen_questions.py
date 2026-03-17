import pandas as pd
import os

# 建立測試問題資料
data = [
    {"NO": 1, "問題": "什麼是 TSC 交管？"},
    {"NO": 2, "問題": "繞路的前提是什麼？"},
    {"NO": 3, "問題": "如果前車故障不動，堵車能解除嗎？"},
    {"NO": 4, "問題": "兩台車要同時進電梯怎麼辦？"},
    {"NO": 5, "問題": "避讓點的選擇條件有哪些？"},
    {"NO": 6, "問題": "Group 的目的為何？"}
]

df = pd.DataFrame(data)

# 儲存到 Excel
output_path = r"c:\VSCode_Proj\Dify\chat_tsc\chat_tsc_questions.xlsx"
df.to_excel(output_path, index=False)

print(f"成功產生題庫檔案: {output_path}")
