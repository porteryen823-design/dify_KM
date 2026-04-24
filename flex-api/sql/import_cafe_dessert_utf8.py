#!/usr/bin/env python3
"""
導入咖啡甜點 Flex Message 到 MySQL
處理 UTF-8 編碼問題
"""
import json
import subprocess

# 讀取 JSON 檔案
with open('../../LineFlexMessage/cafe_dessert_showcase.json', 'r', encoding='utf-8') as f:
    flex_data = json.load(f)

# 準備資料
flex_id = 'cafe_dessert_showcase'
description = '咖啡與甜點推薦 5 選'
contents = json.dumps(flex_data, ensure_ascii=False)

# 轉義單引號
escaped_contents = contents.replace("'", "\\'")

# 建立 SQL 檔（使用 JSON_EXTRACT 的簡單版本）
sql = f"""
DELETE FROM flex_message_templates WHERE id='{flex_id}';

INSERT INTO flex_message_templates (id, description, contents)
VALUES ('{flex_id}', '{description}', '{escaped_contents}');

SELECT id, description FROM flex_message_templates WHERE id='{flex_id}';
"""

# 執行到 Docker MySQL
cmd = ['docker', 'exec', 'docker-db_mysql-1', 'mysql', '-uroot', '-pdifyai123456', 'line_flex']
process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
stdout, stderr = process.communicate(input=sql)

print(stdout)
if stderr:
    print("STDERR:", stderr)
print(f"\nResult: {process.returncode}")
