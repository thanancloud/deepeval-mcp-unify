# CloudBees Unify MCP — Write Tools Test Prompts

All 47 write (W) tools across all domains.
Every prompt discovers required IDs at runtime via read tools before performing mutations.
Cross-domain: write tests use read tools from other domains to set up context.
Lifecycle tests clean up after themselves (create → verify → delete).
Nil UUID for negative tests: `00000000-0000-0000-0000-000000000099`.

**Total W tools: 47**
Domains: access-management (10) · application-security (8) · applications-components (1) · feature-management (10) · organization-administration (7) · policy-engine (3) · workflows (8)

---

## Section 1 — Access Management — Write (10 tools)

### W-AM01
**Tool:** `user_set_timezone`
Call user_whoami to get my userId. Then call user_set_timezone to set my timezone to "UTC". Verify the response confirms success. Then set it back to "America/New_York" as cleanup.

### W-AM02 (Negative)
**Tool:** `user_set_timezone`
Call user_set_timezone with an invalid timezone value "Not/AReal_Zone". Record the exact error. Expected: 400 validation error.

### W-AM03
**Tool:** `teams_create`
Call organizations_list to get an org ID. Create a team named "write-test-team-01" in that org. Report the returned teamId, name, and created timestamp. Then delete the team as cleanup.

### W-AM04 (Negative)
**Tool:** `teams_create`
Attempt to create a team with an empty name (name=""). Record the exact error. Expected: 400 validation error.

### W-AM05
**Tool:** `teams_delete`
Create a team named "write-test-delete-01" using teams_create. Then immediately delete it using teams_delete. Verify deletion by calling teams_get_by_id — it must return 404.

### W-AM06 (Negative)
**Tool:** `teams_delete`
Call teams_delete with a nil team ID (00000000-0000-0000-0000-000000000099). Record the exact error. Expected: 404.

### W-AM07
**Tool:** `teams_invite_create`
Full invite lifecycle:
1. Call organizations_list to get an org ID.
2. Create a team named "write-test-invite-01".
3. Call users_list to find an active user's email.
4. Invite that user using teams_invite_create.
5. Verify the invite appears in teams_invites_list.
6. Delete the invite using teams_invite_delete.
7. Verify the invite no longer appears in teams_invites_list.
8. Delete the team.
Report the outcome of each step.

### W-AM08
**Tool:** `teams_invite_delete`
(Covered in W-AM07 step 6. Run as standalone:)
Create a team "write-test-invite-del-01". Invite a user from users_list. Confirm the invite exists via teams_invites_list. Delete it via teams_invite_delete. Confirm it is gone. Delete the team.

### W-AM09
**Tool:** `teams_members_add`
Full member lifecycle:
1. Call organizations_list to get an org ID.
2. Create a team named "write-test-members-01".
3. Call users_list to get the first active user's ID.
4. Add that user to the team using teams_members_add.
5. Verify the user appears in teams_memberships_list.
6. Remove the user using teams_members_remove.
7. Verify the user no longer appears in teams_memberships_list.
8. Delete the team.
Report the outcome of each step.

### W-AM10
**Tool:** `teams_members_remove`
(Covered in W-AM09 step 6. Run as standalone:)
Create a team "write-test-remove-01". Add a user from users_list. Confirm membership. Remove via teams_members_remove. Confirm removal. Delete the team.

### W-AM11 (Negative)
**Tool:** `teams_members_add`
Create a team "write-test-add-neg-01". Attempt to add a non-existent user ID (00000000-0000-0000-0000-000000000099). Record the exact error. Delete the team.

### W-AM12
**Tool:** `rbac_role_create`
Call organizations_list to get an org ID. Create a new RBAC role named "write-test-role-01" with a description "Temporary test role". Report the returned roleId and name. Then delete the role using rbac_role_delete as cleanup.

### W-AM13 (Negative)
**Tool:** `rbac_role_create`
Attempt to create a role with an empty name. Record the exact error. Expected: 400 validation error.

### W-AM14
**Tool:** `rbac_role_delete`
Call rbac_role_create to create a role named "write-test-role-del-01". Then immediately delete it using rbac_role_delete. Verify by calling rbac_role_get — it must return 404.

### W-AM15 (Negative)
**Tool:** `rbac_role_delete`
Call rbac_role_delete with a nil ID (00000000-0000-0000-0000-000000000099). Record the exact error. Expected: 404.

### W-AM16
**Tool:** `rbac_authorization_create`
Call organizations_list to get an org ID. Call users_list to get a user. Call rbac_roles_list to get a role ID. Then call rbac_authorization_create to grant that role to the user on the org resource. Report the returned authorization ID. Then verify via rbac_authorizations_list that it appears.

---

## Section 2 — Application Security — Write (8 tools)

### W-SEC01
**Tool:** `security_configuration_set`
Call organizations_list to get an org ID. Call security_configuration_get to read the current config. Then call security_configuration_set to update a non-critical field. Verify the change via a subsequent security_configuration_get. Restore the original value.

### W-SEC02
**Tool:** `security_implicit_scans_set`
Call services_list to get a component ID. Enable implicit scans for that component using security_implicit_scans_set (enabled=true). Verify via security_configuration_get. Then disable again (enabled=false) as cleanup.

### W-SEC03
**Tool:** `security_plugin_activate`
Call organizations_list to get an org ID. Call security_plugin_config_get to find a plugin that is currently inactive. Activate it using security_plugin_activate. Verify activation via security_plugin_config_get. Then deactivate it using security_plugin_deactivate as cleanup.

### W-SEC04
**Tool:** `security_plugin_deactivate`
(Covered in W-SEC03 cleanup. Run as standalone:)
Call security_plugin_config_get on the org to find an active plugin. Deactivate it using security_plugin_deactivate. Verify via security_plugin_config_get. Re-activate it using security_plugin_activate.

### W-SEC05
**Tool:** `security_plugin_config_set`
Call organizations_list to get an org ID. Call security_plugin_config_get to find a plugin and its current configuration. Update a config value using security_plugin_config_set. Verify the change via security_plugin_config_get. Restore the original value.

### W-SEC06
**Tool:** `security_sla_configuration_set`
Call organizations_list to get an org ID. Call security_sla_configuration_get to read current SLA config. Set a new SLA configuration using security_sla_configuration_set. Verify via security_sla_configuration_get. Then remove the override using security_sla_configuration_remove.

### W-SEC07
**Tool:** `security_sla_configuration_remove`
Call services_list to get a component ID. Call security_sla_configuration_set to first set a component-level SLA override. Verify it is set. Then remove it using security_sla_configuration_remove. Verify removal via security_sla_configuration_get — the component should now inherit from parent.

### W-SEC08
**Tool:** `security_tenant_sla_configuration_remove`
Call organizations_list to get the root tenant org ID. Call security_sla_configuration_get to check if a tenant-level override exists. If it does, call security_tenant_sla_configuration_remove. Verify the tenant and all children now inherit defaults. If no override existed, record "No tenant SLA override to remove — test skipped (precondition not met)".

---

## Section 3 — Applications & Components — Write (1 tool)

### W-AC01
**Tool:** `scm_repositories_sync`
Call organizations_list to get an org ID. Call scm_gh_app_registrations_list to confirm an SCM integration exists. Then call scm_repositories_sync for that org to trigger an async repository sync. Report the response (job ID or status). Call repositories_list before and after a short wait to verify the sync was initiated.

### W-AC02 (Negative)
**Tool:** `scm_repositories_sync`
Call scm_repositories_sync with a nil org ID (00000000-0000-0000-0000-000000000099). Record the exact error. Expected: 404 or 400.

---

## Section 4 — Feature Management — Write (10 tools)

### W-FM01
**Tool:** `flags_add`
Full flag lifecycle:
1. Call flags_applications_list to get an app ID.
2. Create a Boolean feature flag named "write-test-flag-bool-01" using flags_add.
3. Verify via flags_get that the flag exists with correct name and type.
4. Delete the flag using flags_delete.
5. Verify deletion via flags_get — must return 404.
Report outcome of each step.

### W-FM02
**Tool:** `flags_add` (String type)
Call flags_applications_list to get an app ID. Create a String flag named "write-test-flag-str-01" with default value "default-value". Verify via flags_get. Delete the flag.

### W-FM03
**Tool:** `flags_delete`
(Covered in W-FM01. Run as standalone:)
Create a Boolean flag named "write-test-flag-del-01". Confirm it exists. Delete via flags_delete. Confirm deletion via flags_get — must return 404.

### W-FM04 (Negative)
**Tool:** `flags_delete`
Call flags_delete with a nil flag ID (00000000-0000-0000-0000-000000000099). Record the exact error. Expected: 404.

### W-FM05
**Tool:** `flags_update_defaultValue`
Call flags_list to find an existing Boolean flag. Update its default value using flags_update_defaultValue (toggle between true and false). Verify the change via flags_get. Restore the original default value.

### W-FM06 (Negative)
**Tool:** `flags_update_defaultValue`
Call flags_list to find a Boolean flag. Attempt to set its default value to an invalid type (e.g., send a Number value for a Boolean flag). Record the exact error. Expected: 400 (Known Bug #4).

### W-FM07
**Tool:** `flags_configuration_state_update`
Call flags_applications_list → flags_environments_list to get an environment. Call flags_list to get a flag ID. Disable the flag in that environment using flags_configuration_state_update (enabled=false). Verify via flags_configurations_list. Re-enable it (enabled=true). Verify again.

### W-FM08
**Tool:** `flag_configuration_conditions_set`
Call flags_applications_list → flags_environments_list to get env ID. Get a flag ID from flags_list. Replace the targeting-rule conditions for that flag in that environment using flag_configuration_conditions_set (can set an empty rules list to clear all rules). Verify via flag_configuration_get. Restore original conditions if they existed.

### W-FM09
**Tool:** `flag_serve_to_target_group`
Call flags_applications_list to get an app. Call flag_target_groups_list to get a target group. Call flags_list to get a Boolean flag and flags_environments_list for an environment. Call flag_serve_to_target_group to serve value=true to that target group for the flag in the environment. Verify via flag_configuration_get.

### W-FM10
**Tool:** `flag_target_groups_add`
Full target group lifecycle:
1. Call flags_applications_list to get an app ID.
2. Create a target group named "write-test-tg-01" using flag_target_groups_add.
3. Verify via flag_target_groups_get_by_name.
4. Delete it using flag_target_groups_delete.
5. Verify deletion via flag_target_groups_get — must return 404.
Report outcome of each step.

### W-FM11
**Tool:** `flag_target_groups_delete`
(Covered in W-FM10. Run as standalone:)
Create a target group "write-test-tg-del-01". Confirm existence. Delete via flag_target_groups_delete. Confirm deletion via flag_target_groups_get — must return 404.

### W-FM12 (Negative)
**Tool:** `flag_target_groups_delete`
Call flag_target_groups_delete with a nil ID (00000000-0000-0000-0000-000000000099). Record the exact error. Expected: 404.

### W-FM13
**Tool:** `flag_custom_properties_add`
Full custom property lifecycle:
1. Call flags_applications_list to get an app ID.
2. Add a custom property named "write-test-prop-01" using flag_custom_properties_add.
3. Verify via flag_custom_properties_get_by_name.
4. Delete it using flag_custom_properties_delete.
5. Verify deletion via flag_custom_properties_get — must return 404.
Report outcome of each step.

### W-FM14
**Tool:** `flag_custom_properties_delete`
(Covered in W-FM13. Run as standalone:)
Create a custom property "write-test-prop-del-01". Confirm existence. Delete via flag_custom_properties_delete. Confirm deletion.

---

## Section 5 — Organization Administration — Write (7 tools)

### W-OA01
**Tool:** `organizations_create`
Call organizations_list to get the root org ID. Create a sub-organization with displayName "write-test-suborg-01" and domainName "write-test-suborg-01" under the root. Report the returned id and displayName. Verify via organizations_get. Note: manual cleanup may be required as sub-org deletion is not covered by a delete tool.

### W-OA02 (Negative)
**Tool:** `organizations_create`
Attempt to create an organization with an empty displayName. Record the exact error. Expected: 400 validation error.

### W-OA03
**Tool:** `services_add`
Call organizations_list to get an org ID. Create a new service (component) named "write-test-service-01" using services_add. Report the returned serviceId. Verify via services_get. Then delete it using services_delete as cleanup.

### W-OA04
**Tool:** `services_delete`
(Covered in W-OA03 cleanup. Run as standalone:)
Create a service "write-test-svc-del-01" via services_add. Confirm via services_get. Delete via services_delete. Confirm deletion via services_get — must return 404.

### W-OA05 (Negative)
**Tool:** `services_delete`
Call services_delete with a nil service ID (00000000-0000-0000-0000-000000000099). Record the exact error. Expected: 404.

### W-OA06
**Tool:** `properties_add`
Call services_list to get a component ID. Add a property named "write-test-prop-key" with value "write-test-value" to that component using properties_add. Verify via properties_get that the property appears. Then delete it using property_delete.

### W-OA07
**Tool:** `property_delete`
(Covered in W-OA06 cleanup. Run as standalone:)
Add a property "write-test-del-key" = "del-value" to a component via properties_add. Confirm via properties_get. Delete via property_delete. Confirm it no longer appears in properties_get.

### W-OA08 (Negative)
**Tool:** `property_delete`
Call property_delete for a property name "nonexistent-property-xyz-999" on a real resource. Record the exact error. Expected: 404.

### W-OA09
**Tool:** `endpoint_add`
Call organizations_list to get an org ID. Add a new endpoint (e.g., a notification channel) using endpoint_add. Report the returned endpoint ID and type. Verify via endpoint_list. Note cleanup: delete the endpoint if a delete endpoint tool is available (otherwise note it in Behavioral Notes).

### W-OA10
**Tool:** `endpoint_scm_connector_prepare`
Call organizations_list to get an org ID. Call endpoint_scm_connector_prepare to initiate a new GitHub App SCM connector. Report the returned redirect URL and pending state. Note: this is a two-step process; the redirect URL is what the user would visit to complete the GitHub App installation.

---

## Section 6 — Policy Engine — Write (3 tools)

### W-PE01
**Tool:** `policies_create`
Full policy lifecycle:
1. Call organizations_list to get an org ID.
2. Call policies_get_schema to get the current policy schema.
3. Create a minimal valid policy YAML using policies_create (name: "write-test-policy-01", description: "Test policy").
4. Verify via policies_get that the policy exists.
5. Update the description using policies_update.
6. Verify the update via policies_get.
7. Delete the policy using policies_delete.
8. Verify deletion via policies_get — must return 404.
Report outcome of each step.

### W-PE02
**Tool:** `policies_update`
Call policies_list to find an existing policy. Read it via policies_get. Update its YAML definition using policies_update (change the description field). Verify the change via policies_get. Restore the original definition.

### W-PE03 (Negative)
**Tool:** `policies_update`
Call policies_update with a nil policy ID (00000000-0000-0000-0000-000000000099). Record the exact error. Expected: 404.

### W-PE04
**Tool:** `policies_delete`
(Covered in W-PE01 step 7. Run as standalone:)
Create a policy "write-test-policy-del-01" via policies_create. Confirm via policies_get. Delete via policies_delete. Confirm deletion — must return 404.

### W-PE05 (Negative)
**Tool:** `policies_create`
Attempt to create a policy with invalid YAML (malformed content). Record the exact error. Expected: 400 validation error.

---

## Section 7 — Workflows — Write (8 tools)

### W-WF01
**Tool:** `automation_trigger`
Call services_list to get a component. Call repositories_list to get a workflow repository URL. Call workflow_list to get a workflow branch. Then call automation_trigger with the component ID, workflow repository URL, target branch ref, and workflow branch ref. Report the returned run ID. Verify the run appears in search_runs.
**Note:** Requires a component with a connected repository. Skip with note if none available.

### W-WF02
**Tool:** `automation_trigger_by_branch`
Call services_list to get a component. Call workflow_list to get a workflow file name and branch name. Then call automation_trigger_by_branch with the component ID, branch name, and workflow file name. Report the returned run ID. Verify via runs_list.
**Note:** Requires a component with a workflow file. Skip with note if none available.

### W-WF03
**Tool:** `workflow_trigger`
Call services_list to get a component. Call workflow_list to get a workflow ID. Call workflow_trigger for that component and workflow. Report the returned run ID. Verify via runs_list.
**Note:** Skip if no triggerable workflow exists.

### W-WF04
**Tool:** `automation_stop`
Call search_runs to find a currently running run (status=RUNNING). Stop it using automation_stop. Verify the run transitions to STOPPED or CANCELLED via search_runs.
**Note:** If no running run exists, trigger one via automation_trigger_by_branch first, then stop it.

### W-WF05
**Tool:** `automation_rerun`
Call search_runs to find a recently completed or failed run. Re-run it using automation_rerun. Report the new run ID. Verify it appears in search_runs as a new run.
**Note:** Skip with note if no suitable run exists.

### W-WF06
**Tool:** `automation_approve_manual_gate`
Call automation_pending_tasks_list to find a pending manual gate approval. Approve it using automation_approve_manual_gate. Verify via automation_pending_tasks_list that it no longer appears.
**Note:** If no manual gate is pending, record "No pending manual gates — test skipped (precondition not met)".

### W-WF07
**Tool:** `automation_reject_manual_gate`
Call automation_pending_tasks_list to find a pending manual gate approval. Reject it using automation_reject_manual_gate. Verify via automation_pending_tasks_list that it no longer appears.
**Note:** If no manual gate is pending, record "No pending manual gates — test skipped (precondition not met)".

### W-WF08
**Tool:** `workflow_update_content`
Call services_list to get a component. Call workflow_list to get a workflow. Read the current YAML content via workflow_get_content. Update the content using workflow_update_content (add a comment or change description). Validate the new content via workflow_validate before saving. Verify the change via workflow_get_content. Restore the original content.

### W-WF09 (Negative)
**Tool:** `workflow_update_content`
Call workflow_update_content with a nil workflow ID (00000000-0000-0000-0000-000000000099). Record the exact error. Expected: 404.

### W-WF10 (Negative)
**Tool:** `workflow_update_content`
First call workflow_validate to confirm the content is invalid YAML: "this: is: : invalid:::". Then attempt workflow_update_content with that same invalid YAML. Record the exact error. Expected: 400 validation error.
