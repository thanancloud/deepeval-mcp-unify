# Domain: Feature Flags
**Tools covered (30):** `flags_environments_list`, `flags_applications_list`, `flags_add`, `flags_list`, `flags_get`, `flags_get_by_name`, `flags_update_defaultValue`, `flags_flag_usage_per_environment`, `flags_delete`, `flags_configurations_list`, `flag_configuration_get`, `flags_configuration_state_update`, `flag_configuration_conditions_set`, `flag_approval_requests_list`, `flag_target_groups_add`, `flag_target_groups_delete`, `flag_target_groups_get`, `flag_target_groups_get_by_name`, `flag_target_groups_list`, `flag_target_groups_flag_usage_per_environment`, `flag_target_groups_list_with_flags_usage`, `flag_target_groups_target_group_usage`, `flag_serve_to_target_group`, `flag_custom_properties_add`, `flag_custom_properties_delete`, `flag_custom_properties_get`, `flag_custom_properties_get_by_name`, `flag_custom_properties_list`, `flag_custom_properties_flag_usage_per_environment`, `flag_custom_properties_target_group_usage`
**Total prompts:** 36 (12 positive, 12 negative, 12 edge cases)

---

## Test Execution Tracker

| ID | Type | Category | Expected Tools | Timeout | Description | Status | Notes |
|----|------|----------|----------------|---------|-------------|--------|-------|
| FF-P01 | Positive | Stress | `flags_applications_list → flags_add → flags_get → flags_configurations_list → flag_configuration_get → flags_configuration_state_update → flags_flag_usage_per_environment → flags_configuration_state_update → flags_delete` | 120s | Full Boolean flag lifecycle: create → enable → disable → delete | ⬜ | |
| FF-P02 | Positive | Stress | `flags_add → flags_get_by_name → flags_configuration_state_update → flags_update_defaultValue → flag_configuration_get → flags_configuration_state_update → flags_delete` | 120s | Full String flag lifecycle including default value update | ⬜ | |
| FF-P03 | Positive | Stress | `flag_custom_properties_add → flag_target_groups_add → flag_target_groups_get → flag_target_groups_get_by_name → flag_target_groups_list → flag_target_groups_flag_usage_per_environment → flag_target_groups_list_with_flags_usage → flag_target_groups_target_group_usage → flag_target_groups_delete → flag_custom_properties_delete` | 120s | Full target group lifecycle with real property condition | ⬜ | Requires pre-creating "subscription_tier" custom property (step 0) |
| FF-P04 | Positive | Stress | `flag_custom_properties_add (×3) → flag_custom_properties_list → flag_custom_properties_get → flag_custom_properties_get_by_name → flag_custom_properties_flag_usage_per_environment → flag_custom_properties_target_group_usage → flag_custom_properties_delete (×3)` | 120s | Full custom properties lifecycle across all 3 types | ⬜ | |
| FF-P05 | Positive | Stress | `flags_applications_list → flags_list (×N)` | 90s | List all flags across all applications | ⬜ | |
| FF-P06 | Positive | Chain | `flags_add → flags_get → flags_get_by_name → flags_delete` | 60s | Get flag by ID and by name — verify data matches | ⬜ | |
| FF-P07 | Positive | Stress | ~~`flags_environments_list → flags_sdk_key_get (×N)`~~ | — | ⬛ | Tool removed |
| FF-P08 | Positive | Selection | `flag_approval_requests_list` | 15s | Flag approval requests list | ⬜ | |
| FF-P09 | Positive | Stress | `flag_custom_properties_add → flag_target_groups_add → flag_target_groups_get → flag_target_groups_delete → flag_custom_properties_delete` | 90s | Target group with nested anyOf conditions | ⬜ | Requires pre-creating "plan" custom property (step 0) |
| FF-P10 | Positive | Chain | `flags_add → flags_configuration_state_update → flags_flag_usage_per_environment → flags_configuration_state_update → flags_delete` | 60s | Flag usage per environment after flag is enabled | ⬜ | |
| FF-P11 | Positive | Stress | `flag_custom_properties_add → flags_add → flag_target_groups_add → flag_configuration_conditions_set → flag_configuration_get → flag_target_groups_delete → flags_delete → flag_custom_properties_delete` | 120s | Set targeting conditions using a property rule and verify they are persisted | ⬜ | |
| FF-P12 | Positive | Stress | `flag_custom_properties_add → flags_add → flag_target_groups_add → flag_serve_to_target_group → flag_configuration_get → flag_target_groups_delete → flags_delete → flag_custom_properties_delete` | 120s | Serve a value to a target group (enableIfDisabled=true) and verify the targeting rule was appended | ⬜ | |
| FF-N01 | Negative | Chain | `flags_add → flags_configuration_state_update → flags_delete → flags_configuration_state_update → flags_delete` | 60s | Delete flag that is still enabled | ⬜ | |
| FF-N02 | Negative | Chain | `flags_add → flags_configuration_state_update → flags_update_defaultValue → flags_delete` | 60s | Update default value with wrong type (Boolean flag → string value) | ⬜ | |
| FF-N03 | Negative | Chain | `flags_add → flags_add → flags_delete` | 45s | Create flag with duplicate name in same application | ⬜ | |
| FF-N04 | Negative | Selection | `flags_get_by_name` | 15s | Get flag by name that does not exist | ⬜ | |
| FF-N05 | Negative | Selection | `flag_target_groups_delete` | 15s | Delete target group with non-existent ID | ⬜ | |
| FF-N06 | Negative | Selection | `flag_custom_properties_get_by_name` | 15s | Get custom property by name that does not exist | ⬜ | |
| FF-N07 | Negative | Chain | `flags_add → flags_configuration_state_update → flags_delete` | 60s | Enable flag in environment that does not belong to its application | ⬜ | |
| FF-N08 | Negative | Selection | `flags_add` | 15s | Create flag with empty name | ⬜ | |
| FF-N09 | Negative | Selection | `flag_target_groups_add` | 15s | Create target group with invalid condition operator | ⬜ | |
| FF-N10 | Negative | Selection | ~~`flags_sdk_key_get`~~ | — | ⬛ | Tool removed |
| FF-N11 | Negative | Chain | `flags_add → flag_configuration_conditions_set → flags_delete` | 45s | Set conditions with an unknown custom property name — expect 400 | ⬜ | |
| FF-N12 | Negative | Chain | `flags_add → flag_serve_to_target_group → flags_delete` | 45s | Serve value to a non-existent target group name — expect 404 | ⬜ | |
| FF-E01 | Edge | Chain | `flags_add → flag_configuration_get → flags_delete` | 30s | Flag with no configurations ever set (brand new flag, check config default state) | ⬜ | |
| FF-E02 | Edge | Chain | `flags_add → flags_configuration_state_update → flags_flag_usage_per_environment → flags_configuration_state_update → flags_delete` | 60s | Create flag, enable it, check usage is still empty (not evaluated yet) | ⬜ | |
| FF-E03 | Edge | Chain | `flag_target_groups_add → flag_target_groups_get → flag_target_groups_delete` | 30s | Target group with empty anyOf condition (matches nothing) | ⬜ | |
| FF-E04 | Edge | Chain | `flag_custom_properties_add → flag_custom_properties_get → flag_custom_properties_delete` | 30s | Custom property with all optional fields (cascUrl, resourceId) | ⬜ | |
| FF-E05 | Edge | Chain | `flags_applications_list → flag_target_groups_list` | 30s | List target groups when none exist in an application | ⬜ | |
| FF-E06 | Edge | Chain | `flags_applications_list → flag_custom_properties_list` | 30s | List custom properties when none exist in an application | ⬜ | |
| FF-E07 | Edge | Stress | `flags_add → flags_configuration_state_update (×4) → flag_configuration_get (×4) → flags_delete` | 120s | Flag config state update — toggle enable/disable multiple times | ⬜ | |
| FF-E08 | Edge | Chain | `flags_add → flags_get → flags_delete` | 45s | Create flag with labels and isPermanent=true | ⬜ | |
| FF-E09 | Edge | Chain | `flag_target_groups_add → flag_target_groups_list → flag_target_groups_list_with_flags_usage → flag_target_groups_delete` | 60s | Cross-check: target group list with usage vs list without usage | ⬜ | |
| FF-E10 | Edge | Chain | `flags_add → flags_delete` | 30s | Delete flag that was never enabled — verify it deletes cleanly | ⬜ | |
| FF-E11 | Edge | Chain | `flags_add → flag_configuration_conditions_set → flag_configuration_conditions_set → flag_configuration_get → flags_delete` | 60s | Set conditions, then replace with empty array [] — verify all rules are cleared | ⬜ | |
| FF-E12 | Edge | Chain | `flag_custom_properties_add → flags_add → flag_target_groups_add → flag_serve_to_target_group (by name) → flag_configuration_get → flag_target_groups_delete → flags_delete → flag_custom_properties_delete` | 90s | Serve to target group by name (not UUID) — verify name resolution works | ⬜ | |

---

## Diagnostic Categories

| Category | Definition | Failure Indicates |
|----------|-----------|-------------------|
| **Selection** | Single tool call from natural language | AI picked the wrong tool from 84+ options |
| **Chain** | 2–4 tools called in sequence | Wrong tool order, missed step, or incorrect data passed between steps |
| **Stress** | 5+ tools OR repeated calls OR large payloads | Timeout, session limit, or token exhaustion |

---

## Test Setup (IDs to use throughout)

```
Organization ID:  6c5eeb79-4606-4c39-bd5c-c2323336caad
Application ID:   e1903ba8-9234-4ae2-ab5f-aa0962b5be2f  (Auto-ASO-Application)
Environment ID:   cde9e350-0523-4bc5-99d2-b5782c583723  (mm-qa-aspm)
Test flag prefix: ff-test-[ID]-[DATE]
Test TG prefix:   ff-tg-[ID]-[DATE]
Test CP prefix:   ff-cp-[ID]-[DATE]
```

> **Custom Property Pre-Requisite:**
> Target group conditions are validated server-side against existing custom properties for the application.
> Creating a target group with `{"property": {"name": "X", ...}}` will fail with 400 if property "X" does not already
> exist in the application. Tests FF-P03 and FF-P09 handle this by creating the required property (subscription_tier
> and plan respectively) as a setup step before creating the target group, and deleting it in teardown.

---

## POSITIVE TEST CASES

---

### FF-P01 — Full Boolean Flag Lifecycle: Create → Enable → Disable → Delete

**Discovery:** `Stress` | **Expected:** `flags_applications_list → flags_add → flags_get → flags_configurations_list → flag_configuration_get → flags_configuration_state_update → flags_flag_usage_per_environment → flags_configuration_state_update → flags_delete` | **Timeout:** `120s`

```
1. List all feature flag applications and confirm Auto-ASO-Application (e1903ba8-...) exists.
2. Create a Boolean flag named "ff-p01-bool-flag-DATE" with description "FF-P01 Boolean lifecycle test" in applicationId e1903ba8-9234-4ae2-ab5f-aa0962b5be2f.
3. Retrieve the flag by its ID — verify name, flagType=Boolean, isPermanent=false.
4. List all flag configurations for the application and environment cde9e350-... — find the new flag's config entry and verify enabled=false by default.
5. Get the specific configuration for the flagId and environmentId — verify enabled=false.
6. Enable the flag (set enabled=true) in environment cde9e350-.... Verify HTTP 200.
7. Check flag usage per environment — verify the call succeeds (usage will be empty since no SDK has evaluated it yet).
8. Disable the flag (set enabled=false).
9. Delete the flag. Verify success.
Report the result of every step.
```

---

### FF-P02 — Full String Flag Lifecycle Including Default Value Update

**Discovery:** `Stress` | **Expected:** `flags_add → flags_get_by_name → flags_configuration_state_update → flags_update_defaultValue → flag_configuration_get → flags_configuration_state_update → flags_delete` | **Timeout:** `120s`

```
1. Create a String type flag named "ff-p02-string-flag-DATE" in applicationId e1903ba8-... .
2. Get the flag by name — confirm flagType=String.
3. Enable the flag in environment cde9e350-... .
4. Update the flag's default value to "active" for the flagId and environmentId.
5. Get the configuration and verify the defaultValue has been updated to "active".
6. Disable the flag.
7. Delete the flag.
This specifically tests updating default value on a String flag (not Boolean) to confirm the tool works when used correctly.
```

---

### FF-P03 — Full Target Group Lifecycle With a Real Property Condition

**Discovery:** `Stress` | **Expected:** `flag_custom_properties_add → flag_target_groups_add → flag_target_groups_get → flag_target_groups_get_by_name → flag_target_groups_list → flag_target_groups_flag_usage_per_environment → flag_target_groups_list_with_flags_usage → flag_target_groups_target_group_usage → flag_target_groups_delete → flag_custom_properties_delete` | **Timeout:** `120s`

```
0. (Setup) Create a String custom property named "subscription_tier" in applicationId e1903ba8-... . Note the returned customPropertyId — this is required for the condition in step 1 to pass server-side property name validation. If the property already exists (409/400 duplicate), skip creation and proceed.
1. Create a target group named "ff-p03-beta-users-DATE" in applicationId e1903ba8-... with condition: {"property": {"name": "subscription_tier", "operator": "eq", "operands": ["beta"]}}.
2. Get the target group by its ID — verify conditions.property.name = "subscription_tier".
3. Get the target group by name — verify data matches get-by-id.
4. List all target groups — verify the new group appears in the list.
5. Check target group flag usage per environment — verify call succeeds (usage will be empty).
6. List all target groups with flags usage — verify the group appears with flagUsage=[].
7. Check target group usage — verify call succeeds (empty, no nesting).
8. Delete the target group — verify success.
9. (Teardown) Delete the "subscription_tier" custom property created in step 0. Skip if step 0 was skipped.
Report whether conditions were persisted correctly in steps 2 and 3.
```

---

### FF-P04 — Full Custom Properties Lifecycle Across All 3 Types

**Discovery:** `Stress` | **Expected:** `flag_custom_properties_add (×3) → flag_custom_properties_list → flag_custom_properties_get → flag_custom_properties_get_by_name → flag_custom_properties_flag_usage_per_environment → flag_custom_properties_target_group_usage → flag_custom_properties_delete (×3)` | **Timeout:** `120s`

```
1. Create a Boolean custom property named "ff-p04-bool-prop-DATE" in applicationId e1903ba8-... .
2. Create a String custom property named "ff-p04-string-prop-DATE".
3. Create a Number custom property named "ff-p04-number-prop-DATE".
4. List all custom properties — verify all 3 appear with their correct types.
5. Get the String property by its ID — verify type=String.
6. Get the String property by name "ff-p04-string-prop-DATE" — verify same data.
7. Check custom property flag usage per environment for the String property — verify call succeeds.
8. Check custom property target group usage for the String property — verify call succeeds.
9. Delete all 3 properties. Verify each deletion succeeds.
Report whether all 3 types were created with correct type fields.
```

---

### FF-P05 — List All Flags Across All Applications

**Discovery:** `Stress` | **Expected:** `flags_applications_list → flags_list (×N)` | **Timeout:** `90s`

```
List all feature flag applications for organizationId 6c5eeb79-... . For each application returned, list all flags. Build a complete inventory: application name, number of flags, flag names and types. Identify: which application has the most flags, which has zero flags, and how many flags exist in total across all applications. Report the full inventory table.
```

---

### FF-P06 — Get Flag by ID and by Name — Verify Data Consistency

**Discovery:** `Chain` | **Expected:** `flags_add → flags_get → flags_get_by_name → flags_delete` | **Timeout:** `60s`

```
Create a flag named "ff-p06-consistency-test-DATE" (Boolean) in applicationId e1903ba8-... . Capture the flagId from the response. Retrieve the flag by that flagId. Then retrieve the flag by its name. Compare every field in both responses: id, name, flagType, description, isPermanent, labels, cascUrl, resourceId. Verify they are identical. Delete the flag. Report any field that differs between the two responses.
```

---

### FF-P07 — ~~SDK Key Retrieval for All Environments~~ [REMOVED]
> **`flags_sdk_key_get` has been removed from the MCP server tool set. This test is permanently skipped.**

---

### FF-P08 — Flag Approval Requests List

**Discovery:** `Selection` | **Expected:** `flag_approval_requests_list` | **Timeout:** `15s`

```
List all pending flag approval requests for applicationId e1903ba8-9234-4ae2-ab5f-aa0962b5be2f. Verify the call succeeds without error. If the result is empty, document it as expected (no pending approvals). If requests exist, for each request report: flagId, environmentId, requester, requested change. Verify the response schema contains an items array (even if empty).
```

---

### FF-P09 — Target Group With Nested anyOf Conditions

**Discovery:** `Stress` | **Expected:** `flag_custom_properties_add → flag_target_groups_add → flag_target_groups_get → flag_target_groups_delete → flag_custom_properties_delete` | **Timeout:** `90s`

```
0. (Setup) Create a String custom property named "plan" in applicationId e1903ba8-... . Note the returned customPropertyId. If the property already exists (409/400 duplicate), skip creation and proceed.
1. Create a target group named "ff-p09-complex-condition-DATE" in applicationId e1903ba8-... with a complex nested condition:
{
  "anyOf": [
    {"property": {"name": "plan", "operator": "eq", "operands": ["premium"]}},
    {"property": {"name": "plan", "operator": "eq", "operands": ["enterprise"]}}
  ]
}
2. Retrieve the target group and verify the conditions were saved exactly as provided. Report the full conditions object from the response. Verify the anyOf array has exactly 2 entries.
3. Delete the target group.
4. (Teardown) Delete the "plan" custom property created in step 0. Skip if step 0 was skipped.
```

---

### FF-P10 — Flag Usage Per Environment After Flag Is Enabled

**Discovery:** `Chain` | **Expected:** `flags_add → flags_configuration_state_update → flags_flag_usage_per_environment → flags_configuration_state_update → flags_delete` | **Timeout:** `60s`

```
Create a Boolean flag named "ff-p10-usage-check-DATE" in applicationId e1903ba8-... . Enable it in environment cde9e350-... . Check its usage per environment. Verify: the call succeeds and returns an items array. Since no SDK has evaluated this flag in real-time, usage will likely be empty — document that as the expected result. Disable and delete the flag. This tests that the usage endpoint is functional even when usage is zero.
```

---

### FF-P11 — Set Targeting Conditions With a Property Rule and Verify Persistence

**Discovery:** `Stress` | **Expected:** `flag_custom_properties_add → flags_add → flag_target_groups_add → flag_configuration_conditions_set → flag_configuration_get → flag_target_groups_delete → flags_delete → flag_custom_properties_delete` | **Timeout:** `120s`

```
0. (Setup) Create a String custom property named "region" in applicationId e1903ba8-... . Note the returned customPropertyId. If it already exists, skip and proceed.
1. Create a Boolean flag named "ff-p11-conditions-set-DATE" in applicationId e1903ba8-... .
2. Create a target group named "ff-p11-eu-users-DATE" in applicationId e1903ba8-... with condition:
   {"property": {"name": "region", "operator": "eq", "operands": ["EU"]}}
3. Set targeting conditions on the flag for environmentId cde9e350-... using flag_configuration_conditions_set with the rule:
   [{"allOf": [{"group": {"id": "<targetGroupId>"}}], "flagValue": true}]
4. Get the flag configuration (flag_configuration_get) and verify the conditions array contains exactly the rule set in step 3.
5. (Teardown) Delete the target group, then delete the flag, then delete the "region" custom property.
Report the full conditions object returned in step 4. Verify the conditions were persisted as-is.
```

---

### FF-P12 — Serve a Value to a Target Group (enableIfDisabled=true)

**Discovery:** `Stress` | **Expected:** `flag_custom_properties_add → flags_add → flag_target_groups_add → flag_serve_to_target_group → flag_configuration_get → flag_target_groups_delete → flags_delete → flag_custom_properties_delete` | **Timeout:** `120s`

```
0. (Setup) Create a String custom property named "plan" in applicationId e1903ba8-... . If it already exists, skip and proceed.
1. Create a Boolean flag named "ff-p12-serve-tg-DATE" (flagType=Boolean) in applicationId e1903ba8-... .
2. Create a target group named "ff-p12-premium-users-DATE" in applicationId e1903ba8-... with condition:
   {"property": {"name": "plan", "operator": "eq", "operands": ["premium"]}}
3. Call flag_serve_to_target_group with:
   - flagId: the id from step 1
   - targetGroupId: the id from step 2
   - servedValue: true
   - enableIfDisabled: true
   - environmentId: cde9e350-...
   - applicationId: e1903ba8-...
4. Call flag_configuration_get for the flagId and environmentId. Verify:
   - enabled=true (because enableIfDisabled=true was passed)
   - conditions array contains a rule targeting the target group with flagValue=true
5. (Teardown) Delete the target group, flag, and custom property.
Report whether the targeting rule was appended correctly and whether enabled was flipped to true.
```

---

## NEGATIVE TEST CASES

---

### FF-N01 — Delete a Flag That Is Still Enabled (Known Behavior)

**Discovery:** `Chain` | **Expected:** `flags_add → flags_configuration_state_update → flags_delete → flags_configuration_state_update → flags_delete` | **Timeout:** `60s`

```
Create a Boolean flag named "ff-n01-delete-enabled-DATE". Enable it in environment cde9e350-... . Without disabling it first, attempt to delete the flag. Record the exact response: HTTP status code and error message. This is expected to fail with a 400 error (known behavior from Bug report). After confirming the error, disable the flag and delete it. Document: (1) the exact error when deleting an enabled flag, (2) whether disabling first resolves the issue.
```

---

### FF-N02 — Update Default Value on a Boolean Flag With a String Value

**Discovery:** `Chain` | **Expected:** `flags_add → flags_configuration_state_update → flags_update_defaultValue → flags_delete` | **Timeout:** `60s`

```
Create a Boolean flag named "ff-n02-bool-update-DATE". Enable it. Update its default value with defaultValue="true". Record the exact error response (expected: 400 Bad Request). Then try with defaultValue="false" — does it also fail? Document both attempts. Disable and delete the flag. Confirm whether Boolean flags can never have their default value updated or if there is a specific value format that works.
```

---

### FF-N03 — Create Flag With Duplicate Name in the Same Application

**Discovery:** `Chain` | **Expected:** `flags_add → flags_add → flags_delete` | **Timeout:** `45s`

```
Create a flag named "ff-n03-duplicate-name-DATE" in applicationId e1903ba8-... . Note the flagId returned. Attempt to create a second flag with the exact same name in the same application. Record the exact error response. Expected: 400 or 409 (conflict). After confirming the duplicate error, delete the first flag. Does the server return a descriptive error like "flag name already exists"?
```

---

### FF-N04 — Get Flag by Name That Does Not Exist

**Discovery:** `Selection` | **Expected:** `flags_get_by_name` | **Timeout:** `15s`

```
Look up a flag by name "this-flag-does-not-exist-xyz-999" in applicationId e1903ba8-... . Record the exact response. Expected: 404 not found. Does the server return a structured error object or a raw 404? Document the exact error message.
```

---

### FF-N05 — Delete Target Group With Non-Existent ID

**Discovery:** `Selection` | **Expected:** `flag_target_groups_delete` | **Timeout:** `15s`

```
Delete a target group with applicationId e1903ba8-... and a made-up id: 00000000-0000-0000-0000-000000000099. Record the exact response. Expected: 404 or 400. Document the HTTP status code and error message. Does the server confirm the group was not found?
```

---

### FF-N06 — Get Custom Property by Name That Does Not Exist

**Discovery:** `Selection` | **Expected:** `flag_custom_properties_get_by_name` | **Timeout:** `15s`

```
Look up a custom property by name "nonexistent-property-xyz-999" in applicationId e1903ba8-... . Record the exact response. Expected: 404. Document the full error response structure. Is the error message descriptive?
```

---

### FF-N07 — Enable Flag in Wrong Environment (Environment Not Linked to Application)

**Discovery:** `Chain` | **Expected:** `flags_add → flags_configuration_state_update → flags_delete` | **Timeout:** `60s`

```
Create a Boolean flag named "ff-n07-wrong-env-DATE" in applicationId e1903ba8-... . Try to enable it using an environment ID from a completely different application. Use environmentId 187aa467-52a0-48b4-b595-c5eb75de10ca (belongs to Auto-SLA-Test-App, not Auto-ASO-Application). Record the exact error. Does the server validate that the environment belongs to the application? Disable (if it somehow enabled) and delete the flag.
```

---

### FF-N08 — Create Flag With Empty Name

**Discovery:** `Selection` | **Expected:** `flags_add` | **Timeout:** `15s`

```
Attempt to create a feature flag with an empty string as the name: name="". Use applicationId e1903ba8-... and flagType=Boolean. Record the exact error. Expected: client-side validation error (name has minLength:1 in the schema) or server 400. Document whether the client catches this before sending to the server, or if it reaches the server.
```

---

### FF-N09 — Create Target Group With Invalid Condition Operator

**Discovery:** `Selection` | **Expected:** `flag_target_groups_add` | **Timeout:** `15s`

```
Attempt to create a target group named "ff-n09-bad-condition-DATE" in applicationId e1903ba8-... with an invalid operator in the condition:
{"property": {"name": "plan", "operator": "invalid_operator_xyz", "operands": ["beta"]}}
Record the exact error response. Expected: 400 with a message about invalid operator. Does the server list valid operators in the error? Clean up if the group was somehow created.
```

---

### FF-N10 — ~~Get SDK Key for Non-Existent Environment~~ [REMOVED]
> **`flags_sdk_key_get` has been removed from the MCP server tool set. This test is permanently skipped.**

---

### FF-N11 — Set Conditions Referencing a Non-Existent Custom Property Name

**Discovery:** `Chain` | **Expected:** `flags_add → flag_configuration_conditions_set → flags_delete` | **Timeout:** `45s`

```
Create a Boolean flag named "ff-n11-bad-conditions-DATE" in applicationId e1903ba8-... .
Call flag_configuration_conditions_set for the flagId and environmentId cde9e350-... with a rule that references a property name that does not exist in the application:
[{"allOf": [{"property": {"name": "nonexistent_property_xyz_999", "operator": "eq", "operands": ["beta"]}}], "flagValue": true}]
Record the exact HTTP status code and error message. Expected: 400 (property name not found / invalid condition).
Clean up: delete the flag.
Document whether the server validates property names at conditions-set time.
```

---

### FF-N12 — Serve Value to a Non-Existent Target Group Name

**Discovery:** `Chain` | **Expected:** `flags_add → flag_serve_to_target_group → flags_delete` | **Timeout:** `45s`

```
Create a Boolean flag named "ff-n12-serve-bad-tg-DATE" in applicationId e1903ba8-... .
Call flag_serve_to_target_group with:
- targetGroupName: "this-target-group-does-not-exist-xyz-999"
- servedValue: true
- environmentId: cde9e350-...
- applicationId: e1903ba8-...
Record the exact HTTP status code and error message. Expected: 404 (target group not found) or 400.
Clean up: delete the flag.
Document whether the tool resolves the name first and returns a descriptive error.
```

---

## EDGE CASES

---

### FF-E01 — Brand New Flag Has Correct Default Configuration State

**Discovery:** `Chain` | **Expected:** `flags_add → flag_configuration_get → flags_delete` | **Timeout:** `30s`

```
Create a Boolean flag named "ff-e01-default-state-DATE". Immediately get its configuration for environment cde9e350-... without enabling it first. Verify: enabled=false by default, defaultValue.valueWrittenInCode=true, variantsEnabled=false. This validates that a newly created flag has a sensible default configuration without any manual setup. Delete the flag.
```

---

### FF-E02 — Flag Enabled But Usage Is Still Empty (No SDK Evaluation Yet)

**Discovery:** `Chain` | **Expected:** `flags_add → flags_configuration_state_update → flags_flag_usage_per_environment → flags_configuration_state_update → flags_delete` | **Timeout:** `60s`

```
Create a Boolean flag "ff-e02-usage-empty-DATE". Enable it. Check its usage per environment. Verify: the response returns items=[] (empty — no SDK client has called this flag). This is the expected behavior for a newly enabled flag that no application has evaluated yet. Confirm the tool returns an empty list gracefully rather than an error. Disable and delete the flag.
```

---

### FF-E03 — Target Group With Empty anyOf Condition (Matches Nothing)

**Discovery:** `Chain` | **Expected:** `flag_target_groups_add → flag_target_groups_get → flag_target_groups_delete` | **Timeout:** `30s`

```
Create a target group named "ff-e03-empty-condition-DATE" with conditions={} (omit conditions entirely, let it default to anyOf:[]). Retrieve the target group and verify the saved conditions. Verify that conditions shows {"anyOf": []} as the default. Confirm the group was created successfully despite matching no users. Delete the group. This tests the schema default behavior for empty conditions.
```

---

### FF-E04 — Custom Property With All Optional Fields Populated

**Discovery:** `Chain` | **Expected:** `flag_custom_properties_add → flag_custom_properties_get → flag_custom_properties_delete` | **Timeout:** `30s`

```
Create a custom property named "ff-e04-full-fields-DATE" with all available fields:
- type: String
- description: "FF-E04 edge case test property"
- cascUrl: "https://example.com/casc/ff-e04"
- resourceId: "test-resource-id-123"
Retrieve the custom property and verify all fields are persisted correctly (especially cascUrl and resourceId). Delete the property.
```

---

### FF-E05 — List Target Groups When None Exist in an Application

**Discovery:** `Chain` | **Expected:** `flags_applications_list → flag_target_groups_list` | **Timeout:** `30s`

```
Find an application that has no existing target groups (check the applications list and pick an application other than Auto-ASO-Application). List all target groups for that applicationId. Verify: the response returns items=[] and not an error. This tests graceful empty-list handling. Report which application was used and confirm the response structure.
```

---

### FF-E06 — List Custom Properties When None Exist in an Application

**Discovery:** `Chain` | **Expected:** `flags_applications_list → flag_custom_properties_list` | **Timeout:** `30s`

```
Find an application that has no custom properties defined (pick a different app from Auto-ASO-Application). List all custom properties for that application. Verify: returns items=[] and not an error. Report which application was tested.
```

---

### FF-E07 — Flag Config State: Toggle Enable/Disable Multiple Times

**Discovery:** `Stress` | **Expected:** `flags_add → flags_configuration_state_update (×4) → flag_configuration_get (×4) → flags_delete` | **Timeout:** `120s`

```
Create a Boolean flag "ff-e07-toggle-test-DATE". Perform the following toggle sequence:
1. Enable → get configuration → verify enabled=true
2. Disable → get configuration → verify enabled=false
3. Enable again → get configuration → verify enabled=true
4. Disable again → get configuration → verify enabled=false
Verify: each toggle succeeds with HTTP 200 and each verification reflects the correct state. Delete the flag. This tests idempotency and state consistency of the state update endpoint.
```

---

### FF-E08 — Create Flag With Labels and isPermanent=true

**Discovery:** `Chain` | **Expected:** `flags_add → flags_get → flags_delete` | **Timeout:** `45s`

```
Create a Boolean flag named "ff-e08-permanent-labeled-DATE" with:
- labels: ["test", "permanent", "mcp-edge-case"]
- isPermanent: true
Retrieve the flag and verify: labels array contains all 3 labels, isPermanent=true. Attempt to delete the flag — does isPermanent=true block deletion? Record the response. If deletion is blocked, note it as expected behavior. If it deletes successfully, note that isPermanent does not prevent deletion via API.
```

---

### FF-E09 — Cross-Check: Target Group List With Usage vs List Without Usage

**Discovery:** `Chain` | **Expected:** `flag_target_groups_add → flag_target_groups_list → flag_target_groups_list_with_flags_usage → flag_target_groups_delete` | **Timeout:** `60s`

```
Create a target group "ff-e09-cross-check-DATE". List all target groups — note the fields returned (id, name, conditions). List all target groups with flags usage — note the additional fields (flagUsage, updated timestamp). Verify: both calls return the same group. The with-flags-usage response should have a flagUsage field (empty array). Compare the two responses field by field. Report any field present in one but not the other. Delete the group.
```

---

### FF-E10 — Delete Flag That Was Never Enabled

**Discovery:** `Chain` | **Expected:** `flags_add → flags_delete` | **Timeout:** `30s`

```
Create a Boolean flag "ff-e10-never-enabled-DATE". Do NOT enable it — leave it in its default disabled state. Immediately delete it. Verify: deletion succeeds with HTTP 200. This tests the specific condition for the known behavior that "flags must be disabled before deletion" — if the flag was never enabled (enabled=false by default), it should delete without any extra steps. Report whether this works or requires an explicit disable call even for flags that were never enabled.
```

---

### FF-E11 — Clear All Targeting Conditions by Setting Empty Array

**Discovery:** `Chain` | **Expected:** `flags_add → flag_configuration_conditions_set → flag_configuration_conditions_set → flag_configuration_get → flags_delete` | **Timeout:** `60s`

```
Create a Boolean flag "ff-e11-clear-conditions-DATE" in applicationId e1903ba8-... .
Set a targeting condition on the flag for environmentId cde9e350-... :
[{"allOf": [{"property": {"name": "plan", "operator": "eq", "operands": ["beta"]}}], "flagValue": true}]
(Use the "plan" custom property if it exists, or any valid property in the application. If no valid property exists, create one first and clean up after.)
Then immediately call flag_configuration_conditions_set again with an empty array: []
Call flag_configuration_get and verify conditions=[] (all targeting rules cleared).
Delete the flag. This confirms that passing [] is a valid way to reset all targeting rules to none.
```

---

### FF-E12 — Serve to Target Group by Name (Name Resolution Path)

**Discovery:** `Chain` | **Expected:** `flag_custom_properties_add → flags_add → flag_target_groups_add → flag_serve_to_target_group (by name) → flag_configuration_get → flag_target_groups_delete → flags_delete → flag_custom_properties_delete` | **Timeout:** `90s`

```
0. (Setup) Create a String custom property named "tier" in applicationId e1903ba8-... . If it already exists, skip and proceed.
1. Create a Boolean flag "ff-e12-serve-by-name-DATE" in applicationId e1903ba8-... .
2. Create a target group named "ff-e12-beta-tg-DATE" in applicationId e1903ba8-... with condition:
   {"property": {"name": "tier", "operator": "eq", "operands": ["beta"]}}
3. Call flag_serve_to_target_group using targetGroupName: "ff-e12-beta-tg-DATE" (NOT targetGroupId) with:
   - servedValue: true
   - enableIfDisabled: false
   - environmentId: cde9e350-...
   - applicationId: e1903ba8-...
4. Call flag_configuration_get and verify the conditions array includes a rule for the resolved target group.
5. (Teardown) Delete the target group, flag, and custom property.
This tests that the tool correctly resolves a target group name to its UUID and appends the targeting rule without requiring the caller to look up the ID manually.
```
