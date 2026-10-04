from sentence_transformers import SentenceTransformer
import torch

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

def create_embeddings(chunks: list[str]) -> torch.Tensor:
    embeddings = model.encode(
        chunks,
        convert_to_tensor=True,
        normalize_embeddings=True
    )
    return embeddings