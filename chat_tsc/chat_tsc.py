import requests
import pandas as pd
from datetime import datetime
import os
import sys
import io
import json
import time

# ── Windows 環境 Unicode 輸出修正 (Rules 8-1) ──────────────────────────────────
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# --- 設定區 ---
API_KEY = "app-Lh0LNEm1VAqKpJYjbWNlXWgl" # TSC 問答機器人 API KEY
BASE_URL = "http://localhost:8080/v1/chat-messages"
INPUT_FILE = "chat_tsc_questions.xlsx"
OUTPUT_FILE = "test_results.xlsx"

def ask_dify(question):
    """
    使用 streaming 模式呼叫 Dify API，
    從 SSE 事件流中解析最終答案。
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "inputs": {},
        "query": question,
        "user": "auto-tester",
        "response_mode": "streaming",
        "conversation_id": ""
    }

    start_time = datetime.now()
    start_time_str = start_time.strftime("%Y-%m-%d %H:%M:%S")
    answer = ""

    try:
        with requests.post(BASE_URL, headers=headers, json=data, timeout=600, stream=True) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    decoded = line.decode("utf-8")
                    if decoded.startswith("data:"):
                        raw_json = decoded[5:].strip()
                        if raw_json == "[DONE]":
                            break
                        try:
                            event = json.loads(raw_json)
                            event_type = event.get("event", "")
                            if event_type == "message":
                                answer += event.get("answer", "")
                            elif event_type == "message_end":
                                break
                            elif event_type == "agent_message":
                                answer += event.get("answer", "")
                        except json.JSONDecodeError:
                            pass

        if not answer:
            answer = "API 回傳空白答案，請確認 Dify 應用設置。"

    except Exception as e:
        answer = f"錯誤: {str(e)}"

    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    return {
        "回答": answer,
        "開始時間": start_time_str,
        "結束時間": end_time.strftime("%Y-%m-%d %H:%M:%S"),
        "問答反應時間(秒)": round(duration, 2)
    }

# --- 執行程序 ---
if __name__ == "__main__":
    if not os.path.exists(INPUT_FILE):
        print(f"錯誤：找不到題庫檔案 {INPUT_FILE}")
        exit(1)

    print(f"讀取題庫: {INPUT_FILE}")
    df_questions = pd.read_excel(INPUT_FILE)
    
    test_results = []
    
    # 修正執行邏輯：測試所有題目
    print(f"開始進行自動化測試 (總共 {len(df_questions)} 題)...")
    
    for index, row in df_questions.iterrows():
        no = row['NO']
        question = row['問題']
        
        print(f"[{index+1}/{len(df_questions)}] 正在處理第 {no} 題: {question[:30]}...", end=" ", flush=True)
        
        # 呼叫 API
        api_result = ask_dify(question)
        
        print(f"完成! (耗時 {api_result['問答反應時間(秒)']} 秒)", flush=True)
        
        # 整合結果
        result_entry = {
            "NO": no,
            "問題": question,
            "回答": api_result["回答"],
            "開始時間": api_result["開始時間"],
            "結束時間": api_result["結束時間"],
            "問答反應時間(秒)": api_result["問答反應時間(秒)"]
        }
        test_results.append(result_entry)
        
        # 稍微停頓
        time.sleep(0.5)

    # 儲存結果
    df_results = pd.DataFrame(test_results)
    
    try:
        df_results.to_excel(OUTPUT_FILE, index=False)
        print("-" * 30)
        print(f"測試完成！共耗時約 {round(df_results['問答反應時間(秒)'].sum(), 2)} 秒。")
        print(f"結果已寫入: {os.path.abspath(OUTPUT_FILE)}")
    except PermissionError:
        print("\n" + "!" * 40)
        print(f"錯誤：無法寫入 {OUTPUT_FILE}，請關閉 Excel 檔案後重試！")
        # 備份到 csv 以免數據丟失
        df_results.to_csv("test_results_backup.csv", index=False)
        print("數據已暫存至 test_results_backup.csv")
        print("!" * 40)
