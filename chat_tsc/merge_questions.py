import pandas as pd
import re
import os

def extract_questions_from_md(file_path):
    questions = []
    if not os.path.exists(file_path):
        return questions
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Pattern 1: ### Q: ...
    q1 = re.findall(r'### Q[:|：]\s*(.*?)(?:\n|$)', content)
    questions.extend(q1)
    
    # Pattern 2: ### Q\d+： ...
    q2 = re.findall(r'### Q\d+[:|：]\s*(.*?)(?:\n|$)', content)
    questions.extend(q2)
    
    # Pattern 3: ## Q: ...
    q3 = re.findall(r'## Q[:|：]\s*(.*?)(?:\n|$)', content)
    questions.extend(q3)

    # Some files use "1. **Question**" or similar headers if Q is not explicit
    # But for these specific files, let's look at the structure I saw
    
    # Han Zou (韩邹) uses "1. **Header**" as descriptors. 
    # Shenjiafeng (沈佳峰) uses "## Q: ..." which is handled.
    # Kimroy (金正阳) uses "### Q: ..." which is handled.
    # Zhang Junxian (张俊贤) uses "### Q: ..." which is handled.
    # Qi Hongyang (齊宏洋) uses "### Q\d+：" which is handled.
    
    # For Mike and Wangjun, they use bullet points. I will extract the bolded parts as questions or key concepts.
    if "Mike" in file_path or "wangjun" in file_path or "韩邹" in file_path:
        # Extract bolded terms in list items as potential questions
        bolded = re.findall(r'^\s*[\d+\-\*]\.?\s*\*\*(.*?)\*\*', content, re.MULTILINE)
        for b in bolded:
            if b not in questions:
                questions.append(f"什麼是 {b}？")

    return [q.strip() for q in questions if q.strip()]

files = [
    r"c:\VSCode_Proj\Dify\Doc_tsc\tsc_张俊贤.md",
    r"c:\VSCode_Proj\Dify\Doc_tsc\tsc_齊宏洋.md",
    r"c:\VSCode_Proj\Dify\Doc_tsc\tsc_韩邹.md",
    r"c:\VSCode_Proj\Dify\Doc_tsc\tsc_Mike.md",
    r"c:\VSCode_Proj\Dify\Doc_tsc\tsc_shenjiafeng.md",
    r"c:\VSCode_Proj\Dify\Doc_tsc\tsc交管问答_kimroy 金正阳.md",
    r"c:\VSCode_Proj\Dify\Doc_tsc\tsc_wangjun.md"
]

all_extracted = []
seen = set()

for f in files:
    qs = extract_questions_from_md(f)
    for q in qs:
        if q not in seen:
            all_extracted.append(q)
            seen.add(q)

# 加載現有題庫
existing_path = r"c:\VSCode_Proj\Dify\chat_tsc\chat_tsc_questions.xlsx"
if os.path.exists(existing_path):
    df_existing = pd.read_excel(existing_path)
    existing_questions = set(df_existing['問題'].tolist())
else:
    df_existing = pd.DataFrame(columns=['NO', '問題'])
    existing_questions = set()

# 過濾重複
new_questions = [q for q in all_extracted if q not in existing_questions]

# 建立新的 DataFrame
new_data = []
current_no = len(df_existing) + 1
for q in new_questions:
    new_data.append({"NO": current_no, "問題": q})
    current_no += 1

df_new = pd.DataFrame(new_data)
df_final = pd.concat([df_existing, df_new], ignore_index=True)

# 儲存
df_final.to_excel(existing_path, index=False)

print(f"整理完成！新增了 {len(new_questions)} 個問題。")
print(f"目前題庫總數: {len(df_final)}")
