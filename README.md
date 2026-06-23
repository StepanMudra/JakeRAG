# JakeRAG — Temporal Knowledge Archive

Jake is a time traveler from 2326. He survived the Machine War. He knows things.

This project gives Jake a long-term memory using RAG (Retrieval-Augmented Generation) — so when you ask him about the future, he actually knows the answer.

Built with Ollama + ChromaDB + Discord.py. Part 4 of the [Building Local AI with Ollama](https://medium.com/@mudrastepan/gave-discord-bot-memory-building-local-ai-with-ollama-part-4-2f447c0934a6) series.

---

## How it works

```
Your question → ChromaDB (vector search) → relevant context → TimeTraveler LLM → Jake's answer
```

1. `ingest.py` reads markdown files from `Documents/Jake/`, chunks them by headers, embeds with `nomic-embed-text` and stores in ChromaDB
2. `rag.py` takes a question, finds the 3 most relevant chunks, and sends them as context to the TimeTraveler model
3. `TimeTravelerBot.py` connects the RAG pipeline to a Discord bot

---

## Requirements

- [Ollama](https://ollama.com) installed and running
- TimeTraveler model from [Part 2](https://medium.com/p/a9c246c4b64a) of the series
- `nomic-embed-text` model pulled

```bash
ollama pull nomic-embed-text
```

---

## Installation

```bash
git clone https://github.com/StepanMudra/JakeRAG
cd JakeRAG
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Fill in your Discord bot token in `.env`.

---

## Usage

**1. Add your documents**

Put markdown files into `Documents/Jake/`. Jake will know everything in them.

**2. Ingest documents**

```bash
python3 ingest.py
```

**3. Test in terminal**

```bash
python3 rag.py
```

**4. Run Discord bot**

```bash
python3 TimeTravelerBot.py
```

Then in Discord: `!ms Who are you?`

---

## Project structure

```
JakeRAG/
├── Documents/
│   └── Jake/          ← markdown knowledge base
├── ingest.py          ← chunks and embeds documents into ChromaDB
├── rag.py             ← RAG query pipeline
├── TimeTravelerBot.py ← Discord bot
├── requirements.txt
└── .env.example
```

---

*Be weird!*
