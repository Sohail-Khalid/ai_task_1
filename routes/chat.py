from qdrant_config import embed_model, qdrant, collection_name, llms 
from fastapi import APIRouter
router = APIRouter()


@router.post("/chat/")
async def chat(chat: str):
    try:
        query_embedding = embed_model.embed_text(chat)
        search_results = qdrant.search(collection_name=collection_name, query=query_embedding, top_k=5)
        search_results = search_results.points

        retrieved_texts = [
            {"text": result.payload["text"], "id": result.id}
            for result in search_results
        ]

        context = "\n".join(retrieved_texts)
        prompt = f"Based on the following information:\n\n{context}\n\nAnswer the question: {chat}"
        answer = llms.predict(prompt)

        return {"query": chat, "answer": answer, "context": retrieved_texts}
    
    except Exception as e:
        return {"error": str(e)}
