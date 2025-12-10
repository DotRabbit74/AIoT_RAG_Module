@echo off
echo 正在啟動 Llama-Breeze2 API Server...

:: 1. 進入當前目錄
cd /d %~dp0

:: 2. 啟動虛擬環境
call .venv\Scripts\activate

:: 3. 執行 Server (路徑建議用相對路徑或變數，方便管理)
set MODEL_PATH="D:\LLM_model\Breeze\Llama-Breeze2-8B-Instruct-text-only.Q5_K_M.gguf"

python -m llama_cpp.server --model %MODEL_PATH% --n_gpu_layers -1 --chat_format chatml --host 0.0.0.0 --port 8000 --n_ctx 8192

pause