# Domain: Orgs & Teams
**Tools covered (22):** `user_whoami`, `user_preferences_get`, `user_set_timezone`, `users_list`, `users_get`, `users_get_by_id`, `teams_create`, `teams_delete`, `teams_get`, `teams_get_by_id`, `teams_invite_create`, `teams_invite_delete`, `teams_invites_list`, `teams_members_add`, `teams_members_remove`, `teams_memberships_list`, `organizations_search`, `organizations_list_suborganizations`, `organizations_suborg_report`, `organizations_list`, `organizations_get`, `organizations_create`
**Total prompts:** 33 (11 positive, 11 negative, 11 edge cases)

---

## Test Execution Tracker

| ID | Type | Category | Expected Tools | Timeout | Status | Notes |
|----|------|----------|----------------|---------|--------|-------|
| OT-P01 | Positive | Selection | `user_whoami` | 15s | ⬜ | |
| OT-P02 | Positive | Chain | `user_whoami → user_preferences_get` | 30s | ⬜ | |
| OT-P03 | Positive | Selection | `users_list` | 15s | ⬜ | |
| OT-P04 | Positive | Chain | `users_list → users_get → users_get_by_id` | 30s | ⬜ | |
| OT-P05 | Positive | Chain | `organizations_search → organizations_list_suborganizations` | 30s | ⬜ | |
| OT-P06 | Positive | Stress | `users_list → teams_create → teams_invite_create → teams_invites_list → teams_invite_delete → teams_members_add → teams_get_by_id → teams_delete` | 120s | ⬜ | |
| OT-P07 | Positive | Chain | `teams_create → teams_members_add → teams_memberships_list → teams_delete` | 60s | ⬜ | |
| OT-P08 | Positive | Stress | `organizations_suborg_report (×4)` | 60s | ⬜ | |
| OT-P09 | Positive | Chain | `user_whoami → user_set_timezone → user_preferences_get` | 30s | ⬜ | |
| OT-P10 | Positive | Chain | `organizations_create → organizations_get → organizations_list_suborganizations` | 45s | ⬜ | |
| OT-P11 | Positive | Chain | ~~`organizations_mark_internal → organizations_get`~~ | — | ⬛ | Tool removed |
| OT-P12 | Positive | Chain | `organizations_list → organizations_list (nested=true)` | 30s | ⬜ | |
| OT-N01 | Negative | Chain | `users_get → users_get_by_id` | 30s | ⬜ | |
| OT-N02 | Negative | Selection | `teams_create` | 15s | ⬜ | |
| OT-N03 | Negative | Chain | `teams_create → teams_invite_create → teams_delete` | 45s | ⬜ | |
| OT-N04 | Negative | Selection | `teams_members_add` | 15s | ⬜ | |
| OT-N05 | Negative | Selection | `teams_delete` | 15s | ⬜ | |
| OT-N06 | Negative | Stress | `teams_create → teams_members_add → teams_get_by_id → teams_members_remove → teams_get_by_id → teams_delete` | 90s | ⬜ | |
| OT-N07 | Negative | Selection | `organizations_search` | 15s | ⬜ | |
| OT-N08 | Negative | Chain | `user_set_timezone (×3)` | 30s | ⬜ | |
| OT-N09 | Negative | Selection | `organizations_suborg_report` | 15s | ⬜ | |
| OT-N10 | Negative | Selection | `organizations_create` | 15s | ⬜ | |
| OT-N11 | Negative | Selection | ~~`organizations_flag_malicious`~~ | — | ⬛ | Tool removed |
| OT-N12 | Negative | Selection | `organizations_get` | 15s | ⬜ | |
| OT-E01 | Edge | Selection | `user_preferences_get` | 15s | ⬜ | |
| OT-E02 | Edge | Chain | `teams_create → teams_delete → teams_get` | 30s | ⬜ | |
| OT-E03 | Edge | Chain | `teams_create → teams_invite_create (×2) → teams_invites_list → teams_delete` | 60s | ⬜ | |
| OT-E04 | Edge | Chain | `teams_get → users_list` | 30s | ⬜ | |
| OT-E05 | Edge | Chain | `organizations_search → organizations_list_suborganizations` | 30s | ⬜ | |
| OT-E06 | Edge | Selection | `organizations_list_suborganizations` | 15s | ⬜ | |
| OT-E07 | Edge | Chain | `users_list → users_get → users_get_by_id` | 30s | ⬜ | |
| OT-E08 | Edge | Chain | `teams_create → teams_invite_create → teams_invites_list → teams_delete` | 60s | ⬜ | |
| OT-E09 | Edge | Stress | `organizations_suborg_report (×7)` | 90s | ⬜ | |
| OT-E10 | Edge | Chain | `organizations_create → organizations_get → organizations_list → organizations_list_suborganizations` | 60s | ⬜ | |
| OT-E11 | Edge | Chain | `organizations_list → organizations_list (nested=true)` | 30s | ⬜ | |
| OT-E12 | Edge | Chain | ~~`organizations_flag_malicious → organizations_get`~~ | — | ⬛ | Tool removed |

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

### OT-P01 — Verify Identity: whoami Returns Correct User Profile
**Discovery:** `Selection` | **Expected:** `user_whoami` | **Timeout:** `15s`

```
Who am I? Show me my current identity. Verify the response contains:
- email: cbp-qa-automation+aspmautomation@beescloud.com
- name: aspm automation
- selected_organization: aspm automation organization
Report the full response. Confirm all three fields match expected values exactly. This is the auth baseline check — if this fails, no other tests can run.
```

---

### OT-P02 — Get User Preferences for Current User
**Discovery:** `Chain` | **Expected:** `user_whoami → user_preferences_get` | **Timeout:** `30s`

```
First confirm my identity to get my userId (f3039d4a-7c3a-11f0-9a1c-42010a83ae54). Then retrieve my user preferences. Verify the response contains at least the following preferences: "theme" (value should be "dark"), "onboardingComplete" (bool=true), "jenkinsControllerComplete" (bool=true). Report all preferences returned including their names, types, and values. Confirm the structure has: name, bool/string/int fields, isSecret=false for all preferences.
```

---

### OT-P03 — List All Users and Verify Count and Structure
**Discovery:** `Selection` | **Expected:** `users_list` | **Timeout:** `15s`

```
List all users in the organization without any filters. Verify:
- Returns an items array with at least 5 users
- Each user has: id, email, displayname, status, type, mfaEnabled fields
- All returned users have status=USER_STATUS_ACTIVE
- At least one user has type=USER_TYPE_PERSON
Report: total user count, list of all display names and emails, and whether any user has mfaEnabled=true.
```

---

### OT-P04 — Get User by ID and Verify It Matches the List Result
**Discovery:** `Chain` | **Expected:** `users_list → users_get → users_get_by_id` | **Timeout:** `30s`

```
List all users and find the user "Chitra Perumal" (id: 5da6d58e-4897-11ed-9056-42010a83ae66). Then look up that user by their ID using both available user lookup methods. Compare all fields between:
1. The user object from the user listing
2. The response from looking up the user by search/email
3. The response from looking up the user directly by ID
Verify all three return identical data for the same user. Report any field that differs between the three sources.
```

---

### OT-P05 — Full Organization Hierarchy Traversal
**Discovery:** `Chain` | **Expected:** `organizations_search → organizations_list_suborganizations` | **Timeout:** `30s`

```
Search for organizations matching "aspm*". Confirm aspm-automation-organization appears (id: 6c5eeb79-...). Then list all sub-organizations to get the full sub-org tree. Map the hierarchy using the parentId field:
- Level 0: 6c5eeb79-... (aspm-automation-organization, parentId=00000000-...)
- Level 1: direct children of 6c5eeb79-...
- Level 2: children of level 1 orgs
- Level 3+: deeper nodes

Report: total sub-org count, max depth, number of leaf nodes (orgs with no children), and draw the hierarchy tree with org names and IDs.
```

---

### OT-P06 — Full Team Lifecycle: Create → Invite → Members Add → Get → Delete
**Discovery:** `Stress` | **Expected:** `users_list → teams_create → teams_invite_create → teams_invites_list → teams_invite_delete → teams_members_add → teams_get_by_id → teams_delete` | **Timeout:** `120s`

```
1. List all users and find Srividhya Varadhan (id: 19665a40-60d2-11ed-b20c-42010a83ae66, email: svaradhan@cloudbees.com).
2. Create a new team named "ot-p06-lifecycle-team-20260615".
3. Create an invite for svaradhan@cloudbees.com to the team. Record inviteId.
4. List the pending invites for that team — verify the invite appears.
5. Delete the invite. Verify success.
6. Add Srividhya as a direct member using her userId.
7. Get the team by its ID and verify her userId appears in the userIds array.
8. Delete the team.
Report the result of every step.
```

---

### OT-P07 — teams_memberships_list Returns 501
**Discovery:** `Chain` | **Expected:** `teams_create → teams_members_add → teams_memberships_list → teams_delete` | **Timeout:** `60s`

```
Create a team named "ot-p07-memberships-test-20260615". Add user Menaga QAUser (id: e4ada4c4-28de-11f1-8837-42010a83ae62) as a member. Then list team memberships for that team. Record the exact response — expected: 501 Not Implemented. Also confirm: the tool is listed in the MCP server's tool manifest, meaning it is exposed but not implemented. Delete the team. Document: exact error message, whether the 501 has changed from the last test run, and whether any workaround is possible (e.g., getting the team by ID to see userIds instead).
```

---

### OT-P08 — Org Sub-Report for Multiple Widget IDs
**Discovery:** `Stress` | **Expected:** `organizations_suborg_report (×4)` | **Timeout:** `60s`

```
For organizationId 6c5eeb79-4606-4c39-bd5c-c2323336caad and subOrganizationId 5b363812-7ec6-46a9-990c-56fc50a23cb9 (aspm-automation-sub-org), get the sub-organization report for each widget ID: ci1, ci2, ci3, ci4. Report: the title and data returned for each widget. Note which widgets return data vs empty data vs errors.
```

---

### OT-P09 — Set Timezone With Valid IANA Format
**Discovery:** `Chain` | **Expected:** `user_whoami → user_set_timezone → user_preferences_get` | **Timeout:** `30s`

```
Confirm my identity. Then set my timezone to "America/New_York". Record the response — is it a success or failure? If it succeeds, get my user preferences to verify the timezone preference was updated. If it fails with 400, try "Asia/Kolkata" and "Europe/London" as alternatives. Document which IANA timezone format (if any) the server accepts.
```

---

### OT-P10 — Create a Sub-Organization Under the Root Org
**Discovery:** `Chain` | **Expected:** `organizations_create → organizations_get → organizations_list_suborganizations` | **Timeout:** `45s`

```
Create a new organization with:
- displayName: "ot-p10-test-suborg-20260615"
- domainName: "ot-p10-test-suborg-20260615" (use today's date for uniqueness)
- parentId: 6c5eeb79-4606-4c39-bd5c-c2323336caad

Record the returned org id. Then retrieve that organization by its ID and verify:
- displayName matches what was specified
- parentId = 6c5eeb79-4606-4c39-bd5c-c2323336caad
- Organization appears in the sub-organizations list under the root

Report the full response. Note: clean-up of this test org may need to be done manually if no delete tool exists.
```

---

### OT-P11 — ~~Mark a Sub-Organization as Internal~~ [REMOVED]
> **`organizations_mark_internal` has been removed from the MCP server tool set. This test is permanently skipped.**

---

### OT-P12 — List All Accessible Organizations
**Discovery:** `Chain` | **Expected:** `organizations_list → organizations_list (nested=true)` | **Timeout:** `30s`

```
List all organizations accessible to the current user without any filters. Verify:
- Returns an items/array with at least 1 organization
- Each org has: id, displayName, domainName fields
- The root org (aspm-automation-organization, id: 6c5eeb79-...) appears in the results
- Each org has a parentId field (null or zero-UUID for root orgs)
Then list organizations with nested=true and compare the count to the flat list. Report: total org count (flat), total org count (nested), and whether the root org's sub-orgs appear as nested children.
```

---

## NEGATIVE TEST CASES

---

### OT-N01 — Get User by Non-Existent userId
**Discovery:** `Chain` | **Expected:** `users_get → users_get_by_id` | **Timeout:** `30s`

```
Look up a user by the non-existent ID: 00000000-0000-0000-0000-000000000099. Try both user lookup methods (by search and by ID). Record the exact error from each. Expected: 404 not found. Are the error messages from both methods identical? Document the HTTP status code and error structure returned by each.
```

---

### OT-N02 — Create Team With Empty Name
**Discovery:** `Selection` | **Expected:** `teams_create` | **Timeout:** `15s`

```
Attempt to create a team with name="" (empty string). Record the exact error. Expected: client-side schema validation (name is required) or server-side 400. Does the client catch this before sending to the server, or does the call reach the API? Document the full error response.
```

---

### OT-N03 — Invite User With Invalid Email Format
**Discovery:** `Chain` | **Expected:** `teams_create → teams_invite_create → teams_delete` | **Timeout:** `45s`

```
Create a temporary team named "ot-n03-invalid-invite-20260615". Attempt to invite a user with an invalid email: "not-a-valid-email". Record the exact error. Expected: 400 bad request with email validation error. Delete the team. Document: does the server validate email format? What is the exact error message?
```

---

### OT-N04 — Add Member to Non-Existent Team
**Discovery:** `Selection` | **Expected:** `teams_members_add` | **Timeout:** `15s`

```
Attempt to add a member to a non-existent team (teamId: 00000000-0000-0000-0000-000000000099) with a valid userId: e4ada4c4-28de-11f1-8837-42010a83ae62. Record the exact error response. Expected: 404 (team not found) or 400. Document the HTTP status code and error message.
```

---

### OT-N05 — Delete Team That Does Not Exist
**Discovery:** `Selection` | **Expected:** `teams_delete` | **Timeout:** `15s`

```
Attempt to delete a non-existent team (teamId: 00000000-0000-0000-0000-000000000099). Record the exact error. Expected: 404 or 400. Is the error message descriptive (e.g., "team not found")? Document the full response.
```

---

### OT-N06 — Remove Member From Team
**Discovery:** `Stress` | **Expected:** `teams_create → teams_members_add → teams_get_by_id → teams_members_remove → teams_get_by_id → teams_delete` | **Timeout:** `90s`

```
Create a team named "ot-n06-remove-bug-20260615". Add Chitra Perumal (id: 5da6d58e-4897-11ed-9056-42010a83ae66) as a member. Verify she appears in the team's user list by retrieving the team by ID. Attempt to remove her from the team. Record the exact error response — expected: 400 Bad Request. Delete the team. Document: (1) exact error received, (2) whether the error changed from the previous reproduction run, (3) whether the user is removed despite the error (check the team again after the failed remove).
```

---

### OT-N07 — Organization Search With No Matching Results
**Discovery:** `Selection` | **Expected:** `organizations_search` | **Timeout:** `15s`

```
Search for an organization with query "zzz-this-org-does-not-exist-xyz". Record the response. Expected: empty items array (not an error). Verify the response structure is consistent with a normal search response (same schema, just empty). Document whether the server returns an empty list gracefully or throws a 404.
```

---

### OT-N08 — Set Timezone With Invalid Format
**Discovery:** `Chain` | **Expected:** `user_set_timezone (×3)` | **Timeout:** `30s`

```
Set my timezone to "UTC". Record the exact error (expected: 400 Bad Request). Then try "utc" (lowercase). Then try "GMT". Record all three responses. This investigates what exact format the server rejects and whether there is a pattern. Document each attempt and its result.
```

---

### OT-N09 — Suborg Report With Invalid Widget ID
**Discovery:** `Selection` | **Expected:** `organizations_suborg_report` | **Timeout:** `15s`

```
Get the sub-organization report for organizationId 6c5eeb79-4606-4c39-bd5c-c2323336caad, subOrganizationId 5b363812-7ec6-46a9-990c-56fc50a23cb9, and widgetId "ci99" (non-existent widget). Record the exact response. Expected: 400 or 404 with "widget not found". Does the server return a descriptive error? Document the full error response.
```

---

### OT-N10 — Create Organization With Duplicate domainName
**Discovery:** `Selection` | **Expected:** `organizations_create` | **Timeout:** `15s`

```
Attempt to create a new organization with a domainName that already exists:
- displayName: "ot-n10-duplicate-test"
- domainName: "aspm-automation-organization" (this domainName already exists)
- parentId: 6c5eeb79-4606-4c39-bd5c-c2323336caad

Record the exact error. Expected: 400 or 409 (conflict). Does the server return a descriptive error like "domainName already in use"? Document the full error response.
```

---

### OT-N11 — ~~Flag a Non-Existent Organization as Malicious~~ [REMOVED]
> **`organizations_flag_malicious` has been removed from the MCP server tool set. This test is permanently skipped.**

---

### OT-N12 — Get Organization With Invalid Org ID
**Discovery:** `Selection` | **Expected:** `organizations_get` | **Timeout:** `15s`

```
Retrieve the organization with id: 00000000-0000-0000-0000-000000000099. Record the exact error response. Expected: 404 not found. Document the HTTP status code and error message returned.
```

---

## EDGE CASES

---

### OT-E01 — User Preferences Returns All Known Preference Keys
**Discovery:** `Selection` | **Expected:** `user_preferences_get` | **Timeout:** `15s`

```
Get user preferences for userId f3039d4a-7c3a-11f0-9a1c-42010a83ae54. Verify the response contains exactly these preference keys: "theme", "onboardingComplete", "jenkinsControllerComplete", "jenkinsBulkComponentControllerComplete". Are there any additional preference keys? Do any preferences have isSecret=true? Are there any preferences with non-empty resourceId? Report the complete list of all preference entries.
```

---

### OT-E02 — Create Team Then Immediately Delete It (Empty Team)
**Discovery:** `Chain` | **Expected:** `teams_create → teams_delete → teams_get` | **Timeout:** `30s`

```
Create a team named "ot-e02-immediate-delete-20260615". Do not add any members or invites. Immediately delete that team. Verify: deletion succeeds without error. List all teams to confirm it no longer appears. This tests that an empty team can be deleted without any preconditions.
```

---

### OT-E03 — Invite the Same User Twice to the Same Team
**Discovery:** `Chain` | **Expected:** `teams_create → teams_invite_create (×2) → teams_invites_list → teams_delete` | **Timeout:** `60s`

```
Create a team named "ot-e03-duplicate-invite-20260615". Invite svaradhan@cloudbees.com once (record inviteId1). Immediately invite the same email again (record inviteId2 if different). List invites for the team. How many invites appear? Does the server allow duplicate invites for the same email, return an error, or silently deduplicate? Document the behavior. Clean up all invites and delete the team.
```

---

### OT-E04 — List All Teams Shows Both Predefined and User-Defined Teams
**Discovery:** `Chain` | **Expected:** `teams_get → users_list` | **Timeout:** `30s`

```
List all teams in the organization without any filters. Verify:
- Returns teams of both type=PREDEFINED and type=USERDEFINED
- PREDEFINED teams include "Admins (System)" and "All users for organization" and "Users (System)"
- PREDEFINED teams have isDefault=true or immutable=false
Report: total team count, how many are PREDEFINED vs USERDEFINED, and list all PREDEFINED team names. Verify that the "All users for organization" team contains all user IDs from the users list.
```

---

### OT-E05 — Organization Search With Wildcard Returns All Orgs
**Discovery:** `Chain` | **Expected:** `organizations_search → organizations_list_suborganizations` | **Timeout:** `30s`

```
Search for organizations with query "*" (wildcard). Verify: returns all organizations. Compare the count to the result of listing all sub-organizations. Are the counts consistent? Report total orgs from each approach and any organizations that appear in one but not the other. This validates that search and list are backed by the same data source.
```

---

### OT-E06 — Verify Parent-Child Hierarchy Is Correct in Sub-Org List
**Discovery:** `Selection` | **Expected:** `organizations_list_suborganizations` | **Timeout:** `15s`

```
List all sub-organizations. For each sub-org, record its id and parentId. Build the full tree:
- Find the root org (parentId = 00000000-0000-0000-0000-000000000000)
- Find all direct children of the root
- Find all grandchildren
Verify: every parentId in the list points to an id that also exists in the list (no dangling references). Report any org whose parentId does not match any other org's id. Report the maximum depth of the tree.
```

---

### OT-E07 — Both User Lookup Methods Return Identical Data
**Discovery:** `Chain` | **Expected:** `users_list → users_get → users_get_by_id` | **Timeout:** `30s`

```
Pick Pandurang Parchande (id: 6f116be6-7d9f-11f0-bfb9-42010a83ae54) from the user list. Look up that user using both available methods: by search/email and by direct ID lookup. Compare every field in both responses. Verify: all fields are identical. If any field differs, document what differs and whether it is a bug or expected (e.g., a timestamp that changes on read). This tests that the two user retrieval methods are truly equivalent.
```

---

### OT-E08 — Invite a User Who Is Already a Member of the Org
**Discovery:** `Chain` | **Expected:** `teams_create → teams_invite_create → teams_invites_list → teams_delete` | **Timeout:** `60s`

```
Create a team named "ot-e08-existing-user-invite-20260615". Invite aspm automation (cbp-qa-automation+aspmautomation@beescloud.com) — this user is already a member of the organization. Does the server allow sending an invite to an existing org member? Does it return an error, send the invite anyway, or auto-accept? Record the response. List invites for that team to see if the invite appears. Clean up invites and delete the team.
```

---

### OT-E09 — Suborg Report With All Widget IDs ci1–ci7
**Discovery:** `Stress` | **Expected:** `organizations_suborg_report (×7)` | **Timeout:** `90s`

```
For organizationId 6c5eeb79-4606-4c39-bd5c-c2323336caad and subOrganizationId 5b363812-7ec6-46a9-990c-56fc50a23cb9 (aspm-automation-sub-org), get the sub-organization report for every widget ID: ci1, ci2, ci3, ci4, ci5, ci6, ci7. For each: report the widget title, whether data is present, and any error. Identify which widget IDs are valid and which return errors. Build a table of widgetId → title → data status. This maps the full set of available CI report widgets.
```

---

### OT-E10 — Create Org → Get Org → List Orgs — Verify New Org Appears Immediately
**Discovery:** `Chain` | **Expected:** `organizations_create → organizations_get → organizations_list → organizations_list_suborganizations` | **Timeout:** `60s`

```
Create a sub-org named "ot-e10-visibility-test-20260615" (domainName: "ot-e10-visibility-test-20260615", parentId: 6c5eeb79-4606-4c39-bd5c-c2323336caad). Record the returned id. Immediately retrieve that organization by its ID — verify it returns the new org. Then list all organizations and verify the new org appears in the results. Then list sub-organizations and verify it appears there too. Report whether all three views are consistent. This tests the consistency of the create → read path.
```

---

### OT-E11 — List Organizations With nested=true vs nested=false
**Discovery:** `Chain` | **Expected:** `organizations_list → organizations_list (nested=true)` | **Timeout:** `30s`

```
List all organizations with nested=false (or omit the parameter). Note the total item count and verify each item is a flat org object with no children array. Then list organizations with nested=true. Note the total count and verify that root-level orgs contain a children or subOrganizations array with their sub-orgs. Compare: does nested=true return a different count than nested=false? Report the structure of the response under both modes.
```

---

### OT-E12 — ~~Flag Organization as Malicious Then Verify Flag Is Reflected~~ [REMOVED]
> **`organizations_flag_malicious` has been removed from the MCP server tool set. This test is permanently skipped.**
