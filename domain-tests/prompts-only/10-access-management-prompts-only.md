# Access Management — Prompts Only

---

## POSITIVE TEST CASES

### AM-P01 — Get Current User Profile and Preferences

```
Who am I on CloudBees? Show my full profile including userId, email, name, and selected organization.
Then retrieve my user preferences using that userId. Report:
- Full identity: userId, email, name, selectedOrganization
- Every preference returned: name, type (bool/string/int), current value, isSecret
Confirm at least one preference is returned and that isSecret is false for all of them.
```

---

### AM-P02 — Verify User Lookup by Email and by ID Returns Consistent Data

```
1. Confirm my identity to get my email address.
2. Look up my user record by searching with that email.
3. Retrieve the same user again directly by their ID.
Compare all fields between steps 2 and 3. Verify:
- id matches
- email matches
- displayName matches
- status matches
Report any field that differs between the two lookups. Expected: identical data.
```

---

### AM-P03 — List All Users in Organization

```
List all organizations to get the current org. Then list all users in that organization. Report:
- Total user count
- Each user's: displayName, email, status, type, mfaEnabled
- How many users have status=USER_STATUS_ACTIVE
- How many have mfaEnabled=true
```

---

### AM-P04 — List Teams and Fetch One by ID

```
List all organizations to get the org. List all teams in that org. Pick the first team.
Retrieve that team again directly by its ID.
Verify:
- team name matches between both calls
- team ID matches between both calls
Report: total team count, each team's name and type (PREDEFINED or USERDEFINED).
```

---

### AM-P05 — Full Invite Lifecycle: Create → List → Delete

```
1. List all organizations to get the org.
2. Create a team named "am-p05-invite-test".
3. List all users to get the first active user's email.
4. Send an invite for that user to the team.
5. List pending invites and verify the invite appears.
6. Delete the invite. Verify success.
7. List pending invites again — verify the invite no longer appears.
8. Delete the team.
Report the result of each step. Confirm the lifecycle completes cleanly.
```

---

### AM-P06 — Full Team Member Lifecycle: Add → List → Remove

```
1. List all organizations to get the org.
2. List all users to get the first active user's userId.
3. Create a team named "am-p06-member-lifecycle".
4. Add the user to the team as a member.
5. List team members and verify the user appears.
6. Remove the user from the team.
7. List team members again — verify the user no longer appears.
8. Delete the team.
Report the outcome of each step. Note if listing team members returns 501 (known Bug #2).
```

---

### AM-P07 — List API Tokens for Current User

```
Confirm my identity to get my userId.
List all API tokens for the current user. Report:
- Total number of API tokens
- Each token's name, createdAt, lastUsed (if available)
Confirm that actual token values are never returned (only metadata).
```

---

### AM-P08 — List RBAC Roles and Fetch One by ID

```
List all organizations to get the org. List all RBAC roles for that org.
Pick the first role and retrieve it directly by its ID.
Verify:
- Role ID matches between list and get
- Role name and description are present
Report: total role count, each role's id, name, and description.
```

---

### AM-P09 — RBAC Role Create → Get → Verify Authorizations → Delete

```
1. List all organizations to get the org.
2. Create a new RBAC role named "am-p09-test-role" with description "Temporary test role for AM-P09".
3. Retrieve the role by its ID. Verify name and description match.
4. List all authorizations for the org. Report existing authorization count.
5. Delete the role.
6. Attempt to retrieve the role by its ID again — verify it returns 404.
Report each step's outcome.
```

---

### AM-P10 — List Permissions and Bulk Authorization Check

```
1. List all organizations to get the org.
2. List all available permissions. Report the total count and first 5 permission names.
3. Confirm my identity to get my userId.
4. List all roles to get a real role name.
5. Run a bulk authorization check with two requests:
   a. Check if I have the real role on the org resource
   b. Check if I have role "NONEXISTENT_ROLE_99" on the org resource
Report the pass/fail result for each check.
```

---

### AM-P11 — List SAML Connections

```
List all organizations to get the org. List all SAML connections for that org.
Report: total connections found, each connection's id and name.
If no SAML connections exist, record "0 SAML connections — empty result OK".
```

---

### AM-P12 — List SAML Connections and Email Domains

```
1. List all organizations to get the org.
2. List all SAML connections for that org.
3. List all SAML email domains for that org.
Report: all SAML connections and all email domains associated with SAML.
If either returns empty, record as "0 results — empty result OK".
```

---

## NEGATIVE TEST CASES

### AM-N01 — User Lookup with Non-Existent Email

```
Search for a user by email "no-such-user-xyz-99999@example.invalid".
Record the exact response. Expected: 404 or empty results array.
```

---

### AM-N02 — User Get by Non-Existent ID

```
Retrieve a user directly by the nil UUID: 00000000-0000-0000-0000-000000000099.
Record the exact error message and HTTP status code. Expected: 404.
```

---

### AM-N03 — Create Team with Empty Name

```
Attempt to create a team with name="" (empty string).
List organizations first to get a valid org.
Record the exact error message. Expected: 400 validation error.
```

---

### AM-N04 — Delete Non-Existent Team

```
Attempt to delete a team using the nil UUID: 00000000-0000-0000-0000-000000000099.
Record the exact error message and HTTP status code. Expected: 404.
```

---

### AM-N05 — Invite with Invalid Email Format

```
1. List organizations to get the org.
2. Create a team named "am-n05-bad-invite".
3. Attempt to send an invite with email "not-a-valid-email-format".
4. Record the exact error. Expected: 400 validation error.
5. Delete the team as cleanup.
```

---

### AM-N06 — Add Non-Existent User to Team

```
1. List organizations to get the org.
2. Create a team named "am-n06-bad-member".
3. Attempt to add a member using userId: 00000000-0000-0000-0000-000000000099.
4. Record the exact error. Expected: 404 or 400.
5. Delete the team as cleanup.
```

---

### AM-N07 — Get RBAC Role with Non-Existent ID

```
Attempt to retrieve an RBAC role using the nil UUID: 00000000-0000-0000-0000-000000000099.
Record the exact error message and HTTP status code. Expected: 404.
```

---

### AM-N08 — Create RBAC Role with Empty Name

```
List organizations to get the org.
Attempt to create a role with an empty name="".
Record the exact error message. Expected: 400 validation error.
```

---

### AM-N09 — Delete Non-Existent RBAC Role

```
Attempt to delete a role using the nil UUID: 00000000-0000-0000-0000-000000000099.
Record the exact error message and HTTP status code. Expected: 404.
```

---

### AM-N10 — Set Invalid Timezone

```
Confirm my identity to get my userId.
Attempt to set the timezone to "Not/AReal_Timezone_Zone".
Record the exact error message. Expected: 400 validation error (Known Bug #1).
```

---

## EDGE CASES

### AM-E01 — Fetch Deleted Team Immediately After Deletion

```
1. List organizations to get the org.
2. Create a team named "am-e01-delete-verify".
3. Immediately delete the team.
4. Attempt to retrieve the deleted team by its ID.
Verify the response is 404 or "not found" — NOT the original team object.
This confirms deletion is immediately visible.
```

---

### AM-E02 — Create Two Invites for the Same Team

```
1. List organizations to get the org.
2. Create a team named "am-e02-multi-invite".
3. List all users to get two different users' emails.
4. Send two separate invites — one for each email.
5. List pending invites and verify both appear.
6. Delete the team.
Report: whether both invites are visible simultaneously.
```

---

### AM-E03 — Create Role, List Authorizations, Delete Role

```
1. List organizations to get the org.
2. Create a role named "am-e03-auth-check-role".
3. List all authorizations — confirm none reference the new role yet.
4. Delete the role.
This verifies that a new role starts with zero authorizations.
```

---

### AM-E04 — List Teams in Organization with No Custom Teams

```
List organizations to get the org. List all teams in that org.
Report: how many teams exist (total), how many are PREDEFINED vs USERDEFINED.
If only PREDEFINED teams exist, record "No user-defined teams — empty USERDEFINED list OK".
```

---

### AM-E05 — Bulk Auth Check with Mix of Valid and Invalid Roles

```
1. List organizations to get the org.
2. Confirm my identity to get my userId.
3. List all roles to get one real role name.
4. Run a bulk authorization check with 3 requests:
   a. My user has the real role on the org → expected: true
   b. My user has role "FAKE_ROLE_XYZ" on the org → expected: false
   c. My user has the real role on resource ID "00000000-0000-0000-0000-000000000099" → expected: false
Report each result. Verify mixed results (true + false) are handled correctly.
```

---

### AM-E06 — Set Timezone and Verify Preference Updated

```
1. Confirm my identity to get my userId.
2. Get my current user preferences and record the current timezone value.
3. Attempt to set the timezone to "America/New_York". If it fails, try "UTC".
4. If step 3 succeeds, get preferences again and verify the timezone changed.
5. Set the timezone back to the original value.
Document which IANA timezone values are accepted.
```

---

### AM-E07 — Full Team Lifecycle with Invites AND Members

```
1. List organizations to get the org.
2. List all users to get two users: users[0] and users[1].
3. Create a team named "am-e07-full-lifecycle".
4. Send invites for users[0] and users[1] by email.
5. Add users[0] as a direct member.
6. List team members — verify users[0] appears.
7. Remove users[0] from the team.
8. Delete both invites.
9. Delete the team.
Report each step. Verify invite and membership operations work independently.
```

---

### AM-E08 — Create Duplicate Role Name

```
1. List organizations to get the org.
2. Create a role named "am-e08-dup-role".
3. Attempt to create another role with the same name "am-e08-dup-role".
4. Record the exact error from step 3. Expected: 409 Conflict or 400.
5. Delete the first role as cleanup.
```

---

### AM-E09 — Create Role, Grant Authorization, Verify in List

```
1. List organizations to get the org.
2. List all users to get a user ID.
3. Create a role named "am-e09-auth-grant-role".
4. Grant that role to the user on the org resource.
5. List all authorizations and verify the new grant appears.
6. Delete the role.
Report each step. Note whether the authorization is automatically removed when the role is deleted.
```

---

### AM-E10 — List Invites for Team with No Pending Invites

```
1. List organizations to get the org.
2. Create a team named "am-e10-empty-invites".
3. List pending invites for the new team (no invites have been sent).
4. Verify: empty result or count=0. This must NOT return an error.
5. Delete the team.
```
