from langchain.llms.ollama import Ollama
from langchain.embeddings import HuggingFaceEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

llms = Ollama(model="deepseek-r1:1.5b")

try:
    embed_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    print(" Embeddings model loaded")
except Exception as e:
    print(f"Error loading embeddings: {e}")

qdrant = QdrantClient("localhost", port=6333)

collection_name = "Fast_api_chat_app"

collections = qdrant.get_collections()
existing_collections = [c.name for c in collections.collections]

if collection_name not in existing_collections:
   qdrant.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE)
    )
