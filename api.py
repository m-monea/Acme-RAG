from fastapi import FastAPI
from pydantic import BaseModel
from src.rag import answer_question

app = FastAPI(
    title="Acme Solutions RAG API",
    description="A simple local RAG API using Ollama and ChromaDB.",
    version="1.0.0",
)


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def health_check():
    return {"status": "ok", "message": "Acme RAG API is running"}


@app.post("/ask")
def ask(request: QuestionRequest):
    return answer_question(request.question)
