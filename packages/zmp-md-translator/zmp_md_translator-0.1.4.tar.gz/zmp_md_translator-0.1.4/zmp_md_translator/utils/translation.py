"""Translation utilities for the ZMP Markdown Translator service.

This module provides functions for text chunking and translation using
OpenAI's GPT-3.5 model while preserving markdown formatting.
"""

import logging

from langchain_text_splitters import RecursiveCharacterTextSplitter
from openai import AsyncOpenAI

from zmp_md_translator.config import settings

logger = logging.getLogger(__name__)

# Initialize the client
client = AsyncOpenAI()


async def chunk_text(text: str, max_chunk_size: int = settings.MAX_CHUNK_SIZE):
    """Split text while preserving markdown structure."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=max_chunk_size,
        chunk_overlap=100,
        separators=["\n\n", "\n", ". ", " "],
        keep_separator=True,  # Important to preserve structure
    )
    return splitter.split_text(text)


async def translate_text(
    text: str, target_language: str = settings.DEFAULT_TARGET_LANGUAGE
) -> str:
    """Translate text while preserving markdown structure exactly."""
    messages = [
        {
            "role": "system",
            "content": (
                "You are a markdown translator. Translate the text while "
                "keeping ALL markdown syntax (including whitespace, newlines, "
                "and formatting) exactly the same. The output structure must "
                "match the input structure perfectly."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Translate this markdown to {target_language}. Keep ALL "
                f"formatting identical:\n\n{text}"
            ),
        },
    ]
    response = await client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message.content


async def translate_markdown_content(
    content: str, target_language: str
) -> str:
    """Translate markdown while preserving exact structure."""
    messages = [
        {
            "role": "system",
            "content": (
                "You are a markdown translator. Follow these rules exactly:\n"
                "1. Translate ONLY the text content\n"
                "2. Keep ALL markdown syntax unchanged including:\n"
                "   - Headers (#, ##, etc.)\n"
                "   - Lists (-, *, numbers)\n"
                "   - Links [text](url)\n"
                "   - Images ![alt](url)\n"
                "   - Code blocks (``` and `)\n"
                "   - Tables\n"
                "   - Blockquotes (>)\n"
                "3. Preserve ALL whitespace and newlines\n"
                "4. Keep URLs and code content unchanged\n"
                "5. Output must be exactly like input\n"
                "   - do not add language identifiers\n"
                "6. Do not add ```markdown or"
                "any other language identifiers\n"
            ),
        },
        {
            "role": "user",
            "content": (
                f"Translate this markdown to {target_language}.\n"
                f"Keep ALL formatting identical:\n\n{content}"
            ),
        },
    ]
    response = await client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message.content


async def translate_markdown_file(
    file_path: str, target_language: str, job_id: str
) -> str:
    """Translate markdown file while preserving structure."""
    if not file_path.lower().endswith((".md", ".mdx")):
        raise ValueError("File must be a markdown (.md or .mdx) file")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        logger.error(f"Error reading markdown file {file_path}: {e}")
        raise

    translated = await translate_markdown_content(content, target_language)
    return translated
