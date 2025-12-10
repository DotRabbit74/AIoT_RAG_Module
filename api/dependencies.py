from functools import lru_cache
from module import embedding
from module import llm_interface
from module import prompt_builder
from module import vectorstore
from module.config import settings

class RagModules:
    """RAG 相關模組的單一存取點"""
    
    def __init__(self):
        print("初始化 RAG 相關模組...")
        self.embedder = embedding.EmbeddingModel(model_name=settings.EMBEDDING_MODEL_NAME)
        self.vecDB = vectorstore.VectorStore(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT, collection_name=settings.QDRANT_COLLECTION_NAME)
        self.prompt_builder = prompt_builder.PromptBuilder(max_context_chars=settings.PROMPT_MAX_CONTEXT_CHARS)
        self.llm_client = llm_interface.LLMInterface(base_url=settings.LLM_API_BASE)
        print("初始化完成。")
        
    def get_llm_answer(self, user_query: str, top_k: int = 5, temperature: float = 0.1) -> tuple[str, list]:
        """
        根據使用者問題，透過 RAG 流程取得回答
        """
        # 1. 取得使用者問題的 embedding
        query_embedding = self.embedder.embed_text(user_query)
        
        # 2. 在向量資料庫中檢索相關文件
        search_results = self.vecDB.query(query_vector=query_embedding, top_k=top_k)
        
        # 3. 建立 prompt
        # 使用 list comprehension 前先確保 payload 存在，避免 NoneType error
        retrieved_docs = []
        for hit in search_results:
            if hit.payload:
                # 複製 payload 以免修改到原始物件 (雖然這裡是單次請求，但好習慣)
                doc_data = hit.payload.copy()
                doc_data["score"] = hit.score
                retrieved_docs.append(doc_data)

        context = self.prompt_builder.build_messages(
            user_query, 
            retrieved_docs
        )
                
        # 4. 呼叫 LLM 取得回答
        answer = self.llm_client.generate_response(context, temperature=temperature)
        
        return answer , [doc.get('source','unknown') for doc in retrieved_docs]

@lru_cache()
def get_rag_service() -> RagModules:
    return RagModules()