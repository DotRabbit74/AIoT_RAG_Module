# config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from typing import Optional

class Settings(BaseSettings):
    # 根目錄路徑
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    
    @property
    def DATA_DIR(self) -> Path:
        return self.BASE_DIR / "data"

    @property
    def VECTOR_DB_DIR(self) -> Path:
        return self.DATA_DIR / "vector_db"

    @property
    def LOG_DIR(self) -> Path:
        return self.BASE_DIR / "logs"


    # Qdrant 設定
    # 預設值給 "localhost" (Windows)，Docker部署時透過 .env 改寫
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_COLLECTION_NAME: str = "main_vector_db"
    QDRANT_API_KEY: Optional[str] = None
    VECTOR_DIM: int = 1024  
    TOP_K: int = 5

    # Embedding 模型設定
    EMBEDDING_MODEL_NAME: str = "BAAI/bge-m3" 
    EMBEDDING_BATCH_SIZE: int = 32
    
    # prompt_builder 設定
    PROMPT_MAX_CONTEXT_CHARS: int = 3000  # context 最大字元數 (配合 max-model-len 4096 縮減)

    # LLM 設定
    LLM_MODEL_NAME: str = "breeze-8b"
    LLM_API_HOST: str = "http://localhost"
    LLM_API_PORT: int = 8000
    LLM_MAX_TOKENS: int = 1024

    @property
    def LLM_API_BASE(self) -> str:
        """自動組裝 API Base URL"""
        # 注意：OpenAI client 通常需要 /v1 結尾
        return f"{self.LLM_API_HOST}:{self.LLM_API_PORT}/v1"

    # API 讀取環境
    APP_ENV: str = "dev" # 在.env設定檔中改寫
    
    #API 服務設定
    API_HOST: str = "0.0.0.0" 
    API_PORT: int = 5000
    
    # 其他
    LOG_LEVEL: str = "INFO"


    # 設定.env讀取規則
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore" # 忽略 .env 裡多餘的變數
    )

# 初始化單例
settings = Settings()

# -------------------------
# Debug 用
# -------------------------
if __name__ == "__main__":
    print("--- Current Configuration ---")
    print(f"Base Dir:      {settings.BASE_DIR}")
    print(f"Data Dir:      {settings.DATA_DIR}")
    print(f"LLM API Base:  {settings.LLM_API_BASE}")
    print(f"Qdrant Host:   {settings.QDRANT_HOST}")
    print(f"Vector Dim:    {settings.VECTOR_DIM}")
    print("-----------------------------")