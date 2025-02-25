from fastapi import APIRouter, UploadFile, File
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from qdrant_client.models import PointStruct
from qdrant_config import embed_model, qdrant, collection_name
import uuid
import os
from logger_config import logger 

router = APIRouter()

@router.post("/add_document/")
async def add_document(file: UploadFile = File(...)):
    try:
        if not file:
            logger.error("No file received")
            return {"error": "No file received"}
        
        file_path = f"temp_{file.filename}"
        with open(file_path, "wb") as f:
            file_bytes = await file.read()
            f.write(file_bytes)

        if not os.path.exists(file_path):
            logger.error("File saving failed")
            return {"error": "File save failed"}
        logger.info(f"File saved successfully: {file_path}")

        loader = PyPDFLoader(file_path)
        docs = loader.load()
        if not docs:
            logger.error("PDF loading failed")
            return {"error": "PDF loading failed"}
        logger.info(f"PDF loaded with {len(docs)} pages")

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = text_splitter.split_documents(docs)
        if not chunks:
            logger.error("Text splitting failed")
            return {"error": "Text splitting failed"}
        logger.info(f"Text split into {len(chunks)} chunks")

        texts = [chunk.page_content for chunk in chunks]
        embeddings = embed_model.embed_documents(texts)
        if not embeddings or len(embeddings) != len(texts):
            logger.error("Embedding generation failed")
            return {"error": "Embedding generation failed"}
        logger.info(f"Generated embeddings for {len(embeddings)} chunks")

        points = [
            PointStruct(id=str(uuid.uuid4()), vector=embedding, payload={"text": text})
            for text, embedding in zip(texts, embeddings)
        ]
        if not points:
            logger.error("Point struct creation failed")
            return {"error": "Point struct creation failed"}
        logger.info(f"Prepared {len(points)} points for Qdrant")

        qdrant.upsert(collection_name=collection_name, points=points)
        logger.info(f"Upserted {len(points)} points into Qdrant collection: {collection_name}")

        os.remove(file_path)
        logger.info(f"Temporary file {file_path} deleted successfully")

        return {"message": "Document uploaded and embedded successfully!", "total_chunks": len(points)}

    except Exception as e:
        logger.exception("An error occurred")
        return {"error": str(e)}
