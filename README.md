# AIoT RAG Project

這是一個基於 RAG (Retrieval-Augmented Generation) 的問答系統，整合了 FastAPI, Qdrant (Vector DB) 與 vLLM (LLM Inference)。

## 專案架構

- **api/**: FastAPI 應用程式入口與 API 定義。
- **module/**: 核心模組 (Embedding, VectorStore, PromptBuilder, LLM Interface)。
- **docker-compose.yml**: 定義服務編排 (API, Qdrant, vLLM)。
- **Dockerfile**: API 服務的容器定義。

## 部署需求 (Linux Server)

- Docker & Docker Compose
- NVIDIA Container Toolkit (用於 GPU 加速)
- NVIDIA GPU (建議 24GB VRAM 以上以執行 Breeze-8B)

## 快速開始

1. **設定環境變數**
   在專案根目錄建立 `.env` 檔案：
   ```bash
   HUGGING_FACE_HUB_TOKEN=your_hf_token
   ```

2. **啟動服務**
   ```bash
   docker-compose up -d --build
   ```

3. **API 文件**
   啟動後，可訪問 `http://localhost:5000/docs` 查看 Swagger UI。

## 服務端口

- **RAG API**: 5000
- **Qdrant**: 6333
- **vLLM**: 8000
