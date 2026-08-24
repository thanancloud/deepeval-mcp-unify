# Organization Administration — Prompts Only

---

## POSITIVE TEST CASES

### OA-P01 — List Endpoints for Organization

```
Call organizations_list to get the org ID.
Call endpoint_list for that organization.
Report: each endpoint's id, name, and type (integration, environment, notification channel, automation action).
Total endpoint count.
```

---

### OA-P02 — List Extension Manifests

```
Call organizations_list to get the org ID.
Call extensions_list for that organization.
Report: each extension manifest's name and version.
If none exist, record "0 extensions — empty result OK".
```

---

### OA-P03 — Get Properties for a Component

```
Call services_list to find a component.
Call properties_get for that component (using its resource ID).
Report: each property's name and value.
If no properties exist, record "0 properties — empty result OK".
```

---

### OA-P04 — Add, Verify, and Delete a Property on a Component

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

```
1. Call organizations_list to get the root org ID.
2. Create a sub-org with displayName "oa-p06-test-suborg" and domainName "oa-p06-test-suborg" under the root.
3. Call organizations_get with the new org's ID — verify displayName matches.
4. Call organizations_list_suborganizations — verify the new sub-org appears.
Report each step. Note: manual cleanup may be required (no org delete tool).
```

---

### OA-P07 — Get Ticketing Webhook URL

```
1. Call organizations_list to get the org ID.
2. Call endpoint_list to find a ticketing integration endpoint.
3. If a ticketing endpoint exists, call ticketing_webhook_url_get for it.
4. Report the webhook URL returned.
If no ticketing endpoint exists, record "No ticketing integration found — test skipped".
```

---

### OA-P08 — Prepare SCM Connector Endpoint

```
1. Call organizations_list to get the org ID.
2. Call endpoint_scm_connector_prepare to initiate a new GitHub App SCM connector for that org.
3. Report: the returned redirect URL and the pending state of the endpoint.
Note: this is a two-step process. The redirect URL is what a user would visit to complete GitHub App installation. Do NOT follow the URL.
```

---

## NEGATIVE TEST CASES

### OA-N01 — Create Service with Empty Name

```
Call organizations_list to get the org ID.
Attempt services_add with name="" (empty string).
Record the exact error message. Expected: 400 validation error.
```

---

### OA-N02 — Delete Non-Existent Service

```
Call services_delete with a nil service ID: 00000000-0000-0000-0000-000000000099.
Record the exact error message and HTTP status code. Expected: 404.
```

---

### OA-N03 — Create Organization with Empty Display Name

```
Call organizations_list to get the root org ID.
Attempt organizations_create with displayName="" (empty string).
Record the exact error message. Expected: 400 validation error.
```

---

### OA-N04 — Add Property to Non-Existent Resource

```
Attempt properties_add with a nil resource ID: 00000000-0000-0000-0000-000000000099 and key="test-key", value="test-value".
Record the exact error message and HTTP status code. Expected: 404 or 400.
```

---

### OA-N05 — Delete Non-Existent Property Key

```
Call services_list to get a real component ID.
Attempt property_delete with key="nonexistent-property-key-xyz-9999" on that component.
Record the exact error message. Expected: 404.
```

---

### OA-N06 — Get Properties for Non-Existent Resource

```
Call properties_get with a nil resource ID: 00000000-0000-0000-0000-000000000099.
Record the exact error message and HTTP status code. Expected: 404 or 400.
```

---

### OA-N07 — List Endpoints for Non-Existent Org

```
Call endpoint_list with a nil org ID: 00000000-0000-0000-0000-000000000099.
Record the exact error message and HTTP status code. Expected: 404 or 400.
```

---

### OA-N08 — Get Ticketing Webhook URL with No Endpoint

```
Attempt ticketing_webhook_url_get with a nil endpoint instance ID: 00000000-0000-0000-0000-000000000099.
Record the exact error message. Expected: 404 or 400.
```

---

## EDGE CASES

### OA-E01 — Add Multiple Properties to a Component

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

```
1. Call services_list and record the total service count (before).
2. Create a service named "oa-e02-count-check".
3. Call services_list again — verify the count increased by 1 and "oa-e02-count-check" is present.
4. Delete the service.
5. Call services_list once more — verify it is removed.
```

---

### OA-E03 — New Sub-Org Starts with No Children

```
1. Create a sub-org "oa-e03-empty-suborg".
2. Call resources_list using the new sub-org's ID.
3. Verify: no children resources are present. Empty result is expected and OK.
Note: manual cleanup required.
```

---

### OA-E04 — Add Endpoint and Verify in List

```
1. Call organizations_list to get the org ID.
2. Add a new endpoint (e.g., a notification channel) using endpoint_add.
3. Call endpoint_list — verify the new endpoint appears in the list.
Report: the new endpoint's id, name, and type.
Note: cleanup may require manual deletion if no endpoint_delete tool exists.
```

---

### OA-E05 — Cross-Verify Properties via properties_list and properties_get

```
1. Call services_list to get a component ID.
2. Call properties_list for that component — record each property name.
3. Call properties_get for the same component — record each property name.
4. Verify: both calls return the same set of property names.
Report any fields that appear in one response but not the other.
```

---

### OA-E06 — Create Sub-Org with Duplicate Domain Name

```
1. Call organizations_list to get the root org ID.
2. Create a sub-org with domainName "oa-e06-dup-domain".
3. Attempt to create another sub-org with the same domainName "oa-e06-dup-domain".
4. Record the exact error from step 3. Expected: 409 Conflict or 400.
Note: manual cleanup required for the first sub-org.
```

---

### OA-E07 — Verify Service Deletion is Immediate

```
1. Create a service "oa-e07-immediate-delete".
2. Delete it using services_delete.
3. Immediately call services_get with the deleted serviceId.
4. Verify: 404 is returned — deletion is immediately visible.
```

---

### OA-E08 — Cross-Check Endpoints vs Extensions

```
1. Call organizations_list to get the org ID.
2. Call endpoint_list — record the types and names of all endpoints.
3. Call extensions_list — record the names of all available extension manifests.
4. Note the relationship: are any extensions already installed as endpoints?
Report which extensions appear as active endpoints and which are available but not installed.
```
