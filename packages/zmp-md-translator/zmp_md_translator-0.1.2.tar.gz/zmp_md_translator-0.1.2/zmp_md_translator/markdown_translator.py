"""High-performance markdown translator using OpenAI's GPT models."""

import asyncio
import os
import time
from typing import List, Optional

import aiofiles
import colorlog
from openai import AsyncOpenAI

from .settings import Settings
from .types import ProgressCallback, TranslationProgress, TranslationStatus


class MarkdownTranslator:
    """High-performance markdown translator using OpenAI's GPT models."""

    MODEL_TOKEN_LIMITS = {
        "gpt-3.5-turbo": 4096,
        "gpt-4": 8192,
        "gpt-4o-mini": 128000,
    }

    CHARS_PER_TOKEN = 4

    def __init__(
        self,
        settings: Optional[Settings] = None,
        progress_callback: Optional[ProgressCallback] = None,
    ):
        """Initialize the translator with settings and callbacks."""
        self.settings = settings or Settings()
        self._setup_logger()
        self.client = AsyncOpenAI(api_key=self.settings.OPENAI_API_KEY)

        self.api_semaphore = asyncio.Semaphore(self.settings.MAX_CONCURRENT_REQUESTS)
        self.progress_callback = progress_callback
        self.completed_tasks = 0

    def _setup_logger(self):
        """Set up logging system with color formatting and timestamps."""
        logger = colorlog.getLogger("markdown_translator")
        if not logger.handlers:
            handler = colorlog.StreamHandler()
            formatter = colorlog.ColoredFormatter(
                "%(log_color)s[%(asctime)s] %(message)s",
                log_colors={
                    "DEBUG": "cyan",
                    "INFO": "green",
                    "WARNING": "yellow",
                    "ERROR": "red",
                    "CRITICAL": "red,bg_white",
                },
                datefmt="%Y-%m-%d %H:%M:%S.%f",
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel("INFO")

    async def _report_progress(
        self,
        status: TranslationStatus,
        total: int,
        current_file: Optional[str] = None,
        message: Optional[str] = None,
    ):
        """
        Report translation progress through the callback function.

        Args:
            status (TranslationStatus): Current translation status
            total (int): Total number of files to process
            current_file (Optional[str]): Name of the file being processed
            message (Optional[str]): Additional status message
        """
        if self.progress_callback:
            progress = TranslationProgress(
                status=status,
                current=self.completed_tasks,
                total=total,
                current_file=current_file,
                message=message,
            )
            await self.progress_callback(progress)

    async def translate_repository(
        self,
        target_languages: List[str],
        source_dir: str,
        target_dir: Optional[str] = None,
    ):
        """
        Translate all markdown files in a repository.

        Args:
            target_languages (List[str]): List of language codes
                to translate to.
            source_dir (str): Directory containing markdown files.
            target_dir (Optional[str]): Directory to store translations.
                Defaults to "i18n".
        """
        logger = colorlog.getLogger("markdown_translator")
        start_time = time.time()
        total_tasks = 0

        try:
            await self._report_progress(TranslationStatus.PREPARING, 0)

            # Use source_dir directly
            source_path = os.path.abspath(source_dir)

            if not os.path.exists(source_path):
                raise ValueError(f"Source directory not found: {source_path}")

            # Determine target base directory
            # (relative to current working directory)
            target_base = target_dir or "i18n"
            base_dir = os.path.abspath(target_base)

            # Determine the last part of the source_dir
            source_basename = (
                os.path.basename(os.path.normpath(source_dir)).lower().split("_")[-1]
            )  # Get the last part after underscore

            # Build language-specific target prefixes based on source_basename
            lang_target_prefixes = {}
            for lang in target_languages:
                if source_basename in ["zcp", "ZCP"]:
                    prefix = os.path.join(
                        base_dir,
                        lang,
                        "docusaurus-plugin-content-docs-zcp",
                        "current",
                    )
                elif source_basename in ["apim", "APIM"]:
                    prefix = os.path.join(
                        base_dir,
                        lang,
                        "docusaurus-plugin-content-docs-apim",
                        "current",
                        lang,  # Add language code for APIM
                    )
                elif source_basename in ["amdp", "AMDP"]:
                    prefix = os.path.join(
                        base_dir,
                        lang,
                        "docusaurus-plugin-content-docs-amdp",
                        "current",
                    )
                else:
                    prefix = os.path.join(
                        base_dir,
                        lang,
                        "docusaurus-plugin-content-docs",
                        "current",
                    )

                # Create the target directory
                os.makedirs(prefix, exist_ok=True)
                lang_target_prefixes[lang] = prefix

            # Find markdown files
            source_files = []
            for root, _, files in os.walk(source_path):
                for file in files:
                    if file.endswith((".md", ".mdx")):
                        file_abs = os.path.join(root, file)
                        rel_path = os.path.relpath(file_abs, source_path)
                        source_files.append(rel_path)

            total_tasks = len(source_files) * len(target_languages)
            if total_tasks == 0:
                logger.info("No markdown files found to translate")
                return True

            # Log progress
            files_count = len(source_files)
            langs_count = len(target_languages)
            logger.info(
                f"Found {files_count} files to translate "
                f"into {langs_count} languages"
            )
            logger.info(
                f"Starting translation of {files_count} files "
                f"to {langs_count} languages ({total_tasks} tasks)"
            )

            # Process translations

            await self._report_progress(TranslationStatus.TRANSLATING, total_tasks)
            all_tasks = []

            for file_path in source_files:
                content = await self._read_file(os.path.join(source_path, file_path))
                content_size = len(content)
                file_tasks = []

                for lang in target_languages:
                    target_prefix = lang_target_prefixes[lang]

                    # For APIM, we need to ensure the language directory exists
                    if source_basename in ["apim", "APIM"]:
                        lang_dir = os.path.join(target_prefix)
                        os.makedirs(lang_dir, exist_ok=True)

                    # Join the target prefix with the source file's relative path
                    target_path = os.path.join(target_prefix, file_path)
                    file_tasks.append(
                        self._translate_and_write(
                            content=content,
                            content_size=content_size,
                            target_path=target_path,
                            lang=lang,
                            total_tasks=total_tasks,
                            start_time=time.time(),
                        )
                    )
                all_tasks.append(asyncio.gather(*file_tasks))

            # Process in batches
            batch_size = self.settings.MAX_CONCURRENT_REQUESTS
            for i in range(0, len(all_tasks), batch_size):
                batch = all_tasks[i : i + batch_size]
                await asyncio.gather(*batch)

            # Log completion
            elapsed = time.time() - start_time
            if total_tasks > 0:
                per_file = elapsed / total_tasks
                logger.info(
                    "Translation completed in " f"{elapsed:.2f}s ({per_file:.2f}s/file)"
                )

            await self._report_progress(TranslationStatus.COMPLETED, total_tasks)
            logger.info("All translations completed successfully")
            return True

        except Exception as e:
            logger.error(f"Translation failed: {str(e)}")
            await self._report_progress(
                TranslationStatus.FAILED, total_tasks, message=str(e)
            )
            raise

    async def _translate_and_write(
        self,
        content: str,
        content_size: int,
        target_path: str,
        lang: str,
        total_tasks: int,
        start_time: float,
    ):
        """
        Translate content and write to target file while tracking performance.

        Handles chunking of large files, parallel translation of chunks,
        and maintains file system structure.

        Args:
            content (str): Content to translate
            content_size (int): Size of content in characters
            target_path (str): Path where translated file will be written
            lang (str): Target language code
            total_tasks (int): Total number of translation tasks
            start_time (float): Start time for performance tracking

        Raises:
            Exception: If translation or file writing fails
        """
        logger = colorlog.getLogger("markdown_translator")

        try:
            # Pre-create directory
            os.makedirs(os.path.dirname(target_path), exist_ok=True)

            async with self.api_semaphore:
                if content_size > self.settings.MAX_CHUNK_SIZE:
                    chunks = self._split_content(content, self.settings.MAX_CHUNK_SIZE)
                    # Process chunks in parallel
                    translations = await asyncio.gather(
                        *[self._translate_single_chunk(chunk, lang) for chunk in chunks]
                    )
                    translated_content = "\n".join(translations)
                else:
                    translated_content = await self._translate_single_chunk(
                        content, lang
                    )

            # Write translation
            async with aiofiles.open(target_path, "w", encoding="utf-8") as f:
                await f.write(translated_content)

            elapsed = time.time() - start_time
            rel_path = os.path.relpath(target_path)
            logger.info(f"✓ {rel_path} [{lang}] ({elapsed:.2f}s)")

            self.completed_tasks += 1
            await self._report_progress(
                TranslationStatus.TRANSLATING,
                total_tasks,
                current_file=f"{rel_path} [{lang}]",
            )

        except Exception as e:
            logger.error(f"Failed to translate to {lang}: {str(e)}")
            raise

    async def _read_file(self, path: str) -> str:
        """
        Read file content asynchronously.

        Args:
            path (str): Path to the file to read

        Returns:
            str: Content of the file

        Raises:
            FileNotFoundError: If file doesn't exist
            IOError: If file cannot be read
        """
        async with aiofiles.open(path, "r", encoding="utf-8") as f:
            return await f.read()

    def _calculate_chunk_size(self, content_size: int) -> int:
        """
        Calculate optimal chunk size based on content size and model limits.

        Adjusts chunk size dynamically based on content size to optimize
        translation performance and token usage.

        Args:
            content_size (int): Size of content in characters

        Returns:
            int: Optimal chunk size in characters
        """
        model_token_limit = self.MODEL_TOKEN_LIMITS.get(
            self.settings.OPENAI_MODEL, 4096
        )
        base_size = (model_token_limit // 2) * self.CHARS_PER_TOKEN

        # Adjust chunk size based on content size
        if content_size < 1000:
            return base_size
        elif content_size < 3000:
            return base_size * 2
        else:
            return base_size * 3  # Larger chunks for big files

    def _split_content(self, content: str, max_chunk_size: int) -> List[str]:
        """
        Split content into chunks while preserving markdown structure.

        Ensures that markdown formatting is not broken across chunks
        by splitting at appropriate boundaries.

        Args:
            content (str): Content to split
            max_chunk_size (int): Maximum size of each chunk

        Returns:
            List[str]: List of content chunks
        """
        chunks = []
        current_chunk = []
        current_size = 0

        for line in content.split("\n"):
            line_size = len(line)
            if current_size + line_size > max_chunk_size and current_chunk:
                chunks.append("\n".join(current_chunk))
                current_chunk = []
                current_size = 0
            current_chunk.append(line)
            current_size += line_size + 1  # +1 for newline

        if current_chunk:
            chunks.append("\n".join(current_chunk))

        return chunks

    async def _translate_single_chunk(self, chunk: str, target_language: str) -> str:
        """Translate a single chunk of text using the OpenAI API."""
        prompt = (
            f"Translate the following technical documentation to {target_language}.\n"
            "Critical requirements:\n"
            "1. EXACT STRUCTURE: The output must have exactly the same number of lines as the input\n"
            "2. HTML/MARKDOWN: Keep ALL tags, attributes, and markdown syntax exactly as is\n"
            "3. CODE/PATHS: Never translate code blocks, URLs, file paths, or HTML/markdown syntax\n"
            "4. WHITESPACE: Preserve all indentation, empty lines, and spacing exactly\n"
            "5. TRANSLATION SCOPE: Only translate human-readable text content\n"
            "6. TECHNICAL TERMS: Keep technical terms in English if they are standard terms\n"
            "7. VERIFICATION: Each closing tag must match its opening tag exactly\n\n"
            "Example of what to translate:\n"
            "- '# Heading' -> Translate 'Heading' only, keep '#' and spacing\n"
            "- '<div class=\"example\">' -> Keep exactly as is, no translation\n"
            "- 'This is text' -> Translate this part\n\n"
            f"Text to translate:\n{chunk}"
        )

        response = await self.client.chat.completions.create(
            model=self.settings.OPENAI_MODEL,
            messages=[
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
                {"role": "user", "content": prompt},
            ],
            temperature=0.0,  # Use 0 for maximum consistency
        )

        return response.choices[0].message.content

    def _find_markdown_files(self, source_dir: str) -> List[str]:
        """Find all markdown files in the source directory.

        Args:
            source_dir (str): Directory to search for markdown files

        Returns:
            List[str]: List of relative paths to markdown files

        Raises:
            ValueError: If source directory is not found
        """
        source_path = os.path.abspath(source_dir)
        if not os.path.exists(source_path):
            raise ValueError(f"Source directory not found: {source_path}")

        source_files = []
        for root, _, files in os.walk(source_path):
            for file in files:
                if file.endswith((".md", ".mdx")):
                    file_abs = os.path.join(root, file)
                    rel_path = os.path.relpath(file_abs, source_path)
                    source_files.append(rel_path)

        return source_files
