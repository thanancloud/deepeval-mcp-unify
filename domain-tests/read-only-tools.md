# CloudBees Unify MCP — Read-Only Tools Test Prompts

All 84 read-only (R) tools across all domains.
Prompts resolve IDs at runtime — no hardcoded UUIDs except intentional nil `00000000-0000-0000-0000-000000000099` for negative tests.
Cross-domain: each test uses tools from multiple domains to mirror real usage.

**Total R tools: 84**
Domains: default (18) · access-management (16) · application-security (9) · applications-components (5) · feature-management (16) · organization-administration (5) · policy-engine (5) · reports-analytics (4) · workflows (6)

---

## Section 1 — Default / Core Navigation (18 tools)

### RO-D01
**Tool:** `user_whoami`
Call user_whoami. Report userId, email, name, and selected organization. This is the baseline identity check; all other tests depend on it.

### RO-D02
**Tool:** `organizations_list`
List all organizations accessible to me. Report each org's id, displayName, domainName, and tenant level. Note pagination metadata if present.

### RO-D03
**Tool:** `organizations_get`
First call organizations_list to find any organization. Then call organizations_get with that org's ID. Compare displayName and ID between both calls — they must match.

### RO-D04
**Tool:** `organizations_search`
Search for organizations using a broad term (e.g., part of the org name discovered from organizations_list). Report each match's id, displayName, and domainName.

### RO-D05 (Negative)
**Tool:** `organizations_search`
Search organizations using a random nonsense string "xyzzy-no-match-9999". Expected: empty results array or 404. Record exact response.

### RO-D06
**Tool:** `organizations_list_suborganizations`
List all sub-organizations using the default org configured in the MCP server. Report each sub-org's id, displayName, and parent. Note nextCursor if pagination is present.

### RO-D07
**Tool:** `resources_get`
Call organizations_list to get an org ID. Then call resources_get with that org ID as the UUID. Report the full resource node returned (id, type, displayName, parent).

### RO-D08 (Negative)
**Tool:** `resources_get`
Call resources_get with a nil UUID (00000000-0000-0000-0000-000000000099). Record the exact error. Expected: 404.

### RO-D09
**Tool:** `resources_list`
Call organizations_list_suborganizations to get a sub-org ID. Then call resources_list with that sub-org ID to list its direct children. Report each child's id, type, and displayName.

### RO-D10
**Tool:** `search_resources`
Call organizations_get to get a root org ID. Then call search_resources restricted to type "SERVICE" within that org hierarchy. Report the total count and first 5 results.

### RO-D11
**Tool:** `services_list`
Call organizations_list to get an org ID. Then call services_list for that organization. Report each service's id, name, type (component vs application), and status.

### RO-D12
**Tool:** `services_get`
Call services_list to get a service ID. Then call services_get with that serviceId. Report all top-level fields returned.

### RO-D13 (Negative)
**Tool:** `services_get`
Call services_get with a nil serviceId (00000000-0000-0000-0000-000000000099). Record the exact error. Expected: 404.

### RO-D14
**Tool:** `flags_applications_list`
Call organizations_list to get an org ID. Then call flags_applications_list for that organization. Report each flag application's id, name, and environment count.

### RO-D15
**Tool:** `flags_environments_list`
Call flags_applications_list to get an application ID. Then call flags_environments_list for that application. Report each environment's id, name, and type.

### RO-D16
**Tool:** `flags_get_by_name`
Call flags_applications_list to get an app. Call flags_list (feature-management) to get a flag name. Then call flags_get_by_name with that name and app ID. Verify the returned flag name matches.

### RO-D17
**Tool:** `flag_configuration_get`
Call flags_applications_list → flags_environments_list → flags_list to get a flag ID and environment ID. Then call flag_configuration_get for that flag in that environment. Report the configuration returned.

### RO-D18
**Tool:** `search_runs`
Call services_list to get a component ID. Then call search_runs for that component. Report total runs found, statuses seen, and the most recent run's ID and timestamp.

### RO-D19
**Tool:** `automation_jobs_list`
Call search_runs to find a completed run ID. Then call automation_jobs_list for that run. Report each job's name, status, and duration.

### RO-D20
**Tool:** `logs_list`
Call search_runs to get a run. Call automation_jobs_list to get a job with steps. Then call logs_list for a step in that job. Report the first 5 log lines returned.

### RO-D21
**Tool:** `workflow_list`
Call services_list to get a component. Then call workflow_list for that component. Report each workflow's id, name, and last-modified date.

---

## Section 2 — Access Management — Read (16 tools)

### RO-AM01
**Tool:** `users_list`
Call organizations_list to get an org ID. Then call users_list for that organization. Report total user count, each user's displayName, email, and status.

### RO-AM02
**Tool:** `users_get`
Call user_whoami to get my email. Then call users_get searching by that email. Verify the returned user's email matches.

### RO-AM03
**Tool:** `users_get_by_id`
Call users_list to get the first user's ID. Then call users_get_by_id with that ID. Report all returned fields and confirm the ID matches.

### RO-AM04 (Negative)
**Tool:** `users_get_by_id`
Call users_get_by_id with a nil ID (00000000-0000-0000-0000-000000000099). Record the exact error. Expected: 404.

### RO-AM05 (Negative)
**Tool:** `users_get`
Search for a user by email "no-such-user-xyz-999@example.invalid". Record the exact response. Expected: 404 or empty result.

### RO-AM06
**Tool:** `user_preferences_get`
Call user_whoami to get my userId. Then call user_preferences_get for that userId. Report every preference name, type, and current value.

### RO-AM07
**Tool:** `teams_get`
Call organizations_list to get an org ID. Then call teams_get for that organization. Report each team's name, type (PREDEFINED or USERDEFINED), and member count.

### RO-AM08
**Tool:** `teams_get_by_id`
Call teams_get to get a team ID. Then call teams_get_by_id with that ID. Verify the name and ID match between both calls.

### RO-AM09 (Negative)
**Tool:** `teams_get_by_id`
Call teams_get_by_id with a nil ID (00000000-0000-0000-0000-000000000099). Record the exact error. Expected: 404.

### RO-AM10
**Tool:** `teams_invites_list`
Call teams_get to find a team. Then call teams_invites_list for that team. Report: total pending invites, each invite's email and status. If no invites exist, record "0 pending invites — empty result OK".

### RO-AM11
**Tool:** `teams_memberships_list`
Call teams_get to find a team. Then call teams_memberships_list for that team. Report each member's userId, displayName, and role.

### RO-AM12
**Tool:** `api_tokens_list`
Call api_tokens_list for the current user. Report the count of tokens and each token's name, createdAt, and lastUsed. Confirm actual token values are never returned.

### RO-AM13
**Tool:** `rbac_roles_list`
Call organizations_list to get an org ID. Then call rbac_roles_list for that organization. Report each role's id, name, and description.

### RO-AM14
**Tool:** `rbac_role_get`
Call rbac_roles_list to get a role ID. Then call rbac_role_get with that ID. Report all fields returned and confirm the ID matches.

### RO-AM15 (Negative)
**Tool:** `rbac_role_get`
Call rbac_role_get with a nil ID (00000000-0000-0000-0000-000000000099). Record the exact error. Expected: 404.

### RO-AM16
**Tool:** `rbac_permissions_list`
Call rbac_permissions_list. Report the total count of available permissions and the first 10 permission names.

### RO-AM17
**Tool:** `rbac_authorizations_list`
Call organizations_list to get an org ID. Then call rbac_authorizations_list for that org. Report each authorization's id, principal (user or team), role, and resource.

### RO-AM18
**Tool:** `rbac_authorization_check_bulk`
Call user_whoami to get my userId. Call rbac_roles_list to get a role name. Then call rbac_authorization_check_bulk with 2 authorization requests:
1. Check if my user has the found role on the org resource.
2. Check if my user has a made-up role "NONEXISTENT_ROLE" on the org resource.
Report pass/fail for each check.

### RO-AM19
**Tool:** `saml_connections_list`
Call organizations_list to get an org ID. Then call saml_connections_list for that org. Report each connection's id and name. If none exist, record "0 SAML connections — empty result OK".

### RO-AM20
**Tool:** `saml_email_domains_list`
Call organizations_list to get an org ID. Then call saml_email_domains_list for that org. Report each email domain listed. If none, record "0 email domains — empty result OK".

---

## Section 3 — Application Security — Read (9 tools)

### RO-SEC01
**Tool:** `security_issues_all_get`
Call organizations_list_suborganizations to get a sub-org ID. Then call security_issues_all_get for that sub-org. Report total issue count by severity (critical, high, medium, low).

### RO-SEC02
**Tool:** `security_issues_open_get`
Call services_list to get a component. Call branches_list (applications-components) to get a branch name. Then call security_issues_open_get for that component and branch. Report total open issues and top 3 by severity.

### RO-SEC03 (Negative)
**Tool:** `security_issues_open_get`
Call security_issues_open_get with a nil component ID (00000000-0000-0000-0000-000000000099) and branch "main". Record the exact error. Expected: 404 or 400.

### RO-SEC04
**Tool:** `security_findings_summary_get`
Call services_list to get a component. Call branches_list to get its default branch. Then call security_findings_summary_get for that component and branch. Report the summary fields returned.

### RO-SEC05 (Negative)
**Tool:** `security_findings_summary_get`
Call security_findings_summary_get with a real component ID but a fabricated branchId "00000000-0000-0000-0000-000000000099". Record the exact error. Expected: 404 or 500 (known Bug #6).

### RO-SEC06
**Tool:** `security_configuration_get`
Call organizations_list to get an org ID. Then call security_configuration_get for that organization at platform level. Report all configuration fields returned.

### RO-SEC07
**Tool:** `security_configuration_hierarchy_get`
Call services_list to get a component ID. Then call security_configuration_hierarchy_get for that component. Report each level in the hierarchy (tenant → org → component) and its effective settings.

### RO-SEC08
**Tool:** `security_sla_configuration_get`
Call organizations_list to get an org ID. Then call security_sla_configuration_get for that org. Report the SLA levels and thresholds configured.

### RO-SEC09
**Tool:** `security_filters_list`
Call flags_applications_list to find an application. Then call security_filters_list for that application. Report each filter's id, name, environment, and severity.

### RO-SEC10
**Tool:** `security_filter_tools_list`
Call flags_applications_list to find an application. Then call security_filter_tools_list for that application. Report each filter tool's name and type.

### RO-SEC11
**Tool:** `security_plugin_config_get`
Call organizations_list to get an org ID. Then call security_plugin_config_get for that org at platform level. Report each plugin's name and its configuration fields.

---

## Section 4 — Applications & Components — Read (5 tools)

### RO-AC01
**Tool:** `repositories_list`
Call organizations_list to get an org ID. Then call repositories_list for that org. Report total repository count, each repo's name, SCM provider, and URL.

### RO-AC02
**Tool:** `repositories_search`
Call repositories_list to pick a partial name. Then call repositories_search using that partial string. Verify the known repository appears in results.

### RO-AC03 (Negative)
**Tool:** `repositories_search`
Search repositories using "xyzzy-repo-no-match-9999". Expected: empty results. Record exact response.

### RO-AC04
**Tool:** `branches_list`
Call services_list to get a component ID and org ID. Then call branches_list for that component. Report each branch's name, lastCommit, and author.

### RO-AC05
**Tool:** `scm_gh_app_registrations_list`
Call organizations_list to get an org ID. Then call scm_gh_app_registrations_list for that org. Report each GitHub App's name and URL. If none, record "0 registrations — empty result OK".

### RO-AC06
**Tool:** `scm_branches_list`
Call endpoint_list (organization-administration) to find an SCM endpoint/connector. Get its endpointId. Then call repositories_list to get a repository. Call scm_branches_list with the endpointId and repository. Report branch names returned.

---

## Section 5 — Feature Management — Read (16 tools)

### RO-FM01
**Tool:** `flags_list`
Call flags_applications_list to get an app ID. Then call flags_list for that application. Report each flag's id, name, type (String/Boolean/Number), and enabled status.

### RO-FM02
**Tool:** `flags_get`
Call flags_list to get a flag ID. Then call flags_get with that flag ID. Report all returned fields and confirm ID matches.

### RO-FM03 (Negative)
**Tool:** `flags_get`
Call flags_get with a nil flag ID (00000000-0000-0000-0000-000000000099). Record the exact error. Expected: 404.

### RO-FM04
**Tool:** `flags_configurations_list`
Call flags_applications_list → flags_environments_list to get an environment ID. Then call flags_configurations_list for that environment. Report total flag count and each flag's name and state.

### RO-FM05
**Tool:** `flags_flag_usage_per_environment`
Call flags_list to get a flag ID. Then call flags_flag_usage_per_environment for that flag. Report each environment name and whether the flag is enabled in it.

### RO-FM06
**Tool:** `flag_approval_requests_list`
Call flags_applications_list to get an app ID. Then call flag_approval_requests_list for that application. Report total pending approvals and each request's flag name, requester, and created date. If none, record "0 approval requests — empty result OK".

### RO-FM07
**Tool:** `flag_target_groups_list`
Call flags_applications_list to get an app ID. Then call flag_target_groups_list for that application. Report each target group's id, name, and condition type.

### RO-FM08
**Tool:** `flag_target_groups_get`
Call flag_target_groups_list to get a target group ID. Then call flag_target_groups_get with that ID. Report all fields returned and confirm the ID matches.

### RO-FM09
**Tool:** `flag_target_groups_get_by_name`
Call flag_target_groups_list to get a target group name. Then call flag_target_groups_get_by_name with that name and app ID. Verify the returned group name matches.

### RO-FM10 (Negative)
**Tool:** `flag_target_groups_get`
Call flag_target_groups_get with a nil ID (00000000-0000-0000-0000-000000000099). Record the exact error. Expected: 404.

### RO-FM11
**Tool:** `flag_target_groups_list_with_flags_usage`
Call flags_applications_list to get an app ID. Then call flag_target_groups_list_with_flags_usage for that app. Report each target group's name and the flags that use it.

### RO-FM12
**Tool:** `flag_target_groups_flag_usage_per_environment`
Call flag_target_groups_list to get a target group ID. Then call flag_target_groups_flag_usage_per_environment for that target group. Report each environment and its flag usage count.

### RO-FM13
**Tool:** `flag_target_groups_target_group_usage`
Call flag_target_groups_list to get a target group ID. Then call flag_target_groups_target_group_usage for that target group. Report any other target groups that reference (nest) it.

### RO-FM14
**Tool:** `flag_custom_properties_list`
Call flags_applications_list to get an app ID. Then call flag_custom_properties_list for that application. Report each property's id, name, and type.

### RO-FM15
**Tool:** `flag_custom_properties_get`
Call flag_custom_properties_list to get a property ID. Then call flag_custom_properties_get with that ID. Confirm ID and name match.

### RO-FM16
**Tool:** `flag_custom_properties_get_by_name`
Call flag_custom_properties_list to get a property name. Then call flag_custom_properties_get_by_name with that name and app ID. Verify the returned property name matches.

### RO-FM17 (Negative)
**Tool:** `flag_custom_properties_get`
Call flag_custom_properties_get with a nil ID (00000000-0000-0000-0000-000000000099). Record the exact error. Expected: 404.

### RO-FM18
**Tool:** `flag_custom_properties_flag_usage_per_environment`
Call flag_custom_properties_list to get a property ID. Then call flag_custom_properties_flag_usage_per_environment for that property. Report flag usage counts per environment.

### RO-FM19
**Tool:** `flag_custom_properties_target_group_usage`
Call flag_custom_properties_list to get a property ID. Then call flag_custom_properties_target_group_usage for that property. Report which target groups use this custom property.

---

## Section 6 — Organization Administration — Read (5 tools)

### RO-OA01
**Tool:** `endpoint_list`
Call organizations_list to get an org ID. Then call endpoint_list for that org. Report each endpoint's id, name, type (integration, environment, notification channel, automation action), and status.

### RO-OA02
**Tool:** `extensions_list`
Call organizations_list to get an org ID. Then call extensions_list for that org. Report each extension manifest's name and version. If none, record "0 extensions — empty result OK".

### RO-OA03
**Tool:** `properties_get`
Call services_list to get a component (resource) ID. Then call properties_get for that resource. Report each property's name and value.

### RO-OA04
**Tool:** `properties_list`
Call services_list to get a component ID. Then call properties_list for that component (service). Report the extended properties returned.

### RO-OA05
**Tool:** `ticketing_webhook_url_get`
Call organizations_list to get an org ID. Call endpoint_list to find a ticketing integration endpoint. Then call ticketing_webhook_url_get using that endpoint instance. Report the webhook URL returned. If no ticketing endpoint exists, record "No ticketing integration found — test skipped".

---

## Section 7 — Policy Engine — Read (5 tools)

### RO-PE01
**Tool:** `policies_list`
Call organizations_list to get an org ID. Then call policies_list for that org. Report total policy count, each policy's id, name, and description.

### RO-PE02
**Tool:** `policies_get`
Call policies_list to get a policy ID. Then call policies_get with that ID. Report all policy fields returned and confirm the ID matches.

### RO-PE03 (Negative)
**Tool:** `policies_get`
Call policies_get with a nil ID (00000000-0000-0000-0000-000000000099). Record the exact error. Expected: 404.

### RO-PE04
**Tool:** `policies_get_schema`
Call policies_get_schema without specifying a version (returns latest). Report the schema version and top-level keys. Then call again with an explicit version from the first response. Verify both calls return valid schema objects.

### RO-PE05
**Tool:** `policies_discover`
Call services_list to get a component ID. Call workflow_list to get a workflow context. Then call policies_discover for that component and workflow context. Report each matching policy's name, outcome (worst-case action), and scope.

### RO-PE06
**Tool:** `policies_run_evaluations_list`
Call search_runs to find a completed run ID. Then call policies_run_evaluations_list for that run. Report evaluation results grouped by checkpoint. If no runs exist, record "No runs found — test skipped".

---

## Section 8 — Reports & Analytics — Read (4 tools)

### RO-RA01
**Tool:** `controllers_list`
Call organizations_list to get an org ID. Then call controllers_list for that organization. Report each controller's id, name, and type.

### RO-RA02
**Tool:** `controllers_data_get`
Call controllers_list to get a controller ID. Then call controllers_data_get for that controller. Report the report data fields returned (widget id, data points, time range).

### RO-RA03
**Tool:** `organizations_suborg_report`
Call organizations_list_suborganizations to get a sub-org ID. Then call organizations_suborg_report for that sub-org. Report the report fields and data returned.

### RO-RA04
**Tool:** `report_drilldown_get`
Call controllers_list to get a controller ID. Then call report_drilldown_get for that controller. Report the drilldown data fields. If no drilldown data is available, record the response as-is.

---

## Section 9 — Workflows — Read (6 tools)

### RO-WF01
**Tool:** `actions_list`
Call organizations_list to get an org ID. Then call actions_list for that organization. Report each action's id, name, and type.

### RO-WF02
**Tool:** `workflow_get_content`
Call services_list to get a component. Call workflow_list to get a workflow ID. Then call workflow_get_content for that workflow. Report the workflow YAML structure (top-level keys).

### RO-WF03
**Tool:** `workflow_schema_get`
Call workflow_schema_get. Report the returned JSON schema's top-level keys and version. Confirm the response is valid JSON.

### RO-WF04
**Tool:** `workflow_validate`
Call workflow_get_content to get existing workflow YAML. Then call workflow_validate with that same YAML content. Report whether it is valid and any validation messages.

### RO-WF05 (Negative)
**Tool:** `workflow_validate`
Call workflow_validate with invalid YAML content (e.g., "this: is: invalid: yaml: :::"). Record the exact validation error returned.

### RO-WF06
**Tool:** `runs_list`
Call services_list to get a component ID. Then call runs_list for that component. Report the total count of runs, each run's id, status, triggeredBy, and createdAt timestamp.

### RO-WF07
**Tool:** `automation_pending_tasks_list`
Call organizations_list to get an org ID. Then call automation_pending_tasks_list for that org. Report each pending task's runId, jobName, requestedBy, and requested-at timestamp. If none, record "0 pending tasks — empty result OK".
