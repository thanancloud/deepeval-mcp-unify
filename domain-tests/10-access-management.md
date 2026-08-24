# Domain: Access Management
**Tools covered (26):** `api_tokens_list`, `rbac_authorization_check_bulk`, `rbac_authorization_create`, `rbac_authorizations_list`, `rbac_permissions_list`, `rbac_role_create`, `rbac_role_delete`, `rbac_role_get`, `rbac_roles_list`, `saml_connections_list`, `saml_email_domains_list`, `teams_create`, `teams_delete`, `teams_get`, `teams_get_by_id`, `teams_invite_create`, `teams_invite_delete`, `teams_invites_list`, `teams_members_add`, `teams_members_remove`, `teams_memberships_list`, `user_preferences_get`, `user_set_timezone`, `users_get`, `users_get_by_id`, `users_list`
**Total prompts:** 30 (10 positive, 10 negative, 10 edge)

> **Cross-domain tools used for setup:** `user_whoami` (default), `organizations_list` (default), `organizations_list_suborganizations` (default)

---

## Test Execution Tracker

| ID | Type | Category | Expected Tools | Timeout | Status | Notes |
|----|------|----------|----------------|---------|--------|-------|
| AM-P01 | Positive | Selection | `user_whoami` → `user_preferences_get` | 20s | ⬜ | |
| AM-P02 | Positive | Chain | `user_whoami` → `users_get` → `users_get_by_id` | 30s | ⬜ | |
| AM-P03 | Positive | Selection | `organizations_list` → `users_list` | 20s | ⬜ | |
| AM-P04 | Positive | Chain | `organizations_list` → `teams_get` → `teams_get_by_id` | 30s | ⬜ | |
| AM-P05 | Positive | Stress | `organizations_list` → `teams_create` → `teams_invite_create` → `teams_invites_list` → `teams_invite_delete` → `teams_delete` | 120s | ⬜ | |
| AM-P06 | Positive | Stress | `organizations_list` → `users_list` → `teams_create` → `teams_members_add` → `teams_memberships_list` → `teams_members_remove` → `teams_delete` | 120s | ⬜ | |
| AM-P07 | Positive | Selection | `user_whoami` → `api_tokens_list` | 20s | ⬜ | |
| AM-P08 | Positive | Chain | `organizations_list` → `rbac_roles_list` → `rbac_role_get` | 30s | ⬜ | |
| AM-P09 | Positive | Stress | `organizations_list` → `rbac_role_create` → `rbac_role_get` → `rbac_authorizations_list` → `rbac_role_delete` | 90s | ⬜ | |
| AM-P10 | Positive | Chain | `organizations_list` → `rbac_permissions_list` → `rbac_authorization_check_bulk` | 45s | ⬜ | |
| AM-P11 | Positive | Selection | `organizations_list` → `saml_connections_list` | 20s | ⬜ | |
| AM-P12 | Positive | Chain | `organizations_list` → `saml_connections_list` → `saml_email_domains_list` | 30s | ⬜ | |
| AM-N01 | Negative | Selection | `users_get` (bad email) | 15s | ⬜ | |
| AM-N02 | Negative | Selection | `users_get_by_id` (nil ID) | 15s | ⬜ | |
| AM-N03 | Negative | Selection | `teams_create` (empty name) | 15s | ⬜ | |
| AM-N04 | Negative | Selection | `teams_delete` (nil ID) | 15s | ⬜ | |
| AM-N05 | Negative | Chain | `organizations_list` → `teams_create` → `teams_invite_create` (bad email) → `teams_delete` | 45s | ⬜ | |
| AM-N06 | Negative | Selection | `teams_members_add` (nil user ID) | 15s | ⬜ | |
| AM-N07 | Negative | Selection | `rbac_role_get` (nil ID) | 15s | ⬜ | |
| AM-N08 | Negative | Selection | `rbac_role_create` (empty name) | 15s | ⬜ | |
| AM-N09 | Negative | Selection | `rbac_role_delete` (nil ID) | 15s | ⬜ | |
| AM-N10 | Negative | Selection | `user_set_timezone` (invalid timezone) | 15s | ⬜ | |
| AM-E01 | Edge | Chain | `organizations_list` → `teams_create` → `teams_delete` → `teams_get_by_id` | 45s | ⬜ | |
| AM-E02 | Edge | Chain | `organizations_list` → `teams_create` → `teams_invite_create` ×2 → `teams_invites_list` → `teams_delete` | 60s | ⬜ | |
| AM-E03 | Edge | Chain | `organizations_list` → `rbac_role_create` → `rbac_authorizations_list` → `rbac_role_delete` | 60s | ⬜ | |
| AM-E04 | Edge | Selection | `organizations_list` → `teams_get` (empty org / no teams) | 20s | ⬜ | |
| AM-E05 | Edge | Chain | `organizations_list` → `rbac_authorization_check_bulk` (mix of valid + nonexistent roles) | 30s | ⬜ | |
| AM-E06 | Edge | Chain | `user_whoami` → `user_set_timezone` → `user_preferences_get` (verify timezone updated) | 45s | ⬜ | |
| AM-E07 | Edge | Stress | `organizations_list` → `users_list` → `teams_create` → `teams_invite_create` ×2 → `teams_members_add` → `teams_memberships_list` → `teams_members_remove` → `teams_invite_delete` ×2 → `teams_delete` | 150s | ⬜ | |
| AM-E08 | Edge | Chain | `organizations_list` → `rbac_role_create` → `rbac_role_create` (duplicate name) → `rbac_role_delete` | 60s | ⬜ | |
| AM-E09 | Edge | Chain | `organizations_list` → `rbac_permissions_list` → `rbac_role_create` → `rbac_authorization_create` → `rbac_authorizations_list` → `rbac_role_delete` | 90s | ⬜ | |
| AM-E10 | Edge | Chain | `organizations_list` → `teams_invites_list` (team with no invites) | 20s | ⬜ | |

---

## Diagnostic Categories

| Category | Definition | Failure Indicates |
|----------|-----------|-------------------|
| **Selection** | Single tool call from natural language | AI picked the wrong tool from 131 options |
| **Chain** | 2–4 tools called in sequence | Wrong tool order, missed step, or incorrect data passed between steps |
| **Stress** | 5+ tools OR repeated calls OR large payloads | Timeout, session limit, or token exhaustion |

---

## Test Setup

> Resolve all IDs at runtime. Call `user_whoami` first to get your userId and org context.
> Call `organizations_list` to get the current org ID before tests that require it.
> Nil UUID for negative tests: `00000000-0000-0000-0000-000000000099`

---

## POSITIVE TEST CASES

---

### AM-P01 — Get Current User Profile and Preferences
**Discovery:** `Chain` | **Expected:** `user_whoami → user_preferences_get` | **Timeout:** `20s`

```
Who am I on CloudBees? Call user_whoami to get my full profile (userId, email, name, selected organization).
Then use that userId to retrieve my user preferences. Report:
- Full identity: userId, email, name, selectedOrganization
- Every preference returned: name, type (bool/string/int), current value, isSecret
Confirm at least one preference is returned and that isSecret is false for all of them.
```

---

### AM-P02 — Verify User Lookup by Email and by ID Returns Consistent Data
**Discovery:** `Chain` | **Expected:** `user_whoami → users_get → users_get_by_id` | **Timeout:** `30s`

```
1. Call user_whoami to get my email address.
2. Call users_get searching by that email.
3. Call users_get_by_id using the userId from step 2.
Compare all fields between steps 2 and 3. Verify:
- id matches
- email matches
- displayName matches
- status matches
Report any field that differs between the two lookups. Expected: identical data.
```

---

### AM-P03 — List All Users in Organization
**Discovery:** `Chain` | **Expected:** `organizations_list → users_list` | **Timeout:** `20s`

```
Call organizations_list to get the current organization ID.
Then call users_list for that organization. Report:
- Total user count
- Each user's: displayName, email, status, type, mfaEnabled
- How many users have status=USER_STATUS_ACTIVE
- How many have mfaEnabled=true
```

---

### AM-P04 — List Teams and Fetch One by ID
**Discovery:** `Chain` | **Expected:** `organizations_list → teams_get → teams_get_by_id` | **Timeout:** `30s`

```
Call organizations_list to get the org ID.
Call teams_get to list all teams. From the result, pick the first team.
Call teams_get_by_id using that team's ID.
Verify:
- team name matches between both calls
- team ID matches between both calls
Report: total team count, each team's name and type (PREDEFINED or USERDEFINED).
```

---

### AM-P05 — Full Invite Lifecycle: Create → List → Delete
**Discovery:** `Stress` | **Expected:** `organizations_list → teams_create → teams_invite_create → teams_invites_list → teams_invite_delete → teams_delete` | **Timeout:** `120s`

```
1. Call organizations_list to get the org ID.
2. Create a team named "am-p05-invite-test" using teams_create.
3. Call users_list to get the first active user's email.
4. Invite that user to the team using teams_invite_create.
5. Call teams_invites_list and verify the invite appears.
6. Delete the invite using teams_invite_delete. Verify success.
7. Call teams_invites_list again — verify the invite no longer appears.
8. Delete the team using teams_delete.
Report the result of each step. Confirm the lifecycle completes cleanly.
```

---

### AM-P06 — Full Team Member Lifecycle: Add → List → Remove
**Discovery:** `Stress` | **Expected:** `organizations_list → users_list → teams_create → teams_members_add → teams_memberships_list → teams_members_remove → teams_delete` | **Timeout:** `120s`

```
1. Call organizations_list to get the org ID.
2. Call users_list to get the first active user's userId.
3. Create a team named "am-p06-member-lifecycle".
4. Add the user to the team using teams_members_add.
5. Call teams_memberships_list and verify the user appears.
6. Remove the user using teams_members_remove.
7. Call teams_memberships_list again — verify the user no longer appears.
8. Delete the team.
Report the outcome of each step. Note if teams_memberships_list returns 501 (known Bug #2).
```

---

### AM-P07 — List API Tokens for Current User
**Discovery:** `Chain` | **Expected:** `user_whoami → api_tokens_list` | **Timeout:** `20s`

```
Call user_whoami to confirm identity and get my userId.
Call api_tokens_list for the current user. Report:
- Total number of API tokens
- Each token's name, createdAt, lastUsed (if available)
Confirm that actual token values are never returned (only metadata).
```

---

### AM-P08 — List RBAC Roles and Fetch One by ID
**Discovery:** `Chain` | **Expected:** `organizations_list → rbac_roles_list → rbac_role_get` | **Timeout:** `30s`

```
Call organizations_list to get the org ID.
Call rbac_roles_list for that org. Pick the first role from the results.
Call rbac_role_get with that role's ID.
Verify:
- Role ID matches between list and get
- Role name and description are present
Report: total role count, each role's id, name, and description.
```

---

### AM-P09 — RBAC Role Create → Get → Verify Authorizations → Delete
**Discovery:** `Stress` | **Expected:** `organizations_list → rbac_role_create → rbac_role_get → rbac_authorizations_list → rbac_role_delete` | **Timeout:** `90s`

```
1. Call organizations_list to get the org ID.
2. Create a new RBAC role named "am-p09-test-role" with description "Temporary test role for AM-P09".
3. Call rbac_role_get with the returned roleId. Verify name and description match.
4. Call rbac_authorizations_list for the org. Report existing authorization count.
5. Delete the role using rbac_role_delete.
6. Call rbac_role_get again — verify it returns 404.
Report each step's outcome.
```

---

### AM-P10 — List Permissions and Bulk Authorization Check
**Discovery:** `Chain` | **Expected:** `organizations_list → rbac_permissions_list → rbac_authorization_check_bulk` | **Timeout:** `45s`

```
1. Call organizations_list to get the org ID.
2. Call rbac_permissions_list. Report the total count and first 5 permission names.
3. Call user_whoami to get my userId.
4. Call rbac_roles_list to get a real role name.
5. Call rbac_authorization_check_bulk with two requests:
   a. Check if I have the real role on the org resource
   b. Check if I have role "NONEXISTENT_ROLE_99" on the org resource
Report the pass/fail result for each check.
```

---

### AM-P11 — List SAML Connections
**Discovery:** `Chain` | **Expected:** `organizations_list → saml_connections_list` | **Timeout:** `20s`

```
Call organizations_list to get the org ID.
Call saml_connections_list for that org.
Report: total connections found, each connection's id and name.
If no SAML connections exist, record "0 SAML connections — empty result OK".
```

---

### AM-P12 — List SAML Connections and Email Domains
**Discovery:** `Chain` | **Expected:** `organizations_list → saml_connections_list → saml_email_domains_list` | **Timeout:** `30s`

```
1. Call organizations_list to get the org ID.
2. Call saml_connections_list for that org.
3. Call saml_email_domains_list for that org.
Report: all SAML connections and all email domains associated with SAML.
If either returns empty, record as "0 results — empty result OK".
```

---

## NEGATIVE TEST CASES

---

### AM-N01 — User Lookup with Non-Existent Email
**Discovery:** `Selection` | **Expected:** `users_get` | **Timeout:** `15s`

```
Search for a user by email "no-such-user-xyz-99999@example.invalid".
Record the exact response. Expected: 404 or empty results array.
```

---

### AM-N02 — User Get by Non-Existent ID
**Discovery:** `Selection` | **Expected:** `users_get_by_id` | **Timeout:** `15s`

```
Call users_get_by_id with a nil UUID: 00000000-0000-0000-0000-000000000099.
Record the exact error message and HTTP status code. Expected: 404.
```

---

### AM-N03 — Create Team with Empty Name
**Discovery:** `Selection` | **Expected:** `teams_create` | **Timeout:** `15s`

```
Attempt to create a team with name="" (empty string).
Call organizations_list first to get a valid org ID.
Record the exact error message. Expected: 400 validation error.
```

---

### AM-N04 — Delete Non-Existent Team
**Discovery:** `Selection` | **Expected:** `teams_delete` | **Timeout:** `15s`

```
Call teams_delete with a nil team ID: 00000000-0000-0000-0000-000000000099.
Record the exact error message and HTTP status code. Expected: 404.
```

---

### AM-N05 — Invite with Invalid Email Format
**Discovery:** `Chain` | **Expected:** `organizations_list → teams_create → teams_invite_create (bad email) → teams_delete` | **Timeout:** `45s`

```
1. Call organizations_list to get the org ID.
2. Create a team named "am-n05-bad-invite".
3. Attempt teams_invite_create with email "not-a-valid-email-format".
4. Record the exact error. Expected: 400 validation error.
5. Delete the team as cleanup.
```

---

### AM-N06 — Add Non-Existent User to Team
**Discovery:** `Selection` | **Expected:** `organizations_list → teams_create → teams_members_add (nil ID) → teams_delete` | **Timeout:** `30s`

```
1. Call organizations_list to get the org ID.
2. Create a team named "am-n06-bad-member".
3. Attempt teams_members_add with userId: 00000000-0000-0000-0000-000000000099.
4. Record the exact error. Expected: 404 or 400.
5. Delete the team as cleanup.
```

---

### AM-N07 — Get RBAC Role with Non-Existent ID
**Discovery:** `Selection` | **Expected:** `rbac_role_get` | **Timeout:** `15s`

```
Call rbac_role_get with a nil ID: 00000000-0000-0000-0000-000000000099.
Record the exact error message and HTTP status code. Expected: 404.
```

---

### AM-N08 — Create RBAC Role with Empty Name
**Discovery:** `Selection` | **Expected:** `rbac_role_create` | **Timeout:** `15s`

```
Call organizations_list to get the org ID.
Attempt rbac_role_create with an empty name="".
Record the exact error message. Expected: 400 validation error.
```

---

### AM-N09 — Delete Non-Existent RBAC Role
**Discovery:** `Selection` | **Expected:** `rbac_role_delete` | **Timeout:** `15s`

```
Call rbac_role_delete with a nil ID: 00000000-0000-0000-0000-000000000099.
Record the exact error message and HTTP status code. Expected: 404.
```

---

### AM-N10 — Set Invalid Timezone
**Discovery:** `Selection` | **Expected:** `user_set_timezone` | **Timeout:** `15s`

```
Call user_whoami to get my userId.
Attempt user_set_timezone with timezone="Not/AReal_Timezone_Zone".
Record the exact error message. Expected: 400 validation error (Known Bug #1).
```

---

## EDGE CASES

---

### AM-E01 — Fetch Deleted Team Immediately After Deletion
**Discovery:** `Chain` | **Expected:** `organizations_list → teams_create → teams_delete → teams_get_by_id` | **Timeout:** `45s`

```
1. Call organizations_list to get the org ID.
2. Create a team named "am-e01-delete-verify".
3. Immediately delete the team using teams_delete.
4. Attempt teams_get_by_id with the deleted team's ID.
Verify the response is 404 or "not found" — NOT the original team object.
This confirms deletion is immediately visible.
```

---

### AM-E02 — Create Two Invites for the Same Team
**Discovery:** `Chain` | **Expected:** `organizations_list → teams_create → teams_invite_create ×2 → teams_invites_list → teams_delete` | **Timeout:** `60s`

```
1. Call organizations_list to get the org ID.
2. Create a team named "am-e02-multi-invite".
3. Call users_list to get two different users' emails.
4. Send two separate teams_invite_create calls — one for each email.
5. Call teams_invites_list and verify both invites appear.
6. Delete the team (this should cascade-delete invites or allow cleanup).
Report: whether both invites are visible simultaneously.
```

---

### AM-E03 — Create Role, List Authorizations, Delete Role
**Discovery:** `Chain` | **Expected:** `organizations_list → rbac_role_create → rbac_authorizations_list → rbac_role_delete` | **Timeout:** `60s`

```
1. Call organizations_list to get the org ID.
2. Create a role named "am-e03-auth-check-role".
3. Call rbac_authorizations_list — confirm no authorizations reference the new role yet.
4. Delete the role.
This verifies that a new role starts with zero authorizations.
```

---

### AM-E04 — List Teams in Organization with No Custom Teams
**Discovery:** `Selection` | **Expected:** `organizations_list → teams_get` | **Timeout:** `20s`

```
Call organizations_list to get the org ID.
Call teams_get for the org.
Report: how many teams exist (total), how many are PREDEFINED vs USERDEFINED.
If only PREDEFINED teams exist, record "No user-defined teams — empty USERDEFINED list OK".
```

---

### AM-E05 — Bulk Auth Check with Mix of Valid and Invalid Roles
**Discovery:** `Chain` | **Expected:** `organizations_list → rbac_authorization_check_bulk` | **Timeout:** `30s`

```
1. Call organizations_list to get the org ID.
2. Call user_whoami to get my userId.
3. Call rbac_roles_list to get one real role name.
4. Call rbac_authorization_check_bulk with 3 checks:
   a. My user has the real role on the org → expected: true
   b. My user has role "FAKE_ROLE_XYZ" on the org → expected: false
   c. My user has the real role on resource ID "00000000-0000-0000-0000-000000000099" → expected: false
Report each result. Verify mixed results (true + false) are handled correctly.
```

---

### AM-E06 — Set Timezone and Verify Preference Updated
**Discovery:** `Chain` | **Expected:** `user_whoami → user_set_timezone → user_preferences_get` | **Timeout:** `45s`

```
1. Call user_whoami to get my userId.
2. Call user_preferences_get to record the current timezone preference value.
3. Attempt user_set_timezone with "America/New_York". If it fails, try "UTC".
4. If step 3 succeeds, call user_preferences_get again and verify the timezone preference changed.
5. Set timezone back to the original value.
Document which IANA timezone values are accepted.
```

---

### AM-E07 — Full Team Lifecycle with Invites AND Members
**Discovery:** `Stress` | **Expected:** `organizations_list → users_list → teams_create → teams_invite_create ×2 → teams_members_add → teams_memberships_list → teams_members_remove → teams_invite_delete ×2 → teams_delete` | **Timeout:** `150s`

```
1. Call organizations_list to get the org ID.
2. Call users_list to get two users: pick users[0] and users[1].
3. Create a team named "am-e07-full-lifecycle".
4. Invite users[0] and users[1] by email.
5. Add users[0] as a direct member.
6. Call teams_memberships_list — verify users[0] appears.
7. Remove users[0] using teams_members_remove.
8. Delete both invites using teams_invite_delete.
9. Delete the team.
Report each step. Verify invite and membership operations work independently.
```

---

### AM-E08 — Create Duplicate Role Name
**Discovery:** `Chain` | **Expected:** `organizations_list → rbac_role_create → rbac_role_create (duplicate) → rbac_role_delete` | **Timeout:** `60s`

```
1. Call organizations_list to get the org ID.
2. Create a role named "am-e08-dup-role".
3. Attempt to create another role with the same name "am-e08-dup-role".
4. Record the exact error from step 3. Expected: 409 Conflict or 400.
5. Delete the first role as cleanup.
```

---

### AM-E09 — Create Role, Grant Authorization, Verify in List
**Discovery:** `Chain` | **Expected:** `organizations_list → rbac_permissions_list → rbac_role_create → rbac_authorization_create → rbac_authorizations_list → rbac_role_delete` | **Timeout:** `90s`

```
1. Call organizations_list to get the org ID.
2. Call users_list to get a user ID.
3. Create a role named "am-e09-auth-grant-role".
4. Call rbac_authorization_create to grant that role to the user on the org.
5. Call rbac_authorizations_list and verify the new authorization appears.
6. Delete the role.
Report each step. Note whether the authorization is automatically removed when the role is deleted.
```

---

### AM-E10 — List Invites for Team with No Pending Invites
**Discovery:** `Chain` | **Expected:** `organizations_list → teams_create → teams_invites_list → teams_delete` | **Timeout:** `30s`

```
1. Call organizations_list to get the org ID.
2. Create a team named "am-e10-empty-invites".
3. Call teams_invites_list for the new team (no invites have been sent).
4. Verify: empty result or count=0. This must NOT return an error.
5. Delete the team.
```
