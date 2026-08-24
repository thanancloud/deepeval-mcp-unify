"""Shared pytest fixtures for the deepeval-mcp test suite."""

from __future__ import annotations

import asyncio
import os
from pathlib import Path
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from deepeval.models import AmazonBedrockModel, GeminiModel
from dotenv import load_dotenv

from utils.oauth import MCPOAuthClient
from conf.runner import MCPConversationRunner

load_dotenv(Path(__file__).parent / ".env")


def pytest_sessionstart(session) -> None:
    """Pre-fetch the OAuth token before xdist workers are spawned.

    With -n N, this runs only on the controller process (workers have
    config.workerinput set). By the time workers start, .auth-tokens.json
    exists and every worker's mcp_runner skips the browser flow entirely.
    Also runs harmlessly for non-parallel invocations.
    """
    if not hasattr(session.config, "workerinput"):
        asyncio.run(MCPOAuthClient().get_access_token())


@pytest_asyncio.fixture(scope="session")
async def mcp_runner() -> AsyncGenerator[MCPConversationRunner, None]:
    """Session-scoped MCP runner.

    The entire MCP session lives inside one background asyncio Task so that
    anyio's internal cancel scopes are always entered and exited in the same
    task, avoiding 'Attempted to exit cancel scope in a different task' errors.
    """
    ready: asyncio.Queue[MCPConversationRunner | Exception] = asyncio.Queue()
    done: asyncio.Queue[None] = asyncio.Queue()

    async def _session_task() -> None:
        try:
            async with MCPConversationRunner() as runner:
                await ready.put(runner)
                await done.get()
        except Exception as exc:
            await ready.put(exc)

    task = asyncio.ensure_future(_session_task())
    result = await ready.get()
    if isinstance(result, Exception):
        raise result

    try:
        yield result
    finally:
        await done.put(None)
        await task


@pytest.fixture(scope="session")
def eval_model():
    provider = os.getenv("EVAL_MODEL_PROVIDER", "anthropic").lower()
    if provider == "bedrock":
        return AmazonBedrockModel(
            model=os.getenv("AWS_BEDROCK_MODEL_ID", "us.anthropic.claude-sonnet-4-5-20250929-v1:0"),
            region=os.getenv("AWS_REGION", "us-east-1"),
        )
    if provider == "gemini":
        return GeminiModel(
            model=os.getenv("GEMINI_MODEL_ID", "gemini-2.5-flash"),
            api_key=os.getenv("GOOGLE_API_KEY"),
        )
    return None  # anthropic: deepeval reads ANTHROPIC_API_KEY automatically
