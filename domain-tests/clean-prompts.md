# CloudBees Unify MCP — Clean Test Prompts (No Hardcoded Data)

All prompts discover required IDs and names at runtime using prior tool calls.
No hardcoded UUIDs, emails, component names, or environment-specific values.
Intentionally fake nil UUIDs (`00000000-0000-0000-0000-000000000099`) used only in negative tests.

---

## Identity & Users

### U01
Who am I? Show my full profile including userId, email, name, and selected organization.

### U02
First confirm my identity to get my userId. Then retrieve all user preferences for that userId. Report every preference name, type, and current value.

### U03
Set my timezone to UTC. Use my userId from whoami. Verify the response confirms success.

### U04
List all users in the organization. Report the total count, each user's display name, email, status, and whether MFA is enabled.

### U05
Search for my own user details using the email returned from whoami. Then fetch the same user by their ID. Compare both responses and confirm they return identical data.

### U06 (Negative)
Search for a user by email "no-such-user-xyz-999@example.invalid". Record the exact response. Expected: 404 or empty result.

### U07 (Negative)
Get user details for a non-existent user ID (00000000-0000-0000-0000-000000000099). Record the exact error. Expected: 404.

---

## Teams

### T01
List all existing teams in the organization. Report each team's name, type (PREDEFINED or USERDEFINED), and member count.

### T02
Create a team named "clean-test-team-01". Retrieve it by name (using teams_get). Then retrieve it again by its ID (using teams_get_by_id). Verify all three operations return consistent data. Delete the team.

### T03
Full team member lifecycle:
1. List all users and pick the first active user.
2. Create a team named "clean-team-lifecycle-01".
3. Invite the selected user to the team using teams_invite_create.
4. List pending invites and verify the invite appears.
5. Delete the invite.
6. Add the user as a direct member using teams_members_add.
7. List team memberships and verify the user appears.
8. Remove the user using teams_members_remove. Verify they are no longer a member.
9. Delete the team.
Report the result of every step.

### T04
Create a team named "clean-team-invite-multi-01".
Invite two different users from users_list.
List all pending invites and verify both appear.
Delete both invites.
Delete the team.

### T05 (Negative)
Attempt to create a team with an empty name (name=""). Record the exact error. Expected: 400 validation error.

### T06 (Negative)
Attempt to delete a team using a non-existent team ID (00000000-0000-0000-0000-000000000099). Record the exact error. Expected: 404.

### T07 (Negative)
Attempt to add a user to a team using a non-existent user ID (00000000-0000-0000-0000-000000000099) and a real team ID (from teams_get). Record the exact error.

### T08 (Edge)
Create a team. Immediately delete it. Attempt to retrieve the deleted team by its ID. Verify the response is a 404 or similar "not found" error (not the team object). This confirms deletion is reflected immediately.

### T09 (Edge)
Create a team named "clean-team-multi-invite-01".
List all users and invite the first two users simultaneously (two invite_create calls).
List invites — verify both appear.
Delete both invites.
Delete the team.

---

## Organizations

### O01
List all organizations accessible to me. Report each org's displayName, domainName, and ID.

### O02
List all sub-organizations under the root organization (from organizations_list). Report the hierarchy (parent → children).

### O03
Get the details of the root organization (ID from organizations_list). Verify the response contains displayName, domainName, id, and parentId fields.

### O04
Search for organizations using a broad keyword ("org" or "auto"). Report all matching results with their displayName and domainName.

### O05
Get the sub-org report for the first sub-organization in the list. Report the full report content returned.

### O06
Create a sub-organization with displayName "clean-test-suborg-01" and domainName "clean-test-suborg-01" under the root organization (parentId from organizations_list). Retrieve the newly created sub-org by its ID. List sub-organizations to confirm it appears. Report the created org's ID.

### O07
List all organizations using organizations_list. Then call organizations_list again with the nested=true parameter (if supported). Compare whether the nested call returns additional hierarchy information.

### O08 (Negative)
Search for organizations using a keyword that will match nothing ("zzzzz-no-such-org-xyz-999"). Verify the response is an empty array, not an error.

### O09 (Negative)
Get organization details for a non-existent ID (00000000-0000-0000-0000-000000000099). Record the exact error. Expected: 404.

### O10 (Negative)
Create a sub-organization with displayName "" (empty string). Record the exact error. Expected: 400 validation error.

### O11 (Edge)
List sub-organizations for the root org. For each sub-organization, call organizations_suborg_report once. Verify each report call succeeds. Report the total number of sub-orgs and whether any report call failed.

---

## Components & Repositories

### CR01
List all services (components) in the organization. Report total count, each service name, and its associated organization.

### CR02
List all repositories. Report total count and a sample of repository names.

### CR03
Search repositories using a keyword from one of the repository names returned by repositories_list. Verify the search result includes at least one of those repositories.

### CR04
List all services. Pick the first one. List its branches. Report the branch names and count. Verify the response is an array (empty is acceptable).

### CR05
List all services. Pick a service that has at least one branch. List that service's branches and confirm there are two or more (if available). Retrieve the security findings summary for two different branches and compare the results.

### CR06
List all properties for the first available component (from services_list). Report each property name, type, and value.

### CR07
List all resources for the first available component with filterType "RESOURCE_TYPE_BRANCH". Report the resource IDs and names returned.

### CR08
List all controllers. Report each controller's name and type. Get data for the first controller in the list.

### CR09
List all available CloudBees actions. Report: total action count and a sample of 5 action display names.

### CR10
List all configured endpoints. Report each endpoint's name, type, and status.

### CR11
List all extensions available in the organization. Report each extension's name (empty list is acceptable).

### CR12
List all registered GitHub App registrations for the organization. Report each registration's name and status (empty list is acceptable).

### CR13
Trigger an SCM repositories sync for the organization. Record the exact response (success or async job reference). Note: an actual sync may take time; this test only verifies the call is accepted.

### CR14 (Negative)
List branches for a non-existent component ID (00000000-0000-0000-0000-000000000099). Record the exact error. Expected: 404 or 400.

### CR15 (Negative)
List all services. Search for a service name that does not exist ("xyzzy-no-match-component-99999"). Verify the result is empty, not an error.

### CR16 (Negative)
List properties for a non-existent component ID (00000000-0000-0000-0000-000000000099). Record the exact error. Expected: 404 or 400.

### CR17 (Negative)
List branches for a non-existent SCM endpoint (endpointId 00000000-0000-0000-0000-000000000099, using any repository URL). Record the exact error. Expected: 404 or 400.

### CR18 (Edge)
List all actions. Verify the response handles a large payload (if action count exceeds 100) without timeout. Report the total count and note whether the call completed within 30 seconds.

---

## Automation & Workflows

### AW01
List all automation jobs. Report total count, job names, and their associated components.

### AW02
List all workflows. Report each workflow's name and ID.

### AW03
List all workflows. Get the content of the first workflow. Report the full workflow definition (YAML or JSON).

### AW04
Get the workflow JSON schema. Report the top-level required fields defined in the schema.

### AW05
List all workflows. Validate the content of the first workflow. Report whether it is valid and any errors found.

### AW06
List all automation jobs. List recent runs for the first job. Report the run statuses, timestamps, and total count.

### AW07
List runs for the first automation job. Get the logs for the most recent run. Report the first 5 log entries.

### AW08
List all automation jobs. Trigger the first available job. Record the runId or trigger reference returned.

### AW09
List all automation jobs. Trigger the first job on its default branch. Record the runId returned.

### AW10
List all automation jobs. Trigger the first job. Record the runId. Immediately stop the triggered run. Verify the stop call returns success.

### AW11
List all automation jobs. Rerun the most recent completed run of the first job. Record the new runId.

### AW12
List all automation jobs. Check if any job has a pending manual gate. If one exists, approve it. If none exist, document that as the expected outcome. Confirm the response.

### AW12b
List all automation jobs. Check if any job has a pending manual gate. If one exists, reject it. If none exist, document that as the expected outcome. Confirm the response.

### AW13
List all workflows. Trigger the first workflow. Record the response (runId or trigger reference).

### AW14 (Negative)
Get workflow content for a non-existent workflow ID (00000000-0000-0000-0000-000000000099). Record the exact error. Expected: 404.

### AW15 (Negative)
Trigger a workflow with a non-existent ID (00000000-0000-0000-0000-000000000099). Record the exact error. Expected: 404.

### AW16 (Negative)
Attempt to approve a manual gate with a non-existent runId and gateId (both 00000000-0000-0000-0000-000000000099). Record the exact error. Expected: 404.

### AW17 (Negative)
Attempt to rerun a non-existent run ID (00000000-0000-0000-0000-000000000099) for the first automation job. Record the exact error. Expected: 404.

### AW18 (Negative)
Attempt to stop a non-existent run ID (00000000-0000-0000-0000-000000000099) for the first automation job. Record the exact error. Expected: 404.

### AW19 (Edge)
List all workflows. Add a comment "# clean-smoke-test" to the beginning of the first workflow's content and save it using workflow_update_content. Retrieve the content again and verify the comment appears. Report whether the update was persisted.

---

## Feature Flags — Core

### FF01
List all feature flag applications. Report each application's name and ID.

### FF02
List all feature flag environments. Report each environment's name and ID.

### FF03
Full Boolean flag lifecycle using the first available application and first available environment:
1. Create a Boolean flag named "clean-ff-bool-01-[today's date]".
2. Retrieve it by ID — verify flagType=Boolean and enabled=false by default.
3. Retrieve it by name — verify it matches the get-by-ID response.
4. List all flags in the application — verify the new flag appears.
5. Enable the flag in the first available environment.
6. Check flag usage per environment — document result (empty is expected for a new flag).
7. Disable the flag.
8. Delete the flag.
Report the result of every step.

### FF04
Full String flag lifecycle using the first available application and environment:
1. Create a String flag named "clean-ff-string-01-[today's date]".
2. Enable it in the first environment.
3. Update the flag's default value to "active".
4. Get the configuration and verify defaultValue was updated to "active".
5. Disable and delete the flag.

### FF05
Full custom properties lifecycle (all 3 types) using the first available application:
1. Create a Boolean custom property named "clean-prop-bool-[date]".
2. Create a String custom property named "clean-prop-string-[date]".
3. Create a Number custom property named "clean-prop-number-[date]".
4. List all custom properties — verify all 3 appear with their correct types.
5. Get the String property by ID — verify type=String.
6. Get the String property by name — verify data matches get-by-ID.
7. Check flag usage per environment for the String property — document result.
8. Check target group usage for the String property — document result.
9. Delete all 3 properties. Verify each deletion succeeds.

### FF06
Full target group lifecycle using the first available application:
1. Create a String custom property named "clean-tg-prop-[date]".
2. Create a target group named "clean-tg-01-[date]" with condition: property "clean-tg-prop-[date]" operator "eq" operands ["beta"].
3. Retrieve the group by ID — verify the condition was persisted correctly.
4. Retrieve the group by name — verify it matches get-by-ID.
5. List all target groups — verify the new group appears.
6. Check target group flag usage per environment — document result (empty is expected).
7. List all target groups with flags usage — verify the group appears with flagUsage=[].
8. Check overall target group usage — document result.
9. Delete the target group.
10. Delete the custom property.

### FF07
List all pending flag approval requests for the first available application. Report the count (empty is acceptable). Verify the response schema contains an items array.

### FF08
List all flags across all applications: for each application, list all its flags. Build an inventory: application name, flag count, flag names and types. Report which application has the most flags.

### FF09
List configurations for the first application and first environment using flags_configurations_list. Report the configuration fields returned for each flag entry.

### FF10
Get the configuration for any existing flag in the first application and environment using flag_configuration_get. Report all configuration fields.

### FF11
Set targeting conditions on a flag:
1. Create a String custom property named "clean-conditions-prop-[date]" in the first application.
2. Create a Boolean flag named "clean-ff-conditions-[date]" in the first application.
3. Create a target group named "clean-conditions-tg-[date]" with a property condition using "clean-conditions-prop-[date]" equals "beta".
4. Set targeting conditions on the flag for the first environment linking to the target group (flagValue=true).
5. Get the flag configuration and verify the conditions array contains the rule from step 4.
6. Clear conditions by calling flag_configuration_conditions_set with [].
7. Verify the configuration shows conditions=[].
8. Clean up: delete the target group, flag, and custom property.

### FF12
Serve a value to a target group:
1. Create a String custom property named "clean-serve-prop-[date]" in the first application.
2. Create a Boolean flag named "clean-ff-serve-[date]" in the first application.
3. Create a target group named "clean-serve-tg-[date]" with a property condition.
4. Call flag_serve_to_target_group with servedValue=true and enableIfDisabled=true for the first environment.
5. Get the flag configuration and verify enabled=true and the conditions contain the targeting rule.
6. Clean up all created resources.

### FF13 (Negative)
Create a Boolean flag named "clean-ff-duplicate-[date]" in the first application. Try to create a second flag with the exact same name. Record the exact error. Expected: 400 or 409. Delete the first flag.

### FF14 (Negative)
Create a Boolean flag named "clean-ff-update-bool-[date]". Enable it. Try to update its default value with defaultValue="true". Record the exact error. Disable and delete the flag.

### FF15 (Negative)
Delete a target group with a non-existent ID (00000000-0000-0000-0000-000000000099) in the first application. Record the exact error. Expected: 404 or 400.

### FF16 (Negative)
Look up a flag by name "this-flag-does-not-exist-xyz-999" in the first application. Record the exact response. Expected: 404.

### FF17 (Negative)
Look up a custom property by name "nonexistent-property-xyz-999" in the first application. Record the exact response. Expected: 404.

### FF18 (Negative)
List all feature flag applications. Pick two different applications (if available). Create a Boolean flag in the first application. Try to enable it using an environment that belongs to the second application (not the one the flag was created in). Record the exact error. Clean up: disable if enabled, delete the flag.

### FF19 (Negative)
Create a target group named "clean-tg-bad-op-[date]" in the first application with an invalid operator in the condition: {"property": {"name": "plan", "operator": "invalid_operator_xyz", "operands": ["beta"]}}. Record the exact error. Expected: 400. Clean up if the group was somehow created.

### FF20 (Edge)
Create a Boolean flag. Perform 4 consecutive enable/disable toggles, verifying the state after each toggle:
1. Enable → verify enabled=true
2. Disable → verify enabled=false
3. Enable → verify enabled=true
4. Disable → verify enabled=false
Delete the flag.

### FF21 (Edge)
Create a Boolean flag named "clean-ff-never-enabled-[date]". Do NOT enable it. Immediately delete it. Verify: deletion succeeds without requiring an explicit disable call first.

### FF22 (Edge)
Create a Boolean flag named "clean-ff-permanent-[date]" with labels=["test","permanent"] and isPermanent=true. Retrieve the flag and verify labels and isPermanent=true are persisted. Attempt to delete the flag. Record whether isPermanent blocks deletion or not. Clean up.

### FF23 (Edge)
Create a target group named "clean-tg-empty-[date]" with no conditions (omit conditions entirely). Retrieve and verify the saved conditions default (expected: anyOf=[]). Delete the group. This tests schema defaults for empty conditions.

### FF24 (Edge)
Create a target group named "clean-tg-cross-check-[date]". List all target groups (without usage). List all target groups with flags usage. Compare: verify the same group appears in both responses. Confirm the with-flags-usage response has a flagUsage field. Delete the group.

---

## RBAC

### RB01
List all available RBAC permissions for the organization. Report total count and all permission names.

### RB02
List all RBAC roles in the organization. Report each role's name, type (system vs custom), and description.

### RB03
Full RBAC role lifecycle:
1. List all roles to record baseline count.
2. Create a custom role named "clean-rbac-role-[date]".
3. Get the role by its ID — verify name and organizationId.
4. List roles — verify the new role appears.
5. Delete the role.
6. List roles — verify the role is gone.

### RB04
List all RBAC authorizations in the organization. Report total count and a sample of authorization entries.

### RB05
Create a custom role named "clean-rbac-authz-role-[date]". Use rbac_authorization_create to assign it to the current user (from whoami) in the organization. List authorizations and verify the new entry appears. Delete the role.

### RB06
Perform a bulk authorization check for the current user (from whoami) against the root organization. Use 3–5 permission names from rbac_permissions_list. Report which permissions are allowed and which are denied.

### RB07 (Negative)
Get a role with a non-existent ID (00000000-0000-0000-0000-000000000099). Record the exact error. Expected: 404.

### RB08 (Negative)
Delete a role with a non-existent ID (00000000-0000-0000-0000-000000000099). Record the exact error. Expected: 404 or 400.

### RB09 (Edge)
List all roles. Take the first role. List all roles again and get the same role by ID. Compare the data from list vs get — verify all fields are consistent.

### RB10 (Negative)
Create a role with empty name "". Record the exact error. Expected: 400 validation error.

### RB11 (Negative)
Create a role named "clean-rbac-dup-[date]". Then try to create a second role with the exact same name. Record the exact error from the second call. Expected: 409 or 400 (duplicate). Delete the first role.

### RB12 (Negative)
Create an authorization with a non-existent roleId (00000000-0000-0000-0000-000000000099) using the current user's ID from whoami. Record the exact error. Expected: 404.

### RB13 (Negative)
Perform a bulk authorization check using fabricated permission names that don't exist ("fake.permission.xyz", "does.not.exist.abc"). Record whether the server returns an error or allowed=false for each unknown permission.

### RB14 (Negative)
List RBAC authorizations for a non-existent organization ID (00000000-0000-0000-0000-000000000099). Record the exact error. Expected: 404 or 403.

### RB15 (Negative)
List RBAC permissions for a non-existent organization ID (00000000-0000-0000-0000-000000000099). Record the exact error. Expected: 404 or 403.

### RB16 (Edge)
List all roles. For each role (up to 10), call rbac_role_get. Verify every roleId from the list is fetchable individually. Report any data inconsistency between list and get responses.

### RB17 (Edge)
Create 3 roles: "clean-rbac-alpha-[date]", "clean-rbac-beta-[date]", "clean-rbac-gamma-[date]". List all roles and verify all three appear. Delete all three. List roles again and verify none appear.

---

## Security

### SEC01
List all services (components) in the organization. Pick the first component that has a non-empty default branch. List its branches to get the default branch ID. Get the security findings summary. Report: total findings, severity breakdown (VERY_HIGH / HIGH / MEDIUM / LOW), scanner tools, and lastScanned timestamp.

### SEC02
Using the component identified in SEC01: get all open security issues. Report: total count, severity distribution, and a sample of 3 issue names with their SLA status.

### SEC03
Get all security issues (open and resolved) for the root organization (subOrganizationId from organizations_list). Report total findings and which components are included.

### SEC04
Get the security findings summary and then get open issues for the same component. Compare counts.total from the summary against the number of items in the open issues list. Report any discrepancy. This validates data consistency between the two endpoints.

### SEC05
List all feature flag applications. Get the security filter tools for the first application. Report each tool's name and ID. Call again with includeInDev=true and compare whether additional tools appear.

### SEC06
List all feature flag applications. Get the security filters for the first application. Verify the response contains environment, severity, and SLA filter entries. Report the complete list grouped by type.

### SEC07 (Negative)
Get security findings summary with a non-existent component ID (00000000-0000-0000-0000-000000000099). Use the root organizationId and any real endpointId (from endpoint_list). Record the exact error. Expected: 404 or 400.

### SEC08 (Negative)
Get security findings summary for a valid component but a non-existent branch ID (00000000-0000-0000-0000-000000000099). Record the exact error. Expected: 404 or 400.

### SEC09 (Negative)
Get all security issues for a non-existent sub-org ID (00000000-0000-0000-0000-000000000099). Record the exact error. Expected: 404.

### SEC10 (Negative)
Get security filter tools with a non-existent application ID (00000000-0000-0000-0000-000000000099). Record the exact error. Expected: 404 or 400.

### SEC11 (Negative)
Get security findings summary without providing all required parameters (omit subOrganizationId, endpointId, and branchId — provide only componentId). Record the exact error. Document whether it is a client-side validation error or a server-side error.

### SEC12 (Edge)
Get open security issues for the first component with findings. Filter all issues where sla.status = "BREACHED". Report: count of breached-SLA issues and which vulnerability has been breached the longest.

### SEC13 (Edge)
Get the security findings summary for a component scanned by multiple tools. Report how many scanners are in the tools array. For each scanner, report its name and findings count. Calculate what percentage of total findings each scanner contributes.

---

## Security Advanced (Config, SLA, Plugins)

### SA01
Get the security configuration for the root organization. Report all configuration fields and their current values.

### SA02
Get the security configuration hierarchy for the root organization. Report the hierarchy structure returned.

### SA03
Get the current security configuration. Record the current values. Update one boolean field with its current value (no-op to verify write works). Get the configuration again and verify no unintended changes occurred.

### SA04
Get the SLA configuration for the root organization. Report the severity windows (LOW, MEDIUM, HIGH, VERY_HIGH) in days.

### SA05
Get the current SLA configuration. Set the LOW severity SLA window to 90 days. Get the SLA configuration again to verify the change was applied.

### SA06
List security filter tools for the first available application. Get the plugin configuration for the first plugin returned. Report the plugin name and all configuration fields.

### SA07
Enable implicit security scans for the root organization. Record the response and report whether the call succeeded.

### SA08 (Negative)
Get the security configuration with a non-existent organization ID (00000000-0000-0000-0000-000000000099). Record the exact error. Expected: 404 or 403.

### SA09 (Negative)
Get SLA configuration with a non-existent organization ID (00000000-0000-0000-0000-000000000099). Record the exact error. Expected: 404 or 403.

### SA10 (Edge)
Get the security configuration hierarchy. Compare the hierarchy result against the flat get result (security_configuration_get). Verify the hierarchy includes at least as much information as the flat call. Report any fields present in hierarchy but not in the flat config.

### SA11 (Negative)
Get plugin config for a non-existent plugin name "fake-scanner-plugin-xyz" in the root org. Record the exact error. Expected: 404.

### SA12 (Negative)
Activate a plugin with name "fake-scanner-plugin-xyz" in the root org. Record the exact error. Expected: 404.

### SA13 (Negative)
Deactivate a plugin that is not active. Use a known inactive plugin name or "fake-scanner-plugin-xyz". Record whether it returns 404, 400, or is idempotent.

### SA14 (Negative)
Remove SLA configuration for a sub-organization that has no custom SLA set. Record whether the server returns 404, 200 (idempotent), or another status.

### SA15 (Negative)
Set security configuration with an invalid value (e.g., a numeric threshold set to -1). Record the exact error. Expected: 400 with validation details.

### SA16 (Negative)
Remove tenant SLA configuration for a non-existent org ID (00000000-0000-0000-0000-000000000099). Record the exact error. Expected: 404 or 403.

### SA17 (Edge)
Set SLA config with explicit values for all severity levels (VERY_HIGH: 1 day, HIGH: 7 days, MEDIUM: 30 days, LOW: 90 days). Immediately read it back. Verify all four values match. Restore original values.

### SA18 (Edge)
Set a custom SLA for the first sub-organization. Remove that custom SLA. Get the SLA config and verify it reverted to inherited/default values.

### SA19 (Edge)
Activate a plugin. Update its config with a test value. Get the config back and verify the updated value persisted. Report the before/after values.

### SA20 (Edge)
Update the same security configuration field twice in sequence with different values (A then B). Get config after both writes. Verify the final value is B (last-write-wins). Restore original value.

---

## Services & Endpoints

### SE01
List all services in the organization. Report total count, service names, and their associated organizations.

### SE02
Full service lifecycle:
1. Create a service named "clean-service-[date]".
2. Get the service by its ID — verify name and organizationId.
3. Delete the service.
4. Attempt to get the deleted service — verify it returns 404.

### SE03
List all configured endpoints. Report each endpoint's name, type, and status.

### SE04
Add a new GitHub endpoint named "clean-endpoint-[date]" for the root organization (use placeholder credentials). Record the response — success or error if credentials are required.

### SE05
Prepare an SCM connector for the root organization using GitHub as the provider. Record the OAuth URL or setup object returned.

### SE06 (Negative)
Attempt to get a service with a non-existent service ID (00000000-0000-0000-0000-000000000099). Record the exact error. Expected: 404.

### SE07 (Negative)
Attempt to delete a service with a non-existent ID (00000000-0000-0000-0000-000000000099). Record the exact error. Expected: 404.

### SE08 (Edge)
List all services. Create a service named "clean-service-dup-[date]". Attempt to create another service with the exact same name. Record whether the server allows duplicates or returns a conflict error. Clean up both services if created.

### SE09 (Negative)
Add a service with an empty name "". Record the exact error. Expected: 400 validation error.

### SE10 (Negative)
Add an endpoint with an invalid/fake provider contributionType "cb.fake-provider.fake-type". Record the exact error. Expected: 400 or 422.

### SE11 (Negative)
Prepare an SCM connector with an invalid provider type "invalid-scm-provider-xyz". Record the exact error. Expected: 400 or 422.

### SE12 (Negative)
Get the ticketing webhook URL for a non-existent org ID (00000000-0000-0000-0000-000000000099). Record the exact error. Expected: 404 or 403.

### SE13 (Edge)
Create a service. Get it by ID to confirm it exists. Delete it. Attempt to get it again by the same ID. Verify step 4 returns 404. Confirms deletes are immediately enforced.

### SE14 (Edge)
Call endpoint_scm_connector_prepare twice for the root org — once for "github" and once for "gitlab" (or "bitbucket"). Compare the two responses. Report whether the response structure differs per SCM type.

### SE15 (Edge)
List all services. Create a service named "clean-service-dup-edge-[date]". Attempt to create a second service with the exact same name. Record whether the server returns 409 conflict, 400, or allows duplicates. Clean up.

### SE16 (Edge)
Create 3 services: "clean-svc-alpha-[date]", "clean-svc-beta-[date]", "clean-svc-gamma-[date]". List all services and verify all three appear. Delete all three. List services again to confirm all three are gone.

---

## Search, Properties & Resources

### SP01
Search for resources in the root organization using a broad keyword (try "go" or "auto"). Report the matching resources returned.

### SP02
Search for pipeline runs in the root organization using a status filter (e.g., status=SUCCESS) or a date range for the past 7 days. Report the runs returned.

### SP03
List all properties for the first available component (from services_list). Report each property's name, type, and value.

### SP04
Full property lifecycle for the first available component:
1. List existing properties to establish a baseline.
2. Add a String property "CLEAN_TEST_PROP" with value "clean-value".
3. Get the property by its ID — verify name and value.
4. Delete the property.
5. Verify it no longer appears in the properties list.

### SP05
List resources for the first available component with filterType "RESOURCE_TYPE_BRANCH". Get the details of the first resource by its resource ID. Report all resource fields returned.

### SP06 (Negative)
Get a property with a non-existent property ID (00000000-0000-0000-0000-000000000099) for the first available component. Record the exact error. Expected: 404.

### SP07 (Negative)
Search for resources using a keyword that will return no results ("xyzzy-no-match-resource-99999"). Verify the response is an empty array, not an error.

### SP08 (Negative)
Search runs with an invalid date format: startDate="not-a-date", endDate="also-not-a-date". Record the exact error. Expected: 400 Bad Request. Document whether it is client-side or server-side validation.

### SP09 (Negative)
Get a property with a non-existent propertyId (00000000-0000-0000-0000-000000000099) for the first available component. Record the exact error. Expected: 404.

### SP10 (Negative)
Delete a property with a non-existent propertyId (00000000-0000-0000-0000-000000000099) for the first available component. Record the exact error. Expected: 404.

### SP11 (Negative)
Add a property to the first available component with an empty name "". Record the exact error. Expected: 400 or client-side schema validation.

### SP12 (Negative)
Get a resource with a non-existent resourceId (00000000-0000-0000-0000-000000000099). Record the exact error. Expected: 404.

### SP13 (Edge)
Search resources with a broad wildcard query. Then search again with a more specific term (a substring of one known component name). Compare: the specific search should return a subset of the broad search results. Report both counts.

### SP14 (Edge)
Search runs filtered by status=SUCCESS. Search runs filtered by status=FAILURE. Verify no run appears in both lists (mutually exclusive). Report the count for each status.

### SP15 (Edge)
Add a property "CLEAN_SP_E_PROP_[date]" to the first available component. Delete it. Attempt to get it by the same propertyId. Verify 404 is returned. Confirms property deletes are immediately enforced.

### SP16 (Edge)
List all resources for the first available component. For each resource (up to 10), call resources_get by its ID. Verify every resourceId from the list is fetchable. Report any resource that fails to load individually.

---

## API Tokens, SAML & Reports

### AT01
List all API tokens. Report the count and token names (masked values are acceptable). Report whether any token is expired.

### AT02
List all SAML connections for the organization. Report each connection's name and status (empty list is acceptable).

### AT03
List all SAML email domains for the organization. Report the domains configured (empty list is acceptable).

### AT04
Get a drill-down report for security findings using the root organization. Report the data structure returned.

---

## Tool Chains

### TC01 — Full Identity Snapshot
```
Discover who I am (whoami). Get my user preferences. List all teams and identify which ones contain my userId. List all API tokens. List all sub-organizations. Present a complete identity snapshot: my profile, preferences, team memberships, token count, and the org hierarchy.
```

### TC02 — Organization Hierarchy with CI Metrics
```
List all sub-organizations. Build a hierarchy tree. For the root org and each direct child sub-org, get the sub-organization report. Present the org hierarchy alongside its report data.
```

### TC03 — Team Membership Audit
```
List all users. List all teams. For each user, identify which teams they belong to. Highlight users who are only in predefined system teams (type=PREDEFINED) but no user-defined teams (type=USERDEFINED).
```

### TC04 — Security Findings Leaderboard
```
List all services (components). For each component that has a branch, get its security findings summary. Rank all components by total findings descending, and separately by VERY_HIGH findings. Report a leaderboard table: rank, component name, VERY_HIGH, HIGH, MEDIUM, LOW, total, lastScanned.
```

### TC05 — SLA Breach Report
```
Pick the first component with findings from services_list. Get its open security issues. Filter all issues where sla.status="BREACHED". For each breached issue report: name, severity, first identified date, SLA due date, and days overdue. Sort by most overdue first.
```

### TC06 — Multi-Branch Security Comparison
```
List all services. Find a component that has at least 2 branches (from branches_list). Get the security findings summary for each branch separately. Compare: total findings per branch, severity distribution, and which branch is more secure.
```

### TC07 — Scanner Coverage Audit
```
List all services. For each component with a valid branch, get its security findings summary. Extract the scanner tools array from each summary. Build a matrix: which scanners are used by which components. Report: (1) components with only 1 scanner, (2) components with the most scanners, (3) most common scanners.
```

### TC08 — Feature Flag Health Check
```
List all feature flag applications. For each application, list all flags. For each flag, list its configurations across environments. Build a health summary: total flags per app, how many are enabled per environment, how many are disabled, and any orphaned flags with zero configurations.
```

### TC09 — Flag Usage Audit
```
List all feature flag applications. For each application, list all flags. For each flag, check usage per environment. Find all flags with zero usage across all environments. These are creation-only flags that are never evaluated. List them by application.
```

### TC10 — Target Group Blast Radius
```
List all feature flag applications. For each application, list all target groups with flags usage. Find the target group referenced by the most flags (highest blast radius). Check its per-environment usage. Report: target group name, count of flags using it, which environments it affects.
```

### TC11 — Custom Properties Coverage
```
List all feature flag applications. For each application, list all custom properties. Build a coverage report: which applications have custom properties, how many each has, what types, and which have none (potential targeting gap).
```

### TC12 — Full Team Lifecycle (clean)
```
List all users and pick the first active user who is not the current user (from whoami). Create a team named "clean-tc12-team-[date]". Invite the selected user by email. List pending invites and verify the invite appears. Delete the invite. Add the user as a direct member. Get the team by ID and verify the user appears in userIds. Attempt to remove the user. Delete the team. Report every step result.
```

### TC13 — Full CI/CD Pipeline Lifecycle
```
List all automation jobs and pick the first one that has recent runs. Trigger it. Record the runId. List recent runs and confirm the new run appears. Get logs for the run. Rerun it. Record the new runId. Stop the rerun. Report: original runId, new runId, whether the run appeared in listings, and stop response.
```

### TC14 — Full Workflow Lifecycle
```
List all workflows. Get the content of the first workflow. Get the workflow schema. Validate the content. Add a comment "# clean-tc14-[date]" to the top and save it. Retrieve the content again to confirm the comment persists. Trigger the workflow. Restore the original content. Report every step.
```

### TC15 — Full Feature Flag Write Lifecycle
```
List all applications and environments. Pick the first of each. Create a String flag named "clean-tc15-flag-[date]". Get it by name. List its configurations. Get the config for the first environment. Enable the flag. Update the default value to "enabled". Get the config and verify the update. Disable the flag. Delete it. Report every write step result.
```

### TC16 — Full RBAC Lifecycle
```
List all permissions. Create a role named "clean-tc16-role-[date]". Get the role by ID. Create an authorization assigning this role to the current user (from whoami). List all authorizations and confirm the new entry appears. Perform a bulk permission check for the current user. Delete the role. Report every step.
```

### TC17 — SAML & Auth Configuration Audit
```
List all SAML connections. List all SAML email domains. List all API tokens. List all users. Compile an authentication summary: is SAML enabled, which domains are SAML-managed, how many API tokens are active, total user count.
```

### TC18 — Orphaned Repository Report
```
List all repositories. List all services (components). Cross-reference: find repositories where no component is linked (serviceId is empty or absent). Group results by SCM endpoint. Report: count of orphaned repos per endpoint and their names.
```

### TC19 — Component Property Inheritance Audit
```
List all services. For each component, list its properties. Identify: (1) components with their own component-level properties, (2) components that only inherit org-level properties, (3) components with no properties at all. List any secret properties (isSecret=true) by name only (never value).
```

### TC20 — Cross-Domain: Organization Health Dashboard
```
Call in sequence: whoami (confirm auth), list sub-organizations (count and structure), list all users (total count), list all teams (team count and types), list all components (total, how many have a branch), get security findings summary for up to 5 components (aggregate total findings), list API tokens (active count), list SAML connections (is SSO enabled). Present a single-page health card with all metrics.
```

---
