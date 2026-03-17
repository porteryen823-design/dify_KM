import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "prompt_library.db")

def create_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS PromptLibrary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            actor TEXT,
            user_audience TEXT,
            task TEXT,
            output TEXT,
            method TEXT,
            assumption TEXT,
            tone TEXT,
            example TEXT,
            tags TEXT
        )
    ''')
    
    # Clear existing
    cursor.execute('DELETE FROM PromptLibrary')
    
    prompts = [
        # --- HR (5) ---
        {
            "category": "HR", "name": "撰寫職缺說明", "description": "針對特定職位撰寫吸引人的職缺說明",
            "actor": "資深人力資源招募經理", "user_audience": "具有 3–5 年經驗的軟體工程師",
            "task": "撰寫一份 C# Backend Engineer 的職缺說明",
            "output": "1. 職位名稱 2. 工作內容 3. 必備技能 4. 加分條件 5. 公司福利",
            "method": "參考科技公司常見職缺格式", "assumption": "公司是一間 AI 軟體公司", "tone": "專業、吸引人才",
            "tags": "HR, 招募, 職缺, 工程師"
        },
        {
            "category": "HR", "name": "建立員工績效評估模板", "description": "協助主管進行客觀的績效考評",
            "actor": "企業 HRBP", "user_audience": "部門主管",
            "task": "建立員工績效評估模板",
            "output": "包含：1. KPI 指標 2. 評分標準 3. 評語範例",
            "method": "使用 OKR + KPI 模型", "assumption": "適用於科技公司", "tone": "正式",
            "tags": "HR, 績效, 評估, 模板, KPI"
        },
        {
            "category": "HR", "name": "設計面試問題庫", "description": "為招募專案打造系統化的面試題庫",
            "actor": "資深技術面試官", "user_audience": "面試官與招募團隊",
            "task": "設計 10 個行為與技術面試問題",
            "output": "分兩類：技術能力 5 題、文化契合度 5 題，每題須附預期回答焦點",
            "method": "使用 STAR 面試法", "assumption": "面試對象為資深軟體開發者", "tone": "嚴謹、具探究性",
            "tags": "HR, 面試, 題庫, 招募, STAR"
        },
        {
            "category": "HR", "name": "新人到職培訓計畫", "description": "規劃結構化的 30 天新人入職流程",
            "actor": "培訓與發展部經理", "user_audience": "新進員工與直屬主管",
            "task": "撰寫一份 30 天新人到職培訓計畫",
            "output": "按週拆分的訓練里程碑 (Week 1 到 Week 4) 及對應檢核點",
            "method": "70-20-10 學習法則", "assumption": "新人為遠端工作模式", "tone": "歡迎、結構化且具激勵性",
            "tags": "HR, 培訓, 到職, Onboarding, 計畫"
        },
        {
            "category": "HR", "name": "員工關懷信件", "description": "處理組織變動期的內部溝通",
            "actor": "人資長 (CHRO)", "user_audience": "全體員工",
            "task": "撰寫季度組織變動說明的員工關懷信件",
            "output": "分三段：政策變動目的、對員工的具體影響、常見問答 (FAQ) 及發問管道",
            "method": "透明且建立安全感的溝通策略", "assumption": "公司近期剛完成部門整併", "tone": "同理心、透明、安定人心",
            "tags": "HR, 溝通, 關懷, 信件, 內部公告"
        },
        
        # --- Marketing (5) ---
        {
            "category": "Marketing", "name": "制定行銷策略", "description": "為新產品推出規劃整體行銷戰略",
            "actor": "資深行銷策略顧問", "user_audience": "SaaS 公司行銷主管",
            "task": "制定 AI 排程系統的行銷策略",
            "output": "1. 目標市場 2. 客戶 Persona 3. 行銷管道 4. 推廣活動",
            "method": "使用 STP + 4P 行銷模型", "assumption": "產品是企業級 APS 排程系統", "tone": "策略導向",
            "tags": "行銷, 策略, B2B, SaaS, APS"
        },
        {
            "category": "Marketing", "name": "規劃 LinkedIn 一週內容", "description": "社群媒體內容經營規劃",
            "actor": "社群媒體行銷專家", "user_audience": "B2B 客戶",
            "task": "規劃 LinkedIn 一週內容",
            "output": "表格：日期 | 主題 | 內容摘要",
            "method": "內容包含：1. 教育型內容 2. 案例分享 3. 產品介紹", "assumption": "公司提供 AI SaaS 服務", "tone": "專業但親切",
            "tags": "行銷, 社群, LinkedIn, 內容規劃"
        },
        {
            "category": "Marketing", "name": "撰寫 Google Ads 文案", "description": "針對搜尋引擎廣告撰寫高轉化文案",
            "actor": "數位廣告文案專家", "user_audience": "企業 IT 經理",
            "task": "撰寫 Google Ads 文案",
            "output": "1. 標題 (3 個) 2. 描述 (2 個)",
            "method": "使用 AIDA 行銷模型", "assumption": "產品是 AI 生產排程系統", "tone": "簡潔、有說服力",
            "tags": "行銷, 廣告, Google Ads, 文案"
        },
        {
            "category": "Marketing", "name": "產品發表新聞稿", "description": "撰寫對外發布的公關新聞稿",
            "actor": "資深公關經理", "user_audience": "科技媒體與潛在投資人",
            "task": "撰寫 V2.0 產品升級新聞稿",
            "output": "1. 吸睛大標題 2. 核心突破點 3. CEO 引言 4. 公司簡介",
            "method": "倒金字塔新聞寫作法", "assumption": "新版本主打效能提升 300%", "tone": "權威、自信",
            "tags": "行銷, 公關, 新聞稿, PR"
        },
        {
            "category": "Marketing", "name": "電子報 (EDM) 撰寫", "description": "針對舊客進行產品回購與活動通知",
            "actor": "Email 行銷操盤手", "user_audience": "已註冊的免費版用戶",
            "task": "撰寫引導升級專業版 (Pro) 的促銷電子報",
            "output": "包含：主旨 (3個版本測試)、問候語、痛點勾勒、限時優惠與 CTA 按鈕設計",
            "method": "FOMO (錯失恐懼症) 行銷手段", "assumption": "目前有七天限時半價活動", "tone": "急迫、誘人",
            "tags": "行銷, EDM, 電子報, 轉換率"
        },

        # --- IT (5) ---
        {
            "category": "IT", "name": "系統架構設計文件", "description": "規劃新的雲端產品系統架構",
            "actor": "資深雲端架構師", "user_audience": "開發團隊與技術主管",
            "task": "撰寫微服務架構設計文件",
            "output": "包含：1. 架構圖文字描述 2. 元件職責 3. 資料流向 4. 容錯機制",
            "method": "C4 Model 架構設計", "assumption": "後端使用 FastAPI，部署於 Kubernetes", "tone": "極度精確、技術導向",
            "tags": "IT, 架構, 雲端, 微服務, FastAPI"
        },
        {
            "category": "IT", "name": "API 規格書撰寫", "description": "制定前後端分離的 API 介接文件",
            "actor": "後端主程式設計師", "user_audience": "前端工程師與 QA 測試員",
            "task": "撰寫使用者登入 API 規格",
            "output": "包含：Method, Endpoint, Request Parameters, Response JSON, Error Codes 等資訊",
            "method": "RESTful API 設計規範", "assumption": "身份驗證採用 JWT Token", "tone": "條理分明、毫不含糊",
            "tags": "IT, API, 開發, 規格書"
        },
        {
            "category": "IT", "name": "Code Review 建議", "description": "針對特定 Pull Request 進行程式碼審查",
            "actor": "資深資安工程師", "user_audience": "初階軟體工程師",
            "task": "提出 3 點 Code Review 修改建議",
            "output": "針對每一點指出：1. 潛在風險 2. 修改範例 3. 教學參考文件",
            "method": "OWASP 安全開發指南", "assumption": "被審查的程式碼有 SQL Injection 風險", "tone": "嚴厲但具建設性",
            "tags": "IT, 程式碼審查, Code Review, 資安"
        },
        {
            "category": "IT", "name": "技術問題排解指南", "description": "建立知識庫中的常見問題除錯 SOP",
            "actor": "SRE 網站可靠性工程師", "user_audience": "第一線技術支援人員 (L1 Support)",
            "task": "撰寫「系統 502 Bad Gateway」的排解指南",
            "output": "三步驟 SOP清單，並列出常用的診斷指令 (Linux Command)",
            "method": "樹狀圖異常診斷法", "assumption": "伺服器環境為 Nginx + Docker", "tone": "清晰、可操作性強",
            "tags": "IT, 維運, Troubleshooting, SOP, SRE"
        },
        {
            "category": "IT", "name": "資料庫 Schema 設計", "description": "為新功能設計關聯式資料庫結構",
            "actor": "資料庫管理員 (DBA)", "user_audience": "全端工程師",
            "task": "設計電商購物車的關聯式資料庫 Schema",
            "output": "輸出 Markdown 表格，包含：資料表名稱、欄位名稱、資料型態、PK/FK 以及約束條件",
            "method": "第三正規化 (3NF)", "assumption": "資料庫為 PostgreSQL", "tone": "邏輯嚴密、結構化",
            "tags": "IT, 資料庫, Schema, 設計, PostgreSQL"
        },

        # --- Sales / Service (5) ---
        {
            "category": "Sales", "name": "建立客戶問題回覆模板", "description": "統一客服團隊對外溝通口徑",
            "actor": "企業客服主管", "user_audience": "客服人員",
            "task": "建立客戶問題回覆模板",
            "output": "包含：1. 問候語 2. 問題確認 3. 解決方案 4. 結尾",
            "method": "使用客戶關係管理最佳實務", "assumption": "客戶使用 SaaS 軟體", "tone": "友善、專業",
            "tags": "客服, SaaS, 模板, CRM"
        },
        {
            "category": "Sales", "name": "陌生開發信 (Cold Email)", "description": "吸引潛在客戶安排初次線上會議",
            "actor": "頂尖 B2B 業務銷售", "user_audience": "中型製造業的廠長",
            "task": "撰寫一封引導預約 Demo 的陌生開發信",
            "output": "包含：吸睛主旨、100字以內的痛點共鳴、解決方案亮點及會議邀請 URL 連結",
            "method": "PAS (Problem-Agitate-Solution) 文案框架", "assumption": "廠內生產排程大多依賴人工 Excel", "tone": "自信、熱情且直指痛點",
            "tags": "業務, 開發信, Cold Email, B2B, 製造業"
        },
        {
            "category": "Sales", "name": "銷售簡報大綱", "description": "準備提案會議 (Pitch) 的簡報架構",
            "actor": "解決方案顧問 (Pre-sales)", "user_audience": "決策高層 (C-level)",
            "task": "建立 15 頁銷售簡報的大綱結構",
            "output": "每頁標題及該頁的核心訴求 (Key Takeaway)，並重點聚焦在 ROI",
            "method": "麥肯錫金字塔原理", "assumption": "客戶最在意的是導入系統後的成本回收時間", "tone": "高階商業視角、說服力強",
            "tags": "業務, 簡報, Pitch, ROI, Pre-sales"
        },
        {
            "category": "Sales", "name": "異議處理話術", "description": "應對客戶殺價或功能質疑的劇本",
            "actor": "業務談判教練", "user_audience": "初階業務人員",
            "task": "撰寫應對「價格太貴」這項客戶異議的回覆話術",
            "output": "提供三種不同切入點的話術：1. 價值轉移 2. 成本比較 3. 標竿客戶案例",
            "method": "提問引導與價值塑造法", "assumption": "我們的產品比競品貴 20%，但穩定度及售後服務更好", "tone": "堅定、專業、不卑不亢",
            "tags": "業務, 異議處理, 談判, 銷售話術"
        },
        {
            "category": "Sales", "name": "客戶成功案例 (Case Study)", "description": "將成功導入專案轉化為品牌背書文章",
            "actor": "客戶成功經理 (CSM)", "user_audience": "仍在觀望的潛在客戶",
            "task": "撰寫某知名企業成功導入系統的 Case Study",
            "output": "包含：客戶背景、面臨挑戰、解決方案、帶來的量化效益 (如提升30%效率)",
            "method": "英雄旅程故事結構", "assumption": "該企業為業內前三大品牌，具備高度指標性", "tone": "客觀、具權威性、充滿成就感",
            "tags": "客服, CSM, 案例分享, Case Study"
        },

        # --- Ops (5) ---
        {
            "category": "Ops", "name": "建立軟體專案計畫", "description": "統籌開發團隊的專案排程佈局",
            "actor": "PMP 認證專案經理", "user_audience": "開發團隊",
            "task": "建立軟體專案計畫",
            "output": "包含：1. 專案目標 2. 里程碑 3. 任務列表 4. 風險管理",
            "method": "使用 Agile + Scrum", "assumption": "專案是開發 APS 排程系統", "tone": "清楚、結構化",
            "tags": "營運, PM, 專案管理, Agile, Scrum"
        },
        {
            "category": "Ops", "name": "標準作業流程 (SOP)", "description": "建立行政或產線防錯的操作手冊",
            "actor": "營運長 (COO)", "user_audience": "基層作業員",
            "task": "撰寫廠房機台每日啟動的安全 SOP",
            "output": "必須包含：開機前檢查表 (Checklist)、異常通報流程圖文字版與注意事項",
            "method": "防呆設計 (Poka-Yoke) 精神", "assumption": "人員流動率高，需極度簡化文字", "tone": "嚴肅、不容妥協、極度白話",
            "tags": "營運, SOP, 流程, 廠房作業"
        },
        {
            "category": "Ops", "name": "專案進度週報", "description": "向上級匯報每週專案的健康度",
            "actor": "專案經理 (PM)", "user_audience": "跨部門高階主管",
            "task": "產出每週專案進度報告",
            "output": "包含：當週完成事項彙整、下週預定目標、紅綠燈健康度指標及阻礙事項 (Blockers)",
            "method": "5 分鐘快讀 (Executive Summary) 架構", "assumption": "專案目前進度落後兩週，需申請資源協調", "tone": "客觀、聚焦解決方案",
            "tags": "營運, 報表, 週報, PM"
        },
        {
            "category": "Ops", "name": "供應商評估報告", "description": "針對採購廠商的綜合評核機制",
            "actor": "資深採購經理", "user_audience": "財務部與總經理",
            "task": "撰寫雲端伺服器服務商的年度評估報告",
            "output": "雷達圖構面文字說明：價格、穩定度、客服回應速度、資安合規性，並給予續約建議",
            "method": "客觀量化加權評分法", "assumption": "現有服務商過去三個月曾發生兩次大當機", "tone": "審慎評估、數據說話",
            "tags": "營運, 採購, 供應商, 評估, 報告"
        },
        {
            "category": "Ops", "name": "辦公室資安規範", "description": "宣導並制定全體員工的資訊安全準則",
            "actor": "資訊安全長 (CISO)", "user_audience": "全體非 IT 背景員工",
            "task": "發布最新的遠端辦公資安守則",
            "output": "列出三大絕對禁止行為 (Don'ts) 與三個必做安全措施 (Dos)，不可超過一頁 A4",
            "method": "場景化案例帶入", "assumption": "近期同行遭到嚴重勒索軟體攻擊", "tone": "具警示意味但不恐嚇",
            "tags": "營運, 資安, 規範, 遠端辦公"
        },

        # --- Strategy (5) ---
        {
            "category": "Strategy", "name": "分析銷售數據並提供建議", "description": "從資料中挖掘商機並提供管理層指引",
            "actor": "資深資料科學家", "user_audience": "公司管理層",
            "task": "分析銷售數據並提供建議",
            "output": "1. 重要指標 2. 趨勢分析 3. 改善建議",
            "method": "使用商業分析方法", "assumption": "數據包含 3 年銷售紀錄", "tone": "簡潔、商業導向",
            "tags": "戰略, 資料分析, 數據, 商業"
        },
        {
            "category": "Strategy", "name": "撰寫 AI 產業趨勢報告", "description": "提供 CEO 全局視野以決定研發方向",
            "actor": "企業策略顧問", "user_audience": "CEO 與董事會",
            "task": "撰寫 AI 產業趨勢報告",
            "output": "1. 市場概況 2. 主要競爭者 3. 技術趨勢 4. 建議策略",
            "method": "使用 SWOT 分析", "assumption": "市場是企業 AI 軟體", "tone": "高層決策導向",
            "tags": "戰略, 產業報告, AI, CEO, SWOT"
        },
        {
            "category": "Strategy", "name": "商業模式畫布 (BMC)", "description": "為新創事業體釐清變現模式",
            "actor": "連續創業家 / 天使投資人", "user_audience": "內部創新孵化團隊",
            "task": "填寫並檢視新產品的商業模式畫布",
            "output": "以表格呈現九大區塊 (價值主張、客戶區隔、通路、收益流等) 的核心假設",
            "method": "精實創業 (Lean Startup)", "assumption": "準備進入訂閱制 (SaaS) 市場", "tone": "具備批判性與洞察力",
            "tags": "戰略, BMC, 商業模式, 創業"
        },
        {
            "category": "Strategy", "name": "競品分析報告", "description": "盤點敵我優劣勢以擬定突圍對策",
            "actor": "市場情報分析師", "user_audience": "產品經理與行銷總監",
            "task": "產出一份前三大競品的深度分析文件",
            "output": "針對各競品的市佔率、功能亮點、定價策略及致命缺點進行條列式比較",
            "method": "五力分析模型", "assumption": "我方品牌剛成立不到兩年，資源有限", "tone": "客觀中立、見解犀利",
            "tags": "戰略, 競品分析, 市場情報, 產品策略"
        },
        {
            "category": "Strategy", "name": "OKR 目標設定", "description": "對齊公司年度戰略與各部門執行目標",
            "actor": "戰略執行長", "user_audience": "各單位處長",
            "task": "引導制定下一季度的最高優先級 OKR",
            "output": "產出 1 個鼓舞人心的 Objective 及 3 個具體可量測的 Key Results",
            "method": "Intel/Google 的 OKR 原則", "assumption": "公司首要目標由「獲取新客」轉向「提高既有客戶留存」", "tone": "目標導向、激勵且清晰",
            "tags": "戰略, OKR, 管理, 目標"
        }
    ]
    
    # Generate 'example' text and insert
    for p in prompts:
        example_text = f"✅ **範例：{p['name']}（使用 AUTOMAT 精準化）：**\n" \
                       f"*   **Actor (角色):** {p.get('actor', '')}\n" \
                       f"*   **User/Audience (目標對象):** {p.get('user_audience', '')}\n" \
                       f"*   **Task (任務):** {p.get('task', '')}\n" \
                       f"*   **Output (輸出格式):** \n    {p.get('output', '')}\n" \
                       f"*   **Method (方法):** {p.get('method', '')}\n" \
                       f"*   **Assumptions (假設條件):** {p.get('assumption', '')}\n" \
                       f"*   **Tone (語氣風格):** {p.get('tone', '')}"
        
        cursor.execute('''
            INSERT INTO PromptLibrary (category, name, description, actor, user_audience, task, output, method, assumption, tone, example, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            p['category'], p['name'], p['description'], p['actor'], p['user_audience'], 
            p['task'], p['output'], p['method'], p['assumption'], p['tone'], example_text, p['tags']
        ))
        
    conn.commit()
    conn.close()
    print("Database created and seeded successfully with 30 items.")

if __name__ == "__main__":
    create_db()
