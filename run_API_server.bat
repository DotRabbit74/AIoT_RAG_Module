@echo off
echo 正在啟動 FastAPI 服務...

:: 1. 進入當前目錄
cd /d %~dp0

:: 2. 啟動虛擬環境 (假設您的虛擬環境叫 .venv)
call .venv\Scripts\activate

:: 3. 執行 API (這會觸發 main.py 裡的 uvicorn.run)
python -m api.main

pause