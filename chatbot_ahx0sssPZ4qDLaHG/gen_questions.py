import pandas as pd
import os

# 建立測試問題資料
data = [
    {"NO": 1, "類型": "術語別名", "問題": "交管怎麼設定？", "預期重點": "應辨識「交管」= 交通管制 = Traffic Control"},
    {"NO": 2, "類型": "英文參數", "問題": "EnableStraightRoadFirst 是什麼？", "預期重點": "應定位到 4.2.2.7.3"},
    {"NO": 3, "類型": "操作步驟", "問題": "怎麼新增一台自走車？", "預期重點": "應回答 4.12.2 新增自走車流程"},
    {"NO": 4, "類型": "概念理解", "問題": "什麼是路權？", "預期重點": "應涵蓋 5.1.1.3 路權說明"},
    {"NO": 5, "類型": "交叉引用", "問題": "Group 設定在哪裡？要注意什麼？", "預期重點": "應涵蓋地圖編輯站點屬性 + 5.3 Group 設計原則"},
    {"NO": 6, "類型": "故障排除", "問題": "車子一直要不到路權怎麼辦？", "預期重點": "應涵蓋 5.1.1.3 + 4.2.2.7 相關設定"},
    {"NO": 7, "類型": "邊界測試", "問題": "TSC 可以控制幾台車？", "預期重點": "若手冊無此資訊應誠實回答"}
]

df = pd.DataFrame(data)

# 儲存到 Excel
output_path = r"c:\VSCode_Proj\Dify\chatbot_ahx0sssPZ4qDLaHG\chatbot_ahx0sssPZ4qDLaHG_questions.xlsx"
df.to_excel(output_path, index=False)

print(f"成功產生題庫檔案: {output_path}")
