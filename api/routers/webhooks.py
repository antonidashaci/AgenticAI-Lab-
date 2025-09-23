"""
Webhooks Router

Handles webhook endpoints for external integrations.
"""

from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/job-completed")
async def job_completed_webhook(request: Request):
    """Handle job completion webhook."""
    data = await request.json()
    logger.info(f"Job completed webhook: {data}")
    return {"status": "received"}


@router.post("/platform-callback")
async def platform_callback(request: Request):
    """Handle platform callback webhook."""
    data = await request.json()
    logger.info(f"Platform callback: {data}")
    return {"status": "received"}
