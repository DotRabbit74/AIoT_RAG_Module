#using GEMINI API

from module import embedding
from module import vectorstore
from module import prompt_builder
from google.genai import Client
from dotenv import load_dotenv
import os

load_dotenv()   
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = Client(api_key=GEMINI_API_KEY)

vecDB = vectorstore.VectorStore(collection_name="document_upload_test")
embeder = embedding.EmbeddingModel(device="cuda")
builder = prompt_builder.PromptBuilder(max_context_chars=1500)

input_query = input("請輸入您的問題: ")
embeded_query = embeder.embed_text(input_query)
rag_result = vecDB.query(embeded_query, top_k=7)
llm_query = builder.build_messages(input_query, [hit.payload for hit in rag_result])

contents = ["\n\n".join([f"{m['role'].upper()}:\n{m['content']}" for m in llm_query])]
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=contents)

print(response)