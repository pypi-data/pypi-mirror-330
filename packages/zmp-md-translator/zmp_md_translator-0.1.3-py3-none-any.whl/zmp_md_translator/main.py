#!/usr/bin/env python3
"""CLI application for translating markdown repositories."""

import argparse
import asyncio
import sys

from dotenv import load_dotenv

from zmp_md_translator import MarkdownTranslator, Settings
from zmp_md_translator.types import TranslationProgress


async def progress_callback(progress: TranslationProgress):
    """Handle progress updates."""
    if progress.current_file:
        sys.stderr.write(
            f"\rProcessing {progress.current_file} "
            f"({progress.current}/{progress.total})"
        )
        sys.stderr.flush()


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Translate markdown files in a repository to multiple languages."
    )
    parser.add_argument(
        "--source-dir",
        "-s",
        required=True,
        help="Source directory containing markdown files",
    )
    parser.add_argument(
        "--target-dir",
        "-t",
        default="i18n",
        help="Target directory for translations (default: i18n)",
    )
    parser.add_argument(
        "--languages",
        "-l",
        required=True,
        help="Comma-separated list of target language codes (e.g., ko,ja,fr)",
    )
    parser.add_argument(
        "--model",
        "-m",
        help="OpenAI model to use (overrides .env setting)",
    )
    parser.add_argument(
        "--chunk-size",
        "-c",
        type=int,
        help="Maximum chunk size for translation (overrides .env setting)",
    )
    parser.add_argument(
        "--concurrent",
        "-n",
        type=int,
        help="Maximum concurrent requests (overrides .env setting)",
    )
    return parser.parse_args()


async def main():
    """Run the translator CLI."""
    # Load environment variables
    load_dotenv()

    # Parse command line arguments
    args = parse_args()

    # Create settings with CLI overrides
    settings = Settings()
    if args.model:
        settings.OPENAI_MODEL = args.model
    if args.chunk_size:
        settings.MAX_CHUNK_SIZE = args.chunk_size
    if args.concurrent:
        settings.MAX_CONCURRENT_REQUESTS = args.concurrent

    # Initialize translator
    translator = MarkdownTranslator(
        settings=settings,
        progress_callback=progress_callback,
    )

    # Parse languages
    target_languages = [lang.strip() for lang in args.languages.split(",")]

    try:
        # Run translation
        await translator.translate_repository(
            target_languages=target_languages,
            source_dir=args.source_dir,
            target_dir=args.target_dir,
        )
        return 0
    except Exception as e:
        print(f"\nError: {str(e)}", file=sys.stderr)
        return 1


def run_cli():
    """Synchronous entry point for the CLI."""
    return asyncio.run(main())


if __name__ == "__main__":
    sys.exit(run_cli())
