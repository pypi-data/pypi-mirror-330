"""Translation utilities for markdown files."""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import openai
from dotenv import load_dotenv


@dataclass
class TranslationConfig:
    """Configuration for translation behavior."""

    model: str = "gpt-4o-mini"
    preserve_code_blocks: bool = True
    preserve_links: bool = True
    temperature: float = 0.3


class Translator:
    """Core translator class using OpenAI's API."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        config: Optional[TranslationConfig] = None,
    ):
        """Initialize translator with API key and configuration."""
        load_dotenv()
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key must be provided either directly "
                "or via OPENAI_API_KEY environment variable"
            )
        self.config = config or TranslationConfig()
        self.client = openai.OpenAI(api_key=self.api_key)

    def translate_text(self, content: str, target_language: str) -> str:
        """Translate markdown content preserving formatting."""
        prompt = (
            f"Translate the following markdown text to {target_language}.\n"
            "Preserve all markdown formatting, code blocks, and URLs.\n\n"
            f"Text to translate:\n{content}"
        )
        response = self.client.chat.completions.create(
            model=self.config.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional translator "
                        "that preserves markdown formatting."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=self.config.temperature,
        )
        return response.choices[0].message.content

    def translate_file(
        self, source_path: Path, target_path: Path, target_language: str
    ) -> "TranslationResult":
        """Translate markdown file and save to target location."""
        if not source_path.exists():
            raise FileNotFoundError(f"Source file not found: {source_path}")

        target_path.parent.mkdir(parents=True, exist_ok=True)
        content = source_path.read_text(encoding="utf-8")
        translated = self.translate_text(content, target_language)
        target_path.write_text(translated, encoding="utf-8")

        return TranslationResult(success=True, word_count=len(content.split()))


@dataclass
class TranslationResult:
    """Result of a translation operation."""

    success: bool
    word_count: int
