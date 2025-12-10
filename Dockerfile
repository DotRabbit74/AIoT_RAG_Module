# 使用輕量級 Python
FROM python:3.10-slim

WORKDIR /app

# 安裝系統依賴 (有些 Python 套件編譯需要)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 複製依賴清單
COPY requirements.txt .

# [關鍵] 安裝 Python 套件
# 這裡使用 --no-cache-dir 縮小體積
# 安裝 GPU 版 Torch (預設即為 GPU 版) 以支援 Embedding 加速
RUN pip install --no-cache-dir torch torchvision torchaudio
RUN pip install --no-cache-dir -r requirements.txt

# 複製程式碼
COPY . .

# 啟動指令
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "5000"]
