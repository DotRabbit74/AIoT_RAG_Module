import time
from fastapi import FastAPI, HTTPException, Depends
from api.schemas import ChatRequest, ChatResponse, SourceDocument
from api.dependencies import get_rag_service, RagModules
from module.config import settings

# 初始化 FastAPI
app = FastAPI(
    title="AIoT RAG Chatbot API",
    description="基於 Llama-Breeze2 的 RAG 問答服務",
    version="1.0.0"
)

@app.get("/")
def health_check():
    """ 健康檢查端點 """
    return {
        "status": "ok",
        "env": settings.APP_ENV, # 直接讀取設定
        "llm_target": settings.LLM_API_BASE
    }

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(
    request: ChatRequest,
    rag_service: RagModules = Depends(get_rag_service) # 依賴注入
):
    start_time = time.time()
    try:
        answer, docs = rag_service.get_llm_answer(
            user_query=request.query, 
            top_k=request.top_k,
            temperature=request.temperature
        )

        # 整理回傳格式
        source_list = []
        for doc in docs:
            source_list.append(SourceDocument(
                filename=doc
                #content="" # 可選擇性加入內容
            ))

        process_time = time.time() - start_time

        return ChatResponse(
            answer=answer,
            sources=source_list,
            processing_time=round(process_time, 2)
        )

    except Exception as e:
        # 捕捉所有錯誤並回傳 500
        print(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.main:app", 
        host=settings.API_HOST, 
        port=settings.API_PORT, 
        reload=True 
    )