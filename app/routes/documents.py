from fastapi import APIRouter, UploadFile, File, HTTPException,Depends
from fastapi.security import HTTPBearer
from app.services.chunking_service import create_chunk
from app.services.text_extract import extract_text
from app.services.embedding_service import create_embeddings
from app.services.create_vector_index import create_vector_index
from app.services.store_service import store_doc, load_doc
from app.services.llm_service import generate_answer
bearer_scheme = HTTPBearer()
from pydantic import BaseModel
import faiss
document_route = APIRouter(
    prefix="/document",
    tags= ["Documents"],
    dependencies=[Depends(bearer_scheme)]
)

class SearchRequest(BaseModel):
    doc_id:str
    question:str

context: list[dict[str,str]] = []


@document_route.post("/upload")
async def upload_document( file:UploadFile = File(...),):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )
    pdf_bytes = await file.read()
    try:
        text =  extract_text(pdf_bytes)
    except:
        raise HTTPException(
            status_code= 400,
            detail= "Unable to read PDF"
        )
    if not text.strip():
        raise HTTPException(
            status_code=400,
            detail= "No text to extract"
        )
    chunks = create_chunk(
        text,
        max_word=100
    )
    embedding =create_embeddings(chunks)
    index = create_vector_index(embedding)
    
    doc_id = store_doc(index,chunks) 
    
    return {
        "message":"Document indexed successfully",
        "document_id": doc_id,
        "total_chunks": len(chunks)
    }

@document_route.post('/search')
async def search_document(request:SearchRequest):
    
    context.append({"role":"user","context":request.question})
    index, chunks = load_doc(request.doc_id)
    query = create_embeddings([request.question])
    query = query.cpu().numpy().astype("float32")
    faiss.normalize_L2(query)
    score, indices= index.search(
        query,
        k=min(3, index.ntotal)
    )
    result = []
    for score, idx in zip(score[0],indices[0]):
        if idx == -1:
            continue
        result.append({
            "score": float(score),
            "text": chunks[int(idx)]
        })
    ans  = generate_answer(
        history=context,
        chunks=[res["text"] for res in result]
    )
    context.append({"role":"assistant","content":ans})
    print(context)
    return{
        "question": request.question,
        "results": result,
        "answer":ans
    }