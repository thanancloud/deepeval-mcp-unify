# Workflows — Prompts Only

> **Tools covered:** `actions_list`, `automation_approve_manual_gate`, `automation_pending_tasks_list`, `automation_reject_manual_gate`, `automation_rerun`, `automation_stop`, `automation_trigger`, `automation_trigger_by_branch`, `runs_list`, `workflow_get_content`, `workflow_schema_get`, `workflow_trigger`, `workflow_update_content`, `workflow_validate`

> Tests marked `[REQUIRES LIVE PIPELINE]` use ⬛ Skip when no triggerable workflow is available.
> Tests marked `[REQUIRES PRIOR RUN]` use ⬛ Skip when no completed run exists.
> Tests marked `[REQUIRES PENDING GATE]` use ⬛ Skip when no pending manual gate exists.

---

## POSITIVE TEST CASES

### WF-P01 — List All Actions for Organization

```
Call organizations_list to get the org ID.
Call actions_list for that organization.
Report: total action count, each action's id, name, and type.
If no actions exist, record "0 actions — empty result OK".
```

---

### WF-P02 — List Automation Runs for a Component

```
Call services_list to find a component.
Call runs_list for that component.
Report: total run count, each run's id, status, triggeredBy, and createdAt.
```

---

### WF-P03 — Get Workflow Content for a Component

```
1. Call services_list to find a component.
2. Call workflow_list for that component to get a workflow ID.
3. Call workflow_get_content for that workflow.
Report: the workflow YAML top-level keys (e.g., apiVersion, kind, metadata, spec).
```

---

### WF-P04 — Get Workflow Schema

```
Call workflow_schema_get.
Report: the returned JSON schema's top-level keys and version field.
Confirm the response is valid JSON.
```

---

### WF-P05 — Validate Existing Workflow YAML

```
1. Call services_list to find a component.
2. Call workflow_list to get a workflow.
3. Call workflow_get_content to retrieve its YAML content.
4. Call workflow_validate with that same YAML content.
Verify: the existing workflow YAML is reported as valid.
Report any validation messages returned.
```

---

### WF-P06 — Update Workflow Content and Verify

```
1. Call services_list to find a component.
2. Call workflow_list to get a workflow.
3. Call workflow_get_content to read the current YAML.
4. Make a minimal change (e.g., add or update a comment in the YAML).
5. Call workflow_validate to confirm the modified YAML is still valid.
6. Call workflow_update_content with the updated YAML.
7. Call workflow_get_content again — verify the change is reflected.
8. Restore the original content using workflow_update_content.
Report each step's outcome.
```

---

### WF-P07 — List Pending Manual Gate Tasks

```
Call organizations_list to get the org ID.
Call automation_pending_tasks_list for that organization.
Report: each pending task's runId, jobName, requestedBy, and requested-at timestamp.
If no pending tasks exist, record "0 pending tasks — empty result OK".
```

---

### WF-P08 — Trigger Workflow by Branch and Stop It
`[REQUIRES LIVE PIPELINE]`

```
1. Call services_list to find a component with a connected workflow.
2. Call workflow_list to get a workflow file name.
3. Call automation_trigger_by_branch with the component ID, branch name, and workflow file name.
4. Record the returned run ID.
5. Call runs_list to verify the run appears with status RUNNING or QUEUED.
6. Call automation_stop with the run ID.
7. Call runs_list again — verify the run transitions to STOPPED or CANCELLED.
If no triggerable workflow exists, record "No triggerable workflow found — test skipped".
```

---

## NEGATIVE TEST CASES

### WF-N01 — Validate Invalid YAML

```
Call workflow_validate with clearly invalid YAML: "this: is: : invalid:::yaml{{{".
Record the exact validation error returned. Expected: 400 or validation failure message.
```

---

### WF-N02 — Update Workflow Content with Non-Existent Workflow ID

```
Call workflow_update_content with a nil workflow ID: 00000000-0000-0000-0000-000000000099 and any valid YAML content.
Record the exact error message. Expected: 404.
```

---

### WF-N03 — Update Workflow with Invalid YAML

```
1. Call services_list → workflow_list to get a real workflow ID.
2. Confirm the YAML is invalid first via workflow_validate.
3. Attempt workflow_update_content with that invalid YAML.
Record the exact error message. Expected: 400 validation error.
```

---

### WF-N04 — Stop Non-Existent Run

```
Call automation_stop with a nil run ID: 00000000-0000-0000-0000-000000000099.
Record the exact error message and HTTP status code. Expected: 404 or 400.
```

---

### WF-N05 — Rerun Non-Existent Run

```
Call automation_rerun with a nil run ID: 00000000-0000-0000-0000-000000000099.
Record the exact error message and HTTP status code. Expected: 404 or 400.
```

---

### WF-N06 — List Runs for Non-Existent Component

```
Call runs_list with a nil component ID: 00000000-0000-0000-0000-000000000099.
Record the exact error message and HTTP status code. Expected: 404 or 400.
```

---

### WF-N07 — List Actions for Non-Existent Org

```
Call actions_list with a nil org ID: 00000000-0000-0000-0000-000000000099.
Record the exact error message and HTTP status code. Expected: 404 or 400.
```

---

### WF-N08 — Get Workflow Content for Non-Existent Workflow

```
Call workflow_get_content with a nil workflow ID: 00000000-0000-0000-0000-000000000099.
Record the exact error message and HTTP status code. Expected: 404 or 400.
```

---

## EDGE CASES

### WF-E01 — Validate Workflow YAML Before Updating

```
1. Get a workflow's current content via workflow_get_content.
2. Call workflow_validate with the content.
3. Verify: existing workflow YAML is always valid.
4. Modify one field (add a comment line: "# test comment").
5. Call workflow_validate again — verify the modified content is still valid.
Report both validation responses.
```

---

### WF-E02 — List Jobs for a Completed Run

```
1. Call services_list to get a component.
2. Call search_runs to find a completed run (status=COMPLETED or SUCCEEDED).
3. Call automation_jobs_list for that run.
Report: each job's name, status, and duration. Note the total number of jobs in the run.
```

---

### WF-E03 — Rerun a Completed Run
`[REQUIRES PRIOR RUN]`

```
1. Call services_list to get a component.
2. Call runs_list to find a completed or failed run.
3. Call automation_rerun with that run's ID.
4. Record the new run ID returned.
5. Call runs_list — verify the new run appears.
If no completed run exists, record "No completed run found — test skipped".
```

---

### WF-E04 — Approve a Pending Manual Gate
`[REQUIRES PENDING GATE]`

```
1. Call organizations_list to get the org ID.
2. Call automation_pending_tasks_list to find a pending gate.
3. If a pending gate exists, call automation_approve_manual_gate with the task details.
4. Call automation_pending_tasks_list again — verify the gate no longer appears.
If no pending gate, record "No pending manual gates — test skipped (precondition not met)".
```

---

### WF-E05 — Reject a Pending Manual Gate
`[REQUIRES PENDING GATE]`

```
1. Call automation_pending_tasks_list to find a pending gate (different from WF-E04 to avoid conflict).
2. If a pending gate exists, call automation_reject_manual_gate.
3. Call automation_pending_tasks_list again — verify the gate no longer appears.
If no pending gate, record "No pending manual gates — test skipped (precondition not met)".
```

---

### WF-E06 — Trigger, Verify Running, Then Rerun
`[REQUIRES LIVE PIPELINE]`

```
1. Call services_list to find a triggerable component.
2. Trigger a run via automation_trigger_by_branch.
3. Wait for the run to complete (call search_runs in a loop or after a delay).
4. Call automation_rerun on the completed run.
5. Verify the new run appears in search_runs.
If no triggerable workflow exists, record "No triggerable workflow — test skipped".
```

---

### WF-E07 — Update Workflow Content and Validate Before and After

```
1. Get a workflow's current content via workflow_get_content.
2. Call workflow_validate — confirm it is valid.
3. Add a YAML comment line to the content.
4. Call workflow_validate on the modified content — confirm still valid.
5. Call workflow_update_content with the modified content.
6. Call workflow_get_content — verify the comment appears.
7. Restore the original content via workflow_update_content.
8. Verify restoration via workflow_get_content.
```

---

### WF-E08 — List Runs for Component with No Prior Runs

```
Call services_list to get all components.
Find a component that is new or unlikely to have runs.
Call runs_list for that component.
Verify: empty results are returned without error.
Record "0 runs — empty result OK" if confirmed.
```

---

### WF-E09 — Trigger Automation by Job/Run Reference and Stop
`[REQUIRES LIVE PIPELINE]`

```
1. Call services_list to find a component with an automation job.
2. Call automation_jobs_list (or search_runs) to get a job or run reference.
3. Call automation_trigger using that job/run reference to start a new run.
4. Record the returned run ID.
5. Call runs_list — verify the new run appears with status RUNNING or QUEUED.
6. Call automation_stop with the new run ID.
7. Verify the run transitions to STOPPED or CANCELLED.
If no triggerable job is found, record "No automation job found — test skipped".
Note: automation_trigger is distinct from automation_trigger_by_branch — it uses an existing job/run reference, not a branch name.
```

---

### WF-E10 — Trigger Workflow Directly via workflow_trigger
`[REQUIRES LIVE PIPELINE]`

```
1. Call services_list to find a component with workflows.
2. Call workflow_list for that component to get a workflow ID.
3. Call workflow_trigger with that workflow ID to start a run.
4. Record the returned run ID.
5. Call runs_list — verify the triggered run appears.
6. Call automation_stop with the run ID.
If no workflow is available or triggering is not allowed, record "No triggerable workflow — test skipped".
Note: workflow_trigger triggers a run directly from a workflow object (by workflow ID), not by branch name.
```
