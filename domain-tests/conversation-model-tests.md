# Conversation Model Test Cases
**Domains:** RBAC · Security Advanced · Services & Endpoints · Search, Properties & Resources  
**Purpose:** Minimal, story-driven flows for conversational testing across locations/agents.  
**Org:** `6c5eeb79-4606-4c39-bd5c-c2323336caad` · Component (go): `95fdf71c-de53-43e4-b5dc-bec7170becd6`

---

## RBAC

### RBAC-CONV-01 — Role Lifecycle
**Tools:** `rbac_permissions_list`, `rbac_role_create`, `rbac_role_get`, `rbac_roles_list`, `rbac_role_delete`

1. List all available permissions in the org.
2. Create a custom role named "rbac-conv-test-role".
3. Fetch the role by its new ID and confirm the name matches.
4. List all roles and verify the new role appears.
5. Delete the role.
6. Try to fetch the deleted role — confirm it returns a not-found error.

---

### RBAC-CONV-02 — Assign a Role and Check Permissions
**Tools:** `rbac_role_create`, `user_whoami`, `rbac_authorization_create`, `rbac_authorizations_list`, `rbac_authorization_check_bulk`, `rbac_role_delete`

1. Create a role named "rbac-authz-conv-role".
2. Assign that role to yourself (get your user ID first via whoami).
3. List all authorizations and confirm your new assignment appears.
4. Run a bulk permission check for 3–5 permissions — report which ones you have.
5. Delete the test role.

---

### RBAC-CONV-03 — Duplicate and Error Handling
**Tools:** `rbac_role_create`, `rbac_role_get`, `rbac_role_delete`

1. Create a role named "rbac-dup-conv-test".
2. Try to create a second role with the same name — record what happens.
3. Try to fetch a role with a made-up ID (`00000000-0000-0000-0000-000000000099`) — record the error.
4. Delete the first role.

---

## Security Advanced

### SA-CONV-01 — Security Config Read and Toggle
**Tools:** `security_configuration_get`, `security_configuration_hierarchy_get`, `security_configuration_set`

1. Get the current security configuration for the org.
2. Get the configuration hierarchy and note which fields are inherited vs explicitly set.
3. Toggle a safe boolean field to the opposite value.
4. Read the configuration back and confirm the change is visible.
5. Restore the original value and confirm it reverted.

---

### SA-CONV-02 — SLA Configuration Cycle
**Tools:** `security_sla_configuration_get`, `security_sla_configuration_set`, `security_sla_configuration_remove`

1. Get the current SLA configuration (note the remediation windows per severity).
2. Update the LOW severity window by 1 day from its current value.
3. Read the SLA config back immediately and confirm the change stuck.
4. Remove the custom SLA override for the org.
5. Read the SLA config again and confirm it shows default/inherited values.

---

### SA-CONV-03 — Plugin Lifecycle
**Tools:** `security_filter_tools_list`, `security_plugin_config_get`, `security_plugin_activate`, `security_plugin_config_set`, `security_plugin_deactivate`

1. List available security filter tools to find a valid plugin name.
2. Get the current configuration for that plugin.
3. Activate the plugin — note if it is already active (idempotent).
4. Update one non-critical config field on the plugin.
5. Read the plugin config back and confirm the updated value is saved.
6. Deactivate the plugin and confirm the config is still readable after.

---

### SA-CONV-04 — Implicit Scans Toggle
**Tools:** `security_configuration_get`, `security_implicit_scans_set`

1. Get the current security configuration and note whether implicit scans are on or off.
2. Toggle implicit scans to the opposite state.
3. Read the configuration back and confirm the change.
4. Toggle it back to the original state and confirm it is restored.

---

## Services & Endpoints

### SE-CONV-01 — Service Lifecycle
**Tools:** `services_list`, `services_add`, `services_get`, `services_delete`

1. List all existing services in the org.
2. Create a new service named "se-conv-test-service".
3. List services again and confirm the new one appears.
4. Fetch the service by its ID and review the full detail fields.
5. Delete the service.
6. Try to fetch the deleted service — confirm it returns a not-found error.

---

### SE-CONV-02 — Endpoint Add, Disable, and Verify
**Tools:** `endpoint_list`, `endpoint_add`, `endpoint_disable`, `endpoint_get`

1. List all existing endpoints in the org.
2. Add a new test endpoint named "se-conv-test-endpoint".
3. Confirm it appears in the endpoint list with `isDisabled=false`.

---

### SE-CONV-03 — SCM Connectors and Ticketing Webhook
**Tools:** `ticketing_webhook_url_get`, `endpoint_scm_connector_prepare`, `endpoint_list`

1. Get the ticketing webhook URL for the org and record it.

---

### SE-CONV-04 — Duplicate and Error Handling
**Tools:** `services_list`, `services_add`, `services_get`, `services_delete`

1. List existing services and pick a name that already exists (or create one).
2. Try to create a second service with the same name — record whether the server allows it or rejects it.
3. Try to get a service with a made-up ID (`00000000-0000-0000-0000-000000000099`) — record the error.

---

## Search, Properties & Resources

### SP-CONV-01 — Property Lifecycle
**Tools:** `properties_list`, `properties_add`, `properties_get`, `property_delete`

1. List all properties on the go component.
2. Add a new property with name `SP_CONV_TEST`, value `conv-test-value`, type `string`.
3. List properties again and confirm the new one appears.
4. Fetch the property by its ID and confirm the details match.
5. Delete the property.
6. Try to fetch the deleted property — confirm it returns a not-found error.

---

### SP-CONV-02 — Search Resources and Drill In
**Tools:** `search_resources`, `resources_get`

1. Search resources with a broad keyword (e.g., "auto") and note the total result count and resource types.

---

### SP-CONV-03 — Search Runs by Status
**Tools:** `search_runs`

1. Search for pipeline runs from the past 7 days with status `SUCCESS` — record the count.
2. Search for runs with status `FAILURE` — record the count.

---

### SP-CONV-04 — Resources List and Detail Consistency
**Tools:** `resources_list`, `resources_get`

1. List all resources for the go component filtered by branch type.
2. For each resource returned (up to 5), fetch its full details via `resources_get`.
3. Verify every ID from the list is fetchable.
4. Note any fields visible in the detail view that are not in the list view.
