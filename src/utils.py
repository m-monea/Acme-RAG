from pathlib import Path
from typing import List, Dict


def load_markdown_documents(docs_dir: str) -> List[Dict[str, str]]:
    """Load all Markdown documents from a folder."""
    docs_path = Path(docs_dir)

    if not docs_path.exists():
        raise FileNotFoundError(f"Docs folder not found: {docs_dir}")

    documents = []

    for file_path in sorted(docs_path.glob("*.md")):
        text = file_path.read_text(encoding="utf-8").strip()
        if text:
            documents.append(
                {
                    "source": file_path.name,
                    "text": text,
                }
            )

    return documents


def chunk_text(text: str, chunk_size: int = 900, overlap: int = 120) -> List[str]:
    """Split text into overlapping chunks."""
    if chunk_size <= overlap:
        raise ValueError("chunk_size must be larger than overlap")

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks
