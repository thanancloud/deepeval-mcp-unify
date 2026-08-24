# Token Generation

The suite authenticates with the CloudBees MCP server via OAuth 2.0 Authorization Code + PKCE. A headed browser is only opened when no valid cached token exists. The token is pre-fetched once on the pytest controller before any worker spawns.

---

## Pre-fetch Flow (pytest startup)

```mermaid
flowchart TD
    A([pytest start]) --> B{{"pytest_sessionstart\n(controller only)"}}
    B --> C{workerinput\non config?}
    C -- yes = worker --> Z([skip — worker process])
    C -- no = controller --> D[MCPOAuthClient.get_access_token]

    D --> E{.auth-tokens.json\nexists & valid?}
    E -- yes --> F([return cached access_token\nno browser])
    E -- no --> G{refresh_token\nin cache?}

    G -- yes --> H["POST /token\ngrant_type=refresh_token\nno browser"]
    H --> I{HTTP 200?}
    I -- yes --> J[save new tokens\nto .auth-tokens.json]
    J --> K([return access_token])
    I -- no --> L

    G -- no --> L[full browser PKCE flow\nPlaywright + localhost:3000]
    L --> M[save tokens\nto .auth-tokens.json]
    M --> K

    K --> N{{xdist workers spawn}}
    N --> O["each worker:\nmcp_runner.__aenter__()"]
    O --> P["_load_cached() → HIT"]
    P --> Q([skip browser\nuse cached token])
```

---

## Mid-run Token Refresh

Called at the top of every `runner.run()` — proactively reconnects before the token dies.

```mermaid
flowchart TD
    A([runner.run called]) --> B[_refresh_token_if_needed]
    B --> C{is_token_expiring_soon\nbuffer = 120s?}
    C -- no --> Z([proceed with run\nzero overhead])
    C -- yes --> D[__aexit__\nclose MCP connection]
    D --> E[refresh_access_token]

    E --> F{refresh_token\nin cache?}
    F -- yes --> G["POST /token\ngrant_type=refresh_token"]
    G --> H{HTTP 200?}
    H -- yes --> I[save new tokens]
    H -- no --> J
    F -- no --> J[full browser PKCE flow]
    J --> I

    I --> K[__aenter__\nre-open MCP connection\nwith fresh token]
    K --> Z
```

---

## Token Cache File — `.auth-tokens.json`

| Field | Description |
|-------|-------------|
| `access_token` | Bearer token sent in every MCP request |
| `refresh_token` | Used to get a new access token without a browser |
| `expires_in` | Lifetime in seconds (typically 3600) |
| `issued_at` | Unix timestamp (ms) set when the token was saved |

**Expiry buffers:**

| Buffer | Used in | Meaning |
|--------|---------|---------|
| 60 s | `_load_cached()` | "Is this token usable right now?" |
| 120 s | `is_token_expiring_soon()` | "Should I proactively refresh before the next test?" |

---

## Why the Controller Guard?

`pytest_sessionstart` runs on every process — both the controller and each xdist worker. The guard `not hasattr(session.config, "workerinput")` ensures only the **controller** pre-fetches. xdist sets `workerinput` on worker processes; the controller does not have it.

Without the guard, all 4 workers would race to open the browser simultaneously when no token is cached.

---

## Related files

| File | Role |
|------|------|
| `utils/oauth.py` | `MCPOAuthClient` — PKCE flow, token cache, refresh |
| `conftest.py` | `pytest_sessionstart` hook, `mcp_runner` fixture |
| `.auth-tokens.json` | Runtime token cache (git-ignored) |
