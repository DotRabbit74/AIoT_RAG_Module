# vectorstore.py
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from typing import List, Dict
import numpy as np
import uuid

class VectorStore:
    def __init__(self, host, port, collection_name, vector_dim = 1024):
        """
        init. vectorDB Client
        """
        self.client = QdrantClient(host=host, port=port)
        self.collection_name = collection_name
        self.vector_dim = vector_dim
        self._init_collection()

    def _init_collection(self):
        """
        setup collection ,or do nothing if exists
        """
        try:
            if not self.client.collection_exists(collection_name=self.collection_name):
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(size=self.vector_dim, distance=Distance.COSINE)
                )
                print(f"Collection '{self.collection_name}' created.")
            else:
                print(f"Collection '{self.collection_name}' already exists.")
        except Exception as e:
            print(f"Error initializing collection: {e}")

    def insert_vectors(self, embeddings: List[np.ndarray], metadatas: List[Dict]):
        """
        將vector & metadata 插入 collection
        """
        if len(embeddings) != len(metadatas):
            raise ValueError("The number of embeddings and metadatas must be the same.")

        points = [
            PointStruct(id=str(uuid.uuid4()), vector=emb.tolist(), payload=meta)
            for emb, meta in zip(embeddings, metadatas)
        ]
        self.client.upsert(collection_name=self.collection_name, points=points, wait=True)
        # 回傳操作結果
        print(f"Upserted {len(points)} vectors into '{self.collection_name}'.")

    def query(self, query_vector: np.ndarray, top_k=5):
        """
        單筆 query_vector 搜尋最相似的 top_k 
        """
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector.tolist(),
            limit=top_k
        )
        return results

    def delete_collection(self):
        """
        delete collection
        """
        if self.client.collection_exists(self.collection_name):
            self.client.delete_collection(self.collection_name)
            print(f"Collection '{self.collection_name}' deleted.")

    def get_collection_info(self):
        """
        collection info.
        """
        return self.client.get_collection(self.collection_name)
