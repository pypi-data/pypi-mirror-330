"""Job status management utilities for the ZMP Markdown Translator service.

This module provides functions for tracking and updating translation job
status using Redis as a backend store.
"""

import logging

import redis

from zmp_md_translator.config import settings

logger = logging.getLogger(__name__)

# Initialize Redis client
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    password=settings.REDIS_PASS,
    decode_responses=True,
)


def update_job_status(job_id: str, status: str, message: str):
    """Update the status of a translation job.

    Args:
        job_id: Unique identifier for the job
        status: Current status of the job
        message: Detailed status message
    """
    redis_client.hset(job_id, mapping={"status": status, "message": message})
    logger.info(f"Job {job_id} updated: {status} - {message}")


def get_job_status(job_id: str):
    """Retrieve the current status of a translation job.

    Args:
        job_id: Unique identifier for the job

    Returns:
        dict: Job status information including status and message
    """
    return redis_client.hgetall(job_id)
