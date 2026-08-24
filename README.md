# DeepEval MCP Test Suite — Documentation

This suite evaluates the CloudBees Unify MCP server by running natural-language prompts through an Anthropic agentic loop, measuring whether the agent selected the right MCP tools with the right arguments, and producing a self-contained HTML dashboard from the results.

---

## Table of Contents

1. [Token Generation](#1-token-generation)
2. [mcp_runner fixture](#2-mcp_runner-fixture)
3. [eval_model fixture](#3-eval_model-fixture)
4. [Single-Turn Test — What Gets Measured](#4-single-turn-test--what-gets-measured)
5. [Report Generation](#5-report-generation)
6. [How to Run](#6-how-to-run)
7. [Q&A](#7-qa)

---

## 1. Token Generation

The suite authenticates with the CloudBees MCP server via OAuth 2.0 Authorization Code + PKCE. A headed browser is only opened when no valid cached token exists. The token is pre-fetched once on the pytest controller before any worker spawns.

**Detailed diagrams:** [token-generation.md](token-generation.md)

Key points:
- `.auth-tokens.json` — stores `access_token`, `refresh_token`, `expires_in`, `issued_at`
- Controller pre-fetch via `pytest_sessionstart` (guard: `not hasattr(session.config, "workerinput")`)
- Expiry buffers: 60 s (cache validity) and 120 s (proactive mid-run refresh)
- Mid-run refresh via `_refresh_token_if_needed()` at the top of every `runner.run()` — no browser if `refresh_token` is valid

---

## 2. `mcp_runner` fixture

Defined in `conftest.py`. Session-scoped — one MCP connection per pytest session (or per xdist worker). Opens the connection once, holds it alive across all tests, closes cleanly at session teardown.

**Detailed diagrams:** [mcp-runner.md](mcp-runner.md)

Key points:
- Background Task pattern keeps the `async with` lifetime in one Task to satisfy anyio's cancel-scope constraint
- Agentic loop: up to 10 tool-call iterations per `run()` call
- `scope="session"`: one OAuth + MCP handshake per worker instead of one per test
- With `-n 4`: 4 MCP connections (one per worker), 0 browser launches (token pre-fetched)

---

## 3. `eval_model` fixture

Defined in `conftest.py`. Session-scoped — the judge LLM wrapper is constructed once and shared across all test items.

**Detailed diagrams:** [eval-model.md](eval-model.md)

| `EVAL_MODEL_PROVIDER` | Model used | Notes |
|----------------------|-----------|-------|
| `anthropic` (default) | `None` | DeepEval reads `ANTHROPIC_API_KEY` automatically |
| `bedrock` | `AmazonBedrockModel` | Requires `AWS_BEDROCK_MODEL_ID`, `AWS_REGION` |
| `gemini` | `GeminiModel` | Requires `GEMINI_MODEL_ID`, `GOOGLE_API_KEY` |

Fixture runs lazily after `load_dotenv()` fires — safer than a module-level constant which would run at import time before env vars are available.

---

## 4. Single-Turn Test — What Gets Measured

Each parametrized item (`test_smoke[smoke-N]`) is a **single turn**: one prompt → one agentic loop → one evaluation. No conversation history is carried from one test to the next.

**Detailed diagrams:** [single-turn-test.md](single-turn-test.md)

### Score breakdown

| Score | Question answered | Range |
|-------|------------------|-------|
| **Primitive Usage Score** | Did the agent select the correct MCP tool from the 86+ available? | 0.0 – 1.0 |
| **Argument Correctness Score** | Were the arguments passed to the tool valid and appropriate? | 0.0 – 1.0 |
| **Overall Score** | Weighted combination. Threshold = **0.7** | 0.0 – 1.0 |

Threshold 0.7 means partial credit can still pass. Each `run()` starts with `messages = [{"role": "user", "content": prompt}]` — no cross-test context.

---

## 5. Report Generation

After the test run, `generate_report.py` merges all per-test JSON files into one self-contained HTML dashboard.

**Detailed diagrams:** [report-generation.md](report-generation.md)

```bash
# Merge all reports/*.json automatically
python utils/generate_report.py

# Explicit files
python utils/generate_report.py reports/test_run_20260824_164341.json
```

Dashboard features: summary cards, filter toolbar (All/Passed/Failed + search), results table, click-through detail overlay, dark/light theme toggle (persisted in `localStorage`).

---

## 6. How to Run

### Prerequisites

```bash
pip install -r requirements.txt
playwright install chromium
cp .env.example .env   # fill in credentials
```

### Required `.env` values

```
MCP_SERVER_URL=https://mcp.saas-qa.beescloud.com/v1/mcp
MCP_TEST_USER_EMAIL=your@email.com
MCP_TEST_USER_PASSWORD=yourpassword
MCP_ORG_ID=<organization-uuid>
ANTHROPIC_API_KEY=sk-ant-...        # for the runner LLM
EVAL_MODEL_PROVIDER=anthropic       # or bedrock / gemini
```

### Run patterns

```bash
# Single test case
pytest tests/test_smoke.py -k smoke-1 -v

# Subset of cases
pytest tests/test_smoke.py -k "smoke-1 or smoke-2 or smoke-3" -v

# Full suite — sequential
pytest tests/test_smoke.py -v

# Full suite — parallel (4 workers, browser opens once)
pytest tests/test_smoke.py -n 4 -v

# Re-run only previously failed cases
pytest tests/test_smoke.py --last-failed -v

# Target a specific item by full ID
pytest "tests/test_smoke.py::test_smoke[smoke-14]" -v

# Generate HTML dashboard after the run
python utils/generate_report.py

# Open the latest report
open reports/$(ls -t reports/report_*.html | head -1 | xargs basename)
```

### Collect-only (dry run)

```bash
pytest tests/test_smoke.py --collect-only -q
# Prints all smoke test IDs: test_smoke[smoke-1] … test_smoke[smoke-N]
```

---

## 7. Q&A

### Does each test get a fresh MCP client or the same one with previous context?

**Shared client, stateless conversations.** The MCP connection is shared via `scope="session"`. But each `runner.run()` call starts a brand-new `messages` list — no LLM context carries over from one test to the next.

### Does sharing the client slow things down?

**No — it makes things faster.** OAuth + MCP handshake happen once per worker instead of once per test. With `scope="function"` they'd repeat 20 times.

### What happens if the token expires mid-run?

**Without the fix:** `401 Unauthorized` propagates and crashes all remaining tests in the worker.

**With the fix:** `_refresh_token_if_needed()` fires 120 s before expiry, silently refreshes via `grant_type=refresh_token` (no browser), and re-opens the connection — all before the next `run()` call.

### Why does `pytest -n 4` launch the browser 4 times?

Each xdist worker is a separate OS process. All 4 start simultaneously, all find no cached token, all launch a browser. Fix: `pytest_sessionstart` on the controller pre-fetches the token before workers spawn; workers hit the cache and skip the browser.

### Why does `eval_model` use `scope="session"` not `scope="function"`?

Session scope guarantees construction happens after `load_dotenv()` and before the first test. One wrapper across 20 tests also avoids redundant instantiations.
