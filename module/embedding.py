# embedding.py
from langchain_huggingface import HuggingFaceEmbeddings
from typing import List
import numpy as np

class EmbeddingModel:
    def __init__(self, model_name: str = "BAAI/bge-m3", device: str = "cuda"):
        """
        :param model_name: model name
        :param device: 'cpu' or 'cuda'
        """
        self.model_name = model_name
        self.device = device
        self.model = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={"device": device},
            encode_kwargs={'normalize_embeddings': True}
        )

    def embed_text(self, text: str) -> np.ndarray:
        """
        單筆
        """
        return np.array(self.model.embed_query(text))

    def embed_texts(self, texts: List[str]) -> List[np.ndarray]:
        """
        多筆
        """
        return [np.array(vec) for vec in self.model.embed_documents(texts)]
