"""Git operation utilities for the ZMP Markdown Translator service.

This module provides functions for Git operations like cloning repositories,
finding markdown files, and committing changes.
"""

import asyncio
import logging
import os

from git import Repo

from zmp_md_translator.utils.job_status import update_job_status

logger = logging.getLogger(__name__)


async def clone_or_update_repo(
    repo_url: str,
    local_path: str,
    job_id: str,
):
    """Clone or update Git repository."""
    update_job_status(job_id, "In Progress", "Cloning repo...")  # Shortened

    def git_operation():
        if not os.path.exists(local_path):
            logger.info(f"Cloning repository from {repo_url}...")
            Repo.clone_from(repo_url, local_path)
        else:
            logger.info("Repository exists locally. Pulling latest changes...")
            repo = Repo(local_path)
            repo.remotes.origin.pull()

    await asyncio.to_thread(git_operation)


def find_markdown_files(root_dir: str):
    """Find all markdown files in the given directory recursively.

    Args:
        root_dir: Root directory to search for markdown files

    Returns:
        List of paths to markdown files
    """
    md_files = []
    for dirpath, _, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith((".md", ".mdx")):
                md_files.append(os.path.join(dirpath, file))
    return md_files


def commit_and_push_changes(local_path: str, target_language: str):
    """Commit and push translated files to remote repository.

    Args:
        local_path: Local repository path
        target_language: Target language for commit message
    """
    repo = Repo(local_path)
    repo.git.add(A=True)
    commit_message = f"Translated markdown files to {target_language}"
    repo.index.commit(commit_message)
    repo.remotes.origin.push()
