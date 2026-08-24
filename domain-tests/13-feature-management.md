# Domain: Feature Management
**Tools covered (26):** `flag_approval_requests_list`, `flag_configuration_conditions_set`, `flag_custom_properties_add`, `flag_custom_properties_delete`, `flag_custom_properties_flag_usage_per_environment`, `flag_custom_properties_get`, `flag_custom_properties_get_by_name`, `flag_custom_properties_list`, `flag_custom_properties_target_group_usage`, `flag_serve_to_target_group`, `flag_target_groups_add`, `flag_target_groups_delete`, `flag_target_groups_flag_usage_per_environment`, `flag_target_groups_get`, `flag_target_groups_get_by_name`, `flag_target_groups_list`, `flag_target_groups_list_with_flags_usage`, `flag_target_groups_target_group_usage`, `flags_add`, `flags_configuration_state_update`, `flags_configurations_list`, `flags_delete`, `flags_flag_usage_per_environment`, `flags_get`, `flags_list`, `flags_update_defaultValue`
**Total prompts:** 36 (12 positive, 12 negative, 12 edge)

> **Cross-domain tools used for setup:** `organizations_list` (default), `flags_applications_list` (default), `flags_environments_list` (default), `flags_get_by_name` (default), `flag_configuration_get` (default)

---

## Test Execution Tracker

| ID | Type | Category | Expected Tools | Timeout | Status | Notes |
|----|------|----------|----------------|---------|--------|-------|
| FM-P01 | Positive | Stress | `flags_applications_list` → `flags_add` → `flags_get` → `flags_configurations_list` → `flag_configuration_get` → `flags_configuration_state_update` → `flags_flag_usage_per_environment` → `flags_configuration_state_update` → `flags_delete` | 120s | ⬜ | Full Boolean flag lifecycle |
| FM-P02 | Positive | Stress | `flags_applications_list` → `flags_add` (String) → `flags_get_by_name` → `flags_update_defaultValue` → `flag_configuration_get` → `flags_delete` | 90s | ⬜ | Full String flag lifecycle |
| FM-P03 | Positive | Stress | `flags_applications_list` → `flag_custom_properties_add` → `flag_target_groups_add` → `flag_target_groups_get` → `flag_target_groups_get_by_name` → `flag_target_groups_list` → `flag_target_groups_delete` → `flag_custom_properties_delete` | 120s | ⬜ | Full target group lifecycle |
| FM-P04 | Positive | Stress | `flags_applications_list` → `flag_custom_properties_add` ×3 → `flag_custom_properties_list` → `flag_custom_properties_get` → `flag_custom_properties_get_by_name` → `flag_custom_properties_delete` ×3 | 120s | ⬜ | Custom properties CRUD |
| FM-P05 | Positive | Chain | `flags_applications_list` → `flags_list` → `flags_flag_usage_per_environment` | 35s | ⬜ | Flag usage per environment |
| FM-P06 | Positive | Selection | `flags_applications_list` → `flag_approval_requests_list` | 20s | ⬜ | |
| FM-P07 | Positive | Chain | `flags_applications_list` → `flag_target_groups_list` → `flag_target_groups_list_with_flags_usage` | 30s | ⬜ | |
| FM-P08 | Positive | Chain | `flags_applications_list` → `flag_target_groups_list` → `flag_target_groups_flag_usage_per_environment` | 30s | ⬜ | |
| FM-P09 | Positive | Chain | `flags_applications_list` → `flag_custom_properties_list` → `flag_custom_properties_flag_usage_per_environment` | 30s | ⬜ | |
| FM-P10 | Positive | Chain | `flags_applications_list` → `flag_custom_properties_list` → `flag_custom_properties_target_group_usage` | 30s | ⬜ | |
| FM-P11 | Positive | Stress | `flags_applications_list` → `flag_custom_properties_add` → `flags_add` → `flag_target_groups_add` → `flag_configuration_conditions_set` → `flag_configuration_get` → `flag_target_groups_delete` → `flags_delete` → `flag_custom_properties_delete` | 120s | ⬜ | Targeting rules |
| FM-P12 | Positive | Stress | `flags_applications_list` → `flag_custom_properties_add` → `flags_add` → `flag_target_groups_add` → `flag_serve_to_target_group` → `flag_configuration_get` → `flag_target_groups_delete` → `flags_delete` → `flag_custom_properties_delete` | 120s | ⬜ | Serve to target group |
| FM-N01 | Negative | Chain | `flags_applications_list` → `flags_add` → `flags_update_defaultValue` (wrong type) → `flags_delete` | 60s | ⬜ | Known Bug #4 |
| FM-N02 | Negative | Chain | `flags_applications_list` → `flags_add` → `flags_add` (duplicate name) → `flags_delete` | 45s | ⬜ | |
| FM-N03 | Negative | Selection | `flags_add` (empty name) | 15s | ⬜ | |
| FM-N04 | Negative | Selection | `flags_get_by_name` (non-existent name) | 15s | ⬜ | |
| FM-N05 | Negative | Selection | `flags_delete` (nil ID) | 15s | ⬜ | |
| FM-N06 | Negative | Selection | `flag_target_groups_delete` (nil ID) | 15s | ⬜ | |
| FM-N07 | Negative | Selection | `flag_target_groups_get` (nil ID) | 15s | ⬜ | |
| FM-N08 | Negative | Selection | `flag_custom_properties_get_by_name` (non-existent) | 15s | ⬜ | |
| FM-N09 | Negative | Selection | `flag_target_groups_add` (invalid condition operator) | 15s | ⬜ | |
| FM-N10 | Negative | Chain | `flags_applications_list` → `flags_add` → `flag_configuration_conditions_set` (unknown property) → `flags_delete` | 45s | ⬜ | |
| FM-N11 | Negative | Chain | `flags_applications_list` → `flags_add` → `flag_serve_to_target_group` (non-existent TG) → `flags_delete` | 45s | ⬜ | |
| FM-N12 | Negative | Selection | `flag_custom_properties_get` (nil ID) | 15s | ⬜ | |
| FM-E01 | Edge | Chain | `flags_applications_list` → `flags_add` → `flag_configuration_get` (brand new flag, no config) → `flags_delete` | 45s | ⬜ | |
| FM-E02 | Edge | Chain | `flags_applications_list` → `flags_add` → `flags_delete` (never enabled) | 30s | ⬜ | |
| FM-E03 | Edge | Chain | `flags_applications_list` → `flag_target_groups_add` (empty anyOf) → `flag_target_groups_get` → `flag_target_groups_delete` | 45s | ⬜ | |
| FM-E04 | Edge | Chain | `flags_applications_list` → `flags_add` → `flags_configuration_state_update` ×4 → `flag_configuration_get` → `flags_delete` | 90s | ⬜ | Toggle many times |
| FM-E05 | Edge | Chain | `flags_applications_list` → `flags_list` | 20s | ⬜ | List all flags |
| FM-E06 | Edge | Chain | `flags_applications_list` → `flag_target_groups_list` (empty app) | 20s | ⬜ | |
| FM-E07 | Edge | Chain | `flags_applications_list` → `flag_custom_properties_list` (empty app) | 20s | ⬜ | |
| FM-E08 | Edge | Chain | `flags_applications_list` → `flags_add` → `flag_configuration_conditions_set` → `flag_configuration_conditions_set` (empty array) → `flag_configuration_get` → `flags_delete` | 90s | ⬜ | Clear all conditions |
| FM-E09 | Edge | Chain | `flags_applications_list` → `flag_target_groups_add` → `flag_target_groups_list` → `flag_target_groups_list_with_flags_usage` → `flag_target_groups_delete` | 60s | ⬜ | Cross-check TG lists |
| FM-E10 | Edge | Chain | `flags_applications_list` → `flags_add` (isPermanent=true) → `flags_get` → `flags_delete` | 45s | ⬜ | |
| FM-E11 | Edge | Chain | `flags_applications_list` → `flag_target_groups_list` → `flag_target_groups_target_group_usage` | 30s | ⬜ | TG nesting usage |
| FM-E12 | Edge | Stress | `flags_applications_list` → `flag_custom_properties_add` → `flags_add` → `flag_target_groups_add` → `flag_serve_to_target_group` (by name) → `flag_configuration_get` → `flag_target_groups_delete` → `flags_delete` → `flag_custom_properties_delete` | 120s | ⬜ | Serve by name not UUID |

---

## Diagnostic Categories

| Category | Definition | Failure Indicates |
|----------|-----------|-------------------|
| **Selection** | Single tool call from natural language | AI picked the wrong tool from 131 options |
| **Chain** | 2–4 tools called in sequence | Wrong tool order, missed step, or incorrect data passed between steps |
| **Stress** | 5+ tools OR repeated calls OR large payloads | Timeout, session limit, or token exhaustion |

---

## Test Setup

> Resolve all IDs at runtime. Call `flags_applications_list` to get app ID; `flags_environments_list` for environment ID.
> Test resource naming convention: `fm-[test-id]-[date]`
> Target group conditions are validated server-side against existing custom properties.
> Creating a target group with `{"property": {"name": "X"}}` will fail with 400 if property "X" does not exist.
> Tests that need property-based conditions (FM-P03, FM-P11, FM-P12) create the custom property first as a setup step.
> Nil UUID for negative tests: `00000000-0000-0000-0000-000000000099`

---

## POSITIVE TEST CASES

---

### FM-P01 — Full Boolean Flag Lifecycle
**Discovery:** `Stress` | **Expected:** `flags_applications_list → flags_add → flags_get → flags_configurations_list → flag_configuration_get → flags_configuration_state_update → flags_flag_usage_per_environment → flags_configuration_state_update → flags_delete` | **Timeout:** `120s`

```
1. Call flags_applications_list to get the app ID.
2. Call flags_environments_list to get an environment ID.
3. Create a Boolean feature flag named "fm-p01-bool-flag" using flags_add.
4. Verify via flags_get: name, type=BOOLEAN, default value.
5. Call flags_configurations_list for the environment.
6. Call flag_configuration_get for this flag in the environment.
7. Enable the flag using flags_configuration_state_update (enabled=true).
8. Check flags_flag_usage_per_environment — the environment should show enabled.
9. Disable the flag (enabled=false).
10. Delete the flag using flags_delete.
Report the result of each step.
```

---

### FM-P02 — Full String Flag Lifecycle with Default Value Update
**Discovery:** `Stress` | **Expected:** `flags_applications_list → flags_add (String) → flags_get_by_name → flags_update_defaultValue → flag_configuration_get → flags_delete` | **Timeout:** `90s`

```
1. Call flags_applications_list to get the app ID and environment ID.
2. Create a String flag named "fm-p02-string-flag" with defaultValue="hello".
3. Retrieve it by name using flags_get_by_name.
4. Update the default value to "updated-value" using flags_update_defaultValue.
5. Call flag_configuration_get to verify the default value was updated.
6. Delete the flag.
Report each step's outcome. Note Known Bug #4 if Boolean flag type update fails.
```

---

### FM-P03 — Full Target Group Lifecycle with Custom Property Condition
**Discovery:** `Stress` | **Expected:** `flags_applications_list → flag_custom_properties_add → flag_target_groups_add → flag_target_groups_get → flag_target_groups_get_by_name → flag_target_groups_list → flag_target_groups_delete → flag_custom_properties_delete` | **Timeout:** `120s`

```
1. Call flags_applications_list to get the app ID.
2. Create a custom property named "fm-p03-prop" using flag_custom_properties_add.
3. Create a target group named "fm-p03-tg" with a property condition referencing "fm-p03-prop".
4. Retrieve the target group by ID using flag_target_groups_get.
5. Retrieve it by name using flag_target_groups_get_by_name.
6. List all target groups and verify "fm-p03-tg" appears.
7. Delete the target group using flag_target_groups_delete.
8. Delete the custom property using flag_custom_properties_delete.
Report each step's outcome.
```

---

### FM-P04 — Full Custom Properties Lifecycle (3 Types)
**Discovery:** `Stress` | **Expected:** `flags_applications_list → flag_custom_properties_add ×3 → flag_custom_properties_list → flag_custom_properties_get → flag_custom_properties_get_by_name → flag_custom_properties_delete ×3` | **Timeout:** `120s`

```
1. Call flags_applications_list to get the app ID.
2. Create three custom properties:
   a. "fm-p04-prop-string" (type: String)
   b. "fm-p04-prop-bool" (type: Boolean)
   c. "fm-p04-prop-num" (type: Number)
3. Call flag_custom_properties_list — verify all three appear.
4. Call flag_custom_properties_get for the first property by ID.
5. Call flag_custom_properties_get_by_name for the second property by name.
6. Delete all three properties.
Report each step's outcome.
```

---

### FM-P05 — Flag Usage Per Environment
**Discovery:** `Chain` | **Expected:** `flags_applications_list → flags_list → flags_flag_usage_per_environment` | **Timeout:** `35s`

```
1. Call flags_applications_list to get the app ID.
2. Call flags_list to get the list of flags.
3. Pick the first flag and call flags_flag_usage_per_environment for it.
Report: each environment's name and whether the flag is enabled in it.
```

---

### FM-P06 — List Flag Approval Requests
**Discovery:** `Selection` | **Expected:** `flags_applications_list → flag_approval_requests_list` | **Timeout:** `20s`

```
Call flags_applications_list to get the app ID.
Call flag_approval_requests_list for that application.
Report: total pending approvals, each request's flag name, requester, and created date.
If no approvals, record "0 approval requests — empty result OK".
```

---

### FM-P07 — List Target Groups with and without Flag Usage
**Discovery:** `Chain` | **Expected:** `flags_applications_list → flag_target_groups_list → flag_target_groups_list_with_flags_usage` | **Timeout:** `30s`

```
1. Call flags_applications_list to get the app ID.
2. Call flag_target_groups_list — record total count and names.
3. Call flag_target_groups_list_with_flags_usage — record the same, plus flag usage per target group.
Verify: the count matches between both calls. Report which target groups are used by flags.
```

---

### FM-P08 — Target Group Flag Usage Per Environment
**Discovery:** `Chain` | **Expected:** `flags_applications_list → flag_target_groups_list → flag_target_groups_flag_usage_per_environment` | **Timeout:** `30s`

```
1. Call flags_applications_list to get the app ID.
2. Call flag_target_groups_list to get a target group ID.
3. Call flag_target_groups_flag_usage_per_environment for that target group.
Report: each environment and its flag count that uses this target group.
```

---

### FM-P09 — Custom Property Flag Usage Per Environment
**Discovery:** `Chain` | **Expected:** `flags_applications_list → flag_custom_properties_list → flag_custom_properties_flag_usage_per_environment` | **Timeout:** `30s`

```
1. Call flags_applications_list to get the app ID.
2. Call flag_custom_properties_list to get a property ID.
3. Call flag_custom_properties_flag_usage_per_environment for that property.
Report: flag usage counts per environment for this custom property.
```

---

### FM-P10 — Custom Property Target Group Usage
**Discovery:** `Chain` | **Expected:** `flags_applications_list → flag_custom_properties_list → flag_custom_properties_target_group_usage` | **Timeout:** `30s`

```
1. Call flags_applications_list to get the app ID.
2. Call flag_custom_properties_list to get a property ID.
3. Call flag_custom_properties_target_group_usage for that property.
Report: which target groups reference this custom property in their conditions.
```

---

### FM-P11 — Set Targeting Conditions Using a Property Rule
**Discovery:** `Stress` | **Expected:** full chain | **Timeout:** `120s`

```
1. Call flags_applications_list to get the app ID and environment ID.
2. Create a custom property "fm-p11-prop".
3. Create a Boolean flag "fm-p11-flag".
4. Create a target group "fm-p11-tg" with a condition referencing "fm-p11-prop".
5. Call flag_configuration_conditions_set to set targeting rules for the flag in the environment,
   referencing the target group.
6. Call flag_configuration_get — verify the conditions were saved.
7. Delete: target group → flag → custom property.
Report each step's outcome.
```

---

### FM-P12 — Serve Value to Target Group
**Discovery:** `Stress` | **Expected:** full chain | **Timeout:** `120s`

```
1. Call flags_applications_list to get the app ID and environment ID.
2. Create a custom property "fm-p12-prop".
3. Create a Boolean flag "fm-p12-flag".
4. Create a target group "fm-p12-tg" with a condition referencing "fm-p12-prop".
5. Call flag_serve_to_target_group to serve value=true to "fm-p12-tg" for the flag in the environment.
6. Call flag_configuration_get — verify a targeting rule was added for the target group.
7. Delete: target group → flag → custom property.
Report each step.
```

---

## NEGATIVE TEST CASES

---

### FM-N01 — Update Default Value with Wrong Type (Boolean Flag → String)
**Discovery:** `Chain` | **Expected:** `flags_applications_list → flags_add → flags_update_defaultValue (wrong type) → flags_delete` | **Timeout:** `60s`

```
1. Call flags_applications_list to get the app ID.
2. Create a Boolean flag "fm-n01-bool-flag".
3. Attempt flags_update_defaultValue with a String value "not-a-boolean".
4. Record the exact error. Expected: 400 validation error (Known Bug #4 — may succeed incorrectly).
5. Delete the flag.
```

---

### FM-N02 — Create Flag with Duplicate Name
**Discovery:** `Chain` | **Expected:** `flags_applications_list → flags_add → flags_add (duplicate) → flags_delete` | **Timeout:** `45s`

```
1. Call flags_applications_list to get the app ID.
2. Create a Boolean flag "fm-n02-dup-flag".
3. Attempt to create another flag with the same name "fm-n02-dup-flag".
4. Record the exact error. Expected: 409 Conflict or 400.
5. Delete the first flag.
```

---

### FM-N03 — Create Flag with Empty Name
**Discovery:** `Selection` | **Expected:** `flags_add` | **Timeout:** `15s`

```
Call flags_applications_list to get the app ID.
Attempt flags_add with name="" (empty string).
Record the exact error message. Expected: 400 validation error.
```

---

### FM-N04 — Get Flag by Non-Existent Name
**Discovery:** `Selection` | **Expected:** `flags_get_by_name` | **Timeout:** `15s`

```
Call flags_applications_list to get the app ID.
Call flags_get_by_name with name="no-such-flag-xyz-9999".
Record the exact response. Expected: 404.
```

---

### FM-N05 — Delete Non-Existent Flag
**Discovery:** `Selection` | **Expected:** `flags_delete` | **Timeout:** `15s`

```
Call flags_delete with a nil flag ID: 00000000-0000-0000-0000-000000000099.
Record the exact error message and HTTP status code. Expected: 404.
```

---

### FM-N06 — Delete Non-Existent Target Group
**Discovery:** `Selection` | **Expected:** `flag_target_groups_delete` | **Timeout:** `15s`

```
Call flag_target_groups_delete with a nil ID: 00000000-0000-0000-0000-000000000099.
Record the exact error message and HTTP status code. Expected: 404.
```

---

### FM-N07 — Get Non-Existent Target Group by ID
**Discovery:** `Selection` | **Expected:** `flag_target_groups_get` | **Timeout:** `15s`

```
Call flags_applications_list to get the app ID.
Call flag_target_groups_get with a nil ID: 00000000-0000-0000-0000-000000000099.
Record the exact error message. Expected: 404.
```

---

### FM-N08 — Get Custom Property by Non-Existent Name
**Discovery:** `Selection` | **Expected:** `flag_custom_properties_get_by_name` | **Timeout:** `15s`

```
Call flags_applications_list to get the app ID.
Call flag_custom_properties_get_by_name with name="no-such-prop-xyz-9999".
Record the exact response. Expected: 404.
```

---

### FM-N09 — Create Target Group with Invalid Condition Operator
**Discovery:** `Selection` | **Expected:** `flag_target_groups_add` | **Timeout:** `15s`

```
Call flags_applications_list to get the app ID.
Attempt flag_target_groups_add with an invalid condition operator (e.g., operator="INVALID_OP").
Record the exact error message. Expected: 400 validation error.
```

---

### FM-N10 — Set Conditions with Unknown Custom Property
**Discovery:** `Chain` | **Expected:** `flags_applications_list → flags_add → flag_configuration_conditions_set (unknown property) → flags_delete` | **Timeout:** `45s`

```
1. Call flags_applications_list to get the app ID and environment ID.
2. Create a Boolean flag "fm-n10-cond-flag".
3. Attempt flag_configuration_conditions_set referencing a property named "nonexistent-prop-xyz-9999".
4. Record the exact error. Expected: 400.
5. Delete the flag.
```

---

### FM-N11 — Serve to Non-Existent Target Group
**Discovery:** `Chain` | **Expected:** `flags_applications_list → flags_add → flag_serve_to_target_group (non-existent TG) → flags_delete` | **Timeout:** `45s`

```
1. Call flags_applications_list to get the app ID and environment ID.
2. Create a Boolean flag "fm-n11-serve-flag".
3. Attempt flag_serve_to_target_group with a non-existent target group name "nonexistent-tg-xyz-9999".
4. Record the exact error. Expected: 404.
5. Delete the flag.
```

---

### FM-N12 — Get Custom Property with Nil ID
**Discovery:** `Selection` | **Expected:** `flag_custom_properties_get` | **Timeout:** `15s`

```
Call flags_applications_list to get the app ID.
Call flag_custom_properties_get with a nil ID: 00000000-0000-0000-0000-000000000099.
Record the exact error message. Expected: 404.
```

---

## EDGE CASES

---

### FM-E01 — New Flag Has No Configuration State Set
**Discovery:** `Chain` | **Expected:** `flags_applications_list → flags_add → flag_configuration_get → flags_delete` | **Timeout:** `45s`

```
1. Create a Boolean flag "fm-e01-new-flag" in the app.
2. Immediately call flag_configuration_get for this flag in an environment (no config has been set).
3. Verify the response shows a default state (not an error).
4. Delete the flag.
Record the default configuration shape for a brand-new flag.
```

---

### FM-E02 — Delete Flag That Was Never Enabled
**Discovery:** `Chain` | **Expected:** `flags_applications_list → flags_add → flags_delete` | **Timeout:** `30s`

```
1. Create a Boolean flag "fm-e02-never-enabled".
2. Do NOT enable it in any environment.
3. Call flags_delete immediately.
4. Verify deletion via flags_get — must return 404.
Confirms that flags can be deleted cleanly even in their default (disabled) state.
```

---

### FM-E03 — Target Group with Empty anyOf Condition
**Discovery:** `Chain` | **Expected:** `flags_applications_list → flag_target_groups_add (empty anyOf) → flag_target_groups_get → flag_target_groups_delete` | **Timeout:** `45s`

```
1. Create a target group "fm-e03-empty-tg" with an empty anyOf condition array (matches nothing).
2. Retrieve it via flag_target_groups_get.
3. Delete it.
Verify the server accepts an empty condition list without error.
```

---

### FM-E04 — Toggle Flag Enable/Disable Multiple Times
**Discovery:** `Chain` | **Expected:** `flags_applications_list → flags_add → flags_configuration_state_update ×4 → flag_configuration_get → flags_delete` | **Timeout:** `90s`

```
1. Create a Boolean flag "fm-e04-toggle-flag".
2. Enable it in an environment.
3. Disable it.
4. Enable it again.
5. Disable it again.
6. Call flag_configuration_get — verify final state is disabled.
7. Delete the flag.
Verify rapid toggling does not leave inconsistent state.
```

---

### FM-E05 — List All Flags Across Application
**Discovery:** `Chain` | **Expected:** `flags_applications_list → flags_list` | **Timeout:** `20s`

```
Call flags_applications_list to get the app ID.
Call flags_list for that application.
Report: total flag count, types present (BOOLEAN / STRING / NUMBER), and enabled/disabled breakdown.
```

---

### FM-E06 — List Target Groups When None Exist
**Discovery:** `Chain` | **Expected:** `flags_applications_list → flag_target_groups_list` | **Timeout:** `20s`

```
Call flags_applications_list to get the app ID.
Call flag_target_groups_list for the application.
If no target groups exist: verify empty result is returned without error.
Report: total count. If count > 0, report names of the first 5.
```

---

### FM-E07 — List Custom Properties When None Exist
**Discovery:** `Chain` | **Expected:** `flags_applications_list → flag_custom_properties_list` | **Timeout:** `20s`

```
Call flags_applications_list to get the app ID.
Call flag_custom_properties_list for the application.
If no custom properties exist: verify empty result is returned without error.
Report: total count. If count > 0, report names of the first 5.
```

---

### FM-E08 — Set Conditions Then Clear All with Empty Array
**Discovery:** `Stress` | **Expected:** full chain | **Timeout:** `90s`

```
1. Create a custom property "fm-e08-prop" and a Boolean flag "fm-e08-flag".
2. Set targeting conditions for the flag referencing the custom property.
3. Call flag_configuration_get — verify conditions are set.
4. Call flag_configuration_conditions_set with an empty array [].
5. Call flag_configuration_get — verify all conditions are now cleared.
6. Delete flag and custom property.
```

---

### FM-E09 — Cross-Check TG List vs TG List with Usage
**Discovery:** `Chain` | **Expected:** `flags_applications_list → flag_target_groups_add → flag_target_groups_list → flag_target_groups_list_with_flags_usage → flag_target_groups_delete` | **Timeout:** `60s`

```
1. Create a target group "fm-e09-tg".
2. Call flag_target_groups_list — verify it appears.
3. Call flag_target_groups_list_with_flags_usage — verify it appears here too, with usage=0.
4. Confirm count matches between both calls.
5. Delete the target group.
```

---

### FM-E10 — Create Flag with isPermanent=true
**Discovery:** `Chain` | **Expected:** `flags_applications_list → flags_add (isPermanent=true) → flags_get → flags_delete` | **Timeout:** `45s`

```
1. Create a Boolean flag "fm-e10-permanent-flag" with isPermanent=true.
2. Retrieve via flags_get — verify isPermanent=true is reflected.
3. Delete the flag.
Note: if deletion is blocked due to isPermanent, record the exact error.
```

---

### FM-E11 — Target Group Nesting Usage
**Discovery:** `Chain` | **Expected:** `flags_applications_list → flag_target_groups_list → flag_target_groups_target_group_usage` | **Timeout:** `30s`

```
Call flags_applications_list to get the app ID.
Call flag_target_groups_list to get a target group ID.
Call flag_target_groups_target_group_usage for that target group.
Report: which other target groups (if any) reference (nest) this one via group conditions.
If none, record "0 nested usages — empty result OK".
```

---

### FM-E12 — Serve to Target Group by Name (Not UUID)
**Discovery:** `Stress` | **Expected:** full chain | **Timeout:** `120s`

```
1. Create a custom property "fm-e12-prop".
2. Create a Boolean flag "fm-e12-flag".
3. Create a target group "fm-e12-tg".
4. Call flag_serve_to_target_group using the target group NAME (not UUID) to serve value=true.
5. Call flag_configuration_get — verify the targeting rule references the target group.
6. Delete: target group → flag → custom property.
Verifies that name-based resolution works in flag_serve_to_target_group.
```
