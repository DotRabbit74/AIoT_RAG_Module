from module import embedding
from module import vectorstore

vecDB = vectorstore.VectorStore(collection_name="document_upload_test")
embeder = embedding.EmbeddingModel(device="cuda")

query = input("你ます了?")
embeded_query = embeder.embed_text(query)
res = vecDB.query(embeded_query, top_k=3)
print("りしれ供さ小:")
print(res)

#for hit in res:
#    print(f"ID: {hit.id}, Score: {hit.score}", "\n")
#    print(f"Payload: {hit.payload['text'][:100]}", "\n")