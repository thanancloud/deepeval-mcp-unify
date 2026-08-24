# Domain: Services, Endpoints & Ticketing
**Tools covered (7):** `services_list`, `services_get`, `services_add`, `services_delete`, `endpoint_add`, `endpoint_scm_connector_prepare`, `ticketing_webhook_url_get`
**Total prompts:** 18 (6 positive, 6 negative, 6 edge cases)

> **Note on endpoint_ overlap:** `endpoint_list` is already covered in domain `04-components-repos.md`. This file covers the new endpoint tools (`endpoint_add`, `endpoint_scm_connector_prepare`) that were not in the original 95-tool suite. `endpoint_get` and `endpoint_disable` have been removed from the MCP server.

---

## Test Execution Tracker

| ID | Type | Category | Expected Tools | Timeout | Description | Status | Notes |
|----|------|----------|----------------|---------|-------------|--------|-------|
| SE-P01 | Positive | Selection | `services_list` | 15s | List all services in the organization | ⬜ | |
| SE-P02 | Positive | Chain | `services_list → services_get` | 30s | List services then get details of the first | ⬜ | |
| SE-P03 | Positive | Stress | `services_add → services_list → services_get → services_delete` | 60s | Full service lifecycle: create, list, get, delete | ⬜ | |
| SE-P04 | Positive | Chain | `endpoint_add → endpoint_list` | 30s | Add a new endpoint and verify it appears in listing | ⬜ | |
| SE-P05 | Positive | Selection | `endpoint_scm_connector_prepare` | 15s | Prepare an SCM connector for a supported provider | ⬜ | |
| SE-P06 | Positive | Selection | `ticketing_webhook_url_get` | 15s | Get the ticketing webhook URL for the organization | ⬜ | |
| SE-N01 | Negative | Selection | `services_get` | 15s | Get service with non-existent serviceId | ⬜ | |
| SE-N02 | Negative | Selection | `services_delete` | 15s | Delete non-existent service | ⬜ | |
| SE-N03 | Negative | Selection | `services_add` | 15s | Add service with missing required fields | ⬜ | |
| SE-N04 | Negative | Selection | `endpoint_add` | 15s | Add endpoint with invalid provider type | ⬜ | |
| SE-N05 | Negative | Selection | `endpoint_scm_connector_prepare` | 15s | Prepare SCM connector with invalid provider | ⬜ | |
| SE-N06 | Negative | Selection | `ticketing_webhook_url_get` | 15s | Get ticketing webhook URL with invalid organizationId | ⬜ | |
| SE-E01 | Edge | Chain | `services_add → services_get → services_delete → services_get` | 60s | Verify deleted service returns 404 | ⬜ | |
| SE-E02 | Edge | Chain | `endpoint_scm_connector_prepare (×2)` | 30s | Prepare connectors for two different SCM types | ⬜ | |
| SE-E03 | Edge | Chain | `services_list → services_add` | 30s | Verify duplicate service name handling | ⬜ | |
| SE-E04 | Edge | Chain | `ticketing_webhook_url_get → endpoint_list` | 30s | Get webhook URL then cross-check against endpoints | ⬜ | |
| SE-E05 | Edge | Stress | `services_add (×3) → services_list → services_delete (×3)` | 90s | Create multiple services, verify all appear, delete all | ⬜ | |
| SE-E06 | Edge | Chain | `endpoint_add → endpoint_list` | 30s | Verify new endpoint appears in listing with correct fields | ⬜ | |

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

### SE-P01 — List All Services in the Organization

**Discovery:** `Selection` | **Expected:** `services_list` | **Timeout:** `15s`

```
List all services for organizationId 6c5eeb79-4606-4c39-bd5c-c2323336caad.
Verify:
- Response is not an error
- Returns an array of service objects (may be empty if no services are configured)
- Each service has: id, name, type, and status fields
Report: total service count, names of all services, and their types. If the list is empty, document that — this is a valid state.
```

---

### SE-P02 — List Services Then Get Details of the First

**Discovery:** `Chain` | **Expected:** `services_list → services_get` | **Timeout:** `30s`

```
1. List all services for organizationId 6c5eeb79-4606-4c39-bd5c-c2323336caad.
2. Take the first service from the list. Get its full details using services_get with that serviceId.

Verify: the details match the summary from the listing (id, name). Report the full service object — note any fields in the detail view that are not in the list view.
If no services exist, skip to step notes and document.
```

---

### SE-P03 — Full Service Lifecycle: Create, List, Get, Delete

**Discovery:** `Stress` | **Expected:** `services_add → services_list → services_get → services_delete` | **Timeout:** `60s`

```
Execute the full service lifecycle:
1. Create a new service with:
   - organizationId: 6c5eeb79-4606-4c39-bd5c-c2323336caad
   - name: "se-p03-test-service-DATE"
   - (fill in other required fields based on the tool schema)
   Record the serviceId from the response.
2. List all services — verify the new service appears.
3. Get the service by ID — verify details match.
4. Delete the service.

Report each step result and confirm cleanup. If create fails, record the schema requirements for services_add.
```

---

### SE-P04 — Add a New Endpoint and Verify It Appears

**Discovery:** `Chain` | **Expected:** `endpoint_add → endpoint_list` | **Timeout:** `30s`

```
1. Add a new endpoint for organizationId 6c5eeb79-4606-4c39-bd5c-c2323336caad:
   - type: a simple integration type (use the first type returned by endpoint_list to match an existing type)
   - name: "se-p04-test-endpoint-DATE"
   - (fill in required credentials — use placeholder/test values)
   Record the endpointId from the response.
2. List all endpoints — verify the new endpoint appears.

Report each step. Note: if endpoint_add requires a real credential, document the required fields and skip the actual creation, marking as ⬛ Skip.
```

---

### SE-P05 — Prepare an SCM Connector for a Supported Provider

**Discovery:** `Selection` | **Expected:** `endpoint_scm_connector_prepare` | **Timeout:** `15s`

```
Prepare an SCM connector for organizationId 6c5eeb79-4606-4c39-bd5c-c2323336caad. Use one of the known SCM provider types (e.g., github, gitlab, bitbucket).
Verify:
- Response is not an error
- Returns preparation data (auth URL, token, or setup instructions)
Report: the full response — what does "prepare" return? Does it return an OAuth URL, a webhook URL, or a setup object? This documents the connector preparation flow.
```

---

### SE-P06 — Get the Ticketing Webhook URL for the Organization

**Discovery:** `Selection` | **Expected:** `ticketing_webhook_url_get` | **Timeout:** `15s`

```
Get the ticketing webhook URL for organizationId 6c5eeb79-4606-4c39-bd5c-c2323336caad.
Verify:
- Response is not an error
- Returns a URL string or webhook object with a URL field
Report: the returned URL (or note if empty/null). Does the URL follow a standard pattern? Is it an HTTPS URL? This documents the ticketing integration webhook endpoint.
```

---

## NEGATIVE TEST CASES

---

### SE-N01 — Get Service With Non-Existent serviceId

**Discovery:** `Selection` | **Expected:** `services_get` | **Timeout:** `15s`

```
Get service details with:
- organizationId: 6c5eeb79-4606-4c39-bd5c-c2323336caad
- serviceId: 00000000-0000-0000-0000-000000000099

Record the exact error response. Expected: 404 (service not found). Document the HTTP status and error message.
```

---

### SE-N02 — Delete Non-Existent Service

**Discovery:** `Selection` | **Expected:** `services_delete` | **Timeout:** `15s`

```
Delete a service with:
- organizationId: 6c5eeb79-4606-4c39-bd5c-c2323336caad
- serviceId: 00000000-0000-0000-0000-000000000099

Record the exact error response. Expected: 404 (service not found). Document the HTTP status and error message.
```

---

### SE-N03 — Add Service With Missing Required Fields

**Discovery:** `Selection` | **Expected:** `services_add` | **Timeout:** `15s`

```
Attempt to add a service with:
- organizationId: 6c5eeb79-4606-4c39-bd5c-c2323336caad
- name: "" (empty string, omitting all other required fields)

Record the exact error response. Is validation client-side (MCP schema error) or server-side (400 Bad Request)? Document which fields are required per the error message.
```

---

### SE-N04 — Add Endpoint With Invalid Provider Type

**Discovery:** `Selection` | **Expected:** `endpoint_add` | **Timeout:** `15s`

```
Attempt to add an endpoint with:
- organizationId: 6c5eeb79-4606-4c39-bd5c-c2323336caad
- contributionType: "cb.fake-provider.fake-endpoint-type"
- name: "se-n05-invalid-type-test"

Record the exact error response. Expected: 400 (invalid provider type) or 422. Does the server validate the contributionType against known types? Document the full error response.
```

---

### SE-N05 — Prepare SCM Connector With Invalid Provider

**Discovery:** `Selection` | **Expected:** `endpoint_scm_connector_prepare` | **Timeout:** `15s`

```
Prepare an SCM connector with:
- organizationId: 6c5eeb79-4606-4c39-bd5c-c2323336caad
- providerType: "invalid-scm-provider-xyz"

Record the exact error response. Expected: 400 or 422 (invalid provider type). Document whether the error is a schema validation error or a server-side rejection.
```

---

### SE-N06 — Get Ticketing Webhook URL With Invalid organizationId

**Discovery:** `Selection` | **Expected:** `ticketing_webhook_url_get` | **Timeout:** `15s`

```
Get the ticketing webhook URL for:
- organizationId: 00000000-0000-0000-0000-000000000099

Record the exact error response. Expected: 404 (org not found) or 403 (forbidden). Does it return an error or a null/empty URL? Document the HTTP status and error message.
```

---

## EDGE CASES

---

### SE-E01 — Verify Deleted Service Returns 404

**Discovery:** `Chain` | **Expected:** `services_add → services_get → services_delete → services_get` | **Timeout:** `60s`

```
1. Create a service named "se-e03-delete-verify-DATE" for organizationId 6c5eeb79-4606-4c39-bd5c-c2323336caad.
2. Get the service by ID — verify it exists.
3. Delete the service.
4. Attempt to get the service by the same ID.

Verify: step 4 returns 404. Document whether the server returns a clear "not found" message. This validates that deletes are properly enforced.
```

---

### SE-E02 — Prepare Connectors for Two Different SCM Types

**Discovery:** `Chain` | **Expected:** `endpoint_scm_connector_prepare (×2)` | **Timeout:** `30s`

```
Call endpoint_scm_connector_prepare twice for organizationId 6c5eeb79-4606-4c39-bd5c-c2323336caad:
1. For provider type: github
2. For provider type: gitlab (or bitbucket if gitlab not supported)

Compare the two responses. Report: are the response structures the same? Are the returned URLs or tokens provider-specific? This documents how connector preparation differs per SCM provider.
```

---

### SE-E03 — Verify Duplicate Service Name Handling

**Discovery:** `Chain` | **Expected:** `services_list → services_add` | **Timeout:** `30s`

```
1. List all services for organizationId 6c5eeb79-4606-4c39-bd5c-c2323336caad and pick a service name that already exists (or create one first).
2. Attempt to create a second service with the same name.

Record the response to the second create. Does the server return 409 Conflict (duplicate name), 400 (bad request), or is it allowed (names are non-unique)? Document the behavior and clean up any test services created.
```

---

### SE-E04 — Get Webhook URL Then Cross-Check Against Endpoints

**Discovery:** `Chain` | **Expected:** `ticketing_webhook_url_get → endpoint_list` | **Timeout:** `30s`

```
1. Get the ticketing webhook URL for organizationId 6c5eeb79-4606-4c39-bd5c-c2323336caad. Record the URL.
2. List all endpoints and look for a Jira or ticketing-type endpoint.

Compare: is the webhook URL from ticketing_webhook_url_get related to any registered endpoint in endpoint_list? Does the webhook URL domain match the organization's ticketing integration? Report the relationship between the two tools' data.
```

---

### SE-E05 — Create Multiple Services, Verify All Appear, Delete All

**Discovery:** `Stress` | **Expected:** `services_add (×3) → services_list → services_delete (×3)` | **Timeout:** `90s`

```
1. Create three services in sequence for organizationId 6c5eeb79-4606-4c39-bd5c-c2323336caad:
   - "se-e07-service-alpha-DATE"
   - "se-e07-service-beta-DATE"
   - "se-e07-service-gamma-DATE"
2. Record all three serviceIds.
3. List all services — verify all three appear.
4. Delete all three services.
5. List services again — verify none of the three appear.

Report each step result, total time, and whether any delete fails. This tests batch write operations and list consistency.
```

---

### SE-E06 — Verify New Endpoint Appears in Listing

**Discovery:** `Chain` | **Expected:** `endpoint_add → endpoint_list` | **Timeout:** `30s`

```
1. Create a test endpoint "se-e06-visibility-test-DATE" for organizationId 6c5eeb79-4606-4c39-bd5c-c2323336caad.
2. List all endpoints — verify the new endpoint appears with isDisabled=false.

Report: the endpoint fields visible in the listing (id, name, contributionType, isDisabled). Clean up: note the endpointId for manual deletion if no delete tool is available.
```
