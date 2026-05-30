# Acme Solutions Internal RAG Assistant

A portfolio-ready Retrieval-Augmented Generation project that answers questions using a fictional company's internal knowledge base.

This project uses **free local AI** with Ollama, so it does not require paid API keys.

## What this project demonstrates

- RAG pipeline with document chunking
- Local LLM inference with Ollama
- Local embeddings with `nomic-embed-text`
- Vector search with ChromaDB
- Source citations for answer verification
- CLI chatbot
- Streamlit web interface
- FastAPI endpoint
- Docker-ready structure

## Architecture

```text
Company documents
      ↓
Chunking
      ↓
Embeddings with Ollama
      ↓
ChromaDB vector database
      ↓
Question embedding
      ↓
Similarity search
      ↓
LLM answer with sources
```

## Repository structure

```text
acme-rag-pro/
├── docs/
├── src/
│   ├── config.py
│   ├── rag.py
│   └── utils.py
├── app.py
├── api.py
├── ask.py
├── ingest.py
├── requirements.txt
├── .env.example
├── .gitignore
├── Dockerfile
└── docker-compose.yml
```

## Requirements

Install Ollama first:

https://ollama.com/download

Then pull the free local models:

```bash
ollama pull llama3.2:1b
ollama pull nomic-embed-text
```

## Setup

```bash
git clone https://github.com/m-monea/acme-rag-pro.git
cd acme-rag-pro

python -m venv .venv

# macOS / Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate

pip install -r requirements.txt
cp .env.example .env
```

## Index the documents

```bash
python ingest.py
```

## Ask a question from terminal

```bash
python ask.py "How do I connect to the corporate VPN?"
```

## Run the Streamlit app

```bash
streamlit run app.py
```

## Run the FastAPI server

```bash
uvicorn api:app --reload
```

Then open:

```text
http://127.0.0.1:8000/docs
```

## Example API request

```bash
curl -X POST "http://127.0.0.1:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "What should I do if I receive a phishing email?"}'
```

## Example questions

```text
How do I connect to the corporate VPN?
What is the reimbursement process for business expenses?
How many vacation days do employees receive?
What should I do if I suspect a phishing email?
What are the onboarding steps for a new employee?
Who should I contact during a security incident?
```

## Why this is useful for companies

Many companies have internal documents scattered across folders, wikis, PDFs, and help centers. A RAG assistant helps employees find answers faster while keeping responses grounded in company documents.

## Notes

This is a demo project using a fictional company called Acme Solutions. No private company data is included.
