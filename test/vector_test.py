from module import vectorstore
from module import embedding

vecDB = vectorstore.VectorStore(collection_name="vector_test_512", vector_dim=512)
embeder = embedding.EmbeddingModel(model_name="BAAI/bge-small-zh-v1.5", device="cuda")

test = "this is just a bullshit but idk why it works"
metadata = {"text": test, "source": "vector_text.py"}

vec = embeder.embed_text(test)
vecDB.insert_vectors([vec], [metadata])
res = vecDB.query(vec, top_k=3)

print("Query Results:")
for hit in res:
    print(f"ID: {hit.id}, Score: {hit.score}, Payload: {hit.payload}")


