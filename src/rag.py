from typing import Dict, List
import chromadb
import ollama

from src.config import (
    CHROMA_DIR,
    COLLECTION_NAME,
    DOCS_DIR,
    EMBED_MODEL,
    MODEL_NAME,
    TOP_K,
)
from src.utils import load_markdown_documents, chunk_text


def get_collection():
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    return client.get_or_create_collection(name=COLLECTION_NAME)


def embed_text(text: str) -> List[float]:
    response = ollama.embeddings(model=EMBED_MODEL, prompt=text)
    return response["embedding"]


def ingest_documents() -> int:
    collection = get_collection()
    documents = load_markdown_documents(DOCS_DIR)

    ids = []
    texts = []
    embeddings = []
    metadatas = []

    for doc in documents:
        chunks = chunk_text(doc["text"])

        for index, chunk in enumerate(chunks):
            chunk_id = f"{doc['source']}-{index}"

            ids.append(chunk_id)
            texts.append(chunk)
            embeddings.append(embed_text(chunk))
            metadatas.append(
                {
                    "source": doc["source"],
                    "chunk": index,
                }
            )

    if ids:
        collection.upsert(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    return len(ids)


def retrieve_context(question: str, top_k: int = TOP_K) -> List[Dict[str, str]]:
    collection = get_collection()
    question_embedding = embed_text(question)

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=top_k,
    )

    contexts = []

    for doc, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        contexts.append(
            {
                "text": doc,
                "source": metadata["source"],
                "distance": distance,
            }
        )

    return contexts


def build_prompt(question: str, contexts: List[Dict[str, str]]) -> str:
    context_block = "\n\n".join(
        [
            f"Source: {item['source']}\nContent:\n{item['text']}"
            for item in contexts
        ]
    )

    return f"""
You are Acme Solutions internal assistant.

Answer the user question using only the context below.
If the context does not contain the answer, say:
"I could not find that information in the Acme knowledge base."

Be clear, practical, and concise.

Context:
{context_block}

Question:
{question}

Answer:
""".strip()


def answer_question(question: str) -> Dict[str, object]:
    contexts = retrieve_context(question)
    prompt = build_prompt(question, contexts)

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    sources = sorted({item["source"] for item in contexts})

    return {
        "answer": response["message"]["content"].strip(),
        "sources": sources,
        "contexts": contexts,
    }
