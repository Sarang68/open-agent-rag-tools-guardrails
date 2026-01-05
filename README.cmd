# Open Agent: Tools + RAG + Guardrails (Open Source)

A reference implementation of an **AI agent architecture** that combines:

- **Tools / Action Groups**: deterministic function execution (example: Weather lookup)
- **RAG / Knowledge Base**: PDF ingestion + embeddings + vector retrieval (ChromaDB)
- **Guardrails**: input policy gate (example: profanity filter)

This repo is intentionally designed as a **learning blueprint**: simple, inspectable, and easy to extend.

---

## Architecture (high level)

**Online request path**
1. Client sends a question to `POST /ask`
2. **Guardrails** run first (allow/block)
3. **LangGraph** routes intent:
   - **Tool path** → weather function → Open-Meteo APIs → return result
   - **RAG path** → retrieve chunks from ChromaDB → return grounded snippets

**Offline / batch ingestion**
PDF → chunk → embed → store vectors in ChromaDB → query-time retrieval.

---

## Tech stack

- **API**: FastAPI + Uvicorn
- **Agent Orchestration**: LangGraph
- **PDF Parsing**: pypdf
- **Embeddings Model**: `sentence-transformers/all-MiniLM-L6-v2`
- **Vector DB**: ChromaDB (local persistent)
- **Tool**: Open-Meteo (Geocoding + Forecast) — **no API key**
- **Guardrails**: rule-based policy gate + profanity filter (extensible)

---

## Repository layout

app/
main.py # FastAPI entrypoint (/ask)
agent.py # LangGraph orchestration (guardrails → route → tool/RAG)
config.py # settings via env vars
tools/
weather.py # tool: Open-Meteo weather lookup
rag/
ingest.py # PDF ingestion pipeline (chunk + embed + store)
retriever.py # ChromaDB read/write + top-K retrieval
guardrails/
policy.py # guardrail_check() allow/block logic
profanity.py # profanity list + detector

Local-only directories (should NOT be committed):
- `data/` (your PDFs)
- `chroma_db/` (vector store)
- `.env`
- `.venv/`

---

## Prerequisites

- Python **3.12+** recommended (3.13 may work but can be noisier with some deps)
- Git

---

## Quickstart (recommended: venv, not conda)

### 1) Create and activate a virtual environment

macOS / Linux:
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
Windows (PowerShell):
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
2) Install dependencies
pip install -r requirements.txt
3) Create your local env file
cp .env.example .env
4) Ingest a PDF into the Knowledge Base (ChromaDB)
Create a data/ folder and place your PDF inside (do not commit PDFs to public repos):
mkdir -p data
python -m app.rag.ingest data/your_document.pdf
You should see something like:
Ingested XXX chunks.
5) Run the API
Always run uvicorn through the active interpreter to avoid environment mismatch:
python -m uvicorn app.main:app --reload --port 8000
Server will be available at:
http://127.0.0.1:8000
Docs: http://127.0.0.1:8000/docs
API usage
Weather tool example (Tool path)
curl -X POST "http://127.0.0.1:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question":"What is the weather in Mumbai in Celsius?"}'
RAG example (Knowledge Base path)
curl -X POST "http://127.0.0.1:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question":"Summarize key risks mentioned in the 10-K."}'
Guardrails example (Blocked input)
If your profanity list includes badword1:
curl -X POST "http://127.0.0.1:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question":"this contains badword1"}'
Expected response:
{"answer":"Request blocked by guardrails (profanity).","sources":[]}
Configuration
Settings are defined in app/config.py and can be overridden via .env.
Common variables:

CHROMA_PERSIST_DIR (default: chroma_db)
COLLECTION_NAME (must be 3–63 chars, e.g., kb_store)
ENABLE_PROFANITY_FILTER (true/false)
Example .env:
CHROMA_PERSIST_DIR=chroma_db
COLLECTION_NAME=kb_store
ENABLE_PROFANITY_FILTER=true
ANONYMIZED_TELEMETRY=FALSE
Troubleshooting
1) “ModuleNotFoundError: chromadb” when running uvicorn
This almost always means uvicorn is running from a different Python environment (e.g., conda base).
Fix:

source .venv/bin/activate
python -m uvicorn app.main:app --reload --port 8000
Verify:
which python
python -m pip -V
python -c "import chromadb; print('chromadb OK')"
2) Chroma collection name errors
Collection names must be 3–63 characters and match naming rules.
Use something like:
kb_store
knowledge_base
kb001
Set in .env:
COLLECTION_NAME=kb_store
3) PDF parsing warnings like “Ignoring wrong pointing object…”
These warnings are common for some PDFs. If ingestion prints Ingested X chunks, you are generally fine.
If you ingest and retrieve empty text, try another PDF or a different parser strategy.
4) Chroma telemetry warnings
If you see telemetry warnings, disable telemetry:
export ANONYMIZED_TELEMETRY=FALSE
Or add it to .env.
Extending this project
Ideas for “production-hardening”:
Replace heuristic routing with LLM tool calling (structured tool selection + args)
Add page-level citations (chunk metadata: page number, offsets)
Add evaluation harness (groundedness, regression prompts)
Add observability (structured logs: retrieval hits, tool calls, guardrail blocks)
Upgrade guardrails (NeMo Guardrails / moderation models / injection detection)
Security notes
Do not commit private PDFs, proprietary data, or .env secrets.
Treat outputs as assistive; verify answers for regulated/high-stakes domains.
License
This repository is licensed under the terms of the LICENSE file included in this repo.
Acknowledgements
This repo demonstrates a common “agent blueprint” used across enterprise and open-source ecosystems:
Guardrails → Route → Tool or Retrieve → Respond.
If you build something interesting on top of this, consider opening a PR or sharing your fork.
