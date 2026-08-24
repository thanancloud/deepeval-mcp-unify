# `mcp_runner` Fixture

Session-scoped pytest fixture defined in `conftest.py`. Opens one MCP connection per pytest session (or per xdist worker), shares it across all tests, and closes it cleanly at teardown.

---

## Session Lifecycle

```mermaid
sequenceDiagram
    participant F as conftest fixture
    participant T as _session_task (background Task)
    participant R as MCPConversationRunner
    participant M as MCP Server

    F->>T: asyncio.ensure_future(_session_task)
    T->>R: async with MCPConversationRunner()
    R->>R: get_access_token()
    R->>M: streamablehttp_client connect
    R->>M: ClientSession.initialize()
    R->>M: list_tools()
    M-->>R: 86+ tool definitions
    T->>F: ready.put(runner)
    F->>F: yield runner  (tests run here)
    Note over T: await done.get() — BLOCKED<br/>connection stays alive

    F->>T: done.put(None)  [teardown]
    T->>R: async with exits
    R->>M: disconnect
    T->>F: task completes
```

---

## Agentic Loop (per `run()` call)

```mermaid
flowchart TD
    A([runner.run prompt]) --> B[_refresh_token_if_needed]
    B --> C["messages = [{role:user, content:prompt}]"]
    C --> D{iteration\n≤ 10?}
    D -- no --> Z([return TurnResult])

    D -- yes --> E["Anthropic messages.create\nmodel + tools + messages"]
    E --> F[collect text blocks\ninto final_text]
    F --> G{tool_use blocks\nin response?}

    G -- no or end_turn --> Z
    G -- yes --> H["for each tool_use block:\nsession.call_tool(name, args)"]
    H --> I[MCP Server executes tool]
    I --> J[append ToolCall to result]
    J --> K["append tool_result\nto messages"]
    K --> D
```

---

## Why a Background Task?

`MCPConversationRunner` uses `async with` internally, which creates anyio cancel scopes. A cancel scope must be entered and exited in the **same asyncio Task**.

```mermaid
flowchart LR
    subgraph WRONG ["❌ Naive approach"]
        direction TB
        W1["fixture coroutine\nasync with runner:"] --> W2["yield runner"]
        W2 --> W3["pytest teardown\n(different Task context)"]
        W3 --> W4["async with exits\n→ cancel scope error"]
    end

    subgraph RIGHT ["✅ Background Task pattern"]
        direction TB
        R1["_session_task\n(one Task, never changes)"] --> R2["async with runner:"]
        R2 --> R3["ready.put + done.get\n(BLOCKED — same Task)"]
        R3 --> R4["done.put signals teardown\nasync with exits safely"]
    end
```

Error avoided: `Attempted to exit cancel scope in a different task`

---

## Parallel Execution with `-n 4`

```mermaid
flowchart TD
    C([pytest controller]) --> PS[pytest_sessionstart\npre-fetch OAuth token]
    PS --> W1 & W2 & W3 & W4

    subgraph W1 [Worker 1]
        A1[mcp_runner fixture] --> B1[get_access_token\ncache hit] --> C1[MCP connect\nlist_tools] --> D1[smoke-1, 5, 9, 13, 17]
    end
    subgraph W2 [Worker 2]
        A2[mcp_runner fixture] --> B2[get_access_token\ncache hit] --> C2[MCP connect\nlist_tools] --> D2[smoke-2, 6, 10, 14, 18]
    end
    subgraph W3 [Worker 3]
        A3[mcp_runner fixture] --> B3[get_access_token\ncache hit] --> C3[MCP connect\nlist_tools] --> D3[smoke-3, 7, 11, 15, 19]
    end
    subgraph W4 [Worker 4]
        A4[mcp_runner fixture] --> B4[get_access_token\ncache hit] --> C4[MCP connect\nlist_tools] --> D4[smoke-4, 8, 12, 16, 20]
    end
```

| Mode | MCP connections | OAuth/browser calls |
|------|----------------|---------------------|
| `pytest` (sequential) | 1 | 1 (or 0 if cached) |
| `pytest -n 4` | 4 (one per worker) | 0 (controller pre-fetched) |
| `scope="function"` *(not used)* | 20 | up to 20 |

---

## Related Files

| File | Role |
|------|------|
| `conftest.py` | `mcp_runner` fixture definition |
| `conf/runner.py` | `MCPConversationRunner` — connect, agentic loop, refresh |
| `utils/oauth.py` | `MCPOAuthClient` — token fetch and refresh |
