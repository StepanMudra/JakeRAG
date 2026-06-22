import ollama
import chromadb
from pathlib import Path

DB_PATH = str(Path(__file__).parent / "chroma_db")
EMBED_MODEL = "nomic-embed-text"
LLM_MODEL = "TimeTraveler"
COLLECTION_NAME = "jake_knowledge"
TOP_K = 3


def query(question: str) -> str:
    client = chromadb.PersistentClient(path=DB_PATH)
    collection = client.get_collection(COLLECTION_NAME)

    embed = ollama.embeddings(model=EMBED_MODEL, prompt=question)
    results = collection.query(
        query_embeddings=[embed["embedding"]],
        n_results=TOP_K,
    )

    context_parts = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        context_parts.append(f"[{meta['source']} — {meta['header']}]\n{doc}")
    context = "\n\n---\n\n".join(context_parts)

    prompt = f"""Below is relevant information from my personal knowledge archive about the future.
Use it to answer the question. Stay in character.

{context}

Question: {question}"""

    response = ollama.chat(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        think=False,
    )
    return response["message"]["content"]


def main():
    print("Jake RAG — Temporal Knowledge Archive")
    print("Ask Jake anything about the future. Type 'quit' to exit.\n")

    while True:
        try:
            question = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            break

        if not question:
            continue
        if question.lower() in ("quit", "exit", "q"):
            break

        print("\nJake:", query(question), "\n")


if __name__ == "__main__":
    main()
