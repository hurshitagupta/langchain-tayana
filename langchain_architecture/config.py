from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_name: str
    openrouter_api_key: str
    base_url: str

    top_k: int = Field(ge=1, le=20)
    timeout_ms: int = Field(gt=0)
    max_retries: int = Field(ge=0, le=5)
    max_steps: int = Field(ge=1)
    max_tokens: int = Field(ge=1)

    embedding_model: str
    collection_name: str
    chunk_size: int = Field(gt=0)
    chunk_overlap: int = Field(ge=0)
    knowledge_path: str

    model_config = SettingsConfigDict(env_file=".env")