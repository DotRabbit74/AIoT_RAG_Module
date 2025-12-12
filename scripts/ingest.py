# scripts/ingest.py
import sys
from pathlib import Path


sys.path.append(str(Path(__file__).resolve().parent.parent))

from module.config import settings
from module.text_splitter import TokenTextSplitter
from module.embedding import EmbeddingModel
from module.vectorstore import VectorStore

def main():
    print("=== 開始執行資料注入 (Server-Side) ===")
    
    # 1. 檢查資料目錄 
    data_dir = settings.DATA_DIR
    if not data_dir.exists():
        print(f"❌ 錯誤: 資料目錄不存在 {data_dir}")
        return

    # 2. 初始化模組
    print("正在初始化 RAG 核心模組...")
    splitter = TokenTextSplitter()
    embed_model = EmbeddingModel()
    vector_store = VectorStore()

    # 3. 掃描檔案
    files = list(data_dir.glob("**/*.txt"))
    print(f"掃描目錄: {data_dir} | 發現 {len(files)} 個檔案")

    total_chunks = 0

    # 4. 處理檔案迴圈
    for file_path in files:
        try:
            print(f"   處理中: {file_path.name} ...", end=" ", flush=True)
            
            content = file_path.read_text(encoding="utf-8")
            
            # 切分
            chunks = splitter.split_text(content)
            if not chunks:
                print("跳過 (無內容)")
                continue

            # 轉向量
            vectors = embed_model.embed_texts(chunks)

            # Metadata
            payloads = [
                {"source": file_path.name, "text": chunk} 
                for chunk in chunks
            ]

            # D. 寫入資料庫
            vector_store.insert_vectors(vectors, payloads)
            
            print(f"完成 ({len(chunks)} 片段)")
            total_chunks += len(chunks)

        except Exception as e:
            print(f"\n失敗: {file_path.name} - {e}")

    print(f"\n=== 共注入 {total_chunks} 個片段到 Qdrant ===")

if __name__ == "__main__":
    main()