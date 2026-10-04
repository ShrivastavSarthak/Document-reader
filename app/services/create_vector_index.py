import faiss
import numpy as np

def create_vector_index(embeddings):
    vector= embeddings.cpu().numpy().astype("float32")
    faiss.normalize_L2(vector)
    dimension = vector.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(vector)
    return index