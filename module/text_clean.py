import re
import json

def clean_text(text: str) -> str:
    
    # \n、\t、多重空格
    text = text.replace('\n', ' ').replace('\t', ' ').strip()
    text = re.sub(r'\s+', ' ', text)

    # 控制字元
    text = re.sub(r'[\x00-\x1F\x7F]', '', text)

    return text

def is_json(text: str) -> bool:
    """
    檢查是否為 JSON 格式
    """
    try:
        json.loads(text)
        return True
    except ValueError:
        return False

def process_json_to_text(data, separator=": ", level_separator=" > ") -> str:
    """
    JSON檔清理
    """
    lines = []

    def recurse(current_data, parent_path=""):
        if isinstance(current_data, dict):
            for key, value in current_data.items():
                # 建立當前路徑，例如 "第一章 > 標題"
                new_path = f"{parent_path}{level_separator}{key}" if parent_path else key
                
                if isinstance(value, (dict, list)):
                    # 如果值還是結構，繼續遞迴
                    recurse(value, new_path)
                else:
                    # 如果是葉節點 (Leaf node)，組合路徑與值
                    # 清理值並轉為字串
                    clean_val = str(value).strip()
                    if clean_val:
                        lines.append(f"{new_path}{separator}{clean_val}")
        
        elif isinstance(current_data, list):
            for item in current_data:
                # 對於列表，通常不增加路徑名稱，直接遞迴處理內容
                recurse(item, parent_path)
        
        else:
            # 頂層純值的情況 
            lines.append(f"{parent_path}{separator}{str(current_data)}")

    recurse(data)
    return "\n".join(lines)