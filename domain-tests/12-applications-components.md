# Domain: Applications & Components
**Tools covered (6):** `branches_list`, `repositories_list`, `repositories_search`, `scm_branches_list`, `scm_gh_app_registrations_list`, `scm_repositories_sync`
**Total prompts:** 18 (6 positive, 6 negative, 6 edge)

> **Cross-domain tools used for setup:** `user_whoami` (default), `organizations_list` (default), `services_list` (default), `endpoint_list` (organization-administration)

---

## Test Execution Tracker

| ID | Type | Category | Expected Tools | Timeout | Status | Notes |
|----|------|----------|----------------|---------|--------|-------|
| AC-P01 | Positive | Chain | `organizations_list` → `repositories_list` | 20s | ⬜ | |
| AC-P02 | Positive | Chain | `repositories_list` → `repositories_search` | 25s | ⬜ | |
| AC-P03 | Positive | Chain | `services_list` → `branches_list` | 25s | ⬜ | |
| AC-P04 | Positive | Chain | `organizations_list` → `scm_gh_app_registrations_list` | 20s | ⬜ | |
| AC-P05 | Positive | Chain | `endpoint_list` → `repositories_list` → `scm_branches_list` | 40s | ⬜ | |
| AC-P06 | Positive | Chain | `organizations_list` → `scm_gh_app_registrations_list` → `scm_repositories_sync` | 40s | ⬜ | |
| AC-N01 | Negative | Selection | `repositories_search` (no match) | 15s | ⬜ | |
| AC-N02 | Negative | Selection | `branches_list` (nil component) | 15s | ⬜ | |
| AC-N03 | Negative | Selection | `scm_branches_list` (nil endpointId) | 15s | ⬜ | |
| AC-N04 | Negative | Selection | `scm_repositories_sync` (nil org) | 15s | ⬜ | |
| AC-N05 | Negative | Selection | `repositories_list` (nil org) | 15s | ⬜ | |
| AC-N06 | Negative | Selection | `scm_gh_app_registrations_list` (nil org) | 15s | ⬜ | |
| AC-E01 | Edge | Chain | `repositories_list` → `repositories_search` (full name exact match) | 25s | ⬜ | |
| AC-E02 | Edge | Chain | `services_list` → `branches_list` (component with 1 branch) | 25s | ⬜ | |
| AC-E03 | Edge | Chain | `services_list` → `branches_list` (verify default branch present) | 25s | ⬜ | |
| AC-E04 | Edge | Chain | `organizations_list` → `scm_repositories_sync` → `repositories_list` (before/after count) | 60s | ⬜ | |
| AC-E05 | Edge | Chain | `endpoint_list` → `scm_branches_list` (repo with many branches) | 40s | ⬜ | |
| AC-E06 | Edge | Chain | `services_list` → `repositories_list` → `repositories_search` (cross-verify) | 40s | ⬜ | |

---

## Diagnostic Categories

| Category | Definition | Failure Indicates |
|----------|-----------|-------------------|
| **Selection** | Single tool call from natural language | AI picked the wrong tool from 131 options |
| **Chain** | 2–4 tools called in sequence | Wrong tool order, missed step, or incorrect data passed between steps |
| **Stress** | 5+ tools OR repeated calls OR large payloads | Timeout, session limit, or token exhaustion |

---

## Test Setup

> Resolve all IDs at runtime.
> Call `organizations_list` for org ID; `services_list` for component IDs; `endpoint_list` for SCM endpoint/connector IDs.
> Nil UUID for negative tests: `00000000-0000-0000-0000-000000000099`

---

## POSITIVE TEST CASES

---

### AC-P01 — List Repositories for an Organization
**Discovery:** `Chain` | **Expected:** `organizations_list → repositories_list` | **Timeout:** `20s`

```
Call organizations_list to get the current org ID.
Call repositories_list for that organization.
Report: total repository count, each repo's name, SCM provider (GitHub, etc.), and URL.
```

---

### AC-P02 — Search Repositories by Partial Name
**Discovery:** `Chain` | **Expected:** `repositories_list → repositories_search` | **Timeout:** `25s`

```
Call repositories_list to get the first repository's name.
Extract a 3–5 character partial string from that name.
Call repositories_search using that partial string.
Verify the known repository appears in the search results.
Report: total results found, and whether the expected repo is present.
```

---

### AC-P03 — List Branches for a Component
**Discovery:** `Chain` | **Expected:** `services_list → branches_list` | **Timeout:** `25s`

```
Call services_list to find a component (type=COMPONENT).
Call branches_list for that component using its organization ID.
Report: total branch count, each branch's name, last commit hash, and author.
```

---

### AC-P04 — List GitHub App Registrations
**Discovery:** `Chain` | **Expected:** `organizations_list → scm_gh_app_registrations_list` | **Timeout:** `20s`

```
Call organizations_list to get the org ID.
Call scm_gh_app_registrations_list for that organization.
Report: each registered GitHub App's name and app URL.
If no registrations exist, record "0 GitHub App registrations — empty result OK".
```

---

### AC-P05 — List SCM Branches via SCM Provider
**Discovery:** `Chain` | **Expected:** `endpoint_list → repositories_list → scm_branches_list` | **Timeout:** `40s`

```
1. Call organizations_list to get the org ID.
2. Call endpoint_list for the org to find SCM connector endpoints.
3. From the results, get an endpointId (SCM connector UUID).
4. Call repositories_list to get a repository.
5. Call scm_branches_list with the endpointId and repository name.
Report: branch names returned from the SCM provider directly.
If no SCM connector is found, record "No SCM connector endpoint found — test skipped".
```

---

### AC-P06 — Trigger SCM Repository Sync
**Discovery:** `Chain` | **Expected:** `organizations_list → scm_gh_app_registrations_list → scm_repositories_sync` | **Timeout:** `40s`

```
1. Call organizations_list to get the org ID.
2. Call scm_gh_app_registrations_list to confirm an SCM integration exists.
3. If an integration exists, call scm_repositories_sync for the org.
4. Report the response (job ID, status, or acknowledgement).
5. Call repositories_list after a brief moment — verify the sync was initiated.
If no SCM integration exists, record "No SCM integration found — test skipped".
```

---

## NEGATIVE TEST CASES

---

### AC-N01 — Repository Search with No Matching Results
**Discovery:** `Selection` | **Expected:** `repositories_search` | **Timeout:** `15s`

```
Call repositories_search using "xyzzy-repo-no-match-9999999".
Record the exact response. Expected: empty results array or 0 results — NOT an error.
```

---

### AC-N02 — List Branches for Non-Existent Component
**Discovery:** `Selection` | **Expected:** `branches_list` | **Timeout:** `15s`

```
Call branches_list with a nil component ID: 00000000-0000-0000-0000-000000000099.
Record the exact error message and HTTP status code. Expected: 404 or 400.
```

---

### AC-N03 — SCM Branches List with Invalid Endpoint ID
**Discovery:** `Selection` | **Expected:** `scm_branches_list` | **Timeout:** `15s`

```
Call scm_branches_list with a nil endpointId: 00000000-0000-0000-0000-000000000099 and repository name "fake-repo".
Record the exact error message and HTTP status code. Expected: 404 or 400.
```

---

### AC-N04 — SCM Repository Sync with Non-Existent Org
**Discovery:** `Selection` | **Expected:** `scm_repositories_sync` | **Timeout:** `15s`

```
Call scm_repositories_sync with a nil org ID: 00000000-0000-0000-0000-000000000099.
Record the exact error message and HTTP status code. Expected: 404 or 400.
```

---

### AC-N05 — List Repositories for Non-Existent Org
**Discovery:** `Selection` | **Expected:** `repositories_list` | **Timeout:** `15s`

```
Call repositories_list with a nil org ID: 00000000-0000-0000-0000-000000000099.
Record the exact error message and HTTP status code. Expected: 404 or 400.
```

---

### AC-N06 — List GitHub App Registrations for Non-Existent Org
**Discovery:** `Selection` | **Expected:** `scm_gh_app_registrations_list` | **Timeout:** `15s`

```
Call scm_gh_app_registrations_list with a nil org ID: 00000000-0000-0000-0000-000000000099.
Record the exact error message and HTTP status code. Expected: 404 or 400.
```

---

## EDGE CASES

---

### AC-E01 — Exact Name Match in Repository Search
**Discovery:** `Chain` | **Expected:** `repositories_list → repositories_search` | **Timeout:** `25s`

```
Call repositories_list to get an exact repository name.
Call repositories_search using the full exact name.
Verify: exactly one result is returned matching that name.
Compare: does the exact-match search return the same repository object as the list?
```

---

### AC-E02 — List Branches for Component with Single Branch
**Discovery:** `Chain` | **Expected:** `services_list → branches_list` | **Timeout:** `25s`

```
Call services_list to find components.
Identify a component likely to have only one branch (e.g., a simple or new service).
Call branches_list for that component.
Verify: at least one branch is returned and the call does not error on small branch counts.
```

---

### AC-E03 — Verify Default Branch Is Listed for Every Component
**Discovery:** `Chain` | **Expected:** `services_list → branches_list` | **Timeout:** `25s`

```
Call services_list to get up to 3 components.
For each component, call branches_list.
Verify: for each component, at least one branch is listed. Note if any component returns an empty branch list.
Report: which components have branches and which (if any) return empty.
```

---

### AC-E04 — Repository Count Before and After Sync
**Discovery:** `Chain` | **Expected:** `organizations_list → repositories_list → scm_repositories_sync → repositories_list` | **Timeout:** `60s`

```
1. Call organizations_list to get the org ID.
2. Call repositories_list — record the total count (before sync).
3. Call scm_repositories_sync.
4. Call repositories_list again — record the new total count (after sync).
Report: did the count change? Were any new repositories added?
Note: the sync is asynchronous — a count change is possible but not guaranteed immediately.
```

---

### AC-E05 — SCM Branches for Repository with Many Branches
**Discovery:** `Chain` | **Expected:** `endpoint_list → repositories_list → scm_branches_list` | **Timeout:** `40s`

```
1. Call organizations_list to get the org ID.
2. Call endpoint_list to get an SCM connector endpoint ID.
3. Call repositories_list to find a repository (prefer one expected to have many branches).
4. Call scm_branches_list for that repository.
Report: total branch count returned, whether pagination is indicated in the response.
If no SCM connector, record "No SCM connector — test skipped".
```

---

### AC-E06 — Cross-Verify Repositories via List and Search
**Discovery:** `Chain` | **Expected:** `services_list → repositories_list → repositories_search` | **Timeout:** `40s`

```
1. Call services_list to get a component's associated repository name (if available).
2. Call repositories_list — find that repository in the full list.
3. Call repositories_search with the same repository name.
4. Verify: the repository appears in both results and the data is consistent (same name, same URL).
Report any fields that differ between the list and search responses.
```
