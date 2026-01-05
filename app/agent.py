from typing import Dict, Any
from langgraph.graph import StateGraph, END
from app.rag.retriever import retrieve
from app.tools.weather import get_current_weather
from app.guardrails.policy import guardrail_check

def route(state: Dict[str, Any]) -> str:
    q = state["question"].lower()
    # Simple routing heuristic: weather → tool, otherwise → RAG
    if "weather" in q or "temperature" in q:
        return "tool_weather"
    return "rag_answer"

def tool_weather_node(state):
    question = state.get("question", "")
    city = question.split("in")[-1].strip() if " in " in question.lower() else question.strip()
    result = get_current_weather(city=city, units="celsius")
    return {"question": question, "answer": f"Weather result: {result}", "sources": []}

def rag_answer_node(state):
    question = state.get("question", "")
    docs = retrieve(question, k=4)
    context = "\n\n".join([f"- {d['text']}" for d in docs])
    sources = [d["metadata"].get("source") for d in docs]
    answer = (
        "Grounded answer (from KB snippets):\n"
        f"{context}\n\n"
        "If you want, ask a more specific question and I will narrow the retrieved context."
    )
    return {"question": question, "answer": answer, "sources": sources}

def guardrails_node(state):
    question = state.get("question", "")
    ok, msg = guardrail_check(question)
    if not ok:
        return {"question": question, "answer": msg, "blocked": True, "sources": []}
    return {"question": question, "blocked": False}


def build_agent():
    g = StateGraph(dict)

    g.add_node("guardrails", guardrails_node)
    g.add_node("tool_weather", tool_weather_node)
    g.add_node("rag_answer", rag_answer_node)

    g.set_entry_point("guardrails")

    g.add_conditional_edges(
        "guardrails",
        lambda s: END if s.get("blocked") else route(s),
        {END: END, "tool_weather": "tool_weather", "rag_answer": "rag_answer"}
    )

    g.add_edge("tool_weather", END)
    g.add_edge("rag_answer", END)

    return g.compile()

AGENT = build_agent()

def run_agent(question: str):
    result = AGENT.invoke({"question": question})
    return result.get("answer", ""), result.get("sources", [])

