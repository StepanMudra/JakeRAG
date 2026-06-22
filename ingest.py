import ollama
import chromadb
from pathlib import Path

DOCS_PATH = Path(__file__).parent / "Documents" / "Jake"
DB_PATH = str(Path(__file__).parent / "chroma_db")
EMBED_MODEL = "nomic-embed-text"
COLLECTION_NAME = "jake_knowledge"


def chunk_markdown(text: str, filename: str) -> list[dict]:
    chunks = []
    current_lines = []
    current_header = filename.replace(".md", "")

    for line in text.split("\n"):
        if line.startswith("## ") or line.startswith("# "):
            if current_lines:
                chunk_text = "\n".join(current_lines).strip()
                if len(chunk_text) > 50:
                    chunks.append({
                        "text": chunk_text,
                        "source": filename,
                        "header": current_header,
                    })
            current_header = line.lstrip("#").strip()
            current_lines = [line]
        else:
            current_lines.append(line)

    if current_lines:
        chunk_text = "\n".join(current_lines).strip()
        if len(chunk_text) > 50:
            chunks.append({
                "text": chunk_text,
                "source": filename,
                "header": current_header,
            })

    return chunks


def ingest():
    client = chromadb.PersistentClient(path=DB_PATH)

    try:
        client.delete_collection(COLLECTION_NAME)
        print("Existing collection deleted.")
    except Exception:
        pass

    collection = client.create_collection(COLLECTION_NAME)

    all_chunks = []
    for md_file in sorted(DOCS_PATH.glob("*.md")):
        text = md_file.read_text(encoding="utf-8")
        chunks = chunk_markdown(text, md_file.name)
        all_chunks.extend(chunks)
        print(f"{md_file.name}: {len(chunks)} chunks")

    print(f"\nEmbedding {len(all_chunks)} chunks with {EMBED_MODEL}...")

    for i, chunk in enumerate(all_chunks):
        response = ollama.embeddings(model=EMBED_MODEL, prompt=chunk["text"])
        collection.add(
            ids=[f"chunk_{i}"],
            embeddings=[response["embedding"]],
            documents=[chunk["text"]],
            metadatas=[{"source": chunk["source"], "header": chunk["header"]}],
        )
        if (i + 1) % 10 == 0 or (i + 1) == len(all_chunks):
            print(f"  {i + 1}/{len(all_chunks)}")

    print(f"\n Finished — {len(all_chunks)} chunks saved to ChromaDB")


if __name__ == "__main__":
    ingest()
