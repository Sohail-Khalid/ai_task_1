from qdrant_config import embed_model, qdrant, collection_name, llms
from fastapi import APIRouter

router = APIRouter()


@router.post("/chat/")
async def chat(chat: str):
    try:
        query_embedding = embed_model.embed_query(chat)
        if not query_embedding:
            return {"error": "Failed to generate embedding for the query"}


        search_results = qdrant.search(
            collection_name=collection_name, query_vector=query_embedding, limit=5
        )

        if not search_results:
            return {"query": chat, "answer": "No relevant information found", "context": []}


        retrieved_texts = [
            {"text": result.payload["text"], "id": result.id}
            for result in search_results 
        ]

        context = "\n".join([doc["text"] for doc in retrieved_texts])
        prompt = f"Based on the following information:\n\n{context}\n\nAnswer the question: {chat}"


        answer = llms.predict(prompt)
        if not answer:
            return {"query": chat, "answer": "No response generated", "context": retrieved_texts}


        return {"query": chat, "answer": answer, "context": retrieved_texts}

    except Exception as e:
        return {"error": str(e)}
