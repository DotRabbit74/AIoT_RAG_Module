from pydantic import BaseModel, Field
from typing import List, Optional, Dict

# --- Request (前端傳進來的) ---
class ChatRequest(BaseModel):
    query: str = Field(
        ..., 
        description="使用者的問題", 
    )
    top_k: int = Field(
        5, 
        description="RAG 檢索的文件數量", 
        ge=1, le=10
    )
    # 預留給未來的參數
    temperature: float = Field(0.1, description="模型的隨機性 (0.0 - 1.0)")

# --- Response (回傳給前端的) ---
class SourceDocument(BaseModel):
    filename: str = Field(..., description="來源文件名稱")
    #content: str = Field(..., description="檢索到的文件片段")

class ChatResponse(BaseModel):
    answer: str = Field(..., description="LLM 生成的回答")
    sources: List[SourceDocument] = Field(..., description="參考的來源文件列表")
    
    # 這裡可以加上執行時間等 Meta info
    processing_time: Optional[float] = Field(None, description="處理耗時(秒)")