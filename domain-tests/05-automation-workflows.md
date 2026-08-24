# Domain: Automation & Workflows
**Tools covered (13):** `automation_jobs_list`, `automation_trigger`, `automation_trigger_by_branch`, `automation_rerun`, `automation_stop`, `automation_approve_manual_gate`, `automation_reject_manual_gate`, `workflow_list`, `workflow_get_content`, `workflow_schema_get`, `workflow_validate`, `workflow_update_content`, `workflow_trigger`
**Total prompts:** 23 (8 positive, 8 negative, 7 edge cases)

> **Pre-condition note:** Most write operations in this domain require a live CI/CD pipeline or workflow. Tests marked `[REQUIRES LIVE PIPELINE]` will be skipped in environments with no active jobs. The test still documents the expected behavior and records the skip reason.

---

## Test Execution Tracker

| ID | Type | Description | Category | Expected Tools | Timeout | Requires Live Pipeline | Status | Notes |
|----|------|-------------|----------|----------------|---------|----------------------|--------|-------|
| AW-P01 | Positive | List all workflows | Selection | `workflow_list` | 15s | No | ⬜ | |
| AW-P02 | Positive | Get workflow content and schema | Chain | `workflow_list → workflow_get_content → workflow_schema_get` | 30s | No | ⬜ | |
| AW-P03 | Positive | Validate workflow content against schema | Chain | `workflow_list → workflow_get_content → workflow_schema_get → workflow_validate` | 60s | No | ⬜ | |
| AW-P04 | Positive | Update workflow content and restore original | Stress | `workflow_list → workflow_get_content → workflow_update_content → workflow_get_content → workflow_update_content → workflow_get_content` | 90s | No | ⬜ | |
| AW-P05 | Positive | Trigger workflow | Chain | `workflow_list → workflow_trigger` | 30s | Yes | ⬜ | |
| AW-P06 | Positive | Trigger CI by branch, list runs, get logs | Stress | `repositories_search → branches_list → automation_trigger_by_branch → runs_list → logs_list` | 90s | Yes | ⬜ | |
| AW-P07 | Positive | Rerun a completed pipeline run | Chain | `runs_list → automation_rerun` | 30s | Yes | ⬜ | |
| AW-P08 | Positive | Manual gate: trigger → approve gate | Stress | `automation_trigger_by_branch → runs_list → automation_jobs_list → automation_approve_manual_gate` | 90s | Yes | ⬜ | |
| AW-N01 | Negative | Get workflow content for non-existent workflow | Selection | `workflow_get_content` | 15s | No | ⬜ | |
| AW-N02 | Negative | Validate malformed workflow YAML | Chain | `workflow_list → workflow_validate` | 30s | No | ⬜ | |
| AW-N03 | Negative | Update workflow content with invalid YAML | Chain | `workflow_list → workflow_update_content` | 30s | No | ⬜ | |
| AW-N04 | Negative | Trigger workflow with non-existent workflowId | Selection | `workflow_trigger` | 15s | No | ⬜ | |
| AW-N05 | Negative | Stop a run that is already completed | Chain | `runs_list → automation_stop` | 30s | Yes | ⬜ | |
| AW-N06 | Negative | Approve a gate on a run that has no pending gate | Selection | `automation_approve_manual_gate` | 15s | Yes | ⬜ | |
| AW-N07 | Negative | Trigger by branch on non-existent branch | Chain | `repositories_search → automation_trigger_by_branch` | 30s | Yes | ⬜ | |
| AW-N08 | Negative | List jobs for non-existent run | Selection | `automation_jobs_list` | 15s | No | ⬜ | |
| AW-E01 | Edge | Validate content that is already deployed (should be valid) | Chain | `workflow_list → workflow_get_content → workflow_validate` | 30s | No | ⬜ | |
| AW-E02 | Edge | Update workflow with no-op change and verify round-trip | Chain | `workflow_list → workflow_get_content → workflow_update_content → workflow_get_content` | 45s | No | ⬜ | |
| AW-E03 | Edge | Trigger same workflow twice simultaneously | Chain | `workflow_list → workflow_trigger (×2)` | 45s | Yes | ⬜ | |
| AW-E04 | Edge | Rerun a failed pipeline (not just completed) | Chain | `runs_list → automation_rerun` | 30s | Yes | ⬜ | |
| AW-E05 | Edge | Reject gate then verify run status reflects rejection | Stress | `automation_trigger_by_branch → runs_list → automation_jobs_list → automation_reject_manual_gate → runs_list` | 90s | Yes | ⬜ | |
| AW-E06 | Edge | Workflow schema — verify it covers all workflow fields | Selection | `workflow_schema_get` | 15s | No | ⬜ | |
| AW-E07 | Edge | Automation jobs list — requires all 4 params simultaneously | Chain | `automation_jobs_list (×4 attempts)` | 45s | Yes | ⬜ | |

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

### AW-P01 — List All Workflows
**Requires live pipeline:** No

**Discovery:** `Selection` | **Expected:** `workflow_list` | **Timeout:** `15s`

```
List all workflows in the organization. Verify:
- Returns an items/list array (may be empty if no workflows are defined)
- If workflows exist, each has: id (workflowId), name or displayName
- Call succeeds without error regardless of result count
Report: total workflow count. If empty, document this as expected for a QA environment with no workflows defined. If workflows exist, list their names and IDs.
```

---

### AW-P02 — Get Workflow Content and Schema
**Requires live pipeline:** No

**Discovery:** `Chain` | **Expected:** `workflow_list → workflow_get_content → workflow_schema_get` | **Timeout:** `30s`

```
List all workflows. If at least one workflow exists, get its content using the first workflowId. Record: the content type (YAML string, JSON string, or object). Then get the workflow schema definition. Verify both calls succeed. Report: the first 200 characters of workflow content, and the top-level keys of the schema. If no workflows exist, get the workflow schema alone and verify it returns a valid schema object.
```

---

### AW-P03 — Validate Workflow Content Against Schema
**Requires live pipeline:** No

**Discovery:** `Chain` | **Expected:** `workflow_list → workflow_get_content → workflow_schema_get → workflow_validate` | **Timeout:** `60s`

```
List all workflows and pick the first workflow. Get its current content. Get the workflow schema. Then validate the workflow content using the workflowId. Verify:
- Validation returns a result with a valid=true field (or equivalent success indicator)
- No validation errors are reported for currently deployed content
Report the exact validation response. If no workflows exist, document the skip.
```

---

### AW-P04 — Update Workflow Content and Restore Original
**Requires live pipeline:** No

**Discovery:** `Stress` | **Expected:** `workflow_list → workflow_get_content → workflow_update_content → workflow_get_content → workflow_update_content → workflow_get_content` | **Timeout:** `90s`

```
List all workflows and pick the first workflow. Record its workflowId and get its current content to capture the original. Make a trivial non-breaking change: prepend "# mcp-test-update-DATE\n" to the content. Update the workflow with the modified content. Get the content again and verify the comment appears at the top. Then restore the original content by updating with the original content. Get the content once more to confirm restoration. Report: whether update succeeded, whether verification shows the change, whether restoration succeeded.
```

---

### AW-P05 — Trigger Workflow
**Requires live pipeline:** Yes

**Discovery:** `Chain` | **Expected:** `workflow_list → workflow_trigger` | **Timeout:** `30s`

```
List all workflows and pick a workflow suitable for triggering. Trigger it and record the runId from the response. Verify the trigger call succeeds and returns a runId. Report: the runId returned and the trigger response. If no workflows exist, document the skip.
```

---

### AW-P06 — Trigger CI by Branch, List Runs, Get Logs
**Requires live pipeline:** Yes

**Discovery:** `Stress` | **Expected:** `repositories_search → branches_list → automation_trigger_by_branch → runs_list → logs_list` | **Timeout:** `90s`

```
Search for a repository named "go" under the aspm-sv-qa endpoint. List its branches and pick "master". Trigger a CI run on the master branch. Capture the runId from the response. List recent runs for the component to confirm the triggered run appears. Retrieve logs for that run. Report: trigger response, runId, whether run appears in list, and first 20 log lines. If no suitable pipeline exists, document the skip with the reason.
```

---

### AW-P07 — Rerun a Completed Pipeline Run
**Requires live pipeline:** Yes

**Discovery:** `Chain` | **Expected:** `runs_list → automation_rerun` | **Timeout:** `30s`

```
List runs for a component that has previous runs (try sv-app, componentId: 2060d4c2-..., subOrganizationId: 6c5eeb79-...). If runs exist, pick the most recent completed run and record its automationId and runId. Rerun that pipeline run. Record the new runId returned. Verify: rerun response returns a new runId different from the original. Report: original runId, rerun response, new runId. If no existing runs found, document the skip.
```

---

### AW-P08 — Manual Gate: Trigger Pipeline → Find Gate → Approve
**Requires live pipeline:** Yes

**Discovery:** `Stress` | **Expected:** `automation_trigger_by_branch → runs_list → automation_jobs_list → automation_approve_manual_gate` | **Timeout:** `90s`

```
Find a pipeline that has a manual gate configured. Trigger it. Wait for it to reach the gate (status="waiting" or similar). List runs to find the paused run. List automation jobs for the run to find the gateId. Approve the manual gate with the runId and gateId. Verify: approval response is success. Report the full chain including the run status before and after approval. If no manual gate pipeline exists, document the skip with the reason.
```

---

## NEGATIVE TEST CASES

---

### AW-N01 — Get Workflow Content for Non-Existent Workflow

**Discovery:** `Selection` | **Expected:** `workflow_get_content` | **Timeout:** `15s`

```
Get workflow content with a non-existent workflowId: "00000000-0000-0000-0000-000000000099". Record the exact error response. Expected: 404 not found. Document the HTTP status code and error message.
```

---

### AW-N02 — Validate Malformed Workflow YAML

**Discovery:** `Chain` | **Expected:** `workflow_list → workflow_validate` | **Timeout:** `30s`

```
List all workflows to get a valid workflowId. Then validate the workflow with deliberately invalid YAML content:
content = "this is: not: valid: yaml: content: [broken"
Record the response. Expected: validation error with valid=false and errors listing the YAML parse failure. Does the server return a structured validation error or a raw 400? Document the full validation error response.
```

---

### AW-N03 — Update Workflow With Invalid YAML Content

**Discovery:** `Chain` | **Expected:** `workflow_list → workflow_update_content` | **Timeout:** `30s`

```
List all workflows to get a valid workflowId. Attempt to update it with:
content = "completely invalid {{{{ yaml content }}}} ~~~"
Record the exact error response. Expected: 400 with YAML validation error. Does the server validate content before saving? Document whether the update is rejected or (dangerously) saved despite being invalid.
```

---

### AW-N04 — Trigger Workflow With Non-Existent Workflow ID

**Discovery:** `Selection` | **Expected:** `workflow_trigger` | **Timeout:** `15s`

```
Trigger a workflow with workflowId "00000000-0000-0000-0000-000000000099". Record the exact error. Expected: 404 not found. Document the HTTP status and error message.
```

---

### AW-N05 — Stop a Run That Is Already Completed
**Requires live pipeline:** Yes

**Discovery:** `Chain` | **Expected:** `runs_list → automation_stop` | **Timeout:** `30s`

```
Find a completed run (status=success or status=failed) from the runs listing. Attempt to stop it. Record the response. Expected: 400 or 409 ("run is not active"). Does the server validate run state before allowing stop? Document the exact error. If no completed runs exist, document the skip.
```

---

### AW-N06 — Approve a Gate on a Run With No Pending Gate
**Requires live pipeline:** Yes

**Discovery:** `Selection` | **Expected:** `automation_approve_manual_gate` | **Timeout:** `15s`

```
Find a completed or running run that has NO pending manual gate. Attempt to approve a manual gate with that runId and a made-up gateId: "00000000-0000-0000-0000-000000000099". Record the exact error. Expected: 404 (gate not found) or 400. Document the response. If no suitable run exists, call with a completely fake runId and gateId and document the error.
```

---

### AW-N07 — Trigger CI by Non-Existent Branch
**Requires live pipeline:** Yes

**Discovery:** `Chain` | **Expected:** `repositories_search → automation_trigger_by_branch` | **Timeout:** `30s`

```
Use a valid repository (sv-app, find its repositoryId from a repository search). Trigger a CI run on a non-existent branch name: "branch-does-not-exist-xyz". Record the exact error. Expected: 400 or 404 (branch not found). Document the full error response. Does the server validate the branch exists before attempting to trigger?
```

---

### AW-N08 — List Jobs for Non-Existent Run

**Discovery:** `Selection` | **Expected:** `automation_jobs_list` | **Timeout:** `15s`

```
List automation jobs with:
- subOrganizationId: "6c5eeb79-4606-4c39-bd5c-c2323336caad"
- componentId: "95fdf71c-de53-43e4-b5dc-bec7170becd6"
- runId: "00000000-0000-0000-0000-000000000099"
- automationId: "00000000-0000-0000-0000-000000000099"
Record the exact error. Expected: 404 not found. Document the HTTP status and error message. Note: this tool requires all 4 params simultaneously, making it hard to call with valid data without a live run.
```

---

## EDGE CASES

---

### AW-E01 — Validate Content That Is Already Deployed (Should Be Valid)

**Discovery:** `Chain` | **Expected:** `workflow_list → workflow_get_content → workflow_validate` | **Timeout:** `30s`

```
List all workflows and pick the first workflow. Get its current deployed content. Validate the workflow with the exact same content (no changes). Verify: validation returns valid=true (deployed content must always be valid). If validation fails for deployed content, this is a bug — document the validation errors returned. This is an idempotency check: validating already-deployed content must always succeed.
```

---

### AW-E02 — Update Workflow With No-Op Change and Verify Round-Trip

**Discovery:** `Chain` | **Expected:** `workflow_list → workflow_get_content → workflow_update_content → workflow_get_content` | **Timeout:** `45s`

```
List all workflows and pick the first workflow. Get its content. Update the workflow with the exact same content (no change). Get the content again. Verify: the content after the update is identical to the content before. This tests whether updating with the same content is a no-op or introduces any changes (e.g., adding timestamps, reformatting YAML). Report: whether content changed after a no-op update.
```

---

### AW-E03 — Trigger Same Workflow Twice Simultaneously
**Requires live pipeline:** Yes

**Discovery:** `Chain` | **Expected:** `workflow_list → workflow_trigger (×2)` | **Timeout:** `45s`

```
List all workflows and pick a workflow. Trigger it twice in quick succession (second call immediately after first). Record both runIds. Verify: two different runIds are returned. Does the server allow concurrent runs of the same workflow? Or does it queue/reject the second trigger? Report: both responses, whether the runIds differ, and the status of each run.
```

---

### AW-E04 — Rerun a Failed Pipeline
**Requires live pipeline:** Yes

**Discovery:** `Chain` | **Expected:** `runs_list → automation_rerun` | **Timeout:** `30s`

```
Find a run with status=FAILED in the runs listing. Rerun that specific failed run. Verify: rerun is accepted and returns a new runId. Does rerun behave differently for failed runs vs completed runs? Report: original failed run details, rerun response, new runId. If no failed runs exist, document the skip.
```

---

### AW-E05 — Reject Gate and Verify Run Status Changes
**Requires live pipeline:** Yes

**Discovery:** `Stress` | **Expected:** `automation_trigger_by_branch → runs_list → automation_jobs_list → automation_reject_manual_gate → runs_list` | **Timeout:** `90s`

```
Trigger a pipeline with a manual gate. Find the run paused at the gate. Reject the manual gate with the runId and gateId. List runs again and check the run status — it should now be FAILED or REJECTED. Verify: the status changed after rejection. Report: run status before rejection, rejection response, run status after rejection. If no manual gate pipeline exists, document the skip.
```

---

### AW-E06 — Workflow Schema Covers All Known Workflow Fields

**Discovery:** `Selection` | **Expected:** `workflow_schema_get` | **Timeout:** `15s`

```
Get the workflow schema. Inspect the returned schema. Verify it includes definitions for at least: steps, environment, triggers, on (event triggers), jobs. Report: the top-level keys of the schema, schema version/identifier if present, and whether the schema is a valid JSON Schema object (has "type" or "$schema" fields). This validates the schema is complete and useful for client-side validation.
```

---

### AW-E07 — Automation Jobs List Requires All 4 Parameters — Test Parameter Sensitivity

**Discovery:** `Chain` | **Expected:** `automation_jobs_list (×4 attempts)` | **Timeout:** `45s`

```
The automation jobs listing requires all 4 params: subOrganizationId, componentId, runId, automationId. Test what happens with each missing param:
1. Omit runId — record error
2. Omit automationId — record error
3. Omit componentId — record error
4. Provide all 4 but with a fake runId (00000000-...) — record error

Document: which missing parameter produces which error message. This maps the server-side validation behavior and helps understand which params are validated first. Note: this is a parameter sensitivity test, not a functional test.
```
