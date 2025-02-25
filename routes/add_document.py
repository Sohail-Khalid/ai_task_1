from fastapi import APIRouter, UploadFile, File
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from qdrant_client.models import PointStruct
from qdrant_config import embed_model, qdrant, collection_name 
import uuid
import os

router = APIRouter()

@router.post("/add_document/")
async def add_document(file: UploadFile = File(...)):
    try:
        file_path = f"temp_{file.filename}"
        with open(file_path, "wb") as f:
            f.write(await file.read())  

        loader = PyPDFLoader(file_path)
        docs = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = text_splitter.split_documents(docs)

        texts = [chunk.page_content for chunk in chunks]
        embeddings = embed_model.embed_documents(texts)

        points = [
            PointStruct(id=str(uuid.uuid4()), vector=embedding, payload={"text": text})
            for text, embedding in zip(texts, embeddings)
        ]
        qdrant.upsert(collection_name=collection_name, points=points)

        os.remove(file_path)

        return {"message": "Document uploaded and embedded successfully!", "total_chunks": len(points)}

    except Exception as e:
        return {"error": str(e)}
