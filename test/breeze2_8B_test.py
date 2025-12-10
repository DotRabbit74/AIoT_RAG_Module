from openai import OpenAI
from module import prompt_builder
from module import embedding
from module import vectorstore

client = OpenAI(
    base_url="http://localhost:8000/v1", 
    api_key="EMPTY"
)

vecDB = vectorstore.VectorStore(collection_name="document_upload_test")
embeder = embedding.EmbeddingModel(device="cuda")
builder = prompt_builder.PromptBuilder(max_context_chars=7000)

input_query = input("請輸入您的問題: ")
embeded_query = embeder.embed_text(input_query)
rag_result = vecDB.query(embeded_query, top_k=3)
llm_query = builder.build_messages(input_query, [hit.payload.update({"score": hit.score}) or hit.payload for hit in rag_result])

print("--- 送到模型的訊息 ---\n") 
print(llm_query)


try:
    response = client.chat.completions.create(
        model="breeze-8b",
        messages=llm_query, 
        max_tokens=1024, # 輸出token限制
        temperature=0.1
    )
    print("--- 模型回答 ---")
    print(response.choices[0].message.content)

except Exception as e:
    print(f"調用失敗，請檢查伺服器狀態: {e}")