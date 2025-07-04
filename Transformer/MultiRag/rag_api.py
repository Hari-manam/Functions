# Transformer/MultiRag/rag_api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict

from .rag_types import standard_rag, fusion_rag, speculative_rag, corrective_rag, agentic_rag

app = FastAPI()

class RAGRequest(BaseModel):
    query: str
    rag_type: str
    extra_params: Optional[Dict] = {}

@app.post("/rag")
def run_rag(request: RAGRequest):
    if request.rag_type == "standard":
        return standard_rag.run(request.query)
    elif request.rag_type == "fusion":
        return fusion_rag.run(request.query)
    elif request.rag_type == "speculative":
        return speculative_rag.run(request.query)
    elif request.rag_type == "corrective":
        return corrective_rag.run(request.query)
    elif request.rag_type == "agentic":
        return agentic_rag.run(request.query)
    else:
        raise HTTPException(status_code=400, detail="Invalid RAG type.")

@app.get("/")
def read_root():
    return {"message": "API is running!"}