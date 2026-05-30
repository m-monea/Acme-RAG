from src.rag import ingest_documents


if __name__ == "__main__":
    count = ingest_documents()
    print(f"Indexed {count} document chunks.")
