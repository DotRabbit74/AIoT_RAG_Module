from module import embedding, vectorstore, text_clean, text_splitter
import json

vecDB = vectorstore.VectorStore(collection_name="document_upload_test", vector_dim=1024)
embeder = embedding.EmbeddingModel(device="cuda")
splitter = text_splitter.TokenTextSplitter(using_tokenizer=False)

def DB_insert(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        if text_clean.is_json(content):
            content = text_clean.process_json_to_text(json.loads(content))
        clean_content = text_clean.clean_text(content)
        chunks = splitter.split_text(clean_content)
        embeddings = embeder.embed_texts(chunks)
        metadata = [{"text": chunk, "source": file_path, "index": i} for i, chunk in enumerate(chunks)]
        vecDB.insert_vectors(embeddings, metadata)

file_path = "data/test_doc.txt"
DB_insert(file_path)
print("Document inserted into vector database.")

