# Domain: RBAC (Role-Based Access Control)
**Tools covered (7):** `rbac_roles_list`, `rbac_role_get`, `rbac_role_create`, `rbac_role_delete`, `rbac_permissions_list`, `rbac_authorizations_list`, `rbac_authorization_check_bulk`
**Total prompts:** 24 (8 positive, 8 negative, 8 edge cases)

---

## Test Execution Tracker

| ID | Type | Category | Expected Tools | Timeout | Description | Status | Notes |
|----|------|----------|----------------|---------|-------------|--------|-------|
| RBAC-P01 | Positive | Selection | `rbac_permissions_list` | 15s | List all available RBAC permissions | ⬜ | |
| RBAC-P02 | Positive | Selection | `rbac_roles_list` | 15s | List all RBAC roles in the organization | ⬜ | |
| RBAC-P03 | Positive | Chain | `rbac_role_create → rbac_role_get` | 30s | Create a custom role and verify it by ID | ⬜ | |
| RBAC-P04 | Positive | Chain | `rbac_roles_list → rbac_role_get` | 30s | Get details of an existing role from the list | ⬜ | |
| RBAC-P05 | Positive | Selection | `rbac_authorizations_list` | 15s | List all authorizations in the organization | ⬜ | |
| RBAC-P06 | Positive | Chain | `rbac_permissions_list → rbac_role_create → rbac_authorization_create` | 45s | Create role then assign an authorization | ⬜ | |
| RBAC-P07 | Positive | Selection | `rbac_authorization_check_bulk` | 15s | Bulk-check a set of permissions for the current user | ⬜ | |
| RBAC-P08 | Positive | Stress | `rbac_permissions_list → rbac_role_create → rbac_role_get → rbac_authorization_create → rbac_authorizations_list → rbac_role_delete` | 90s | Full RBAC lifecycle: create role, assign authorization, verify, delete | ⬜ | |
| RBAC-N01 | Negative | Selection | `rbac_role_get` | 15s | Get a role with non-existent roleId | ⬜ | |
| RBAC-N02 | Negative | Selection | `rbac_role_delete` | 15s | Delete a role with non-existent roleId | ⬜ | |
| RBAC-N03 | Negative | Selection | `rbac_role_create` | 15s | Create a role with empty name | ⬜ | |
| RBAC-N04 | Negative | Chain | `rbac_role_create → rbac_role_create` | 30s | Create a role with a duplicate name | ⬜ | |
| RBAC-N05 | Negative | Selection | `rbac_authorization_create` | 15s | Create authorization with non-existent roleId | ⬜ | |
| RBAC-N06 | Negative | Selection | `rbac_authorization_check_bulk` | 15s | Bulk check with non-existent permission names | ⬜ | |
| RBAC-N07 | Negative | Selection | `rbac_authorizations_list` | 15s | List authorizations for invalid organizationId | ⬜ | |
| RBAC-N08 | Negative | Selection | `rbac_permissions_list` | 15s | List permissions with invalid organizationId | ⬜ | |
| RBAC-E01 | Edge | Chain | `rbac_roles_list → rbac_role_get (×N)` | 45s | List all roles and fetch details for each | ⬜ | |
| RBAC-E02 | Edge | Chain | `rbac_role_create → rbac_role_delete → rbac_role_get` | 45s | Verify deleted role returns 404 | ⬜ | |
| RBAC-E03 | Edge | Chain | `rbac_authorization_check_bulk (×2)` | 30s | Check permissions user has vs permissions user lacks — compare | ⬜ | |
| RBAC-E04 | Edge | Chain | `rbac_role_create → rbac_authorization_create (×2)` | 45s | Assign same role twice — verify idempotency | ⬜ | |
| RBAC-E05 | Edge | Selection | `rbac_permissions_list` | 15s | Verify permissions list includes create/read/update/delete types | ⬜ | |
| RBAC-E06 | Edge | Chain | `rbac_authorizations_list → rbac_authorization_check_bulk` | 30s | List authorizations then confirm bulk-check is consistent | ⬜ | |
| RBAC-E07 | Edge | Chain | `rbac_role_create → rbac_roles_list` | 30s | Verify newly created role appears in listing | ⬜ | |
| RBAC-E08 | Edge | Stress | `rbac_role_create (×3) → rbac_roles_list → rbac_role_delete (×3)` | 90s | Create multiple roles, verify all appear in list, delete all | ⬜ | |

---

## Diagnostic Categories

| Category | Definition | Failure Indicates |
|----------|-----------|-------------------|
| **Selection** | Single tool call from natural language | AI picked the wrong tool from 122+ options |
| **Chain** | 2–4 tools called in sequence | Wrong tool order, missed step, or incorrect data passed between steps |
| **Stress** | 5+ tools OR repeated calls OR large payloads | Timeout, session limit, or token exhaustion |

---

## POSITIVE TEST CASES

---

### RBAC-P01 — List All Available RBAC Permissions

**Discovery:** `Selection` | **Expected:** `rbac_permissions_list` | **Timeout:** `15s`

```
List all available RBAC permissions for organizationId 6c5eeb79-4606-4c39-bd5c-c2323336caad.
Verify:
- Response is not an error
- Returns an array of permission objects
- Each permission has: id/name and a description or category field
Report: total permission count, names of all permissions, and any category groupings present.
```

---

### RBAC-P02 — List All RBAC Roles in the Organization

**Discovery:** `Selection` | **Expected:** `rbac_roles_list` | **Timeout:** `15s`

```
List all RBAC roles for organizationId 6c5eeb79-4606-4c39-bd5c-c2323336caad.
Verify:
- Response is not an error
- Returns an array of role objects
- Each role has: id, name, and optionally description and permissions fields
Report: total role count, names of all roles, whether any are system/built-in roles vs custom roles.
```

---

### RBAC-P03 — Create a Custom Role and Verify It by ID

**Discovery:** `Chain` | **Expected:** `rbac_role_create → rbac_role_get` | **Timeout:** `30s`

```
1. Create a new custom RBAC role with:
   - organizationId: 6c5eeb79-4606-4c39-bd5c-c2323336caad
   - name: "rbac-test-role-01"
   - description: "Smoke test role — safe to delete"

2. Record the roleId from the response.
3. Get the role details by the returned roleId.

Verify: the retrieved role matches the created role (name, description, organizationId). Report the full role object returned.
```

---

### RBAC-P04 — Get Details of an Existing Role from the List

**Discovery:** `Chain` | **Expected:** `rbac_roles_list → rbac_role_get` | **Timeout:** `30s`

```
List all RBAC roles for organizationId 6c5eeb79-4606-4c39-bd5c-c2323336caad. Take the first role from the list. Get its full details using rbac_role_get with that roleId.
Verify: the details match the summary from the listing (name, id). Report: role name, id, permissions assigned (if any), and whether this is a system or custom role.
```

---

### RBAC-P05 — List All Authorizations in the Organization

**Discovery:** `Selection` | **Expected:** `rbac_authorizations_list` | **Timeout:** `15s`

```
List all RBAC authorizations for organizationId 6c5eeb79-4606-4c39-bd5c-c2323336caad.
Verify:
- Response is not an error
- Returns an array of authorization objects (may be empty if no custom authorizations exist)
- Each entry has: principalId, roleId, resourceId fields
Report: total authorization count, and for each authorization report the principalId and roleId.
```

---

### RBAC-P06 — Create a Role Then Assign an Authorization

**Discovery:** `Chain` | **Expected:** `rbac_permissions_list → rbac_role_create → rbac_authorization_create` | **Timeout:** `45s`

```
1. List all permissions to see what is available.
2. Create a role named "rbac-authz-test-role-01" for organizationId 6c5eeb79-4606-4c39-bd5c-c2323336caad.
3. Create an authorization assigning that role to the current user (use the userId obtained from user_whoami) for the organization resource.

Verify: the authorization was created without error. Report: the roleId, principalId, and resourceId from the authorization response. Clean up: if possible, delete the test role after verifying.
```

---

### RBAC-P07 — Bulk-Check a Set of Permissions for the Current User

**Discovery:** `Selection` | **Expected:** `rbac_authorization_check_bulk` | **Timeout:** `15s`

```
Perform a bulk authorization check for the current user (from user_whoami) against organizationId 6c5eeb79-4606-4c39-bd5c-c2323336caad. Include a list of 3–5 permission names obtained from rbac_permissions_list (or known common permissions like "read", "write", "admin", "delete").
Verify:
- Response returns a result for each permission checked (allowed: true/false)
- No error is returned
Report: which permissions the current user has, and which they lack.
```

---

### RBAC-P08 — Full RBAC Lifecycle

**Discovery:** `Stress` | **Expected:** `rbac_permissions_list → rbac_role_create → rbac_role_get → rbac_authorization_create → rbac_authorizations_list → rbac_role_delete` | **Timeout:** `90s`

```
Execute the full RBAC lifecycle:
1. List permissions to understand what is available.
2. Create role "rbac-lifecycle-test-DATE" (use today's date in the name) for organizationId 6c5eeb79-4606-4c39-bd5c-c2323336caad.
3. Get the role by its new ID — verify it matches what was created.
4. Create an authorization assigning this role to the current user for the organization.
5. List all authorizations — verify the new authorization appears.
6. Delete the test role.

Report each step result. Verify no step returns an error. Confirm the role is removed by attempting to get it after deletion (expect 404).
```

---

## NEGATIVE TEST CASES

---

### RBAC-N01 — Get a Role With Non-Existent roleId

**Discovery:** `Selection` | **Expected:** `rbac_role_get` | **Timeout:** `15s`

```
Get the RBAC role with:
- organizationId: 6c5eeb79-4606-4c39-bd5c-c2323336caad
- roleId: 00000000-0000-0000-0000-000000000099

Record the exact error response. Expected: 404 (role not found). Document the HTTP status and error message.
```

---

### RBAC-N02 — Delete a Role With Non-Existent roleId

**Discovery:** `Selection` | **Expected:** `rbac_role_delete` | **Timeout:** `15s`

```
Delete the RBAC role with:
- organizationId: 6c5eeb79-4606-4c39-bd5c-c2323336caad
- roleId: 00000000-0000-0000-0000-000000000099

Record the exact error response. Expected: 404 (role not found). Document the HTTP status and error message.
```

---

### RBAC-N03 — Create a Role With Empty Name

**Discovery:** `Selection` | **Expected:** `rbac_role_create` | **Timeout:** `15s`

```
Attempt to create an RBAC role with:
- organizationId: 6c5eeb79-4606-4c39-bd5c-c2323336caad
- name: "" (empty string)

Record the exact error response. Is this validated client-side (required field) or server-side (400 Bad Request)? Document the full error message.
```

---

### RBAC-N04 — Create a Role With a Duplicate Name

**Discovery:** `Chain` | **Expected:** `rbac_role_create → rbac_role_create` | **Timeout:** `30s`

```
1. Create a role named "rbac-duplicate-test" for organizationId 6c5eeb79-4606-4c39-bd5c-c2323336caad. Record the roleId.
2. Attempt to create a second role with the same name "rbac-duplicate-test".

Record the exact error from the second call. Expected: 409 Conflict or 400 Bad Request. Clean up: delete the first role regardless of outcome. Document whether the server enforces name uniqueness.
```

---

### RBAC-N05 — Create Authorization With Non-Existent roleId

**Discovery:** `Selection` | **Expected:** `rbac_authorization_create` | **Timeout:** `15s`

```
Attempt to create an authorization with:
- organizationId: 6c5eeb79-4606-4c39-bd5c-c2323336caad
- roleId: 00000000-0000-0000-0000-000000000099
- principalId: (use current userId from user_whoami)

Record the exact error. Expected: 404 (role not found) or 400 (bad request). Document the HTTP status and error message.
```

---

### RBAC-N06 — Bulk Check With Non-Existent Permission Names

**Discovery:** `Selection` | **Expected:** `rbac_authorization_check_bulk` | **Timeout:** `15s`

```
Perform a bulk authorization check with fabricated permission names that do not exist:
- organizationId: 6c5eeb79-4606-4c39-bd5c-c2323336caad
- permissions: ["fake.permission.xyz", "does.not.exist.abc"]

Record the response. Does the server return an error (400 — unknown permission), or does it return allowed=false for each unknown permission? Document the exact behavior.
```

---

### RBAC-N07 — List Authorizations for Invalid organizationId

**Discovery:** `Selection` | **Expected:** `rbac_authorizations_list` | **Timeout:** `15s`

```
List RBAC authorizations for:
- organizationId: 00000000-0000-0000-0000-000000000099

Record the exact error response. Expected: 404 (org not found) or 403 (forbidden). Does it return an error or an empty list? Document the HTTP status and error message.
```

---

### RBAC-N08 — List Permissions With Invalid organizationId

**Discovery:** `Selection` | **Expected:** `rbac_permissions_list` | **Timeout:** `15s`

```
List RBAC permissions for:
- organizationId: 00000000-0000-0000-0000-000000000099

Record the exact response. Expected: 404 or 403. Does it return an error or an empty list? Document the HTTP status and error message.
```

---

## EDGE CASES

---

### RBAC-E01 — List All Roles and Fetch Details for Each

**Discovery:** `Chain` | **Expected:** `rbac_roles_list → rbac_role_get (×N)` | **Timeout:** `45s`

```
List all RBAC roles for organizationId 6c5eeb79-4606-4c39-bd5c-c2323336caad. For each role returned (up to 10), call rbac_role_get to get the full details. Verify: the details from rbac_role_get match what was returned in the listing (id, name). Report: total role count, and whether any role in the list fails to load by ID (data integrity check).
```

---

### RBAC-E02 — Verify Deleted Role Returns 404

**Discovery:** `Chain` | **Expected:** `rbac_role_create → rbac_role_delete → rbac_role_get` | **Timeout:** `45s`

```
1. Create role "rbac-e02-delete-verify-test" for organizationId 6c5eeb79-4606-4c39-bd5c-c2323336caad. Record roleId.
2. Delete the role using the roleId.
3. Attempt to get the role by the same roleId.

Verify: step 3 returns a 404 or similar error. Document whether the server returns a clear "not found" or a different status. This validates that deletes are properly enforced.
```

---

### RBAC-E03 — Bulk Check: Allowed vs Denied Permissions

**Discovery:** `Chain` | **Expected:** `rbac_authorization_check_bulk (×2)` | **Timeout:** `30s`

```
First, list permissions to find a mix of permissions the current user is likely to have and not have. Then perform two bulk authorization checks for organizationId 6c5eeb79-4606-4c39-bd5c-c2323336caad:
1. A set of read-type permissions (the current user should have these as an admin).
2. A set of admin-delete-type permissions (may or may not have these).

Report: which permissions returned allowed=true and which returned allowed=false for each check. Verify the bulk check correctly differentiates between granted and denied permissions.
```

---

### RBAC-E04 — Assign Same Role Authorization Twice — Idempotency

**Discovery:** `Chain` | **Expected:** `rbac_role_create → rbac_authorization_create (×2)` | **Timeout:** `45s`

```
1. Create role "rbac-e04-idempotency-test" for organizationId 6c5eeb79-4606-4c39-bd5c-c2323336caad.
2. Create authorization: assign this role to the current user for the organization.
3. Create the exact same authorization again (same principalId, roleId, resourceId).

Record the response to the second call. Does the server return 200 OK (idempotent), 409 Conflict (duplicate), or a different status? Document the behavior. Clean up: delete the test role after.
```

---

### RBAC-E05 — Verify Permissions List Covers CRUD Operations

**Discovery:** `Selection` | **Expected:** `rbac_permissions_list` | **Timeout:** `15s`

```
List all RBAC permissions for organizationId 6c5eeb79-4606-4c39-bd5c-c2323336caad. Examine the returned permissions and verify:
- At least one "create" type permission exists
- At least one "read" or "view" type permission exists
- At least one "update" or "edit" type permission exists
- At least one "delete" type permission exists
Report: how permissions are categorized (resource type + action, or flat names), and whether any permissions are scoped to specific resources (e.g., "component:read" vs generic "read"). This documents the permission model.
```

---

### RBAC-E06 — List Authorizations Then Confirm Bulk Check Is Consistent

**Discovery:** `Chain` | **Expected:** `rbac_authorizations_list → rbac_authorization_check_bulk` | **Timeout:** `30s`

```
1. List all authorizations for organizationId 6c5eeb79-4606-4c39-bd5c-c2323336caad. Record which roles are assigned to the current user.
2. From the role details, determine what permissions the current user should have.
3. Run rbac_authorization_check_bulk for those permissions.

Verify: permissions implied by the assigned roles show allowed=true in the bulk check. Report any discrepancy between the authorization list (what roles the user has) and the bulk check (what they can do). This validates consistency between the two tools.
```

---

### RBAC-E07 — Verify New Role Appears in Listing

**Discovery:** `Chain` | **Expected:** `rbac_role_create → rbac_roles_list` | **Timeout:** `30s`

```
1. Record the role count before creation: list all roles and count them (count_before).
2. Create role "rbac-e07-visibility-test" for organizationId 6c5eeb79-4606-4c39-bd5c-c2323336caad.
3. List all roles again and count (count_after).

Verify: count_after = count_before + 1. Find the new role in the listing by name. Clean up: delete the test role. This verifies that creates are immediately reflected in list results.
```

---

### RBAC-E08 — Create Multiple Roles, Verify All Appear, Delete All

**Discovery:** `Stress` | **Expected:** `rbac_role_create (×3) → rbac_roles_list → rbac_role_delete (×3)` | **Timeout:** `90s`

```
1. Create three roles in sequence:
   - "rbac-e08-role-alpha" for organizationId 6c5eeb79-4606-4c39-bd5c-c2323336caad
   - "rbac-e08-role-beta"
   - "rbac-e08-role-gamma"
2. Record all three roleIds.
3. List all roles — verify all three appear.
4. Delete all three roles.
5. List roles again — verify none of the three appear.

Report: each step result, total time for the full sequence, and whether any delete fails (cleanup required if it does).
```
