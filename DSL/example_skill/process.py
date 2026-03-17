import sys
import collections
import re

def analyze_text(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.splitlines()
            words = re.findall(r'\w+', content.lower())
            
            word_counts = collections.Counter(words)
            top_5 = word_counts.most_common(5)
            
            print(f"--- 分析結果 ---")
            print(f"總行數: {len(lines)}")
            print(f"總字數: {len(words)}")
            print(f"高頻詞彙 (Top 5):")
            for word, count in top_5:
                print(f"  - {word}: {count} 次")
    except Exception as e:
        print(f"錯誤: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("請提供檔案路徑")
    else:
        analyze_text(sys.argv[1])
