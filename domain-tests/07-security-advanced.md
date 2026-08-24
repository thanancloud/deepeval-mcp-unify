# Domain: Security — Advanced (Configuration, Plugins, SLA)
**Tools covered (12):** `security_configuration_get`, `security_configuration_hierarchy_get`, `security_configuration_set`, `security_plugin_activate`, `security_plugin_deactivate`, `security_plugin_config_get`, `security_plugin_config_set`, `security_sla_configuration_get`, `security_sla_configuration_set`, `security_sla_configuration_remove`, `security_tenant_sla_configuration_remove`, `security_implicit_scans_set`
**Total prompts:** 24 (8 positive, 8 negative, 8 edge cases)

---

## Test Execution Tracker

| ID | Type | Category | Expected Tools | Timeout | Description | Status | Notes |
|----|------|----------|----------------|---------|-------------|--------|-------|
| SA-P01 | Positive | Selection | `security_configuration_get` | 15s | Get security configuration for the organization | ⬜ | |
| SA-P02 | Positive | Selection | `security_configuration_hierarchy_get` | 15s | Get security configuration hierarchy | ⬜ | |
| SA-P03 | Positive | Chain | `security_configuration_get → security_configuration_set` | 30s | Read config then update a field and restore it | ⬜ | |
| SA-P04 | Positive | Selection | `security_sla_configuration_get` | 15s | Get SLA configuration for the organization | ⬜ | |
| SA-P05 | Positive | Chain | `security_sla_configuration_get → security_sla_configuration_set` | 30s | Read SLA config then update it | ⬜ | |
| SA-P06 | Positive | Selection | `security_plugin_config_get` | 15s | Get plugin configuration for a known security plugin | ⬜ | |
| SA-P07 | Positive | Chain | `security_plugin_activate → security_plugin_config_get` | 30s | Activate a plugin and verify it is configurable | ⬜ | |
| SA-P08 | Positive | Chain | `security_configuration_get → security_implicit_scans_set` | 30s | Enable implicit scans and verify the change | ⬜ | |
| SA-N01 | Negative | Selection | `security_configuration_get` | 15s | Get security config with invalid organizationId | ⬜ | |
| SA-N02 | Negative | Selection | `security_sla_configuration_get` | 15s | Get SLA config with invalid organizationId | ⬜ | |
| SA-N03 | Negative | Selection | `security_plugin_config_get` | 15s | Get plugin config for non-existent pluginId | ⬜ | |
| SA-N04 | Negative | Selection | `security_plugin_activate` | 15s | Activate non-existent plugin | ⬜ | |
| SA-N05 | Negative | Selection | `security_plugin_deactivate` | 15s | Deactivate a plugin that is not active | ⬜ | |
| SA-N06 | Negative | Selection | `security_sla_configuration_remove` | 15s | Remove SLA config that was never set | ⬜ | |
| SA-N07 | Negative | Selection | `security_configuration_set` | 15s | Set configuration with invalid values | ⬜ | |
| SA-N08 | Negative | Selection | `security_tenant_sla_configuration_remove` | 15s | Remove tenant SLA with invalid organizationId | ⬜ | |
| SA-E01 | Edge | Chain | `security_sla_configuration_set → security_sla_configuration_get` | 30s | Set SLA config and immediately read it back | ⬜ | |
| SA-E02 | Edge | Chain | `security_sla_configuration_set → security_sla_configuration_remove → security_sla_configuration_get` | 45s | Set, remove, and verify SLA config is cleared | ⬜ | |
| SA-E03 | Edge | Chain | `security_plugin_activate → security_plugin_config_set → security_plugin_config_get` | 45s | Activate plugin, update config, verify persisted | ⬜ | |
| SA-E04 | Edge | Chain | `security_plugin_deactivate → security_plugin_config_get` | 30s | Deactivate plugin then verify its config state | ⬜ | |
| SA-E05 | Edge | Chain | `security_configuration_hierarchy_get → security_configuration_get` | 30s | Compare hierarchy vs flat config — check inheritance | ⬜ | |
| SA-E06 | Edge | Selection | `security_implicit_scans_set` | 15s | Toggle implicit scans off then back on | ⬜ | |
| SA-E07 | Edge | Chain | `security_configuration_set (×2)` | 30s | Update same config field twice — last write wins | ⬜ | |
| SA-E08 | Edge | Stress | `security_sla_configuration_get → security_sla_configuration_set → security_configuration_set → security_plugin_config_get → security_implicit_scans_set` | 90s | Multi-setting security configuration session | ⬜ | |

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

### SA-P01 — Get Security Configuration for the Organization

**Discovery:** `Selection` | **Expected:** `security_configuration_get` | **Timeout:** `15s`

```
Get the security configuration for organizationId 6c5eeb79-4606-4c39-bd5c-c2323336caad.
Verify:
- Response is not an error
- Returns a configuration object with fields describing security settings (enabled features, scan policies, etc.)
Report: all configuration fields returned and their current values. This establishes the baseline security configuration.
```

---

### SA-P02 — Get Security Configuration Hierarchy

**Discovery:** `Selection` | **Expected:** `security_configuration_hierarchy_get` | **Timeout:** `15s`

```
Get the security configuration hierarchy for organizationId 6c5eeb79-4606-4c39-bd5c-c2323336caad.
Verify:
- Response is not an error
- Returns a hierarchy object showing inherited configuration from parent orgs vs overrides at this org level
Report: the full hierarchy structure, noting which fields are inherited vs explicitly set. This tests whether the hierarchy endpoint returns richer data than the flat get endpoint.
```

---

### SA-P03 — Read Config Then Update a Field and Restore

**Discovery:** `Chain` | **Expected:** `security_configuration_get → security_configuration_set` | **Timeout:** `30s`

```
1. Get the current security configuration for organizationId 6c5eeb79-4606-4c39-bd5c-c2323336caad. Record the current values.
2. Identify a safe-to-toggle boolean field in the configuration.
3. Set the configuration with that field toggled to the opposite value.
4. Get the configuration again to verify the change was applied.
5. Restore the original value by calling set again with the original.

Report: which field was toggled, the original value, the new value after update, and confirmation that the restore succeeded. Document the response format for configuration_set.
```

---

### SA-P04 — Get SLA Configuration for the Organization

**Discovery:** `Selection` | **Expected:** `security_sla_configuration_get` | **Timeout:** `15s`

```
Get the SLA configuration for organizationId 6c5eeb79-4606-4c39-bd5c-c2323336caad.
Verify:
- Response is not an error
- Returns SLA settings (remediation windows per severity: VERY_HIGH, HIGH, MEDIUM, LOW)
Report: all SLA fields returned, the number of days configured per severity, and whether SLA enforcement is enabled.
```

---

### SA-P05 — Read SLA Config Then Update It

**Discovery:** `Chain` | **Expected:** `security_sla_configuration_get → security_sla_configuration_set` | **Timeout:** `30s`

```
1. Get the current SLA configuration for organizationId 6c5eeb79-4606-4c39-bd5c-c2323336caad. Record current SLA windows.
2. Set the SLA configuration — update the LOW severity window (e.g., add 1 day to whatever the current value is).
3. Get the SLA configuration again to verify the change was applied.
4. Restore the original SLA values.

Report: the original and updated SLA values, and whether the update was immediately reflected. Document the response format for sla_configuration_set.
```

---

### SA-P06 — Get Plugin Configuration for a Known Security Plugin

**Discovery:** `Selection` | **Expected:** `security_plugin_config_get` | **Timeout:** `15s`

```
Get the plugin configuration for organizationId 6c5eeb79-4606-4c39-bd5c-c2323336caad. Use one of the known security plugins (e.g., trivy, snyk, semgrep, or the first plugin in the security_filter_tools_list result).
Verify:
- Response is not an error
- Returns plugin-specific configuration fields
Report: the plugin name/id, all configuration fields returned, and their current values (masked if secrets).
```

---

### SA-P07 — Activate a Plugin and Verify It Is Configurable

**Discovery:** `Chain` | **Expected:** `security_plugin_activate → security_plugin_config_get` | **Timeout:** `30s`

```
1. Activate a security plugin for organizationId 6c5eeb79-4606-4c39-bd5c-c2323336caad (use a known plugin name from the available list, such as trivy or semgrep). Record the response.
2. Get the plugin configuration for that plugin.

Verify: activation succeeds (or is already active), and the config is readable after activation. Report: the activation response and the plugin configuration fields returned.
Note: if the plugin is already active, the activate call should be idempotent — document that behavior.
```

---

### SA-P08 — Enable Implicit Scans and Verify the Change

**Discovery:** `Chain` | **Expected:** `security_configuration_get → security_implicit_scans_set` | **Timeout:** `30s`

```
1. Get the current security configuration for organizationId 6c5eeb79-4606-4c39-bd5c-c2323336caad. Note the current state of implicit scans (enabled or disabled).
2. Call security_implicit_scans_set to enable implicit scans (set to true).
3. Get the configuration again to verify the change was applied.
4. Restore to the original state.

Report: the original state, the response from implicit_scans_set, and confirmation the change was reflected in the configuration. Document the exact field name that controls implicit scans.
```

---

## NEGATIVE TEST CASES

---

### SA-N01 — Get Security Config With Invalid organizationId

**Discovery:** `Selection` | **Expected:** `security_configuration_get` | **Timeout:** `15s`

```
Get the security configuration for:
- organizationId: 00000000-0000-0000-0000-000000000099

Record the exact error response. Expected: 404 (org not found) or 403 (forbidden). Document the HTTP status and error message.
```

---

### SA-N02 — Get SLA Config With Invalid organizationId

**Discovery:** `Selection` | **Expected:** `security_sla_configuration_get` | **Timeout:** `15s`

```
Get the SLA configuration for:
- organizationId: 00000000-0000-0000-0000-000000000099

Record the exact error response. Expected: 404 or 403. Does the server return an error or default SLA values? Document the full response.
```

---

### SA-N03 — Get Plugin Config for Non-Existent pluginId

**Discovery:** `Selection` | **Expected:** `security_plugin_config_get` | **Timeout:** `15s`

```
Get plugin configuration with:
- organizationId: 6c5eeb79-4606-4c39-bd5c-c2323336caad
- pluginId: "this-plugin-does-not-exist-xyz"

Record the exact error response. Expected: 404 (plugin not found) or 400. Document the HTTP status and error message.
```

---

### SA-N04 — Activate Non-Existent Plugin

**Discovery:** `Selection` | **Expected:** `security_plugin_activate` | **Timeout:** `15s`

```
Activate a security plugin with:
- organizationId: 6c5eeb79-4606-4c39-bd5c-c2323336caad
- pluginId: "fake-scanner-plugin-xyz"

Record the exact error response. Expected: 404 (plugin not found) or 400. Document the full error response.
```

---

### SA-N05 — Deactivate a Plugin That Is Not Active

**Discovery:** `Selection` | **Expected:** `security_plugin_deactivate` | **Timeout:** `15s`

```
Deactivate a security plugin that is known to not be activated in this org (use a plugin name that is not in the active list):
- organizationId: 6c5eeb79-4606-4c39-bd5c-c2323336caad
- pluginId: "fake-scanner-plugin-xyz" or a known inactive plugin

Record the exact response. Does it return 404, 400, or is deactivation idempotent (returns success even if not active)? Document the behavior.
```

---

### SA-N06 — Remove SLA Config That Was Never Set

**Discovery:** `Selection` | **Expected:** `security_sla_configuration_remove` | **Timeout:** `15s`

```
Remove the SLA configuration for a sub-organization that has no custom SLA set:
- organizationId: 6c5eeb79-4606-4c39-bd5c-c2323336caad
- subOrganizationId: (use a sub-org that inherits from parent, not one with a custom SLA)

Record the exact response. Does removing a non-existent custom SLA return 404, 200 (idempotent), or another status? This tests the remove-when-not-set behavior.
```

---

### SA-N07 — Set Configuration With Invalid Values

**Discovery:** `Selection` | **Expected:** `security_configuration_set` | **Timeout:** `15s`

```
Attempt to set the security configuration with invalid values:
- organizationId: 6c5eeb79-4606-4c39-bd5c-c2323336caad
- Provide a configuration field with an out-of-range value (e.g., a numeric threshold set to -1, or a boolean field set to "not-a-bool")

Record the exact error response. Expected: 400 Bad Request with validation details. Document which field triggered the error and the full validation message.
```

---

### SA-N08 — Remove Tenant SLA With Invalid organizationId

**Discovery:** `Selection` | **Expected:** `security_tenant_sla_configuration_remove` | **Timeout:** `15s`

```
Remove the tenant-level SLA configuration for:
- organizationId: 00000000-0000-0000-0000-000000000099

Record the exact error response. Expected: 404 (org not found) or 403 (forbidden). Document the HTTP status and error message. This tests the tenant-level SLA removal path with a bad org ID.
```

---

## EDGE CASES

---

### SA-E01 — Set SLA Config Then Immediately Read It Back

**Discovery:** `Chain` | **Expected:** `security_sla_configuration_set → security_sla_configuration_get` | **Timeout:** `30s`

```
1. Set the SLA configuration for organizationId 6c5eeb79-4606-4c39-bd5c-c2323336caad with explicit values for all severity levels:
   - VERY_HIGH: 1 day
   - HIGH: 7 days
   - MEDIUM: 30 days
   - LOW: 90 days
2. Immediately get the SLA configuration.

Verify: all four severity SLA values match exactly what was set. Report any discrepancy. Restore original SLA values after. This tests write-then-read consistency.
```

---

### SA-E02 — Set, Remove, and Verify SLA Config Is Cleared

**Discovery:** `Chain` | **Expected:** `security_sla_configuration_set → security_sla_configuration_remove → security_sla_configuration_get` | **Timeout:** `45s`

```
1. Set a custom SLA configuration for a sub-organization under organizationId 6c5eeb79-4606-4c39-bd5c-c2323336caad.
2. Remove the custom SLA for the same sub-org.
3. Get the SLA configuration — verify it has reverted to inherited/default values.

Report: the set response, the remove response, and the final get result. This tests the full set → remove → inherit cycle.
```

---

### SA-E03 — Activate Plugin, Update Config, Verify Persisted

**Discovery:** `Chain` | **Expected:** `security_plugin_activate → security_plugin_config_set → security_plugin_config_get` | **Timeout:** `45s`

```
1. Activate a known security plugin for organizationId 6c5eeb79-4606-4c39-bd5c-c2323336caad.
2. Set the plugin configuration with a test value (e.g., update a non-critical config field).
3. Get the plugin configuration and verify the updated value is returned.

Report: the plugin name, the config field updated, the before/after values, and whether the update was immediately visible. This tests the activate → configure → verify pipeline.
```

---

### SA-E04 — Deactivate Plugin Then Verify Config State

**Discovery:** `Chain` | **Expected:** `security_plugin_deactivate → security_plugin_config_get` | **Timeout:** `30s`

```
1. Deactivate a security plugin for organizationId 6c5eeb79-4606-4c39-bd5c-c2323336caad (use a non-critical plugin, not one that would disrupt active scanning).
2. Attempt to get the plugin configuration after deactivation.

Verify: is the config still accessible after deactivation, or does the get return an error? Report the deactivation response and the config-get result. Re-activate the plugin to restore state.
```

---

### SA-E05 — Compare Hierarchy vs Flat Config — Check Inheritance

**Discovery:** `Chain` | **Expected:** `security_configuration_hierarchy_get → security_configuration_get` | **Timeout:** `30s`

```
1. Get the security configuration hierarchy for organizationId 6c5eeb79-4606-4c39-bd5c-c2323336caad.
2. Get the flat security configuration for the same org.

Compare: are all fields in the flat config also present in the hierarchy? Does the hierarchy show any fields that are inherited from a parent org but not visible in the flat config? Report all differences between the two responses. This tests whether the hierarchy endpoint provides additive information.
```

---

### SA-E06 — Toggle Implicit Scans Off Then Back On

**Discovery:** `Selection` | **Expected:** `security_implicit_scans_set` | **Timeout:** `15s`

```
1. Get the current implicit scans state for organizationId 6c5eeb79-4606-4c39-bd5c-c2323336caad.
2. Set implicit scans to false (disabled).
3. Get the configuration and verify it shows disabled.
4. Set implicit scans back to true (enabled).
5. Get the configuration and verify it shows enabled.

Report: each step result, confirming the toggle works in both directions. This tests the implicit scans feature flag in both states.
```

---

### SA-E07 — Update Same Config Field Twice — Last Write Wins

**Discovery:** `Chain` | **Expected:** `security_configuration_set (×2)` | **Timeout:** `30s`

```
1. Get the current security configuration for organizationId 6c5eeb79-4606-4c39-bd5c-c2323336caad. Note the original value of a safe-to-toggle field.
2. Set that field to value A.
3. Immediately set the same field to value B (different from A).
4. Get the configuration — verify value B is the current value.

This tests that last-write-wins semantics are respected. Report the sequence of values and confirm the final state. Restore the original value.
```

---

### SA-E08 — Multi-Setting Security Configuration Session

**Discovery:** `Stress` | **Expected:** `security_sla_configuration_get → security_sla_configuration_set → security_configuration_set → security_plugin_config_get → security_implicit_scans_set` | **Timeout:** `90s`

```
Execute a sequence of security configuration operations for organizationId 6c5eeb79-4606-4c39-bd5c-c2323336caad:
1. Get SLA configuration — record all current values.
2. Update the SLA configuration (change one severity window by 1 day).
3. Set a non-critical security configuration field (toggle a safe boolean).
4. Get the plugin configuration for the first available plugin.
5. Set implicit scans to the current value (no-op write to confirm idempotency).
6. Get SLA configuration again — verify changes from step 2 persisted.
7. Restore all original values.

Report: each step result, total elapsed time, and whether all 7 operations completed within the 90s timeout. Flag any step that takes longer than 15s individually.
```
