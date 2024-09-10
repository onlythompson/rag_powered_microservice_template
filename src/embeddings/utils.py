import numpy as np
from typing import List

def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    """Compute cosine similarity between two vectors."""
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    return dot_product / (norm_v1 * norm_v2)

def normalize_embedding(embedding: List[float]) -> List[float]:
    """Normalize an embedding vector to unit length."""
    norm = np.linalg.norm(embedding)
    return [x / norm for x in embedding]