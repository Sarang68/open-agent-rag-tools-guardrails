# Open Agent: Tools + RAG + Guardrails (Open Source)

A reference implementation of an **AI agent architecture** that combines:

- **Tools / Action Groups**: deterministic function execution (example: Weather lookup)
- **RAG / Knowledge Base**: PDF ingestion + embeddings + vector retrieval (ChromaDB)
- **Guardrails**: input policy gate (example: profanity filter)

This repo is intentionally designed as a **learning blueprint**: simple, inspectable, and easy to extend.

---

## Architecture (high level)

**Online request path**
1. Client
