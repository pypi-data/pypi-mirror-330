"""Configuration module for the markdown translator."""

from typing import ClassVar, Dict

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuration settings for the markdown translator."""

    # Required OpenAI settings
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4o-mini"
    DEFAULT_TARGET_LANGUAGE: str = "Korean"

    # Repository settings
    REPO_BASE_PATH: str = "./repo"
    TARGET_DIR: str = "i18n"

    # Translation settings
    MAX_CHUNK_SIZE: int = 2000
    MAX_CONCURRENT_REQUESTS: int = 15

    # Redis settings
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASS: str = ""

    # Language settings
    SUPPORTED_LANGUAGES: ClassVar[Dict[str, str]] = {
        "ko": "Korean",
        "fr": "French",
        "ja": "Japanese",  # Changed from jp to ja for ISO standard
        "es": "Spanish",
        "de": "German",
        "zh": "Chinese",
        "ru": "Russian",
        "it": "Italian",
        "pt": "Portuguese",
        "ar": "Arabic",
    }

    # Performance tuning
    TRANSLATION_BATCH_SIZE: int = 5  # Number of files to process in parallel

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",
        case_sensitive=False,
    )


# Initialize settings without loading .env file
settings = Settings(_env_file=None)
