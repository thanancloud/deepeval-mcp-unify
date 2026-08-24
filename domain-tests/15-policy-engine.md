# Domain: Policy Engine
**Tools covered (8):** `policies_create`, `policies_delete`, `policies_discover`, `policies_get`, `policies_get_schema`, `policies_list`, `policies_run_evaluations_list`, `policies_update`
**Total prompts:** 18 (6 positive, 6 negative, 6 edge)

> **Cross-domain tools used for setup:** `user_whoami` (default), `organizations_list` (default), `services_list` (default), `workflow_list` (workflows), `search_runs` (default), `runs_list` (workflows)

---

## Test Execution Tracker

| ID | Type | Category | Expected Tools | Timeout | Status | Notes |
|----|------|----------|----------------|---------|--------|-------|
| PE-P01 | Positive | Chain | `organizations_list` → `policies_list` | 20s | ⬜ | |
| PE-P02 | Positive | Chain | `organizations_list` → `policies_list` → `policies_get` | 25s | ⬜ | |
| PE-P03 | Positive | Selection | `policies_get_schema` | 15s | ⬜ | |
| PE-P04 | Positive | Stress | `organizations_list` → `policies_get_schema` → `policies_create` → `policies_get` → `policies_update` → `policies_get` (verify) → `policies_delete` → `policies_get` (verify 404) | 120s | ⬜ | Full lifecycle |
| PE-P05 | Positive | Chain | `services_list` → `workflow_list` → `policies_discover` | 40s | ⬜ | |
| PE-P06 | Positive | Chain | `services_list` → `search_runs` → `policies_run_evaluations_list` | 35s | ⬜ | |
| PE-N01 | Negative | Selection | `policies_get` (nil ID) | 15s | ⬜ | |
| PE-N02 | Negative | Selection | `policies_delete` (nil ID) | 15s | ⬜ | |
| PE-N03 | Negative | Selection | `policies_update` (nil ID) | 15s | ⬜ | |
| PE-N04 | Negative | Selection | `policies_create` (invalid YAML) | 15s | ⬜ | |
| PE-N05 | Negative | Selection | `policies_discover` (nil component) | 15s | ⬜ | |
| PE-N06 | Negative | Selection | `policies_run_evaluations_list` (nil run ID) | 15s | ⬜ | |
| PE-E01 | Edge | Chain | `policies_get_schema` → `policies_get_schema` (explicit version) | 25s | ⬜ | |
| PE-E02 | Edge | Chain | `organizations_list` → `policies_list` → `policies_get` → `policies_update` (restore) | 60s | ⬜ | Update existing policy |
| PE-E03 | Edge | Chain | `organizations_list` → `policies_create` → `policies_list` (verify count) → `policies_delete` | 60s | ⬜ | |
| PE-E04 | Edge | Chain | `organizations_list` → `policies_create` → `policies_delete` → `policies_get` (confirm 404) | 60s | ⬜ | Immediate delete verify |
| PE-E05 | Edge | Chain | `services_list` → `search_runs` → `policies_run_evaluations_list` (multiple runs) | 60s | ⬜ | |
| PE-E06 | Edge | Chain | `organizations_list` → `policies_create` (duplicate name) → `policies_delete` | 60s | ⬜ | |

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
> Call `organizations_list` for org ID; `policies_get_schema` before creating policies (use schema to construct valid YAML).
> Nil UUID for negative tests: `00000000-0000-0000-0000-000000000099`

Minimal valid policy YAML template (adjust to match current schema):
```yaml
apiVersion: automation.cloudbees.io/v1alpha1
kind: Policy
metadata:
  name: pe-test-policy
  description: "Test policy for PE domain tests"
spec:
  rules: []
```

---

## POSITIVE TEST CASES

---

### PE-P01 — List Policies in Organization
**Discovery:** `Chain` | **Expected:** `organizations_list → policies_list` | **Timeout:** `20s`

```
Call organizations_list to get the org ID.
Call policies_list for that organization (with cursor-based pagination if needed).
Report: total policy count, each policy's id, name, and description.
```

---

### PE-P02 — Get Policy by ID
**Discovery:** `Chain` | **Expected:** `organizations_list → policies_list → policies_get` | **Timeout:** `25s`

```
Call organizations_list to get the org ID.
Call policies_list to get the first policy's ID.
Call policies_get with that ID.
Verify: policy name and ID match between list and get.
Report: all fields returned by policies_get.
```

---

### PE-P03 — Get Policy Schema (Latest Version)
**Discovery:** `Selection` | **Expected:** `policies_get_schema` | **Timeout:** `15s`

```
Call policies_get_schema without specifying a version (returns the latest).
Report: the schema version and top-level keys.
Confirm the response is a valid JSON schema.
```

---

### PE-P04 — Full Policy Lifecycle: Create → Get → Update → Delete
**Discovery:** `Stress` | **Expected:** `organizations_list → policies_get_schema → policies_create → policies_get → policies_update → policies_get (verify) → policies_delete → policies_get (verify 404)` | **Timeout:** `120s`

```
1. Call organizations_list to get the org ID.
2. Call policies_get_schema to get the current schema and construct valid YAML.
3. Create a policy named "pe-p04-test-policy" using policies_create.
4. Call policies_get — verify it exists and name matches.
5. Update the policy description using policies_update (change description field).
6. Call policies_get again — verify the description was updated.
7. Delete the policy using policies_delete.
8. Call policies_get — verify 404 is returned.
Report each step's outcome.
```

---

### PE-P05 — Discover Policies for a Component and Workflow
**Discovery:** `Chain` | **Expected:** `services_list → workflow_list → policies_discover` | **Timeout:** `40s`

```
1. Call services_list to get a component ID.
2. Call workflow_list for that component to get a workflow context.
3. Call policies_discover with the component ID and workflow context.
Report: each matching policy's name, outcome (worst-case action), rules, and scope.
If no policies match, record "0 policies in scope — empty result OK".
```

---

### PE-P06 — List Policy Evaluations for a Run
**Discovery:** `Chain` | **Expected:** `services_list → search_runs → policies_run_evaluations_list` | **Timeout:** `35s`

```
1. Call services_list to get a component.
2. Call search_runs for that component to find a completed run.
3. Call policies_run_evaluations_list for that run.
Report: evaluation results grouped by checkpoint, each checkpoint's pass/fail outcome.
If no runs exist, record "No completed runs found — test skipped".
```

---

## NEGATIVE TEST CASES

---

### PE-N01 — Get Policy with Non-Existent ID
**Discovery:** `Selection` | **Expected:** `policies_get` | **Timeout:** `15s`

```
Call policies_get with a nil ID: 00000000-0000-0000-0000-000000000099.
Record the exact error message and HTTP status code. Expected: 404.
```

---

### PE-N02 — Delete Policy with Non-Existent ID
**Discovery:** `Selection` | **Expected:** `policies_delete` | **Timeout:** `15s`

```
Call policies_delete with a nil ID: 00000000-0000-0000-0000-000000000099.
Record the exact error message and HTTP status code. Expected: 404.
```

---

### PE-N03 — Update Policy with Non-Existent ID
**Discovery:** `Selection` | **Expected:** `policies_update` | **Timeout:** `15s`

```
Call policies_update with a nil ID: 00000000-0000-0000-0000-000000000099 and any valid YAML content.
Record the exact error message. Expected: 404.
```

---

### PE-N04 — Create Policy with Invalid YAML
**Discovery:** `Selection` | **Expected:** `policies_create` | **Timeout:** `15s`

```
Call organizations_list to get the org ID.
Attempt policies_create with invalid YAML content: "this: is: not: valid: yaml:::{{{".
Record the exact error message. Expected: 400 validation error.
```

---

### PE-N05 — Discover Policies with Non-Existent Component
**Discovery:** `Selection` | **Expected:** `policies_discover` | **Timeout:** `15s`

```
Call policies_discover with a nil component ID: 00000000-0000-0000-0000-000000000099.
Record the exact error message and HTTP status code. Expected: 404 or 400.
```

---

### PE-N06 — Policy Run Evaluations with Non-Existent Run
**Discovery:** `Selection` | **Expected:** `policies_run_evaluations_list` | **Timeout:** `15s`

```
Call policies_run_evaluations_list with a nil run ID: 00000000-0000-0000-0000-000000000099.
Record the exact error message and HTTP status code. Expected: 404 or 400.
```

---

## EDGE CASES

---

### PE-E01 — Get Schema for Latest and Explicit Version
**Discovery:** `Chain` | **Expected:** `policies_get_schema → policies_get_schema (explicit version)` | **Timeout:** `25s`

```
1. Call policies_get_schema without a version — record the returned schema version number.
2. Call policies_get_schema again with that explicit version number.
3. Verify both responses are identical.
Report the current schema version and whether explicit-version fetching works.
```

---

### PE-E02 — Update an Existing Policy and Restore
**Discovery:** `Chain` | **Expected:** `organizations_list → policies_list → policies_get → policies_update → policies_get (verify)` | **Timeout:** `60s`

```
1. Call organizations_list and policies_list to find an existing policy.
2. Call policies_get to read the current YAML definition.
3. Modify the description field using policies_update.
4. Call policies_get — verify the change is reflected.
5. Restore the original definition using policies_update.
6. Verify restoration via policies_get.
```

---

### PE-E03 — Policy Count Changes After Create and Delete
**Discovery:** `Chain` | **Expected:** `organizations_list → policies_create → policies_list (verify count) → policies_delete` | **Timeout:** `60s`

```
1. Call policies_list and record the count (before).
2. Create a policy "pe-e03-count-check".
3. Call policies_list — verify the count increased by 1.
4. Delete the policy.
5. Call policies_list — verify the count returned to original.
```

---

### PE-E04 — Verify Policy Deletion is Immediate
**Discovery:** `Chain` | **Expected:** `organizations_list → policies_create → policies_delete → policies_get (confirm 404)` | **Timeout:** `60s`

```
1. Create a policy "pe-e04-immediate-delete".
2. Delete it using policies_delete.
3. Immediately call policies_get with the deleted policy ID.
4. Verify: 404 is returned — deletion is immediately visible.
```

---

### PE-E05 — Policy Evaluations for Multiple Runs
**Discovery:** `Chain` | **Expected:** `services_list → search_runs → policies_run_evaluations_list (×2 runs)` | **Timeout:** `60s`

```
1. Call services_list to get a component.
2. Call search_runs to get the two most recent completed runs.
3. Call policies_run_evaluations_list for each run.
4. Compare: do both runs have policy evaluations? Are the outcomes consistent?
Report: checkpoint names and results for both runs. Note if any policy evaluation is missing for a run.
```

---

### PE-E06 — Create Policy with Duplicate Name
**Discovery:** `Chain` | **Expected:** `organizations_list → policies_create → policies_create (duplicate name) → policies_delete` | **Timeout:** `60s`

```
1. Call organizations_list to get the org ID.
2. Create a policy named "pe-e06-dup-policy".
3. Attempt to create another policy with the same name "pe-e06-dup-policy".
4. Record the exact error. Expected: 409 Conflict or 400.
5. Delete the first policy.
```
