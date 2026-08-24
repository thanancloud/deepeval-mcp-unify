"""
MCPConversationRunner: connects to the CloudBees MCP server via OAuth, then runs
an Anthropic LLM agentic loop that calls MCP tools in response to natural-language
prompts. Returns every tool call made along with the model's final text response.
"""

from __future__ import annotations

import os
from contextlib import AsyncExitStack
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import anthropic
from dotenv import load_dotenv
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
  
from utils.oauth import MCPOAuthClient

load_dotenv(Path(__file__).parent / ".env")

MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "https://mcp.saas-qa.beescloud.com/v1/mcp")
RUNNER_MODEL_PROVIDER = os.getenv("RUNNER_MODEL_PROVIDER", "anthropic").lower()
MODEL_ID = os.getenv("ANTHROPIC_MODEL_ID", "claude-sonnet-4-5")
BEDROCK_MODEL_ID = os.getenv("AWS_BEDROCK_MODEL_ID", "us.anthropic.claude-sonnet-4-5-20250929-v1:0")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
MAX_TOOL_ITERATIONS = 10


def _build_anthropic_client():
    if RUNNER_MODEL_PROVIDER == "bedrock":
        return anthropic.AnthropicBedrock(
            aws_region=AWS_REGION,
            aws_profile=os.getenv("AWS_PROFILE"),
            
        )
    return anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


@dataclass
class ToolCall:
    name: str
    input_params: dict[str, Any]
    raw_output: str
    mcp_result: Any = None  # mcp.types.CallToolResult — required by MCPToolCall


@dataclass
class TurnResult:
    prompt: str
    tool_calls: list[ToolCall] = field(default_factory=list)
    final_text: str = ""


class MCPConversationRunner:
    """
    Manages a single MCP session and runs multi-turn Anthropic agentic loops.

    Usage:
        runner = MCPConversationRunner()
        await runner.connect()
        result = await runner.run("Who am I on CloudBees?")
        await runner.disconnect()

    Or use as an async context manager:
        async with MCPConversationRunner() as runner:
            result = await runner.run(...)
    """

    def __init__(self) -> None:
        self._session: ClientSession | None = None
        self._tools: list[dict] = []
        self._anthropic = _build_anthropic_client()
        self._model_id = BEDROCK_MODEL_ID if RUNNER_MODEL_PROVIDER == "bedrock" else MODEL_ID
        self._exit_stack = AsyncExitStack()

    # ── Lifecycle ──────────────────────────────────────────────────────────────

    async def __aenter__(self) -> "MCPConversationRunner":
        token = await MCPOAuthClient().get_access_token()
        headers = {"Authorization": f"Bearer {token}"}

        read, write, _ = await self._exit_stack.enter_async_context(
            streamablehttp_client(MCP_SERVER_URL, headers=headers)
        )
        self._session = await self._exit_stack.enter_async_context(
            ClientSession(read, write)
        )
        await self._session.initialize()
        tools_result = await self._session.list_tools()
        self._tools = [
            {
                "name": t.name,
                "description": t.description or "",
                "input_schema": t.inputSchema,
            }
            for t in tools_result.tools
        ]
        return self

    async def __aexit__(self, *_: object) -> None:
        await self._exit_stack.aclose()
        self._session = None
        self._exit_stack = AsyncExitStack()

    async def connect(self) -> None:
        await self.__aenter__()

    async def disconnect(self) -> None:
        await self.__aexit__(None, None, None)

    @property
    def tools(self) -> list[dict]:
        return self._tools

    # ── Diagnostic helper ──────────────────────────────────────────────────────

    async def test_connect(self) -> None:
        """Quick connectivity check — prints tool count and exits."""
        await self.connect()
        print(f"[ok] Connected. {len(self._tools)} tools available.")
        await self.disconnect()

    # ── Token refresh ──────────────────────────────────────────────────────────

    async def _refresh_token_if_needed(self) -> None:
        """Re-open the MCP connection with a fresh token if expiry is within 2 minutes.

        Uses the OAuth refresh_token grant — no browser required unless the
        refresh token itself has expired, in which case the browser flow runs.
        """
        client = MCPOAuthClient()
        if not client.is_token_expiring_soon(buffer_seconds=120):
            return
        await self.__aexit__(None, None, None)
        await client.refresh_access_token()
        await self.__aenter__()

    # ── Agentic loop ───────────────────────────────────────────────────────────

    async def run(self, prompt: str) -> TurnResult:
        """
        Send one user prompt and run the agentic loop until the model stops
        calling tools or MAX_TOOL_ITERATIONS is reached.
        """
        await self._refresh_token_if_needed()
        assert self._session, "Call connect() before run()"

        result = TurnResult(prompt=prompt)
        messages: list[dict] = [{"role": "user", "content": prompt}]

        for _ in range(MAX_TOOL_ITERATIONS):
            response = self._anthropic.messages.create(
                model=self._model_id,
                max_tokens=4096,
                tools=self._tools,
                messages=messages,
            )

            # Collect the assistant's reply
            messages.append({"role": "assistant", "content": response.content})

            # Gather text blocks for final_text
            for block in response.content:
                if block.type == "text":
                    result.final_text += block.text

            # Check for tool use
            tool_use_blocks = [b for b in response.content if b.type == "tool_use"]

            if not tool_use_blocks or response.stop_reason == "end_turn":
                break

            # Execute each tool and feed results back
            tool_results = []
            for block in tool_use_blocks:
                mcp_result = await self._session.call_tool(
                    block.name, arguments=block.input or {}
                )

                raw = ""
                for content_block in mcp_result.content:
                    if hasattr(content_block, "text"):
                        raw += content_block.text

                result.tool_calls.append(
                    ToolCall(
                        name=block.name,
                        input_params=dict(block.input or {}),
                        raw_output=raw,
                        mcp_result=mcp_result,
                    )
                )

                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": raw,
                    }
                )

            messages.append({"role": "user", "content": tool_results})

        return result
