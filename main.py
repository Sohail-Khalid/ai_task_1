from fastapi import FastAPI
from routes import  add_document, chat


app = FastAPI(title="Chatbot with Rag and FastAPI")

app.include_router(add_document.router)
app.include_router(chat.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)


