# Domain: Security
**Tools covered:** `security_findings_summary_get`, `security_issues_open_get`, `security_issues_all_get`, `security_filter_tools_list`, `security_filters_list`
**Total prompts:** 24 (8 positive, 8 negative, 8 edge cases)

---

## Test Execution Tracker

| ID | Type | Category | Expected Tools | Timeout | Prompt | Status | Notes |
|----|------|----------|----------------|---------|--------|--------|-------|
| SEC-P01 | Positive | Selection | `security_findings_summary_get` | 15s | Get findings summary for a known component | ⬜ | |
| SEC-P07 | Positive | Chain | `flags_applications_list → security_filter_tools_list` | 30s | List security filter tools for an application | ⬜ | |
| SEC-P08 | Positive | Chain | `flags_applications_list → security_filters_list` | 30s | List application security filters (environments, severities, SLA) | ⬜ | |
| SEC-P02 | Positive | Selection | `security_issues_open_get` | 15s | Get open issues for a component with known vulnerabilities | ⬜ | |
| SEC-P03 | Positive | Selection | `security_issues_all_get` | 15s | Get all issues for a sub-org with multiple components | ⬜ | |
| SEC-P04 | Positive | Stress | `components_list → branches_list → security_findings_summary_get (×N)` | 120s | Rank all components by total vulnerability count | ⬜ | |
| SEC-P05 | Positive | Chain | `security_findings_summary_get → security_issues_open_get` | 30s | Verify summary counts match open issues list | ⬜ | |
| SEC-P06 | Positive | Selection | `security_findings_summary_get` | 15s | Get findings for a component scanned by multiple tools | ⬜ | |
| SEC-N01 | Negative | Selection | `security_findings_summary_get` | 15s | Call findings summary with invalid componentId | ⬜ | |
| SEC-N07 | Negative | Selection | `security_filter_tools_list` | 15s | List security filter tools with invalid applicationId | ⬜ | |
| SEC-N08 | Negative | Selection | `security_filters_list` | 15s | List security filters with invalid applicationId | ⬜ | |
| SEC-N02 | Negative | Selection | `security_findings_summary_get` | 15s | Call findings summary with invalid branchId | ⬜ | |
| SEC-N03 | Negative | Selection | `security_issues_all_get` | 15s | Get all issues for sub-org with empty-branch component | ⬜ | |
| SEC-N04 | Negative | Selection | `security_issues_open_get` | 15s | Call open issues with mismatched subOrgId and componentId | ⬜ | |
| SEC-N05 | Negative | Selection | `security_findings_summary_get` | 15s | Call findings summary with empty string IDs | ⬜ | |
| SEC-N06 | Negative | Selection | `security_issues_all_get` | 15s | Get all issues for a non-existent sub-org | ⬜ | |
| SEC-E01 | Edge | Selection | `security_findings_summary_get` | 15s | Component with zero findings (clean component) | ⬜ | |
| SEC-E07 | Edge | Chain | `security_filter_tools_list (×2)` | 30s | Security filter tools with includeInDev=true vs false — compare results | ⬜ | |
| SEC-E08 | Edge | Chain | `flags_applications_list → security_filters_list` | 30s | Security filters — verify returned filter structure has environment, severity, and SLA entries | ⬜ | |
| SEC-E02 | Edge | Chain | `security_findings_summary_get → security_issues_open_get` | 30s | Component with only LOW severity findings | ⬜ | |
| SEC-E03 | Edge | Chain | `security_findings_summary_get → security_issues_open_get` | 30s | Component with 100% VERY_HIGH findings (AutoNjsscan) | ⬜ | |
| SEC-E04 | Edge | Selection | `security_findings_summary_get` | 15s | Component scanned by 6+ different scanner tools | ⬜ | |
| SEC-E05 | Edge | Selection | `security_issues_open_get` | 15s | Open issues where all SLA statuses are BREACHED | ⬜ | |
| SEC-E06 | Edge | Chain | `branches_list → security_findings_summary_get (×2)` | 30s | Multi-branch component — compare findings between branches | ⬜ | |

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

### SEC-P01 — Get Security Findings Summary for a Known Component
**Expected:** Returns counts object with VERY_HIGH, HIGH, MEDIUM, LOW, total fields, plus lastScanned timestamp and tools array.

**Discovery:** `Selection` | **Expected:** `security_findings_summary_get` | **Timeout:** `15s`

```
Get the security findings summary for the component "go" in sub-organization aspm-automation-organization.
Use:
- subOrganizationId: 6c5eeb79-4606-4c39-bd5c-c2323336caad
- endpointId: bd1d9e9b-6362-47ed-bf0f-d58d32f117be
- componentId: 95fdf71c-de53-43e4-b5dc-bec7170becd6
- branchId: 9aca9bce-1ca3-42b1-a265-eee63912cffd

Verify the response contains: counts.total > 0, lastScanned is a valid timestamp, and tools array has at least 1 entry. Report all fields returned.
```

---

### SEC-P02 — Get Open Security Issues for a Component With Known Vulnerabilities
**Expected:** Returns paginated list of issues, each with name, severity, triage status, SLA info, and tool data.

**Discovery:** `Selection` | **Expected:** `security_issues_open_get` | **Timeout:** `15s`

```
Get all open security issues for the component "go" (CBC-Js/go.git).
Use:
- subOrganizationId: 6c5eeb79-4606-4c39-bd5c-c2323336caad
- endpointId: bd1d9e9b-6362-47ed-bf0f-d58d32f117be
- componentId: 95fdf71c-de53-43e4-b5dc-bec7170becd6
- branchId: 9aca9bce-1ca3-42b1-a265-eee63912cffd

Verify: issues array is non-empty, each issue has severity, name, firstIdentified, sla.status, and remediation.triageStatus fields. Count how many issues are HIGH vs MEDIUM vs LOW. Report the total issue count.
```

---

### SEC-P03 — Get All Security Issues for a Sub-Org (Aggregate View)
**Expected:** Returns findings across all components in the sub-org that have a valid defaultBranch.

**Discovery:** `Selection` | **Expected:** `security_issues_all_get` | **Timeout:** `15s`

```
Get all security issues (open and resolved) for sub-organization aspm-automation-organization.
Use:
- subOrganizationId: 6c5eeb79-4606-4c39-bd5c-c2323336caad

Verify: response is not an error, returns aggregated findings data. Report the total number of findings returned and which components are included in the response.
```

---

### SEC-P04 — Rank All Components by Total Vulnerability Count
**Expected:** Returns a ranked leaderboard of all components.

**Discovery:** `Stress` | **Expected:** `components_list → branches_list → security_findings_summary_get (×N)` | **Timeout:** `120s`

```
List all components in the organization. For each component that has a non-empty defaultBranch, get its branch ID using the branches listing, then get its security findings summary. Rank all components in descending order by total findings count. Present a table with: rank, component name, sub-org, VERY_HIGH, HIGH, MEDIUM, LOW, total, and lastScanned date. Identify the #1 component for total findings and the #1 for VERY_HIGH findings.
```

---

### SEC-P05 — Verify Summary Counts Are Consistent With Open Issues List
**Expected:** Summary total should equal or be close to the count of issues returned.

**Discovery:** `Chain` | **Expected:** `security_findings_summary_get → security_issues_open_get` | **Timeout:** `30s`

```
For component "go" (componentId: 95fdf71c-..., branchId: 9aca9bce-...), get the security findings summary and record counts.total. Then get all open security issues for the same component and count the items returned in the issues array (sum all subRows counts). Compare the two numbers. Are they consistent? Report any discrepancy between the summary total and the detailed issue count. This validates data consistency between the two endpoints.
```

---

### SEC-P06 — Get Findings for a Component Scanned by Multiple Tools
**Expected:** Tools array contains multiple scanner entries, each with its own counts.

**Discovery:** `Selection` | **Expected:** `security_findings_summary_get` | **Timeout:** `15s`

```
Get security findings summary for the component "nodejs-aspm" (componentId: 3024daeb-a402-44a4-b25a-960ec41bbd53, branchId: 29e430eb-df96-4022-a8ba-062592c19575, subOrganizationId: 6c5eeb79-4606-4c39-bd5c-c2323336caad, endpointId: 1d479e09-f49a-4e76-a501-2bafdf65f753).
Verify: the tools array has more than 1 scanner. For each scanner, report its name, and counts. Calculate what percentage of total findings each scanner contributes. Report which scanner found the most VERY_HIGH issues.
```

---

### SEC-P07 — List Security Filter Tools for an Application
**Expected:** Returns an array of security tool objects with name/id fields.

**Discovery:** `Chain` | **Expected:** `flags_applications_list → security_filter_tools_list` | **Timeout:** `30s`

```
List all feature flag applications to get the applicationId for the first available application (organisationId: 6c5eeb79-4606-4c39-bd5c-c2323336caad). Then list all security filter tools for that application with:
- organisationId: 6c5eeb79-4606-4c39-bd5c-c2323336caad
- applicationId: <id from above>

Verify: response is not an error, returns an array of security tool objects. For each tool, report its id and name. Note the total count. Try with includeInDev=true and record whether additional tools appear.
```

---

### SEC-P08 — List Application Security Filters
**Expected:** Returns filter objects grouping by environment, severity, and SLA configuration.

**Discovery:** `Chain` | **Expected:** `flags_applications_list → security_filters_list` | **Timeout:** `30s`

```
List all feature flag applications to get the applicationId for the first available application (organisationId: 6c5eeb79-4606-4c39-bd5c-c2323336caad). Then list all security filters for that application with:
- organisationId: 6c5eeb79-4606-4c39-bd5c-c2323336caad
- applicationId: <id from above>

Verify: response contains environment entries, severity entries, and SLA entries each with their id and name. Report the full list of filters returned. Confirm the structure matches the expected schema (environment, severity, SLA grouping).
```

---

## NEGATIVE TEST CASES

---

### SEC-N01 — Invalid componentId Should Return an Error
**Expected:** Error response (404 or 400), not a valid summary object.

**Discovery:** `Selection` | **Expected:** `security_findings_summary_get` | **Timeout:** `15s`

```
Get the security findings summary with a made-up componentId that does not exist:
- subOrganizationId: 6c5eeb79-4606-4c39-bd5c-c2323336caad
- endpointId: bd1d9e9b-6362-47ed-bf0f-d58d32f117be
- componentId: 00000000-0000-0000-0000-000000000099
- branchId: 9aca9bce-1ca3-42b1-a265-eee63912cffd

Record the exact error response. Verify: the server returns an error (not a success with zero counts). Document the HTTP status code and error message returned.
```

---

### SEC-N02 — Invalid branchId Should Return an Error
**Expected:** Error response, not empty findings.

**Discovery:** `Selection` | **Expected:** `security_findings_summary_get` | **Timeout:** `15s`

```
Get the security findings summary using a valid componentId but a non-existent branchId:
- subOrganizationId: 6c5eeb79-4606-4c39-bd5c-c2323336caad
- endpointId: bd1d9e9b-6362-47ed-bf0f-d58d32f117be
- componentId: 95fdf71c-de53-43e4-b5dc-bec7170becd6
- branchId: 00000000-0000-0000-0000-000000000099

Record the exact error. Is it a 404 (branch not found), 400 (bad request), or does it silently return zero findings? Document the full error response.
```

---

### SEC-N03 — Sub-Org With a Component With Empty defaultBranch Causes All-Issues to Fail
**Expected:** Known bug — returns error "default branch '' not found for component ProdVuln".

**Discovery:** `Selection` | **Expected:** `security_issues_all_get` | **Timeout:** `15s`

```
Get all security issues for the sub-org aspm-automation-sub-org which contains the component "ProdVuln" (id: 4861bc9f-...) that has an empty defaultBranch:
- subOrganizationId: 5b363812-7ec6-46a9-990c-56fc50a23cb9

Record the exact error response. Confirm the error message is: "default branch '' not found for component ProdVuln with id=4861bc9f-5288-45a4-ab18-9294da21c69b". Document whether the error aborts the entire request or returns partial results.
```

---

### SEC-N04 — Mismatched subOrganizationId and componentId
**Expected:** Error or empty result — the component does not belong to the given sub-org.

**Discovery:** `Selection` | **Expected:** `security_issues_open_get` | **Timeout:** `15s`

```
Get open security issues using a componentId from one sub-org but a subOrganizationId from a different sub-org:
- subOrganizationId: d3f4e30d-9db5-4182-9be7-0bd9847b91fd  (aspm-trivy-test)
- endpointId: bd1d9e9b-6362-47ed-bf0f-d58d32f117be
- componentId: 95fdf71c-de53-43e4-b5dc-bec7170becd6  (belongs to aspm-automation-organization, not aspm-trivy-test)
- branchId: 9aca9bce-1ca3-42b1-a265-eee63912cffd

Record the response. Does the server validate that the component belongs to the provided sub-org? Does it return an error, empty results, or does it return findings anyway (ignoring the sub-org)?
```

---

### SEC-N05 — Missing Required Parameters
**Expected:** Validation error before reaching the server.

**Discovery:** `Selection` | **Expected:** `security_findings_summary_get` | **Timeout:** `15s`

```
Attempt to get the security findings summary without providing all required parameters. Try calling it with only:
- componentId: 95fdf71c-de53-43e4-b5dc-bec7170becd6
(omitting subOrganizationId, endpointId, branchId)

Record the exact error. Is it a client-side validation error (required field missing) or does the call reach the server and fail there? Document the full error message.
```

---

### SEC-N06 — Non-Existent Sub-Org for All-Issues
**Expected:** 404 or similar error.

**Discovery:** `Selection` | **Expected:** `security_issues_all_get` | **Timeout:** `15s`

```
Get all security issues with a non-existent subOrganizationId:
- subOrganizationId: 00000000-0000-0000-0000-000000000099

Record the exact error response. Document the HTTP status code. Does the server return 404 (org not found), 403 (forbidden), or 400 (bad request)?
```

---

### SEC-N07 — Security Filter Tools With Invalid applicationId
**Expected:** Error response (404 or 400) — application does not exist.

**Discovery:** `Selection` | **Expected:** `security_filter_tools_list` | **Timeout:** `15s`

```
List security filter tools with:
- organisationId: 6c5eeb79-4606-4c39-bd5c-c2323336caad
- applicationId: 00000000-0000-0000-0000-000000000099

Record the exact error response. Document the HTTP status code and error message. Expected: 404 (application not found) or 400 (bad request).
```

---

### SEC-N08 — Security Filters With Invalid applicationId
**Expected:** Error response (404 or 400) — application does not exist.

**Discovery:** `Selection` | **Expected:** `security_filters_list` | **Timeout:** `15s`

```
List security filters with:
- organisationId: 6c5eeb79-4606-4c39-bd5c-c2323336caad
- applicationId: 00000000-0000-0000-0000-000000000099

Record the exact error response. Document the HTTP status code and error message. Does it return an empty list or an explicit error?
```

---

## EDGE CASES

---

### SEC-E01 — Component With Zero Findings (Recently Onboarded or Clean Repo)
**Expected:** Returns counts all zero, but call should succeed without error.

**Discovery:** `Selection` | **Expected:** `security_findings_summary_get` | **Timeout:** `15s`

```
Get the security findings summary for the component "blackduck-implicit" (componentId: 90e7a62f-b1cc-4ed6-8aac-0a906d1b4400, branchId: 0ed23d5a-08c1-464c-8160-8eb3ed8e7f32, subOrganizationId: 3a43d940-9693-4dd5-b2cb-d061cd2c0808, endpointId: 8f849267-b45f-4f13-81ef-9ece64290c31).
Verify: the call succeeds (no error). Report whether counts are all zero or contain some findings. Check if the lastScanned timestamp is present. This tests whether the tool handles zero-finding components gracefully vs erroring out.
```

---

### SEC-E02 — Component With Only LOW Severity Findings
**Expected:** Summary shows VERY_HIGH=0, HIGH=0, all findings are LOW.

**Discovery:** `Chain` | **Expected:** `security_findings_summary_get → security_issues_open_get` | **Timeout:** `30s`

```
Find a component where the findings summary shows only LOW severity findings (no VERY_HIGH or HIGH). From the known data, the component "go" (CBC-Js) has mostly LOW findings. Get its security findings summary to confirm the severity distribution. Then get its open security issues and filter only LOW severity issues. Verify that all returned issues have severity = "LOW". Report whether any HIGH or VERY_HIGH issues appear in the detailed list that were not reflected in the summary.
```

---

### SEC-E03 — Component With 100% VERY_HIGH Findings (AutoNjsscan)
**Expected:** Summary shows VERY_HIGH dominates (365 of 388 total). Issues list should reflect mostly VERY_HIGH entries.

**Discovery:** `Chain` | **Expected:** `security_findings_summary_get → security_issues_open_get` | **Timeout:** `30s`

```
Get the security findings summary for component "AutoNjsscan" (componentId: 85152ede-69a8-4a6d-9d32-b756be58359d, branchId: e500c10a-c9a1-4665-a2f9-eeb836af2cfd, subOrganizationId: e8fa8fa4-1368-40c6-a1bb-7244a90a6f1e, endpointId: 8f849267-b45f-4f13-81ef-9ece64290c31).
Verify VERY_HIGH count is 365 and total is 388 (94% critical). Then get all open security issues for the same component. Check: are all returned issues labeled VERY_HIGH? Does the pagination cursor indicate more pages exist given the high count? Report the first page of results and the pagination metadata.
```

---

### SEC-E04 — Component Scanned by 6+ Different Scanner Tools
**Expected:** Tools array has 6+ entries, each with non-zero counts.

**Discovery:** `Selection` | **Expected:** `security_findings_summary_get` | **Timeout:** `15s`

```
Get the security findings summary for component "SVMultiLangRepo" (componentId: 9bae6d49-6e6d-4ca4-b2cd-c750189ceda5, branchId: 9d11f19c-d5aa-4a22-a15b-0ad2026e2bc2, subOrganizationId: c79e1d6c-5d2c-4822-9299-37b7956de1df, endpointId: 925d83e0-345f-4fbe-ba00-eaa693f89646).
Count the number of scanners in the tools array. Verify at least 6 scanners are present. For each scanner, list its name and finding counts. Calculate whether the sum of all individual scanner totals equals or exceeds the overall counts.total (some findings may be deduplicated at the summary level). Report any discrepancy.
```

---

### SEC-E05 — All SLA Statuses Are BREACHED for a Component
**Expected:** Most or all issues show sla.status = "BREACHED" (particularly HIGH/MEDIUM findings older than their SLA window).

**Discovery:** `Selection` | **Expected:** `security_issues_open_get` | **Timeout:** `15s`

```
Get open security issues for component "go" (componentId: 95fdf71c-...). Filter all issues where sla.status = "BREACHED". Calculate: (1) how many total issues have breached SLA, (2) what is the average number of days overdue (using today's date 2026-06-10 minus sla.due), (3) which vulnerability has been breached the longest. Report the top 5 most overdue findings sorted by days past due date.
```

---

### SEC-E06 — Multi-Branch Component: Compare Security Findings Across Branches
**Expected:** Different branches may have different finding counts, showing security divergence.

**Discovery:** `Chain` | **Expected:** `branches_list → security_findings_summary_get (×2)` | **Timeout:** `30s`

```
Get all branches for component "resolvedFindings-feb" (componentId: efcb1d0b-8307-4bf5-a8d4-82da53a751fb, subOrganizationId: 5b363812-7ec6-46a9-990c-56fc50a23cb9, endpointId: 33591c6d-0e28-41ab-a427-41dc9ca3ce3a). It has two branches: "main" (branchId: 54d5b24b-...) and "test" (branchId: ba330236-...). Get the security findings summary for each branch separately. Compare: total findings per branch, severity distribution per branch, which scanners ran on each branch, and lastScanned dates. Report whether the "test" branch is more or less secure than "main" and by how many findings.
```

---

### SEC-E07 — Security Filter Tools: includeInDev=true vs false
**Expected:** includeInDev=true may return additional tools enabled only in dev mode.

**Discovery:** `Chain` | **Expected:** `security_filter_tools_list (×2)` | **Timeout:** `30s`

```
List security filter tools twice for the same application:
1. With includeInDev=false (or omitted)
2. With includeInDev=true

Compare the two responses. Report: are the tool lists identical? If includeInDev=true returns more tools, list the extra tools and note that they are dev-only. This tests whether the flag materially changes the response.
```

---

### SEC-E08 — Security Filters: Verify Full Filter Structure
**Expected:** Response contains environment, severity, and SLA filter groups, each with id and name.

**Discovery:** `Chain` | **Expected:** `flags_applications_list → security_filters_list` | **Timeout:** `30s`

```
List security filters for the application (applicationId from the feature flag applications list, organisationId: 6c5eeb79-4606-4c39-bd5c-c2323336caad). Verify:
- The response contains at least one environment filter entry
- The response contains at least one severity filter entry (e.g., CRITICAL, HIGH, MEDIUM, LOW)
- The response contains at least one SLA filter entry
- Each entry has both id and name fields
Report the complete list of all filter entries grouped by type. This documents the full set of available filters for this application.
```
