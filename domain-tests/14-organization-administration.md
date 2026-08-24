# Domain: Organization Administration
**Tools covered (12):** `endpoint_add`, `endpoint_list`, `endpoint_scm_connector_prepare`, `extensions_list`, `organizations_create`, `properties_add`, `properties_get`, `properties_list`, `property_delete`, `services_add`, `services_delete`, `ticketing_webhook_url_get`
**Total prompts:** 24 (8 positive, 8 negative, 8 edge)

> **Cross-domain tools used for setup:** `user_whoami` (default), `organizations_list` (default), `organizations_get` (default), `organizations_list_suborganizations` (default), `services_list` (default), `services_get` (default), `resources_list` (default)

---

## Test Execution Tracker

| ID | Type | Category | Expected Tools | Timeout | Status | Notes |
|----|------|----------|----------------|---------|--------|-------|
| OA-P01 | Positive | Chain | `organizations_list` → `endpoint_list` | 20s | ⬜ | |
| OA-P02 | Positive | Chain | `organizations_list` → `extensions_list` | 20s | ⬜ | |
| OA-P03 | Positive | Chain | `services_list` → `properties_get` | 25s | ⬜ | |
| OA-P04 | Positive | Stress | `organizations_list` → `services_list` → `properties_add` → `properties_get` → `property_delete` → `properties_get` (verify) | 90s | ⬜ | |
| OA-P05 | Positive | Stress | `organizations_list` → `services_add` → `services_get` → `services_delete` → `services_get` (verify deleted) | 90s | ⬜ | |
| OA-P06 | Positive | Stress | `organizations_list` → `organizations_create` → `organizations_get` → `organizations_list_suborganizations` | 60s | ⬜ | |
| OA-P07 | Positive | Chain | `organizations_list` → `endpoint_list` → `ticketing_webhook_url_get` | 35s | ⬜ | |
| OA-P08 | Positive | Chain | `organizations_list` → `endpoint_scm_connector_prepare` | 25s | ⬜ | |
| OA-N01 | Negative | Selection | `services_add` (empty name) | 15s | ⬜ | |
| OA-N02 | Negative | Selection | `services_delete` (nil ID) | 15s | ⬜ | |
| OA-N03 | Negative | Selection | `organizations_create` (empty displayName) | 15s | ⬜ | |
| OA-N04 | Negative | Selection | `properties_add` (nil resource) | 15s | ⬜ | |
| OA-N05 | Negative | Selection | `property_delete` (non-existent key) | 15s | ⬜ | |
| OA-N06 | Negative | Selection | `properties_get` (nil resource) | 15s | ⬜ | |
| OA-N07 | Negative | Selection | `endpoint_list` (nil org) | 15s | ⬜ | |
| OA-N08 | Negative | Selection | `ticketing_webhook_url_get` (no ticketing endpoint) | 15s | ⬜ | |
| OA-E01 | Edge | Chain | `organizations_list` → `services_add` → `properties_add` ×3 → `properties_list` → `property_delete` ×3 → `services_delete` | 120s | ⬜ | Multiple properties |
| OA-E02 | Edge | Chain | `organizations_list` → `services_add` → `services_list` (verify count) → `services_delete` | 60s | ⬜ | |
| OA-E03 | Edge | Chain | `organizations_list` → `organizations_create` → `resources_list` (new suborg's children) | 60s | ⬜ | |
| OA-E04 | Edge | Chain | `organizations_list` → `endpoint_add` → `endpoint_list` (verify) | 60s | ⬜ | |
| OA-E05 | Edge | Chain | `services_list` → `properties_list` → `properties_get` (cross-verify) | 35s | ⬜ | |
| OA-E06 | Edge | Chain | `organizations_list` → `organizations_create` (duplicate domainName) | 45s | ⬜ | |
| OA-E07 | Edge | Chain | `organizations_list` → `services_add` → `services_delete` → `services_get` (confirm 404) | 60s | ⬜ | |
| OA-E08 | Edge | Chain | `organizations_list` → `endpoint_list` → `extensions_list` (cross-check available integrations) | 35s | ⬜ | |

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
> Call `organizations_list` for org IDs; `services_list` for component IDs.
> Nil UUID for negative tests: `00000000-0000-0000-0000-000000000099`

---

## POSITIVE TEST CASES

---

### OA-P01 — List Endpoints for Organization
**Discovery:** `Chain` | **Expected:** `organizations_list → endpoint_list` | **Timeout:** `20s`

```
Call organizations_list to get the org ID.
Call endpoint_list for that organization.
Report: each endpoint's id, name, and type (integration, environment, notification channel, automation action).
Total endpoint count.
```

---

### OA-P02 — List Extension Manifests
**Discovery:** `Chain` | **Expected:** `organizations_list → extensions_list` | **Timeout:** `20s`

```
Call organizations_list to get the org ID.
Call extensions_list for that organization.
Report: each extension manifest's name and version.
If none exist, record "0 extensions — empty result OK".
```

---

### OA-P03 — Get Properties for a Component
**Discovery:** `Chain` | **Expected:** `services_list → properties_get` | **Timeout:** `25s`

```
Call services_list to find a component.
Call properties_get for that component (using its resource ID).
Report: each property's name and value.
If no properties exist, record "0 properties — empty result OK".
```

---

### OA-P04 — Add, Verify, and Delete a Property on a Component
**Discovery:** `Stress` | **Expected:** `organizations_list → services_list → properties_add → properties_get → property_delete → properties_get (verify)` | **Timeout:** `90s`

```
1. Call organizations_list to get the org ID.
2. Call services_list to get a component ID.
3. Add a property named "oa-p04-test-key" with value "oa-p04-test-value" using properties_add.
4. Call properties_get — verify the property appears.
5. Delete the property using property_delete.
6. Call properties_get again — verify "oa-p04-test-key" no longer appears.
Report each step's outcome.
```

---

### OA-P05 — Service Create, Get, and Delete Lifecycle
**Discovery:** `Stress` | **Expected:** `organizations_list → services_add → services_get → services_delete → services_get (verify)` | **Timeout:** `90s`

```
1. Call organizations_list to get the org ID.
2. Create a new service (component) named "oa-p05-test-service" using services_add.
3. Call services_get with the returned serviceId — verify name matches.
4. Delete the service using services_delete.
5. Call services_get again — verify 404 is returned.
Report each step's outcome.
```

---

### OA-P06 — Create Sub-Organization and Verify in Hierarchy
**Discovery:** `Stress` | **Expected:** `organizations_list → organizations_create → organizations_get → organizations_list_suborganizations` | **Timeout:** `60s`

```
1. Call organizations_list to get the root org ID.
2. Create a sub-org with displayName "oa-p06-test-suborg" and domainName "oa-p06-test-suborg" under the root.
3. Call organizations_get with the new org's ID — verify displayName matches.
4. Call organizations_list_suborganizations — verify the new sub-org appears.
Report each step. Note: manual cleanup may be required (no org delete tool).
```

---

### OA-P07 — Get Ticketing Webhook URL
**Discovery:** `Chain` | **Expected:** `organizations_list → endpoint_list → ticketing_webhook_url_get` | **Timeout:** `35s`

```
1. Call organizations_list to get the org ID.
2. Call endpoint_list to find a ticketing integration endpoint.
3. If a ticketing endpoint exists, call ticketing_webhook_url_get for it.
4. Report the webhook URL returned.
If no ticketing endpoint exists, record "No ticketing integration found — test skipped".
```

---

### OA-P08 — Prepare SCM Connector Endpoint
**Discovery:** `Chain` | **Expected:** `organizations_list → endpoint_scm_connector_prepare` | **Timeout:** `25s`

```
1. Call organizations_list to get the org ID.
2. Call endpoint_scm_connector_prepare to initiate a new GitHub App SCM connector for that org.
3. Report: the returned redirect URL and the pending state of the endpoint.
Note: this is a two-step process. The redirect URL is what a user would visit to complete GitHub App installation. Do NOT follow the URL.
```

---

## NEGATIVE TEST CASES

---

### OA-N01 — Create Service with Empty Name
**Discovery:** `Selection` | **Expected:** `services_add` | **Timeout:** `15s`

```
Call organizations_list to get the org ID.
Attempt services_add with name="" (empty string).
Record the exact error message. Expected: 400 validation error.
```

---

### OA-N02 — Delete Non-Existent Service
**Discovery:** `Selection` | **Expected:** `services_delete` | **Timeout:** `15s`

```
Call services_delete with a nil service ID: 00000000-0000-0000-0000-000000000099.
Record the exact error message and HTTP status code. Expected: 404.
```

---

### OA-N03 — Create Organization with Empty Display Name
**Discovery:** `Selection` | **Expected:** `organizations_create` | **Timeout:** `15s`

```
Call organizations_list to get the root org ID.
Attempt organizations_create with displayName="" (empty string).
Record the exact error message. Expected: 400 validation error.
```

---

### OA-N04 — Add Property to Non-Existent Resource
**Discovery:** `Selection` | **Expected:** `properties_add` | **Timeout:** `15s`

```
Attempt properties_add with a nil resource ID: 00000000-0000-0000-0000-000000000099 and key="test-key", value="test-value".
Record the exact error message and HTTP status code. Expected: 404 or 400.
```

---

### OA-N05 — Delete Non-Existent Property Key
**Discovery:** `Selection` | **Expected:** `property_delete` | **Timeout:** `15s`

```
Call services_list to get a real component ID.
Attempt property_delete with key="nonexistent-property-key-xyz-9999" on that component.
Record the exact error message. Expected: 404.
```

---

### OA-N06 — Get Properties for Non-Existent Resource
**Discovery:** `Selection` | **Expected:** `properties_get` | **Timeout:** `15s`

```
Call properties_get with a nil resource ID: 00000000-0000-0000-0000-000000000099.
Record the exact error message and HTTP status code. Expected: 404 or 400.
```

---

### OA-N07 — List Endpoints for Non-Existent Org
**Discovery:** `Selection` | **Expected:** `endpoint_list` | **Timeout:** `15s`

```
Call endpoint_list with a nil org ID: 00000000-0000-0000-0000-000000000099.
Record the exact error message and HTTP status code. Expected: 404 or 400.
```

---

### OA-N08 — Get Ticketing Webhook URL with No Endpoint
**Discovery:** `Selection` | **Expected:** `ticketing_webhook_url_get` | **Timeout:** `15s`

```
Attempt ticketing_webhook_url_get with a nil endpoint instance ID: 00000000-0000-0000-0000-000000000099.
Record the exact error message. Expected: 404 or 400.
```

---

## EDGE CASES

---

### OA-E01 — Add Multiple Properties to a Component
**Discovery:** `Stress` | **Expected:** `organizations_list → services_add → properties_add ×3 → properties_list → property_delete ×3 → services_delete` | **Timeout:** `120s`

```
1. Create a service "oa-e01-multi-prop".
2. Add three properties: "key-alpha"="val1", "key-beta"="val2", "key-gamma"="val3".
3. Call properties_list — verify all three appear.
4. Delete all three properties using property_delete.
5. Call properties_list again — verify all three are gone.
6. Delete the service.
```

---

### OA-E02 — Verify Service Appears in List After Creation
**Discovery:** `Chain` | **Expected:** `organizations_list → services_add → services_list (verify) → services_delete` | **Timeout:** `60s`

```
1. Call services_list and record the total service count (before).
2. Create a service named "oa-e02-count-check".
3. Call services_list again — verify the count increased by 1 and "oa-e02-count-check" is present.
4. Delete the service.
5. Call services_list once more — verify it is removed.
```

---

### OA-E03 — New Sub-Org Starts with No Children
**Discovery:** `Chain` | **Expected:** `organizations_list → organizations_create → resources_list (new suborg)` | **Timeout:** `60s`

```
1. Create a sub-org "oa-e03-empty-suborg".
2. Call resources_list using the new sub-org's ID.
3. Verify: no children resources are present. Empty result is expected and OK.
Note: manual cleanup required.
```

---

### OA-E04 — Add Endpoint and Verify in List
**Discovery:** `Chain` | **Expected:** `organizations_list → endpoint_add → endpoint_list (verify)` | **Timeout:** `60s`

```
1. Call organizations_list to get the org ID.
2. Add a new endpoint (e.g., a notification channel) using endpoint_add.
3. Call endpoint_list — verify the new endpoint appears in the list.
Report: the new endpoint's id, name, and type.
Note: cleanup may require manual deletion if no endpoint_delete tool exists.
```

---

### OA-E05 — Cross-Verify Properties via properties_list and properties_get
**Discovery:** `Chain` | **Expected:** `services_list → properties_list → properties_get` | **Timeout:** `35s`

```
1. Call services_list to get a component ID.
2. Call properties_list for that component — record each property name.
3. Call properties_get for the same component — record each property name.
4. Verify: both calls return the same set of property names.
Report any fields that appear in one response but not the other.
```

---

### OA-E06 — Create Sub-Org with Duplicate Domain Name
**Discovery:** `Chain` | **Expected:** `organizations_list → organizations_create → organizations_create (duplicate)` | **Timeout:** `45s`

```
1. Call organizations_list to get the root org ID.
2. Create a sub-org with domainName "oa-e06-dup-domain".
3. Attempt to create another sub-org with the same domainName "oa-e06-dup-domain".
4. Record the exact error from step 3. Expected: 409 Conflict or 400.
Note: manual cleanup required for the first sub-org.
```

---

### OA-E07 — Verify Service Deletion is Immediate
**Discovery:** `Chain` | **Expected:** `organizations_list → services_add → services_delete → services_get (confirm 404)` | **Timeout:** `60s`

```
1. Create a service "oa-e07-immediate-delete".
2. Delete it using services_delete.
3. Immediately call services_get with the deleted serviceId.
4. Verify: 404 is returned — deletion is immediately visible.
```

---

### OA-E08 — Cross-Check Endpoints vs Extensions
**Discovery:** `Chain` | **Expected:** `organizations_list → endpoint_list → extensions_list` | **Timeout:** `35s`

```
1. Call organizations_list to get the org ID.
2. Call endpoint_list — record the types and names of all endpoints.
3. Call extensions_list — record the names of all available extension manifests.
4. Note the relationship: are any extensions already installed as endpoints?
Report which extensions appear as active endpoints and which are available but not installed.
```
