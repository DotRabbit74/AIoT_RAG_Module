from module import embedding
import time

EMBEDDING_MODEL_NAME = "BAAI/bge-small-zh-v1.5"

print("Warming up...")


embeder = embedding.EmbeddingModel(model_name=EMBEDDING_MODEL_NAME, device="cpu")
embeder.embed_text("暖機用句子")


start = time.time()
vec = embeder.embed_text("How_da_o")
end = time.time()

elapsed = end - start



print(f"elapsed time: {elapsed:.3f} ")
