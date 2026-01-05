from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # LLM choice:
    # - "ollama" for local
    # - "openai" if you later want OpenAI-compatible hosted endpoint
    LLM_PROVIDER: str = "ollama"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_CHAT_MODEL: str = "llama3.1"
    OLLAMA_EMBED_MODEL: str = "nomic-embed-text"

    # RAG / Vector DB
    CHROMA_PERSIST_DIR: str = "chroma_db"
    COLLECTION_NAME: str = "kb_store"
    # Simple guardrails
    ENABLE_PROFANITY_FILTER: bool = True

settings = Settings()

