import hashlib
import math

import numpy as np
from openai import OpenAI

from backend.config import Settings


class EmbeddingService:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None

    @property
    def provider(self) -> str:
        return "openai" if self.client else "local-hash"

    def embed_texts(self, texts: list[str]) -> np.ndarray:
        if not texts:
            return np.zeros((0, 384), dtype="float32")
        if self.client:
            response = self.client.embeddings.create(model=self.settings.openai_embedding_model, input=texts)
            vectors = [item.embedding for item in response.data]
            return _normalize(np.array(vectors, dtype="float32"))
        return _normalize(np.array([_hash_embedding(text) for text in texts], dtype="float32"))


def _hash_embedding(text: str, dimensions: int = 384) -> np.ndarray:
    vector = np.zeros(dimensions, dtype="float32")
    for token in text.lower().split():
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        index = int.from_bytes(digest[:4], "little") % dimensions
        sign = 1 if digest[4] % 2 == 0 else -1
        vector[index] += sign * (1 + math.log1p(len(token)))
    return vector


def _normalize(vectors: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    norms[norms == 0] = 1
    return vectors / norms
