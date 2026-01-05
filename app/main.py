from fastapi import FastAPI
from pydantic import BaseModel
from app.agent import run_agent

app = FastAPI(title="Open Agent: Tools + RAG + Guardrails")

class Query(BaseModel):
    question: str

@app.post("/ask")
def ask(q: Query):
    answer, sources = run_agent(q.question)
    return {"answer": answer, "sources": sources}

