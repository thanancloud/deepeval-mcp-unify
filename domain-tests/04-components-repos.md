
# Domain: Components & Repositories
**Tools covered (19):** `repositories_list`, `repositories_search`, `branches_list`, `runs_list`, `logs_list`, `actions_list`, `resources_list`, `properties_list`, `endpoint_list`, `controllers_list`, `controllers_data_get`, `report_drilldown_get`, `api_tokens_list`, `saml_connections_list`, `saml_email_domains_list`, `extensions_list`, `scm_branches_list`, `scm_gh_app_registrations_list`, `scm_repositories_sync`
**Total prompts:** 36 (12 positive, 12 negative, 12 edge cases)

---

## Test Execution Tracker

| ID | Type | Category | Expected Tools | Timeout | Description | Status | Notes |
|----|------|----------|----------------|---------|-------------|--------|-------|
| CR-P01 | Positive | Selection | ~~`components_list`~~ | — | ⬛ | Tool removed |
| CR-P02 | Positive | Chain | ~~`components_search (x3)`~~ | — | ⬛ | Tool removed |
| CR-P03 | Positive | Chain | `repositories_list -> repositories_search` | 30s | List and search repositories across SCM providers | ⬜ | |
| CR-P04 | Positive | Chain | `branches_list (x2)` | 30s | List branches for a component with multiple branches | ⬜ | |
| CR-P05 | Positive | Selection | `endpoint_list` | 15s | List endpoints — verify all integration types | ⬜ | |
| CR-P06 | Positive | Selection | `properties_list` | 15s | List properties for a component (inherited secret) | ⬜ | |
| CR-P07 | Positive | Chain | `resources_list -> branches_list` | 30s | List resources (branches) for a component | ⬜ | |
| CR-P08 | Positive | Chain | `api_tokens_list -> saml_connections_list -> saml_email_domains_list` | 30s | Auth audit: API tokens, SAML connections, email domains | ⬜ | |
| CR-P09 | Positive | Selection | `actions_list` | 15s | List all actions in the organization | ⬜ | |
| CR-P10 | Positive | Chain | `scm_repositories_sync -> repositories_list` | 30s | SCM repositories sync — trigger and verify response | ⬜ | |
| CR-P11 | Positive | Selection | `extensions_list` | 15s | List extensions for the organization | ⬜ | |
| CR-P12 | Positive | Selection | `scm_gh_app_registrations_list` | 15s | List GitHub App registrations for the organization | ⬜ | |
| CR-N01 | Negative | Selection | ~~`components_create`~~ | — | ⬛ | Tool removed |
| CR-N02 | Negative | Selection | ~~`components_create`~~ | — | ⬛ | Tool removed |
| CR-N03 | Negative | Selection | ~~`components_delete`~~ | — | ⬛ | Tool removed |
| CR-N04 | Negative | Selection | `branches_list` | 15s | List branches for non-existent component | ⬜ | |
| CR-N05 | Negative | Selection | `runs_list` | 15s | List runs for non-existent component | ⬜ | |
| CR-N06 | Negative | Chain | `controllers_list -> controllers_data_get` | 30s | Get controller data with no controllers in org | ⬜ | |
| CR-N07 | Negative | Selection | `report_drilldown_get` | 15s | Get report drilldown with no controllers in org | ⬜ | |
| CR-N08 | Negative | Selection | `repositories_list` | 15s | List repositories for non-existent org | ⬜ | |
| CR-N09 | Negative | Selection | `properties_list` | 15s | List properties for non-existent component | ⬜ | |
| CR-N10 | Negative | Selection | `scm_branches_list` | 15s | List SCM branches with invalid endpointId | ⬜ | |
| CR-N11 | Negative | Selection | `scm_branches_list` | 15s | List SCM branches with non-existent repository URL | ⬜ | |
| CR-N12 | Negative | Selection | `extensions_list` | 15s | List extensions with invalid organizationId | ⬜ | |
| CR-E01 | Edge | Selection | ~~`components_list`~~ | — | ⬛ | Tool removed |
| CR-E02 | Edge | Chain | ~~`repositories_list -> components_list`~~ | — | ⬛ | Tool removed |
| CR-E03 | Edge | Selection | ~~`components_list`~~ | — | ⬛ | Tool removed |
| CR-E04 | Edge | Chain | `endpoint_list (x3+)` | 45s | Endpoint list — paginate through all results | ⬜ | |
| CR-E05 | Edge | Chain | `saml_connections_list -> saml_email_domains_list` | 30s | SAML configured org vs non-configured — compare responses | ⬜ | |
| CR-E06 | Edge | Selection | `actions_list` | 15s | Actions list — verify large response is handled | ⬜ | |
| CR-E07 | Edge | Stress | ~~`endpoint_list -> components_create -> components_list -> components_search -> branches_list -> components_delete`~~ | — | ⬛ | Tool removed (components_create/delete/list/search) |
| CR-E08 | Edge | Selection | `repositories_search` | 15s | Cross-provider repo search (GitHub + GitLab + Bitbucket) | ⬜ | |
| CR-E09 | Edge | Chain | `runs_list (x2)` | 30s | Runs list with limit parameter | ⬜ | |
| CR-E10 | Edge | Chain | `repositories_list -> scm_repositories_sync -> repositories_list` | 45s | SCM sync then repo list — verify repo count changes | ⬜ | |
| CR-E11 | Edge | Chain | ~~`scm_branches_list -> components_search -> branches_list`~~ | — | ⬛ | Tool removed (components_search) |
| CR-E12 | Edge | Chain | `extensions_list (x3)` | 30s | Extensions list with filterInstalled=true vs false | ⬜ | |

---

## Diagnostic Categories

| Category | Definition | Failure Indicates |
|----------|-----------|-------------------|
| **Selection** | Single tool call from natural language | AI picked the wrong tool from 84+ options |
| **Chain** | 2–4 tools called in sequence | Wrong tool order, missed step, or incorrect data passed between steps |
| **Stress** | 5+ tools OR repeated calls OR large payloads | Timeout, session limit, or token exhaustion |

---

## POSITIVE TEST CASES

---

### CR-P01 — ~~List All Components and Verify Structure~~ [REMOVED]
> **`components_list` has been removed from the MCP server tool set. This test is permanently skipped.**

---

### CR-P02 — ~~Search Components With Wildcard and Specific Name~~ [REMOVED]
> **`components_search` has been removed from the MCP server tool set. This test is permanently skipped.**

---

### CR-P03 — List and Search Repositories Across All SCM Providers

**Discovery:** `Chain` | **Expected:** `repositories_list → repositories_search` | **Timeout:** `30s`

```
List all repositories for organizationId 6c5eeb79-... . Count total repositories. Identify how many are from GitHub vs GitLab vs Bitbucket by inspecting the endpointId field. Then search repositories with query="snyk*" to find Snyk-related repos. Verify:
- The full listing returns 100+ items
- The search filters correctly by prefix
- Each repo has: id (may be empty for unlinked repos), name, url, endpointId, defaultBranch
Report: total repo count, provider breakdown, count of repos with empty id (not linked to a component).
```

---

### CR-P04 — List Branches for a Multi-Branch Component

**Discovery:** `Chain` | **Expected:** `branches_list → branches_list` | **Timeout:** `30s`

```
List branches for component "resolvedFindings-feb" (componentId: efcb1d0b-8307-4bf5-a8d4-82da53a751fb). This component has 2 branches: "main" and "test". Verify:
- Returns exactly 2 branches
- Each branch has: id, name, parentId (= componentId), type=RESOURCE_TYPE_BRANCH, isDisabled=false
- Branch names are "main" and "test"
Report all branch details. Then list branches for a single-branch component (go, componentId: 95fdf71c-...) and verify only 1 branch is returned.
```

---

### CR-P05 — List All Endpoints and Verify Integration Types

**Discovery:** `Selection` | **Expected:** `endpoint_list` | **Timeout:** `15s`

```
List all endpoints for organizationId 6c5eeb79-... with contributionTypes="cb.platform.endpoint-type". Verify:
- Returns 13+ endpoints
- Endpoint types include: cb.github.github-app-endpoint-type, cb.gitlab-server.gitlab-server-token-endpoint-type, cb.bitbucket.bitbucket-cloud-token-endpoint-type, cb.jira.jira-token-endpoint-type
- Each endpoint has: id, name, contributionId, contributionType, isDisabled, resourceId
Report: total endpoint count, breakdown by contributionId (type of integration), any disabled endpoints. Identify the Jira endpoint.
```

---

### CR-P06 — List Properties for a Component Including Inherited Secrets

**Discovery:** `Selection` | **Expected:** `properties_list` | **Timeout:** `15s`

```
List all properties for componentId 95fdf71c-de53-43e4-b5dc-bec7170becd6 (go component). Verify:
- Returns at least 1 property (GH_SECURITY_PAT)
- The secret property has isSecret=true and string value masked as "*****"
- source field is either "INHERITED" or "COMPONENT"
- The tree object shows the full inheritance chain
Report: all property names, their types (bool/string/etc), isSecret status, source, and whether any property has a non-empty exportName.
```

---

### CR-P07 — List Resources (Branches) for a Component

**Discovery:** `Chain` | **Expected:** `resources_list → branches_list` | **Timeout:** `30s`

```
List all resources for entityId 95fdf71c-de53-43e4-b5dc-bec7170becd6 and filterType "RESOURCE_TYPE_BRANCH". Verify:
- Returns 1 resource (master branch)
- Resource has: id, name="master", parentId (= componentId), type=RESOURCE_TYPE_BRANCH, isDisabled=false
Compare this result to listing branches for the same component — verify they return identical data. This checks whether listing resources and listing branches are interchangeable for branch lookup.
```

---

### CR-P08 — Auth Audit: API Tokens, SAML Connections, Email Domains

**Discovery:** `Chain` | **Expected:** `api_tokens_list → saml_connections_list → saml_email_domains_list` | **Timeout:** `30s`

```
List all API tokens. Verify: returns at least 1 token ("ASPM USER API PAT QA"), token value is NOT included in the response (isSecret behavior), each token has: id, name, description, createdAt, expiresAt, userId. List all SAML connections. Verify: returns empty array (no SAML configured for this org). List all SAML email domains. Verify: returns empty array (no SAML = no email domains). Report: API token count and expiry dates, SAML status, and whether this org is using SSO.
```

---

### CR-P09 — List All Actions in the Organization

**Discovery:** `Selection` | **Expected:** `actions_list` | **Timeout:** `15s`

```
List all actions for organizationId 6c5eeb79-4606-4c39-bd5c-c2323336caad. Verify the call succeeds and returns a large items array. Report: total action count, sample of 5 action names (from displayName or contributions[].displayName), action categories present. Note: this is a large response (446KB+ from previous test) — verify the tool handles it without timeout.
```

---

### CR-P10 — SCM Repositories Sync: Trigger and Verify Response
**Expected:** Returns a success or async acknowledgement; the sync is enqueued.

**Discovery:** `Chain` | **Expected:** `scm_repositories_sync → repositories_list` | **Timeout:** `30s`

```
Trigger an SCM repositories sync for organizationId: 6c5eeb79-4606-4c39-bd5c-c2323336caad. Do not pass endpointIds (sync all endpoints). Record the exact response — expected: success acknowledgement or async job reference. Then list all repositories and note the current repo count. This establishes a baseline. Note: an actual sync may take time; this test verifies the call is accepted without error.
```

---

### CR-P11 — List Extensions for the Organization
**Expected:** Returns an array of extension manifests with name, category, and installed status.

**Discovery:** `Selection` | **Expected:** `extensions_list` | **Timeout:** `15s`

```
List all extensions for organizationId: 6c5eeb79-4606-4c39-bd5c-c2323336caad. Verify:
- Response is not an error
- Returns items array (may be empty if no extensions installed)
- Each extension has: id/name, category, and an installed/enabled flag
Report: total extension count, list of extension names, and which are installed vs available. Note any category breakdown.
```

---

### CR-P12 — List GitHub App Registrations for the Organization
**Expected:** Returns registered GitHub App names and their app URLs.

**Discovery:** `Selection` | **Expected:** `scm_gh_app_registrations_list` | **Timeout:** `15s`

```
List all GitHub App registrations for organizationId: 6c5eeb79-4606-4c39-bd5c-c2323336caad. Verify:
- Response is not an error
- Returns a list of GitHub App registrations
- Each entry has: name and appUrl fields
Report: total count of registered GitHub Apps and their names. If the list is empty, document that (this org may not have any GitHub Apps registered). This tests the GitHub App registry integration.
```

---

## NEGATIVE TEST CASES

---

### CR-N01 — ~~Create Component With Non-Existent Endpoint ID~~ [REMOVED]
> **`components_create` has been removed from the MCP server tool set. This test is permanently skipped.**

---

### CR-N02 — ~~Create Component With Invalid Repository URL Format~~ [REMOVED]
> **`components_create` has been removed from the MCP server tool set. This test is permanently skipped.**

---

### CR-N03 — ~~Delete Non-Existent Component~~ [REMOVED]
> **`components_delete` has been removed from the MCP server tool set. This test is permanently skipped.**

---

### CR-N04 — List Branches for Non-Existent Component

**Discovery:** `Selection` | **Expected:** `branches_list` | **Timeout:** `15s`

```
List branches for componentId "00000000-0000-0000-0000-000000000099". Record the exact error. Expected: 404 or 400. Does the server return an error or an empty array?
```

---

### CR-N05 — List Runs for Non-Existent Component

**Discovery:** `Selection` | **Expected:** `runs_list` | **Timeout:** `15s`

```
List runs with:
- subOrganizationId: "6c5eeb79-4606-4c39-bd5c-c2323336caad"
- componentId: "00000000-0000-0000-0000-000000000099"
Record the exact error. Expected: 404 or empty array. Document the response.
```

---

### CR-N06 — Get Controller Data With No Controllers in Org

**Discovery:** `Chain` | **Expected:** `controllers_list → controllers_data_get` | **Timeout:** `30s`

```
List all controllers for organizationId 6c5eeb79-... . Verify it returns empty (no controllers). Attempt to get controller data with a made-up controllerId: "00000000-0000-0000-0000-000000000099". Record the exact error. This documents that getting controller data is untestable in this org due to no controllers being configured. Note the exact error response.
```

---

### CR-N07 — Get Report Drilldown With No Controllers in Org

**Discovery:** `Selection` | **Expected:** `report_drilldown_get` | **Timeout:** `15s`

```
Attempt to get a report drilldown with:
- organizationId: "6c5eeb79-4606-4c39-bd5c-c2323336caad"
- controllerId: "00000000-0000-0000-0000-000000000099"
- reportId: "test-report"
Record the exact error. This documents that report drilldown is untestable in this org due to no controllers. Document whether the error is 404 (controller not found) or some other status.
```

---

### CR-N08 — List Repositories for Non-Existent Organization

**Discovery:** `Selection` | **Expected:** `repositories_list` | **Timeout:** `15s`

```
List repositories with organizationId "00000000-0000-0000-0000-000000000099". Record the exact response. Expected: 404 or 403 (org not found / no access). Does the server return an error or silently return an empty list?
```

---

### CR-N09 — List Properties for Non-Existent Component

**Discovery:** `Selection` | **Expected:** `properties_list` | **Timeout:** `15s`

```
List properties with componentId "00000000-0000-0000-0000-000000000099". Record the exact response. Expected: 404 or empty list. Document the response structure.
```

---

### CR-N10 — List SCM Branches With Invalid endpointId
**Expected:** Error (404 or 400) — endpoint does not exist.

**Discovery:** `Selection` | **Expected:** `scm_branches_list` | **Timeout:** `15s`

```
List SCM branches with:
- organizationId: 6c5eeb79-4606-4c39-bd5c-c2323336caad
- endpointId: 00000000-0000-0000-0000-000000000099
- repositoryUrl: https://github.com/rjain0404/VulnerableGoRepo4GH.git

Record the exact error. Expected: 404 (endpoint not found) or 400. Document the HTTP status and error message.
```

---

### CR-N11 — List SCM Branches With Non-Existent Repository URL
**Expected:** Error from the SCM provider — repository not found.

**Discovery:** `Selection` | **Expected:** `scm_branches_list` | **Timeout:** `15s`

```
List SCM branches with a valid endpointId but a repository URL that does not exist:
- organizationId: 6c5eeb79-4606-4c39-bd5c-c2323336caad
- endpointId: 413e7e54-f227-44dc-9b0d-d793e7c6f5d4
- repositoryUrl: https://github.com/rjain0404/this-repo-does-not-exist-xyz.git

Record the exact error. Does the server return a 404 from GitHub, a generic 400, or propagate the SCM error? Document the full error response.
```

---

### CR-N12 — List Extensions With Invalid organizationId
**Expected:** Error (404 or 403) — organization does not exist.

**Discovery:** `Selection` | **Expected:** `extensions_list` | **Timeout:** `15s`

```
List extensions with organizationId: 00000000-0000-0000-0000-000000000099. Record the exact error. Expected: 404 (org not found) or 403 (forbidden). Does the server return an error or an empty list? Document the HTTP status and error message.
```

---

## EDGE CASES

---

### CR-E01 — ~~Components With Empty defaultBranch vs Valid defaultBranch~~ [REMOVED]
> **`components_list` has been removed from the MCP server tool set. This test is permanently skipped.**

---

### CR-E02 — ~~Repositories With No Linked Component (Orphaned Repos)~~ [REMOVED]
> **`components_list` has been removed from the MCP server tool set. This test is permanently skipped.**

---

### CR-E03 — ~~Component Linked to Multiple Environments~~ [REMOVED]
> **`components_list` has been removed from the MCP server tool set. This test is permanently skipped.**

---

### CR-E04 — Endpoint List — Paginate Through All Results

**Discovery:** `Chain` | **Expected:** `endpoint_list → endpoint_list → endpoint_list` | **Timeout:** `45s`

```
List endpoints with pageLength=5 and pageNo=1. Note the pagination metadata (lastPage, page, pageLength). Call again with pageNo=2 if lastPage=false. Continue until lastPage=true. Verify: combining all pages gives the same total as a single call with large pageLength. Report: total pages, total endpoints, whether pagination works correctly.
```

---

### CR-E05 — SAML Not Configured — Verify Empty Responses Are Correct

**Discovery:** `Chain` | **Expected:** `saml_connections_list → saml_email_domains_list` | **Timeout:** `30s`

```
List all SAML connections for organizationId 6c5eeb79-... . Verify it returns {"items": []} — not an error. List all SAML email domains for the same org. Verify it also returns {"items": []}. Confirm that both tools handle the "no SAML configured" state gracefully and return empty lists rather than errors. This validates that the empty state is a valid, expected response (not a bug).
```

---

### CR-E06 — Actions List — Verify Large Response Is Handled Gracefully

**Discovery:** `Selection` | **Expected:** `actions_list` | **Timeout:** `15s`

```
List all actions for organizationId 6c5eeb79-... . The previous test run showed this returns 446KB of data. Verify: (1) the call completes without timeout, (2) the response is valid JSON, (3) the items array is non-empty, (4) each action has at least: displayName, uses, contributions fields. Report: total action count, and list the displayName of the first 10 actions. This tests that the MCP server handles large payloads without truncation or error.
```

---

### CR-E07 — ~~Component Full Lifecycle: Create → List → Search → Delete~~ [REMOVED]
> **`components_create`, `components_list`, `components_search`, and `components_delete` have all been removed from the MCP server tool set. This test is permanently skipped.**

---

### CR-E08 — Cross-Provider Repository Search

**Discovery:** `Selection` | **Expected:** `repositories_search` | **Timeout:** `15s`

```
Search repositories with query="go*" (no organizationId filter). This should return repositories named starting with "go" from all SCM providers. Verify: results include repos from GitHub (github.com URLs), GitLab (gitlab.com URLs), and possibly Bitbucket. For each result, report the provider (inferred from URL) and whether it has a linked component (serviceId non-empty). This tests that the search is truly cross-provider.
```

---

### CR-E09 — Runs List With Limit Parameter

**Discovery:** `Chain` | **Expected:** `runs_list → runs_list` | **Timeout:** `30s`

```
List runs for a component that has had runs (use sv-app, componentId: 2060d4c2-a9fe-4049-ae39-fc925b11be9d, subOrganizationId: 6c5eeb79-...) with limit=1. Then call again with limit=5. Compare results. Verify: limit=1 returns at most 1 run, limit=5 returns at most 5 runs. If no runs exist, document that and note the call still succeeds. This tests the limit parameter behavior.
```

---

### CR-E10 — SCM Sync Then Repo List — Verify Consistency

**Discovery:** `Chain` | **Expected:** `repositories_list → scm_repositories_sync → repositories_list` | **Timeout:** `45s`

```
List all repositories and record the current total repo count (call this count_before). Then trigger an SCM repositories sync for organizationId 6c5eeb79-... . Wait a few seconds. List repositories again and compare the count (count_after). Report: count_before, count_after, and any difference. If counts changed, list the new repos added. If counts are unchanged, note that the sync found no new repos. This validates the sync → list pipeline.
```

---

### CR-E11 — ~~SCM Branches vs Platform Branches — Compare for the Same Repository~~ [REMOVED]
> **`components_search` has been removed from the MCP server tool set. This test is permanently skipped.**

```
