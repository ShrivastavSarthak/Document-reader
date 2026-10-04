from pathlib import Path
import uuid
import json
import faiss
STORAGE_URL = Path("app\documents")

def store_doc(index, chunks):
    doc_id = str(uuid.uuid4())
    doc_dir =STORAGE_URL / doc_id
    doc_dir.mkdir(parents=True,exist_ok=True)
    faiss.write_index(
        index,
        str(doc_dir/"index.faiss")
    )
    
    with open(
        doc_dir / "chunk.json",
        "w",
        encoding="utf=8"
    ) as file:
        json.dump(chunks,file,ensure_ascii=False, indent=2)
    return doc_id

def load_doc(doc_id):
    doc_id = str(uuid.UUID(doc_id))
    doc_dir = STORAGE_URL / doc_id
    index = faiss.read_index(
        str(doc_dir / "index.faiss")
    )
    
    with open(
        doc_dir / "chunk.json",
        "r",
        encoding="utf-8",
    ) as file:
        chunks = json.load(file) 
    return index, chunks
