import faiss
import numpy as np


class ResumeVectorStore:
    def __init__(self, chunks: list[str], embeddings: np.ndarray):
        if embeddings.ndim != 2 or embeddings.shape[0] != len(chunks):
            raise ValueError("Embeddings must align with resume chunks.")
        self.chunks = chunks
        self.index = faiss.IndexFlatIP(embeddings.shape[1])
        self.index.add(embeddings.astype("float32"))

    def search(self, query_embedding: np.ndarray, top_k: int) -> list[str]:
        if len(self.chunks) == 0:
            return []
        scores, indices = self.index.search(query_embedding.astype("float32"), min(top_k, len(self.chunks)))
        return [self.chunks[index] for index in indices[0] if index >= 0]
