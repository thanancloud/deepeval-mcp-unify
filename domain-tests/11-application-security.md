# Domain: Application Security
**Tools covered (17):** `security_configuration_get`, `security_configuration_hierarchy_get`, `security_configuration_set`, `security_filter_tools_list`, `security_filters_list`, `security_findings_summary_get`, `security_implicit_scans_set`, `security_issues_all_get`, `security_issues_open_get`, `security_plugin_activate`, `security_plugin_config_get`, `security_plugin_config_set`, `security_plugin_deactivate`, `security_sla_configuration_get`, `security_sla_configuration_remove`, `security_sla_configuration_set`, `security_tenant_sla_configuration_remove`
**Total prompts:** 24 (8 positive, 8 negative, 8 edge)

> **Cross-domain tools used for setup:** `user_whoami` (default), `organizations_list` (default), `organizations_list_suborganizations` (default), `services_list` (default), `branches_list` (applications-components), `flags_applications_list` (default)

---

## Test Execution Tracker

| ID | Type | Category | Expected Tools | Timeout | Status | Notes |
|----|------|----------|----------------|---------|--------|-------|
| SEC-P01 | Positive | Chain | `organizations_list` → `security_configuration_get` | 20s | ⬜ | |
| SEC-P02 | Positive | Chain | `services_list` → `security_configuration_hierarchy_get` | 25s | ⬜ | |
| SEC-P03 | Positive | Chain | `organizations_list_suborganizations` → `security_issues_all_get` | 25s | ⬜ | |
| SEC-P04 | Positive | Chain | `services_list` → `branches_list` → `security_issues_open_get` | 35s | ⬜ | |
| SEC-P05 | Positive | Chain | `services_list` → `branches_list` → `security_findings_summary_get` | 35s | ⬜ | |
| SEC-P06 | Positive | Chain | `organizations_list` → `security_plugin_config_get` → `security_plugin_activate` → `security_plugin_deactivate` | 60s | ⬜ | |
| SEC-P07 | Positive | Stress | `organizations_list` → `security_sla_configuration_get` → `security_sla_configuration_set` → `security_sla_configuration_get` → `security_sla_configuration_remove` | 90s | ⬜ | |
| SEC-P08 | Positive | Chain | `flags_applications_list` → `security_filters_list` → `security_filter_tools_list` | 35s | ⬜ | |
| SEC-N01 | Negative | Selection | `security_issues_open_get` (nil component ID) | 15s | ⬜ | |
| SEC-N02 | Negative | Chain | `services_list` → `security_findings_summary_get` (fake branchId) | 25s | ⬜ | Known Bug #6 |
| SEC-N03 | Negative | Selection | `security_configuration_get` (nil org ID) | 15s | ⬜ | |
| SEC-N04 | Negative | Selection | `security_sla_configuration_get` (nil resource) | 15s | ⬜ | |
| SEC-N05 | Negative | Selection | `security_plugin_activate` (nil resource) | 15s | ⬜ | |
| SEC-N06 | Negative | Selection | `security_plugin_config_set` (invalid config) | 15s | ⬜ | |
| SEC-N07 | Negative | Chain | `security_issues_all_get` (nil subOrg ID) | 15s | ⬜ | |
| SEC-N08 | Negative | Selection | `security_configuration_set` (nil org ID) | 15s | ⬜ | |
| SEC-E01 | Edge | Chain | `services_list` → `security_implicit_scans_set` (enable) → `security_configuration_get` → `security_implicit_scans_set` (disable) | 60s | ⬜ | |
| SEC-E02 | Edge | Chain | `organizations_list` → `security_configuration_hierarchy_get` (org level) | 25s | ⬜ | |
| SEC-E03 | Edge | Stress | `services_list` → `security_plugin_config_get` → `security_plugin_config_set` → `security_plugin_config_get` (verify) | 60s | ⬜ | |
| SEC-E04 | Edge | Chain | `services_list` → `security_sla_configuration_set` → `security_sla_configuration_get` → `security_sla_configuration_remove` → `security_sla_configuration_get` (verify inherited) | 90s | ⬜ | |
| SEC-E05 | Edge | Chain | `organizations_list_suborganizations` → `security_issues_all_get` (empty sub-org) | 25s | ⬜ | |
| SEC-E06 | Edge | Chain | `services_list` → `branches_list` → `security_issues_open_get` → `security_findings_summary_get` (cross-verify counts) | 60s | ⬜ | |
| SEC-E07 | Edge | Chain | `organizations_list` → `security_tenant_sla_configuration_remove` | 30s | ⬜ | |
| SEC-E08 | Edge | Stress | `organizations_list` → `security_configuration_get` → `security_configuration_set` → `security_configuration_get` (verify) → `security_configuration_set` (restore) | 90s | ⬜ | |

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
> Call `organizations_list` to get org ID; `services_list` to get component IDs; `branches_list` to get branch names.
> Nil UUID for negative tests: `00000000-0000-0000-0000-000000000099`

---

## POSITIVE TEST CASES

---

### SEC-P01 — Get Security Configuration for Organization
**Discovery:** `Chain` | **Expected:** `organizations_list → security_configuration_get` | **Timeout:** `20s`

```
Call organizations_list to get the current org ID.
Call security_configuration_get for that organization at platform level.
Report: all configuration fields returned (enabled/disabled states, severity thresholds, etc.).
```

---

### SEC-P02 — Get Security Configuration Hierarchy for a Component
**Discovery:** `Chain` | **Expected:** `services_list → security_configuration_hierarchy_get` | **Timeout:** `25s`

```
Call services_list to find a component (type=COMPONENT).
Call security_configuration_hierarchy_get for that component.
Report: each level in the hierarchy (tenant → org → sub-org → component) with its effective settings.
Note which settings are inherited vs explicitly set at each level.
```

---

### SEC-P03 — Get Security Issues Across All Components in Sub-Org
**Discovery:** `Chain` | **Expected:** `organizations_list_suborganizations → security_issues_all_get` | **Timeout:** `25s`

```
Call organizations_list_suborganizations to get a sub-org ID.
Call security_issues_all_get for that sub-org.
Report: total issue count by severity (critical, high, medium, low). Note Known Bug #5:
if a component in the sub-org has an empty defaultBranch, the call may abort early.
```

---

### SEC-P04 — Get Open Security Issues for a Component Branch
**Discovery:** `Chain` | **Expected:** `services_list → branches_list → security_issues_open_get` | **Timeout:** `35s`

```
Call services_list to find a component.
Call branches_list for that component to get its default or main branch name.
Call security_issues_open_get for that component and branch.
Report: total open issues, breakdown by severity, and the first 3 issue titles.
Note Known Bug #7: security_issues_open_get may ignore subOrganizationId ownership.
```

---

### SEC-P05 — Get Security Findings Summary for a Component Branch
**Discovery:** `Chain` | **Expected:** `services_list → branches_list → security_findings_summary_get` | **Timeout:** `35s`

```
Call services_list to find a component.
Call branches_list to get the default branch name.
Call security_findings_summary_get for that component and branch.
Report: all summary fields returned (total findings, by severity, by tool, etc.).
```

---

### SEC-P06 — Security Plugin Activate and Deactivate
**Discovery:** `Chain` | **Expected:** `organizations_list → security_plugin_config_get → security_plugin_activate → security_plugin_deactivate` | **Timeout:** `60s`

```
1. Call organizations_list to get the org ID.
2. Call security_plugin_config_get for the org to see all plugins and their current activation state.
3. Find a plugin that is currently INACTIVE. Activate it using security_plugin_activate.
4. Verify activation by calling security_plugin_config_get again.
5. Deactivate the same plugin using security_plugin_deactivate.
6. Verify deactivation via security_plugin_config_get.
If all plugins are already active, pick one to deactivate and re-activate.
Report each step's outcome.
```

---

### SEC-P07 — SLA Configuration Set, Get, and Remove
**Discovery:** `Stress` | **Expected:** `organizations_list → security_sla_configuration_get → security_sla_configuration_set → security_sla_configuration_get → security_sla_configuration_remove` | **Timeout:** `90s`

```
1. Call organizations_list to get the org ID.
2. Call security_sla_configuration_get to read the current SLA config. Record it.
3. Call security_sla_configuration_set to set a new SLA config (adjust one threshold).
4. Call security_sla_configuration_get again — verify the change was applied.
5. Call security_sla_configuration_remove to remove the override.
6. Call security_sla_configuration_get one more time — verify it now inherits from parent.
Report each step's outcome and the before/after SLA values.
```

---

### SEC-P08 — List Security Filters and Filter Tools for an Application
**Discovery:** `Chain` | **Expected:** `flags_applications_list → security_filters_list → security_filter_tools_list` | **Timeout:** `35s`

```
Call flags_applications_list to get a list of applications.
Pick the first application.
Call security_filters_list for that application. Report each filter's id, name, environment, and severity.
Call security_filter_tools_list for the same application. Report each filter tool's name and type.
```

---

## NEGATIVE TEST CASES

---

### SEC-N01 — Open Security Issues with Non-Existent Component
**Discovery:** `Selection` | **Expected:** `security_issues_open_get` | **Timeout:** `15s`

```
Call security_issues_open_get with a nil component ID (00000000-0000-0000-0000-000000000099) and branchName="main".
Record the exact error message and HTTP status code. Expected: 404 or 400.
```

---

### SEC-N02 — Findings Summary with Invalid Branch ID
**Discovery:** `Chain` | **Expected:** `services_list → security_findings_summary_get` | **Timeout:** `25s`

```
Call services_list to get a real component ID.
Call security_findings_summary_get with that component ID but a fabricated branchId: 00000000-0000-0000-0000-000000000099.
Record the exact error. Expected: 404 or 500 (Known Bug #6 — 500 is a backend bug, mark as ⚠️ Warn if reproduced).
```

---

### SEC-N03 — Security Configuration Get with Non-Existent Org
**Discovery:** `Selection` | **Expected:** `security_configuration_get` | **Timeout:** `15s`

```
Call security_configuration_get with a nil resource ID: 00000000-0000-0000-0000-000000000099.
Record the exact error message and HTTP status code. Expected: 404 or 400.
```

---

### SEC-N04 — SLA Configuration Get with Non-Existent Resource
**Discovery:** `Selection` | **Expected:** `security_sla_configuration_get` | **Timeout:** `15s`

```
Call security_sla_configuration_get with a nil resource ID: 00000000-0000-0000-0000-000000000099.
Record the exact error message and HTTP status code. Expected: 404 or 400.
```

---

### SEC-N05 — Plugin Activate with Non-Existent Resource
**Discovery:** `Selection` | **Expected:** `security_plugin_activate` | **Timeout:** `15s`

```
Call security_plugin_activate with a nil resource ID: 00000000-0000-0000-0000-000000000099 and a plugin name "nonexistent-plugin".
Record the exact error message and HTTP status code. Expected: 404 or 400.
```

---

### SEC-N06 — Plugin Config Set with Invalid Config
**Discovery:** `Selection` | **Expected:** `security_plugin_config_set` | **Timeout:** `15s`

```
Call organizations_list to get the org ID.
Attempt security_plugin_config_set with a completely invalid/empty config body.
Record the exact error message. Expected: 400 validation error.
```

---

### SEC-N07 — Security Issues All Get with Non-Existent Sub-Org
**Discovery:** `Selection` | **Expected:** `security_issues_all_get` | **Timeout:** `15s`

```
Call security_issues_all_get with a nil sub-org ID: 00000000-0000-0000-0000-000000000099.
Record the exact error message and HTTP status code. Expected: 404 or 400.
```

---

### SEC-N08 — Security Configuration Set with Non-Existent Resource
**Discovery:** `Selection` | **Expected:** `security_configuration_set` | **Timeout:** `15s`

```
Call security_configuration_set with a nil resource ID: 00000000-0000-0000-0000-000000000099.
Record the exact error message. Expected: 404 or 400.
```

---

## EDGE CASES

---

### SEC-E01 — Toggle Implicit Scans On and Off
**Discovery:** `Chain` | **Expected:** `services_list → security_implicit_scans_set (enable) → security_configuration_get → security_implicit_scans_set (disable)` | **Timeout:** `60s`

```
1. Call services_list to get a component ID.
2. Call security_implicit_scans_set with enabled=true for that component.
3. Call security_configuration_get for the component — verify implicit scans shows enabled.
4. Call security_implicit_scans_set with enabled=false.
5. Verify via security_configuration_get that implicit scans is now disabled.
Report before and after state.
```

---

### SEC-E02 — Configuration Hierarchy at Org Level (No Component)
**Discovery:** `Chain` | **Expected:** `organizations_list → security_configuration_hierarchy_get` | **Timeout:** `25s`

```
Call organizations_list to get the org ID (not a component ID).
Call security_configuration_hierarchy_get for the org itself.
Report: how many hierarchy levels are returned, and which level has effective authority over each setting.
This verifies hierarchy works for org-level resources, not just components.
```

---

### SEC-E03 — Plugin Config Set and Verify
**Discovery:** `Stress` | **Expected:** `services_list → security_plugin_config_get → security_plugin_config_set → security_plugin_config_get (verify)` | **Timeout:** `60s`

```
1. Call services_list to get a component ID.
2. Call security_plugin_config_get for the component — record the current config for one plugin.
3. Modify one config value for that plugin using security_plugin_config_set.
4. Call security_plugin_config_get again — verify the change is reflected.
5. Restore the original config value.
Report before/after config values.
```

---

### SEC-E04 — Component-Level SLA Override and Inheritance Restore
**Discovery:** `Stress` | **Expected:** `services_list → security_sla_configuration_set → security_sla_configuration_get → security_sla_configuration_remove → security_sla_configuration_get (verify inherited)` | **Timeout:** `90s`

```
1. Call services_list to get a component ID.
2. Set a component-level SLA override using security_sla_configuration_set.
3. Verify the override via security_sla_configuration_get.
4. Remove the override using security_sla_configuration_remove.
5. Call security_sla_configuration_get — verify the component now inherits from its parent.
Report whether the inherited values differ from the override values.
```

---

### SEC-E05 — Security Issues All Get for Sub-Org with No Components
**Discovery:** `Chain` | **Expected:** `organizations_list_suborganizations → security_issues_all_get` | **Timeout:** `25s`

```
Call organizations_list_suborganizations to get all sub-orgs.
Find a sub-org that has no or few components.
Call security_issues_all_get for that sub-org.
Verify: empty result does not produce an error. Record "0 issues" as acceptable.
```

---

### SEC-E06 — Cross-Verify Open Issues vs Findings Summary Counts
**Discovery:** `Stress` | **Expected:** `services_list → branches_list → security_issues_open_get → security_findings_summary_get` | **Timeout:** `60s`

```
1. Call services_list to get a component.
2. Call branches_list to get the default branch.
3. Call security_issues_open_get for that component+branch. Note total open issues.
4. Call security_findings_summary_get for the same component+branch. Note summary totals.
5. Cross-verify: the total open count from step 3 should roughly align with the summary from step 4.
Report any significant discrepancy between the two calls.
```

---

### SEC-E07 — Remove Tenant-Level SLA Configuration
**Discovery:** `Chain` | **Expected:** `organizations_list → security_tenant_sla_configuration_remove` | **Timeout:** `30s`

```
Call organizations_list to get the root tenant org ID.
Call security_sla_configuration_get to check if a tenant-level SLA override currently exists.
If an override exists: call security_tenant_sla_configuration_remove. Verify that the tenant and its children now inherit the default SLA settings.
If no override exists: record "No tenant SLA override present — test skipped (precondition not met)".
```

---

### SEC-E08 — Set Security Configuration and Restore
**Discovery:** `Stress` | **Expected:** `organizations_list → security_configuration_get → security_configuration_set → security_configuration_get (verify) → security_configuration_set (restore)` | **Timeout:** `90s`

```
1. Call organizations_list to get the org ID.
2. Call security_configuration_get — record the current config.
3. Modify a non-critical field (e.g., enable/disable a setting) using security_configuration_set.
4. Call security_configuration_get — verify the change is reflected.
5. Restore the original configuration using security_configuration_set with the original values.
6. Verify restoration via security_configuration_get.
Report before/after values for any field changed.
```
