# Application Security — Prompts Only

---

## POSITIVE TEST CASES

### SEC-P01 — Get Security Configuration for Organization

```
List all organizations to get the current org.
Get the security configuration for that organization at platform level.
Report: all configuration fields returned (enabled/disabled states, severity thresholds, etc.).
```

---

### SEC-P02 — Get Security Configuration Hierarchy for a Component

```
List all services to find a component (type=COMPONENT).
Get the security configuration hierarchy for that component.
Report: each level in the hierarchy (tenant → org → sub-org → component) with its effective settings.
Note which settings are inherited vs explicitly set at each level.
```

---

### SEC-P03 — Get Security Issues Across All Components in Sub-Org

```
List all sub-organizations to get a sub-org ID.
Get all security issues for that sub-org.
Report: total issue count by severity (critical, high, medium, low). Note Known Bug #5:
if a component in the sub-org has an empty defaultBranch, the call may abort early.
```

---

### SEC-P04 — Get Open Security Issues for a Component Branch

```
List all services to find a component.
List branches for that component to get its default or main branch name.
Get all open security issues for that component and branch.
Report: total open issues, breakdown by severity, and the first 3 issue titles.
Note Known Bug #7: open security issues may ignore subOrganizationId ownership.
```

---

### SEC-P05 — Get Security Findings Summary for a Component Branch

```
List all services to find a component.
List branches to get the default branch name.
Get the security findings summary for that component and branch.
Report: all summary fields returned (total findings, by severity, by tool, etc.).
```

---

### SEC-P06 — Security Plugin Activate and Deactivate

```
1. List all organizations to get the org.
2. Get the plugin configuration for the org to see all plugins and their current activation state.
3. Find a plugin that is currently INACTIVE. Activate it.
4. Verify activation by getting the plugin configuration again.
5. Deactivate the same plugin.
6. Verify deactivation via the plugin configuration.
If all plugins are already active, pick one to deactivate and re-activate.
Report each step's outcome.
```

---

### SEC-P07 — SLA Configuration Set, Get, and Remove

```
1. List all organizations to get the org.
2. Get the current SLA configuration. Record it.
3. Set a new SLA configuration (adjust one threshold).
4. Get the SLA configuration again — verify the change was applied.
5. Remove the SLA configuration override.
6. Get the SLA configuration one more time — verify it now inherits from parent.
Report each step's outcome and the before/after SLA values.
```

---

### SEC-P08 — List Security Filters and Filter Tools for an Application

```
List all flag management applications to get an application.
Get all security filters for that application. Report each filter's id, name, environment, and severity.
Get all security filter tools for the same application. Report each filter tool's name and type.
```

---

## NEGATIVE TEST CASES

### SEC-N01 — Open Security Issues with Non-Existent Component

```
Attempt to get open security issues with a nil component ID (00000000-0000-0000-0000-000000000099) and branchName="main".
Record the exact error message and HTTP status code. Expected: 404 or 400.
```

---

### SEC-N02 — Findings Summary with Invalid Branch ID

```
List all services to get a real component ID.
Attempt to get the security findings summary for that component but with a fabricated branchId: 00000000-0000-0000-0000-000000000099.
Record the exact error. Expected: 404 or 500 (Known Bug #6 — 500 is a backend bug, mark as ⚠️ Warn if reproduced).
```

---

### SEC-N03 — Security Configuration Get with Non-Existent Org

```
Attempt to get the security configuration for a nil resource ID: 00000000-0000-0000-0000-000000000099.
Record the exact error message and HTTP status code. Expected: 404 or 400.
```

---

### SEC-N04 — SLA Configuration Get with Non-Existent Resource

```
Attempt to get the SLA configuration for a nil resource ID: 00000000-0000-0000-0000-000000000099.
Record the exact error message and HTTP status code. Expected: 404 or 400.
```

---

### SEC-N05 — Plugin Activate with Non-Existent Resource

```
Attempt to activate a security plugin with a nil resource ID: 00000000-0000-0000-0000-000000000099 and plugin name "nonexistent-plugin".
Record the exact error message and HTTP status code. Expected: 404 or 400.
```

---

### SEC-N06 — Plugin Config Set with Invalid Config

```
List all organizations to get the org.
Attempt to set the plugin configuration with a completely invalid/empty config body.
Record the exact error message. Expected: 400 validation error.
```

---

### SEC-N07 — Security Issues All Get with Non-Existent Sub-Org

```
Attempt to get all security issues for a nil sub-org ID: 00000000-0000-0000-0000-000000000099.
Record the exact error message and HTTP status code. Expected: 404 or 400.
```

---

### SEC-N08 — Security Configuration Set with Non-Existent Resource

```
Attempt to set the security configuration for a nil resource ID: 00000000-0000-0000-0000-000000000099.
Record the exact error message. Expected: 404 or 400.
```

---

## EDGE CASES

### SEC-E01 — Toggle Implicit Scans On and Off

```
1. List all services to get a component.
2. Enable implicit scans for that component.
3. Get the security configuration for the component — verify implicit scans shows enabled.
4. Disable implicit scans.
5. Verify via the security configuration that implicit scans is now disabled.
Report before and after state.
```

---

### SEC-E02 — Configuration Hierarchy at Org Level (No Component)

```
List all organizations to get the org ID (not a component ID).
Get the security configuration hierarchy for the org itself.
Report: how many hierarchy levels are returned, and which level has effective authority over each setting.
This verifies hierarchy works for org-level resources, not just components.
```

---

### SEC-E03 — Plugin Config Set and Verify

```
1. List all services to get a component.
2. Get the plugin configuration for the component — record the current config for one plugin.
3. Modify one config value for that plugin.
4. Get the plugin configuration again — verify the change is reflected.
5. Restore the original config value.
Report before/after config values.
```

---

### SEC-E04 — Component-Level SLA Override and Inheritance Restore

```
1. List all services to get a component.
2. Set a component-level SLA override.
3. Verify the override via the SLA configuration.
4. Remove the SLA override.
5. Get the SLA configuration — verify the component now inherits from its parent.
Report whether the inherited values differ from the override values.
```

---

### SEC-E05 — Security Issues All Get for Sub-Org with No Components

```
List all sub-organizations to get all sub-orgs.
Find a sub-org that has no or few components.
Get all security issues for that sub-org.
Verify: empty result does not produce an error. Record "0 issues" as acceptable.
```

---

### SEC-E06 — Cross-Verify Open Issues vs Findings Summary Counts

```
1. List all services to get a component.
2. List branches to get the default branch.
3. Get open security issues for that component+branch. Note total open issues.
4. Get the security findings summary for the same component+branch. Note summary totals.
5. Cross-verify: the total open count from step 3 should roughly align with the summary from step 4.
Report any significant discrepancy between the two calls.
```

---

### SEC-E07 — Remove Tenant-Level SLA Configuration

```
List all organizations to get the root tenant org.
Get the current SLA configuration to check if a tenant-level override exists.
If an override exists: remove the tenant-level SLA configuration. Verify that the tenant and its children now inherit the default SLA settings.
If no override exists: record "No tenant SLA override present — test skipped (precondition not met)".
```

---

### SEC-E08 — Set Security Configuration and Restore

```
1. List all organizations to get the org.
2. Get the current security configuration — record it.
3. Modify a non-critical field (e.g., enable/disable a setting).
4. Get the security configuration — verify the change is reflected.
5. Restore the original configuration.
6. Verify restoration.
Report before/after values for any field changed.
```
