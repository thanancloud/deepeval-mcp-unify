"""
Smoke tests for all active CloudBees Unify MCP tools.

Each SMOKE_CASES entry runs as an independent pytest item (test_smoke[smoke-N]).
The MCP session is opened once per pytest session (session-scoped mcp_runner).
Each test evaluates its own LLMTestCase and writes its own report to reports/.

Useful run patterns:
    pytest                                          # run all cases
    pytest -k smoke-6                               # run one case by ID
    pytest -k "smoke-1 or smoke-2"                  # run a subset
    pytest --last-failed                            # re-run only failures
    pytest test_smoke.py::test_smoke[smoke-14]      # fully-qualified item ID
    pytest -n auto                                  # parallel with pytest-xdist
"""

from __future__ import annotations

import asyncio

import pytest
from deepeval import evaluate
from deepeval.evaluate import DisplayConfig
from deepeval.metrics import MCPUseMetric
from deepeval.test_case import LLMTestCase, MCPServer, MCPToolCall

from conf.runner import MCPConversationRunner
from tests.test_cases import SMOKE_CASES

REPORTS_DIR = "./reports"


@pytest.mark.asyncio
@pytest.mark.parametrize("case", SMOKE_CASES, ids=[c.id for c in SMOKE_CASES])
async def test_smoke(mcp_runner: MCPConversationRunner, eval_model, case) -> None:
    result = await mcp_runner.run(case.prompt)

    mcp_server = MCPServer(
        server_name="cloudbees-unify-mcp",
        available_tools=mcp_runner.tools,
    )
    mcp_tools_called = [
        MCPToolCall(
            name=tc.name,
            args=tc.input_params,
            result=tc.mcp_result,
        )
        for tc in result.tool_calls
    ]
    test_case = LLMTestCase(
        input=result.prompt,
        actual_output=result.final_text,
        mcp_servers=[mcp_server],
        mcp_tools_called=mcp_tools_called,
    )

    metric = MCPUseMetric(threshold=0.7, model=eval_model)
    loop = asyncio.get_event_loop()
    eval_result = await loop.run_in_executor(
        None,
        lambda: evaluate(
            test_cases=[test_case],
            metrics=[metric],
            display_config=DisplayConfig(
                file_type="html",
                file_output_dir=REPORTS_DIR,
                results_folder=REPORTS_DIR,
                truncate_passing_cases=False,
            ),
        ),
    )

    failed = [r for r in eval_result.test_results if not r.success]
    assert not failed, (
        f"[{case.id}] "
        + "; ".join(
            f"{m.name} score={m.score:.2f} < {m.threshold}"
            for m in (failed[0].metrics_data or [])
            if not m.success
        )
    )
