# Single-Turn Test — What Gets Measured

Each parametrized item (`test_smoke[smoke-N]`) is a **single turn**: one prompt in, one agentic loop, one evaluation. No conversation history carries from one test to the next.

---

## Full Test Flow

```mermaid
flowchart TD
    A([test_smoke smoke-N]) --> B

    subgraph EXEC [Step 1 — Execution]
        B["mcp_runner.run(case.prompt)"]
        B --> B1["LLM receives:\nprompt + 86 available tool definitions"]
        B1 --> B2{tool_use\nblock?}
        B2 -- yes --> B3["call_tool(name, args)\n→ MCP server → result"]
        B3 --> B4["feed result back\ninto messages"]
        B4 --> B2
        B2 -- no / end_turn --> B5["TurnResult\n(prompt, tool_calls[], final_text)"]
    end

    B5 --> C

    subgraph ASSEMBLE [Step 2 — Test Case Assembly]
        C["LLMTestCase(\n  input = original prompt\n  actual_output = final_text\n  mcp_servers = [86+ available tools]\n  mcp_tools_called = [name, args, mcp_result]\n)"]
    end

    C --> D

    subgraph EVAL [Step 3 — Evaluation]
        D["MCPUseMetric(threshold=0.7, model=eval_model)"]
        D --> D1["Judge LLM scores:\nPrimitive Usage Score\nArgument Correctness Score"]
        D1 --> D2["Overall Score\n0.0 – 1.0"]
    end

    D2 --> E

    subgraph REPORT [Step 4 — Report Write]
        E["DisplayConfig(file_type='html')\n→ reports/test_run_*.json\n→ reports/evaluation_*.html"]
    end

    E --> F{score\n>= 0.7?}
    F -- yes --> G([✅ pytest PASS])
    F -- no --> H(["❌ pytest FAIL\nscore=X.XX < 0.7\nReason: ..."])
```

---

## Score Breakdown

```mermaid
flowchart LR
    TC["LLMTestCase"] --> M["MCPUseMetric\njudge LLM"]

    M --> PS["Primitive Usage Score\nDid the agent pick\nthe RIGHT tool?"]
    M --> AC["Argument Correctness Score\nWere the args\ncorrect for that tool?"]

    PS & AC --> OS["Overall Score\nweighted combination"]

    OS --> T{">= 0.7?"}
    T -- yes --> P(["✅ PASS"])
    T -- no  --> F(["❌ FAIL"])
```

### Score examples

| Scenario | Prim Use | Arg Correct | Overall |
|----------|----------|-------------|---------|
| Right tool, right args | 1.00 | 1.00 | 1.00 |
| Right tool, wrong args | 1.00 | 0.00 | ~0.50 |
| Partial tool match | 0.50 | 1.00 | 0.50 |
| Wrong tool entirely | 0.25 | 0.00 | 0.00 |

Threshold **0.7** means partial credit can still pass — the agent doesn't need to be perfect on every call.

---

## "Single Turn" Explained

```mermaid
sequenceDiagram
    participant T1 as test smoke-13
    participant T2 as test smoke-14
    participant R as runner.run()

    T1->>R: run("List all memberships...")
    Note over R: messages = [{role:user, content:...}]
    R-->>T1: TurnResult

    T2->>R: run("Remove the first user...")
    Note over R: messages = [{role:user, content:...}]
    Note over R: Fresh list — no memory of smoke-13
    R-->>T2: TurnResult
```

Each `run()` call starts with `messages = [{"role": "user", "content": prompt}]`. There is no shared conversation state. `smoke-14` has zero knowledge of what `smoke-13` did — the LLM context is fully isolated per test.

---

## What the Evaluation Judge Sees

```mermaid
flowchart TD
    J["Evaluation LLM\neval_model"]

    J --> Q1["Available tools:\nlist of 86+ MCPServer tools"]
    J --> Q2["Tools actually called:\n[MCPToolCall(name, args, result)]"]
    J --> Q3["Original prompt:\nwhat the user asked"]
    J --> Q4["Agent final answer:\nactual_output"]

    Q1 & Q2 & Q3 & Q4 --> S1["Score: did agent pick\nthe right primitive?"]
    Q2 & Q3 --> S2["Score: were args\ncorrect for the intent?"]

    S1 --> R1["Primitive Usage Score + Reason"]
    S2 --> R2["Argument Correctness Score"]
```

---

## Related Files

| File | Role |
|------|------|
| `tests/test_smoke.py` | Parametrized test function |
| `tests/test_cases.py` | `EvalCase` definitions (prompt + expected tool) |
| `conf/runner.py` | Agentic loop — `run()` method |
| `conftest.py` | `mcp_runner` and `eval_model` fixtures |
