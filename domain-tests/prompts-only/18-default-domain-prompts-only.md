# Default Domain (Core Navigation & Discovery) — Prompts Only

> All tools in this domain are read-only. These are the "entry point" tools used as setup steps across all other domains.

---

## POSITIVE TEST CASES

### DD-P01 — Verify Identity (Auth Baseline)

```
Call user_whoami.
Report: userId, email, name, selectedOrganization.
This is the auth baseline check — if this fails, no other tests can run.
Confirm the response contains all four fields with non-empty values.
```

---

### DD-P02 — Get Organization by ID

```
Call organizations_list to get all organizations. Pick the first one.
Call organizations_get with that org's ID.
Verify: the id and displayName match between list and get.
Report all fields returned by organizations_get.
```

---

### DD-P03 — Search Organizations and List Sub-Organizations

```
1. Call organizations_search using a broad term (e.g., first 4 characters of the org name from user_whoami).
2. Confirm at least one result is returned.
3. Call organizations_list_suborganizations using the default org.
4. Map the hierarchy: report Level 0 (root), Level 1 children, and total sub-org count.
```

---

### DD-P04 — List Services and Get One by ID

```
1. Call organizations_list to get the org ID.
2. Call services_list to get all services.
3. Pick the first service and call services_get with its serviceId.
4. Verify: name and id match between list and get.
Report: total service count, each service's name, type (COMPONENT vs APPLICATION), and status.
```

---

### DD-P05 — Get Resource Node and List its Children

```
1. Call organizations_list to get the org ID.
2. Call resources_get with the org ID as the UUID.
3. Call resources_list with the org ID to get its direct children.
Report: the resource node from resources_get, and the children list from resources_list.
```

---

### DD-P06 — Search Resources by Type

```
1. Call organizations_list to get the root org ID.
2. Call search_resources restricted to type "SERVICE" within that org hierarchy.
Report: total count found, first 5 results with id, type, and displayName.
```

---

### DD-P07 — Flag Discovery Chain: Apps → Environments → Get by Name → Config

```
1. Call organizations_list to get the org ID.
2. Call flags_applications_list to get an application ID.
3. Call flags_environments_list to get an environment ID.
4. Call flags_list (feature-management) to get a flag name. Then call flags_get_by_name.
5. Call flag_configuration_get for that flag in that environment.
Report the chain of IDs resolved at each step and the final configuration returned.
```

---

### DD-P08 — Full Automation Chain: Runs → Jobs → Logs → Workflows

```
1. Call services_list to find a component with automation runs.
2. Call search_runs for that component — get the most recent completed run.
3. Call automation_jobs_list for that run — get a job with steps.
4. Call logs_list for the first step in that job — report the first 5 log lines.
5. Call workflow_list for the same component — list all available workflows.
Report the chain of IDs resolved at each step.
```

---

## NEGATIVE TEST CASES

### DD-N01 — Get Organization with Non-Existent ID

```
Call organizations_get with a nil ID: 00000000-0000-0000-0000-000000000099.
Record the exact error message and HTTP status code. Expected: 404.
```

---

### DD-N02 — Search Organizations with No Match

```
Call organizations_search with "xyzzy-org-no-match-9999999".
Record the exact response. Expected: empty array — NOT an error.
```

---

### DD-N03 — Get Service with Non-Existent Service ID

```
Call services_get with a nil serviceId: 00000000-0000-0000-0000-000000000099.
Record the exact error message and HTTP status code. Expected: 404.
```

---

### DD-N04 — Get Resource Node with Non-Existent UUID

```
Call resources_get with a nil UUID: 00000000-0000-0000-0000-000000000099.
Record the exact error message and HTTP status code. Expected: 404.
```

---

### DD-N05 — Search Runs for Non-Existent Component

```
Call search_runs with a nil component ID: 00000000-0000-0000-0000-000000000099.
Record the exact response. Expected: 404 or empty results.
```

---

### DD-N06 — List Jobs for Non-Existent Run

```
Call automation_jobs_list with a nil run ID: 00000000-0000-0000-0000-000000000099.
Record the exact error message and HTTP status code. Expected: 404 or 400.
```

---

### DD-N07 — List Logs for Non-Existent Step

```
Call logs_list with a nil step ID: 00000000-0000-0000-0000-000000000099.
Record the exact error message and HTTP status code. Expected: 404 or 400.
```

---

### DD-N08 — Get Flag by Non-Existent Name

```
Call flags_applications_list to get an app ID.
Call flags_get_by_name with name="no-such-flag-xyz-9999".
Record the exact response. Expected: 404 or empty result.
```

---

## EDGE CASES

### DD-E01 — List Children of a Deep Sub-Organization

```
1. Call organizations_list_suborganizations to get all sub-orgs.
2. Find the deepest sub-org (one that is a child of another child).
3. Call resources_list for that deep sub-org.
Report: its direct children and their types. If no children, record "0 children — empty result OK".
```

---

### DD-E02 — Search Resources Filtered to Type SERVICE

```
1. Call organizations_list to get the org ID.
2. Call search_resources with resourceType=["SERVICE"] within the org hierarchy.
3. Also call services_list for the same org.
4. Cross-verify: the count from search_resources should roughly match services_list.
Report any discrepancy.
```

---

### DD-E03 — Search Runs Filtered by Status FAILED

```
1. Call services_list to get a component.
2. Call search_runs with status filter=FAILED.
3. Report: count of failed runs, most recent failure's run ID and timestamp.
If no failed runs exist, record "0 failed runs — filter working correctly".
```

---

### DD-E04 — Get Flag Config for Flag Not Configured in Environment

```
1. Call flags_applications_list to get an app.
2. Call flags_environments_list to get all environments.
3. Pick a flag from flags_list (feature-management) that you suspect is not configured in all environments.
4. Call flag_configuration_get for that flag in each environment.
Report: which environments have explicit config vs which return the default/empty config.
```

---

### DD-E05 — Sub-Organization Pagination with Cursor

```
1. Call organizations_list_suborganizations.
2. If the response includes a nextCursor, call organizations_list_suborganizations again with that cursor.
3. Collect and de-duplicate all sub-orgs across both pages.
Report: total sub-orgs found, whether pagination was triggered, and the cursor value (if any).
```

---

### DD-E06 — Workflow List for Component with No Workflows

```
1. Call services_list to find an application (type=APPLICATION rather than COMPONENT).
2. Call workflow_list for that application.
Verify: empty result does not produce an error.
Record "0 workflows — empty result OK" if confirmed.
```

---

### DD-E07 — Multi-Hop Resource Traversal

```
1. Call organizations_search to find the org.
2. Call organizations_get to read the full org object.
3. Call resources_list to get its direct children.
4. For one child resource, call search_resources to find all SERVICE nodes within it.
Report: the complete traversal path and the services found at the leaf level.
```

---

### DD-E08 — Log List for Step with No Log Output

```
1. Call services_list to get a component.
2. Call search_runs to find a short or fast run.
3. Call automation_jobs_list — find a very short job or a skipped step.
4. Call logs_list for that step.
Verify: empty log response does not produce an error. Record "0 log lines — empty result OK".
```
