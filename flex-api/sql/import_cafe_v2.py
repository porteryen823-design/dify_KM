#!/usr/bin/env python3
"""
直接導入 cafe_dessert_showcase 到 MySQL，避免編碼問題
"""
import json
import subprocess

# 讀取 JSON 檔案
with open('../../LineFlexMessage/cafe_dessert_showcase.json', 'r', encoding='utf-8') as f:
    flex_json = json.load(f)

# 序列化為 JSON 字符串（保留中文）
contents_json = json.dumps(flex_json, ensure_ascii=False)

# 建立 SQL（簡單的 INSERT，避免複雜的 JSON_OBJECT 語法）
sql = f"""
DELETE FROM flex_message_templates WHERE id='cafe_dessert_showcase';

INSERT INTO flex_message_templates (id, description, contents)
VALUES ('cafe_dessert_showcase', '咖啡與甜點推薦 5 選', {json.dumps(contents_json)});

SELECT id, description, CHAR_LENGTH(contents) as len FROM flex_message_templates WHERE id='cafe_dessert_showcase';
"""

# 寫到臨時檔
with open('/tmp/cafe_v2.sql', 'w', encoding='utf-8') as f:
    f.write(sql)

# 執行
result = subprocess.run(
    ['docker', 'exec', 'docker-db_mysql-1', 'mysql', '-uroot', '-pdifyai123456', 'line_flex'],
    stdin=open('/tmp/cafe_v2.sql', 'r', encoding='utf-8'),
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    encoding='utf-8'
)

print("Import result:")
print(result.stdout)
if result.returncode != 0:
    print("ERROR:", result.stderr)
