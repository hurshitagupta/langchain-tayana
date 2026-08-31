import pytest
from pydantic import ValidationError

from config import Settings


def test_settings_success(monkeypatch):
    monkeypatch.setenv("MODEL_NAME", "openai/gpt-oss-120b")
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
    monkeypatch.setenv("BASE_URL", "https://openrouter.ai/api/v1")
    monkeypatch.setenv("TOP_K", "4")
    monkeypatch.setenv("TIMEOUT_MS", "30000")
    monkeypatch.setenv("MAX_RETRIES", "2")
    monkeypatch.setenv("MAX_STEPS", "2")
    monkeypatch.setenv("MAX_TOKENS", "1000")
    monkeypatch.setenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    monkeypatch.setenv("COLLECTION_NAME", "architecture_docs")
    monkeypatch.setenv("CHUNK_SIZE", "300")
    monkeypatch.setenv("CHUNK_OVERLAP", "50")
    monkeypatch.setenv("KNOWLEDGE_PATH", "data/knowledge.txt")

    settings = Settings(_env_file=None)

    assert settings.top_k == 4
    assert settings.max_steps == 2


def test_settings_failure(monkeypatch):
    monkeypatch.setenv("TOP_K", "0")

    with pytest.raises(ValidationError):
        Settings()