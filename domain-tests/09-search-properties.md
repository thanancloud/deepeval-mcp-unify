# Domain: Search, Properties & Resources (New Tools)
**Tools covered (6):** `search_resources`, `search_runs`, `properties_add`, `properties_get`, `property_delete`, `resources_get`
**Total prompts:** 18 (6 positive, 6 negative, 6 edge cases)

> **Note on existing overlap:** `properties_list` and `resources_list` are already covered in `04-components-repos.md`. This file covers the new tools `properties_add`, `properties_get`, `property_delete`, `resources_get`, and the brand-new search tools `search_resources` and `search_runs`.

---

## Test Execution Tracker

| ID | Type | Category | Expected Tools | Timeout | Description | Status | Notes |
|----|------|----------|----------------|---------|-------------|--------|-------|
| SP-P01 | Positive | Selection | `search_resources` | 15s | Search for resources by name/keyword | ⬜ | |
| SP-P02 | Positive | Selection | `search_runs` | 15s | Search for pipeline runs by filter criteria | ⬜ | |
| SP-P03 | Positive | Chain | `properties_list → properties_get` | 30s | List properties then get one by ID | ⬜ | |
| SP-P04 | Positive | Stress | `properties_add → properties_list → properties_get → property_delete` | 60s | Full property lifecycle: add, list, get, delete | ⬜ | |
| SP-P05 | Positive | Chain | `resources_list → resources_get` | 30s | List resources then get one by ID | ⬜ | |
| SP-P06 | Positive | Chain | `search_resources → resources_get` | 30s | Search resources then fetch the first result's details | ⬜ | |
| SP-N01 | Negative | Selection | `search_resources` | 15s | Search resources with no-match query | ⬜ | |
| SP-N02 | Negative | Selection | `search_runs` | 15s | Search runs with invalid date range | ⬜ | |
| SP-N03 | Negative | Selection | `properties_get` | 15s | Get property with non-existent propertyId | ⬜ | |
| SP-N04 | Negative | Selection | `property_delete` | 15s | Delete non-existent property | ⬜ | |
| SP-N05 | Negative | Selection | `properties_add` | 15s | Add property with missing required fields | ⬜ | |
| SP-N06 | Negative | Selection | `resources_get` | 15s | Get resource with non-existent resourceId | ⬜ | |
| SP-E01 | Edge | Chain | `search_resources (×2)` | 30s | Search with wildcard vs specific term — compare results | ⬜ | |
| SP-E02 | Edge | Chain | `search_runs (×2)` | 30s | Search runs: success status vs failure status | ⬜ | |
| SP-E03 | Edge | Chain | `properties_add → property_delete → properties_get` | 45s | Verify deleted property returns 404 | ⬜ | |
| SP-E04 | Edge | Chain | `resources_list → resources_get (×N)` | 45s | Get details for all listed resources | ⬜ | |
| SP-E05 | Edge | Chain | `search_resources → components_list` | 30s | Cross-check search results vs components list | ⬜ | |
| SP-E06 | Edge | Stress | `search_resources → search_runs → properties_list → properties_get → resources_list → resources_get` | 90s | Full read-only walkthrough of all new tools | ⬜ | |

---

## Diagnostic Categories

| Category | Definition | Failure Indicates |
|----------|-----------|-------------------|
| **Selection** | Single tool call from natural language | AI picked the wrong tool from 122+ options |
| **Chain** | 2–4 tools called in sequence | Wrong tool order, missed step, or incorrect data passed between steps |
| **Stress** | 5+ tools OR repeated calls OR large payloads | Timeout, session limit, or token exhaustion |

---

## POSITIVE TEST CASES

---

### SP-P01 — Search for Resources by Name/Keyword

**Discovery:** `Selection` | **Expected:** `search_resources` | **Timeout:** `15s`

```
Search for resources in organizationId 6c5eeb79-4606-4c39-bd5c-c2323336caad using a broad keyword (e.g., "go" or "auto" to match known components).
Verify:
- Response is not an error
- Returns an array of resource objects matching the query
- Each resource has: id, name, type fields
Report: total results count, names of the first 5 results, and the resource types returned. Note how search_resources differs from search_runs (what resource types it covers).
```

---

### SP-P02 — Search for Pipeline Runs by Filter Criteria

**Discovery:** `Selection` | **Expected:** `search_runs` | **Timeout:** `15s`

```
Search for pipeline runs in organizationId 6c5eeb79-4606-4c39-bd5c-c2323336caad. Apply a filter (e.g., status=SUCCESS or a date range for the past 7 days).
Verify:
- Response is not an error
- Returns an array of run objects matching the filter
- Each run has: id, status, startedAt, completedAt, componentId fields
Report: total matching run count, distribution of statuses (SUCCESS/FAILURE/ABORTED), and the most recent run's details.
```

---

### SP-P03 — List Properties Then Get One by ID

**Discovery:** `Chain` | **Expected:** `properties_list → properties_get` | **Timeout:** `30s`

```
1. List all properties for componentId 95fdf71c-de53-43e4-b5dc-bec7170becd6 (go component).
2. Take the first property from the list. Get its full details using properties_get with that propertyId.

Verify: the details match the summary (name, type, value, isSecret). Report: any additional fields in the detail view not in the listing (e.g., full tree, scope). Note if isSecret properties have values masked in the detail view.
```

---

### SP-P04 — Full Property Lifecycle: Add, List, Get, Delete

**Discovery:** `Stress` | **Expected:** `properties_add → properties_list → properties_get → property_delete` | **Timeout:** `60s`

```
Execute the full property lifecycle for componentId 95fdf71c-de53-43e4-b5dc-bec7170becd6 (go component):
1. Add a new property:
   - name: "SP_TEST_PROP_DATE"
   - value: "smoke-test-value"
   - type: string
   - isSecret: false
   Record the propertyId.
2. List properties — verify the new property appears.
3. Get the property by ID — verify details match.
4. Delete the property.

Report each step result and confirm cleanup. If add fails, document the required schema for properties_add.
```

---

### SP-P05 — List Resources Then Get One by ID

**Discovery:** `Chain` | **Expected:** `resources_list → resources_get` | **Timeout:** `30s`

```
1. List resources for entityId 95fdf71c-de53-43e4-b5dc-bec7170becd6 with filterType "RESOURCE_TYPE_BRANCH".
2. Take the first resource (the master branch). Get its full details using resources_get with that resourceId.

Verify: the detail view matches the listing entry (id, name, type). Report: any additional fields in resources_get vs resources_list (e.g., metadata, configuration, or linked run data).
```

---

### SP-P06 — Search Resources Then Fetch the First Result's Details

**Discovery:** `Chain` | **Expected:** `search_resources → resources_get` | **Timeout:** `30s`

```
1. Search for resources with a query matching a known resource (e.g., "master" or "main" branch name).
2. Take the first result and call resources_get with its resourceId.

Verify: the detailed resource object from resources_get matches what was returned in the search. Report any extra fields. This validates that search_resources returns valid IDs that can be used with resources_get.
```

---

## NEGATIVE TEST CASES

---

### SP-N01 — Search Resources With No-Match Query

**Discovery:** `Selection` | **Expected:** `search_resources` | **Timeout:** `15s`

```
Search for resources with a query that will not match anything:
- organizationId: 6c5eeb79-4606-4c39-bd5c-c2323336caad
- query: "zzz-this-resource-absolutely-does-not-exist-xyz"

Record the response. Expected: empty array (not an error). Does the server return {"items": []} or a 404? Document the exact behavior — empty results should not be an error condition.
```

---

### SP-N02 — Search Runs With Invalid Date Range

**Discovery:** `Selection` | **Expected:** `search_runs` | **Timeout:** `15s`

```
Search for runs with an invalid date range:
- organizationId: 6c5eeb79-4606-4c39-bd5c-c2323336caad
- startDate: "not-a-date"
- endDate: "also-not-a-date"

Record the exact error response. Expected: 400 Bad Request with validation details. Is date format validated client-side (schema error) or server-side? Document the full error message.
```

---

### SP-N03 — Get Property With Non-Existent propertyId

**Discovery:** `Selection` | **Expected:** `properties_get` | **Timeout:** `15s`

```
Get property details with:
- componentId: 95fdf71c-de53-43e4-b5dc-bec7170becd6
- propertyId: 00000000-0000-0000-0000-000000000099

Record the exact error response. Expected: 404 (property not found). Document the HTTP status and error message.
```

---

### SP-N04 — Delete Non-Existent Property

**Discovery:** `Selection` | **Expected:** `property_delete` | **Timeout:** `15s`

```
Delete a property with:
- componentId: 95fdf71c-de53-43e4-b5dc-bec7170becd6
- propertyId: 00000000-0000-0000-0000-000000000099

Record the exact error response. Expected: 404 (property not found). Document the HTTP status and error message.
```

---

### SP-N05 — Add Property With Missing Required Fields

**Discovery:** `Selection` | **Expected:** `properties_add` | **Timeout:** `15s`

```
Attempt to add a property with:
- componentId: 95fdf71c-de53-43e4-b5dc-bec7170becd6
- name: "" (empty, omitting value and type)

Record the exact error response. Is it a schema validation error (required field missing) or a server-side 400? Document which fields are required per the error.
```

---

### SP-N06 — Get Resource With Non-Existent resourceId

**Discovery:** `Selection` | **Expected:** `resources_get` | **Timeout:** `15s`

```
Get resource details with:
- resourceId: 00000000-0000-0000-0000-000000000099

Record the exact error response. Expected: 404 (resource not found). Document the HTTP status and error message.
```

---

## EDGE CASES

---

### SP-E01 — Search Resources: Wildcard vs Specific Term

**Discovery:** `Chain` | **Expected:** `search_resources (×2)` | **Timeout:** `30s`

```
Search resources for organizationId 6c5eeb79-4606-4c39-bd5c-c2323336caad twice:
1. With a wildcard or broad query (e.g., "auto*" or just "a").
2. With the specific name "AutoNjsscan".

Compare: does the specific-name search return exactly 1 result that matches? Does the wildcard return a superset? Report both result counts and note whether results from search 2 are a subset of search 1. This validates search precision vs recall.
```

---

### SP-E02 — Search Runs: Success Status vs Failure Status

**Discovery:** `Chain` | **Expected:** `search_runs (×2)` | **Timeout:** `30s`

```
Search for runs in organizationId 6c5eeb79-4606-4c39-bd5c-c2323336caad twice:
1. Filter by status=SUCCESS.
2. Filter by status=FAILURE (or FAILED).

Compare: total success count vs failure count. Verify that no run appears in both lists (they should be mutually exclusive). Report the counts and the most recent run of each status. This validates that status filtering works correctly.
```

---

### SP-E03 — Verify Deleted Property Returns 404

**Discovery:** `Chain` | **Expected:** `properties_add → property_delete → properties_get` | **Timeout:** `45s`

```
1. Add a property "SP_E03_DELETE_VERIFY_DATE" to componentId 95fdf71c-de53-43e4-b5dc-bec7170becd6. Record the propertyId.
2. Delete the property.
3. Attempt to get the property by the same propertyId.

Verify: step 3 returns 404 (property not found). Document the exact error. This validates that property deletes are immediately enforced.
```

---

### SP-E04 — Get Details for All Listed Resources

**Discovery:** `Chain` | **Expected:** `resources_list → resources_get (×N)` | **Timeout:** `45s`

```
List all resources for entityId 95fdf71c-de53-43e4-b5dc-bec7170becd6 (up to 10 resources). For each resource in the list, call resources_get with its resourceId. Verify: every resourceId from the listing is fetchable. Report any resource that fails to load by ID. Note fields visible in resources_get but not in resources_list. This tests list vs get data consistency.
```

---

### SP-E05 — Cross-Check Search Results vs Components List

**Discovery:** `Chain` | **Expected:** `search_resources → components_list` | **Timeout:** `30s`

```
1. Search resources with query "go*" in organizationId 6c5eeb79-4606-4c39-bd5c-c2323336caad.
2. List all components for the same org.

Cross-check: do the resource IDs in the search results match component IDs from the listing? Are there resources returned that are not components (e.g., branches, runs)? Report: the resource types returned by search_resources, and how many of the returned resource IDs correspond to known components. This documents what entity types search_resources covers.
```

---

### SP-E06 — Full Read-Only Walkthrough of All New Tools

**Discovery:** `Stress` | **Expected:** `search_resources → search_runs → properties_list → properties_get → resources_list → resources_get` | **Timeout:** `90s`

```
Execute a complete read-only walkthrough:
1. search_resources: search for "go*" — record result count.
2. search_runs: search for recent runs (last 7 days) — record result count.
3. properties_list: list properties for componentId 95fdf71c-... — record property count.
4. properties_get: get the first property by ID.
5. resources_list: list resources for the same componentId.
6. resources_get: get the first resource by ID.

Report each step result, elapsed time per step, and total elapsed time. Flag any step that exceeds 15s individually. This serves as a smoke test for all 6 tools in a single session.
```
