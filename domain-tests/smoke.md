# CloudBees MCP — Unit Smoke Prompts (Layer 1)

One prompt per tool. Run in Claude Code with the CloudBees MCP server connected.
Goal: confirm each tool responds without crashing, returns expected schema shape.

## How to use
Paste each prompt into Claude Code. After the tool call, verify the response matches the expected shape.
Mark Pass / Fail / Warn (empty result but no error).

---

## Diagnostic Categories

| Category | Definition | Failure Indicates |
|----------|-----------|-------------------|
| **Selection** | Single tool call from natural language | AI picked the wrong tool from 84+ options |
| **Chain** | 2–4 tools called in sequence | Wrong tool order, missed step, or incorrect data passed between steps |
| **Stress** | 5+ tools OR repeated calls OR large payloads | Timeout, session limit, or token exhaustion |

---

## Identity & User Preferences

| # | Tool | Prompt | Expected Shape | Category | Timeout |
|---|------|--------|----------------|----------|---------|
| 1 | `user_whoami` | "Who am I on CloudBees? Show my full profile." | `{ userId, email, name }` | Selection | 15s |
| 2 | `user_preferences_get` | "Show my CloudBees user preferences." | `{ preferences: {...} }` | Selection | 15s |
| 3 | `user_set_timezone` | "Set my CloudBees timezone to UTC." | Success acknowledgement | Selection | 15s |

---

## Users

| # | Tool | Prompt | Expected Shape | Category | Timeout |
|---|------|--------|----------------|----------|---------|
| 4 | `users_list` | "List all users in the CloudBees organization." | Array of user objects | Selection | 15s |
| 5 | `users_get` | "Search for my own user details using my email address." | Single user object | Selection | 15s |
| 6 | `users_get_by_id` | "Get user details for user ID f3039d4a-7c3a-11f0-9a1c-42010a83ae54." | Same single user object | Selection | 15s |

---

## Teams

| # | Tool | Prompt | Expected Shape | Category | Timeout |
|---|------|--------|----------------|----------|---------|
| 7 | `teams_create` | "Create a team named 'smoke-test-team-01'." | `{ teamId, name }` | Selection | 15s |
| 8 | `teams_get` | "List all teams and find the one named 'smoke-test-team-01'." | Team object | Selection | 15s |
| 9 | `teams_get_by_id` | "Get team details using the teamId from the team I just created." | Same team object | Selection | 15s |
| 10 | `teams_invite_create` | "Invite the first user in the list to the smoke-test-team-01." | `{ inviteId }` | Selection | 15s |
| 11 | `teams_invites_list` | "List all pending invites for smoke-test-team-01." | Array with the new invite | Selection | 15s |
| 12 | `teams_invite_delete` | "Delete the invite we just created." | Success | Selection | 15s |
| 13 | `teams_members_add` | "Add the first user to smoke-test-team-01 as a member." | Success | Selection | 15s |
| 14 | `teams_memberships_list` | "List all memberships in smoke-test-team-01." | Array with the user | Selection | 15s |
| 15 | `teams_members_remove` | "Remove that user from smoke-test-team-01." | Success | Selection | 15s |
| 16 | `teams_delete` | "Delete smoke-test-team-01." | Success | Selection | 15s |

---

## Organizations

| # | Tool | Prompt | Expected Shape | Category | Timeout |
|---|------|--------|----------------|----------|---------|
| 17 | `organizations_search` | "Search for organizations with 'cloudbees' in the name." | Array of org objects | Selection | 15s |
| 18 | `organizations_list_suborganizations` | "List all sub-organizations under the current organization." | Array of sub-orgs | Selection | 15s |
| 19 | `organizations_suborg_report` | "Get the sub-org report (widget ci1) for the first sub-organization." | Report object | Selection | 15s |
| 20 | `organizations_list` | "List all organizations accessible to me." | Array of org objects | Selection | 15s |
| 21 | `organizations_get` | "Get the organization with ID 6c5eeb79-4606-4c39-bd5c-c2323336caad." | Single org object | Selection | 15s |
| 22 | `organizations_create` | "Create a sub-organization with displayName 'smoke-org-01' and domainName 'smoke-org-01' under parent 6c5eeb79-4606-4c39-bd5c-c2323336caad." | `{ id, displayName }` | Selection | 15s |
| 23 | ~~`organizations_mark_internal`~~ | *REMOVED — tool no longer available* | — | — | — |
| 24 | ~~`organizations_flag_malicious`~~ | *REMOVED — tool no longer available* | — | — | — |

---

## Components & SCM

| # | Tool | Prompt | Expected Shape | Category | Timeout |
|---|------|--------|----------------|----------|---------|
| 25 | ~~`components_create`~~ | *REMOVED — tool no longer available* | — | — | — |
| 26 | ~~`components_list`~~ | *REMOVED — tool no longer available* | — | — | — |
| 27 | ~~`components_search`~~ | *REMOVED — tool no longer available* | — | — | — |
| 28 | ~~`components_delete`~~ | *REMOVED — tool no longer available* | — | — | — |
| 29 | `extensions_list` | "List all available extensions for the organization." | Array of extension manifests | Selection | 15s |
| 30 | `scm_branches_list` | "List branches from the SCM provider for the VulnerableGoRepo4GH repository (endpoint 413e7e54-f227-44dc-9b0d-d793e7c6f5d4, url https://github.com/rjain0404/VulnerableGoRepo4GH.git)." | Array of branch names | Selection | 15s |
| 31 | `scm_gh_app_registrations_list` | "List registered GitHub App registrations for the organization." | Array of GitHub App entries | Selection | 15s |
| 32 | `scm_repositories_sync` | "Trigger a sync of repositories from the SCM provider for the organization." | Success / async job reference | Selection | 15s |

---

## Resources, Properties, Endpoints

| # | Tool | Prompt | Expected Shape | Category | Timeout |
|---|------|--------|----------------|----------|---------|
| 33 | `resources_list` | "List all available resources in CloudBees." | Array of resource objects | Selection | 15s |
| 34 | `properties_list` | "List all properties for the 'go' component (95fdf71c-de53-43e4-b5dc-bec7170becd6)." | Array of property objects | Selection | 15s |
| 35 | `endpoint_list` | "List all configured endpoints." | Array of endpoint objects | Selection | 15s |

---

## Controllers

| # | Tool | Prompt | Expected Shape | Category | Timeout |
|---|------|--------|----------------|----------|---------|
| 36 | `controllers_list` | "List all CloudBees controllers." | Array of controllers | Selection | 15s |
| 37 | `controllers_data_get` | "Get data for the first controller in the list." | Controller data object | Selection | 15s |

---

## CI/CD Automation

| # | Tool | Prompt | Expected Shape | Category | Timeout |
|---|------|--------|----------------|----------|---------|
| 38 | `automation_jobs_list` | "List all automation jobs." | Array of job objects | Selection | 15s |
| 39 | `automation_trigger` | "Trigger the first automation job." | `{ runId }` or trigger reference | Selection | 15s |
| 40 | `automation_trigger_by_branch` | "Trigger the first job on its default branch." | `{ runId }` | Selection | 15s |
| 41 | `automation_rerun` | "Rerun the most recent run of the first job." | `{ runId }` | Selection | 15s |
| 42 | `automation_stop` | "Stop the run we just triggered." | Success | Selection | 15s |
| 43 | `automation_approve_manual_gate` | "Check if any job has a pending manual gate and approve it." | Success or 'no pending gates' | Selection | 15s |
| 44 | `automation_reject_manual_gate` | "Check if any job has a pending manual gate and reject it." | Success or 'no pending gates' | Selection | 15s |

---

## Repositories, Branches, Runs, Logs, Actions

| # | Tool | Prompt | Expected Shape | Category | Timeout |
|---|------|--------|----------------|----------|---------|
| 45 | `repositories_list` | "List all repositories in the organization." | Array of repo objects | Selection | 15s |
| 46 | `repositories_search` | "Search repositories for 'test'." | Array of matching repos | Selection | 15s |
| 47 | `branches_list` | "List branches for the first repository's linked component." | Array of branch names | Selection | 15s |
| 48 | `runs_list` | "List recent runs for the first automation job." | Array of run objects | Selection | 15s |
| 49 | `logs_list` | "List logs for the most recent run." | Array of log entries | Selection | 15s |
| 50 | `actions_list` | "List all available CloudBees actions." | Array of action objects | Selection | 15s |

---

## Workflows

| # | Tool | Prompt | Expected Shape | Category | Timeout |
|---|------|--------|----------------|----------|---------|
| 51 | `workflow_list` | "List all workflows." | Array of workflow objects | Selection | 15s |
| 52 | `workflow_get_content` | "Get the content of the first workflow." | Workflow YAML/JSON string | Selection | 15s |
| 53 | `workflow_schema_get` | "Get the workflow schema." | JSON Schema object | Selection | 15s |
| 54 | `workflow_validate` | "Validate the content of the first workflow." | `{ valid: true/false, errors: [] }` | Selection | 15s |
| 55 | `workflow_update_content` | "Add a comment '# smoke test' to the first workflow and save." | Success | Selection | 15s |
| 56 | `workflow_trigger` | "Trigger the first workflow." | `{ runId }` | Selection | 15s |

---

## Feature Flags — Core

| # | Tool | Prompt | Expected Shape | Category | Timeout |
|---|------|--------|----------------|----------|---------|
| 58 | `flags_environments_list` | "List all feature flag environments." | Array of env objects | Selection | 15s |
| 59 | `flags_applications_list` | "List all feature flag applications." | Array of app objects | Selection | 15s |
| 60 | `flags_add` | "Create a boolean feature flag named 'smoke-flag-01'." | `{ flagId, name }` | Selection | 15s |
| 61 | `flags_list` | "List all feature flags in the first application." | Array including smoke-flag-01 | Selection | 15s |
| 62 | `flags_get` | "Get the smoke-flag-01 flag details by its ID." | Single flag object | Selection | 15s |
| 63 | `flags_get_by_name` | "Get the flag named 'smoke-flag-01' by name." | Same flag object | Selection | 15s |
| 64 | `flags_update_defaultValue` | "Update smoke-flag-01 default value to 'false'." | Success | Selection | 15s |
| 65 | `flags_flag_usage_per_environment` | "Show usage of smoke-flag-01 per environment." | Usage data | Selection | 15s |
| 66 | ~~`flags_sdk_key_get`~~ | *REMOVED — tool no longer available* | — | — | — |
| 67 | `flags_delete` | "Delete smoke-flag-01." | Success | Selection | 15s |

---

## Feature Flags — Configuration

| # | Tool | Prompt | Expected Shape | Category | Timeout |
|---|------|--------|----------------|----------|---------|
| 68 | `flags_configurations_list` | "List all flag configurations for the first application and environment." | Array of config objects | Selection | 15s |
| 69 | `flag_configuration_get` | "Get the configuration for smoke-flag-01 in the first environment." | Config detail object | Selection | 15s |
| 70 | `flags_configuration_state_update` | "Enable smoke-flag-01 in the first environment." | Success | Selection | 15s |
| 71 | `flag_configuration_conditions_set` | "Set targeting conditions on smoke-flag-01 in the first environment, linking to smoke-tg-01 with flagValue=true." | Success | Selection | 15s |
| 72 | `flags_applications_list` | *(already covered at #59)* | — | Selection | 15s |
| 73 | `flag_approval_requests_list` | "List all pending flag approval requests." | Array (may be empty) | Selection | 15s |

---

## Feature Flags — Target Groups

| # | Tool | Prompt | Expected Shape | Category | Timeout |
|---|------|--------|----------------|----------|---------|
| 74 | `flag_target_groups_add` | "Create a target group named 'smoke-tg-01'." | `{ groupId, name }` | Selection | 15s |
| 75 | `flag_target_groups_get` | "Get the smoke-tg-01 target group by its ID." | Group object | Selection | 15s |
| 76 | `flag_target_groups_get_by_name` | "Get the target group named 'smoke-tg-01' by name." | Same group object | Selection | 15s |
| 77 | `flag_target_groups_list` | "List all target groups in the first application." | Array including smoke-tg-01 | Selection | 15s |
| 78 | `flag_target_groups_flag_usage_per_environment` | "Check flag usage per environment for smoke-tg-01." | Usage data | Selection | 15s |
| 79 | `flag_target_groups_list_with_flags_usage` | "List all target groups with their flag usage data." | Array with usage | Selection | 15s |
| 80 | `flag_target_groups_target_group_usage` | "Get overall usage for smoke-tg-01." | Usage object | Selection | 15s |
| 80a | `flag_serve_to_target_group` | "Serve value true to smoke-tg-01 for smoke-flag-01 in the first environment with enableIfDisabled=true." | Success | Selection | 15s |
| 81 | `flag_target_groups_delete` | "Delete smoke-tg-01." | Success | Selection | 15s |

---

## Feature Flags — Custom Properties

| # | Tool | Prompt | Expected Shape | Category | Timeout |
|---|------|--------|----------------|----------|---------|
| 82 | `flag_custom_properties_add` | "Create a string custom property named 'smoke-prop-01'." | `{ propId, name }` | Selection | 15s |
| 83 | `flag_custom_properties_get` | "Get the smoke-prop-01 custom property by its ID." | Property object | Selection | 15s |
| 84 | `flag_custom_properties_get_by_name` | "Get the custom property named 'smoke-prop-01' by name." | Same property object | Selection | 15s |
| 85 | `flag_custom_properties_list` | "List all custom properties in the first application." | Array including smoke-prop-01 | Selection | 15s |
| 86 | `flag_custom_properties_flag_usage_per_environment` | "Check flag usage per environment for smoke-prop-01." | Usage data | Selection | 15s |
| 87 | `flag_custom_properties_target_group_usage` | "Get target group usage for smoke-prop-01." | Usage object | Selection | 15s |
| 88 | `flag_custom_properties_delete` | "Delete smoke-prop-01." | Success | Selection | 15s |

---

## Security

| # | Tool | Prompt | Expected Shape | Category | Timeout |
|---|------|--------|----------------|----------|---------|
| 89 | `security_findings_summary_get` | "Get the security findings summary for the 'go' component." | Summary with counts | Selection | 15s |
| 90 | `security_issues_open_get` | "List all open security issues for the 'go' component." | Array of issues | Selection | 15s |
| 91 | `security_issues_all_get` | "List all security issues (open and resolved) for the first sub-org." | Array (count >= open) | Selection | 15s |
| 92 | `security_filter_tools_list` | "List all security filter tools for the first feature flag application." | Array of security tool objects | Selection | 15s |
| 93 | `security_filters_list` | "List all application security filters for the first feature flag application." | Array of filter objects (environments, severities, SLA) | Selection | 15s |

---

## Auth & SAML

| # | Tool | Prompt | Expected Shape | Category | Timeout |
|---|------|--------|----------------|----------|---------|
| 94 | `api_tokens_list` | "List all API tokens." | Array of token objects | Selection | 15s |
| 95 | `saml_connections_list` | "List all SAML connections." | Array of connection objects | Selection | 15s |
| 96 | `saml_email_domains_list` | "List all SAML email domains." | Array of domain objects | Selection | 15s |

---

## Reports

| # | Tool | Prompt | Expected Shape | Category | Timeout |
|---|------|--------|----------------|----------|---------|
| 97 | `report_drilldown_get` | "Get a drill-down report for security findings." | Report object with data | Selection | 15s |

---

## RBAC

| # | Tool | Prompt | Expected Shape | Category | Timeout |
|---|------|--------|----------------|----------|---------|
| 98 | `rbac_permissions_list` | "List all available RBAC permissions for the organization." | Array of permission objects | Selection | 15s |
| 99 | `rbac_roles_list` | "List all RBAC roles in the organization." | Array of role objects | Selection | 15s |
| 100 | `rbac_role_create` | "Create a custom RBAC role named 'smoke-rbac-role-01'." | `{ roleId, name }` | Selection | 15s |
| 101 | `rbac_role_get` | "Get the details of the 'smoke-rbac-role-01' role by its ID." | Single role object | Selection | 15s |
| 102 | `rbac_authorizations_list` | "List all RBAC authorizations in the organization." | Array of authorization objects | Selection | 15s |
| 103 | `rbac_authorization_check_bulk` | "Check if the current user has read and write permissions in the organization." | `{ permissions: [{name, allowed}] }` | Selection | 15s |
| 104 | `rbac_authorization_create` | "Assign the 'smoke-rbac-role-01' role to the current user (from whoami) in the root organization." | `{ authorizationId }` | Selection | 15s |
| 105 | `rbac_role_delete` | "Delete the 'smoke-rbac-role-01' role." | Success | Selection | 15s |

---

## Security — Advanced (Configuration, Plugins, SLA)

| # | Tool | Prompt | Expected Shape | Category | Timeout |
|---|------|--------|----------------|----------|---------|
| 106 | `security_configuration_get` | "Get the security configuration for the organization." | Security config object | Selection | 15s |
| 107 | `security_configuration_hierarchy_get` | "Get the security configuration hierarchy for the organization." | Hierarchy config object | Selection | 15s |
| 108 | `security_configuration_set` | "Toggle the first boolean security configuration field to its current value (no-op update to verify write works)." | Success | Selection | 15s |
| 109 | `security_sla_configuration_get` | "Get the SLA configuration for the organization." | SLA config with severity windows | Selection | 15s |
| 110 | `security_sla_configuration_set` | "Set the LOW severity SLA window to 90 days." | Success | Selection | 15s |
| 111 | `security_sla_configuration_remove` | "Remove the custom SLA configuration for the first sub-organization." | Success | Selection | 15s |
| 112 | `security_tenant_sla_configuration_remove` | "Remove the tenant-level SLA configuration for the organization." | Success | Selection | 15s |
| 113 | `security_plugin_activate` | "Activate the first available security plugin for the organization." | Success | Selection | 15s |
| 114 | `security_plugin_config_get` | "Get the configuration for the first available security plugin." | Plugin config object | Selection | 15s |
| 115 | `security_plugin_config_set` | "Update a non-critical config field on the first security plugin." | Success | Selection | 15s |
| 116 | `security_plugin_deactivate` | "Deactivate the security plugin we just activated." | Success | Selection | 15s |
| 117 | `security_implicit_scans_set` | "Enable implicit security scans for the organization." | Success | Selection | 15s |

---

## Services & Endpoints (New)

| # | Tool | Prompt | Expected Shape | Category | Timeout |
|---|------|--------|----------------|----------|---------|
| 118 | `services_list` | "List all services in the organization." | Array of service objects | Selection | 15s |
| 119 | `services_add` | "Create a service named 'smoke-service-01'." | `{ serviceId, name }` | Selection | 15s |
| 120 | `services_get` | "Get the details of the 'smoke-service-01' service by its ID." | Single service object | Selection | 15s |
| 121 | `services_delete` | "Delete the 'smoke-service-01' service." | Success | Selection | 15s |
| 122 | `endpoint_add` | "Add a new GitHub endpoint named 'smoke-endpoint-01' (use placeholder credentials)." | `{ endpointId, name }` or error if credentials required | Selection | 15s |
| 123 | `endpoint_scm_connector_prepare` | "Prepare a GitHub SCM connector for the organization." | OAuth URL or setup object | Selection | 15s |
| 126 | `ticketing_webhook_url_get` | "Get the ticketing webhook URL for the organization." | Webhook URL string or object | Selection | 15s |

---

## Search, Properties & Resources (New)

| # | Tool | Prompt | Expected Shape | Category | Timeout |
|---|------|--------|----------------|----------|---------|
| 127 | `search_resources` | "Search for resources containing 'go' in the organization." | Array of resource results | Selection | 15s |
| 128 | `search_runs` | "Search for recent pipeline runs in the organization (last 7 days)." | Array of run objects | Selection | 15s |
| 129 | `properties_get` | "Get the first property for the 'go' component by its property ID." | Single property object | Selection | 15s |
| 130 | `properties_add` | "Add a string property 'SMOKE_TEST_PROP' with value 'smoke-value' to the 'go' component." | `{ propertyId, name }` | Selection | 15s |
| 131 | `property_delete` | "Delete the 'SMOKE_TEST_PROP' property we just added." | Success | Selection | 15s |
| 132 | `resources_get` | "Get the details of the master branch resource for the 'go' component by its resource ID." | Single resource detail object | Selection | 15s |

---

## Results Tracker

Copy this table into your test run notes:

```
Tool                                    | Status | Notes
----------------------------------------|--------|------
user_whoami                             |        |
user_preferences_get                    |        |
user_set_timezone                       |        |
users_list                              |        |
users_get                               |        |
users_get_by_id                         |        |
teams_create                            |        |
teams_get                               |        |
teams_get_by_id                         |        |
teams_invite_create                     |        |
teams_invites_list                      |        |
teams_invite_delete                     |        |
teams_members_add                       |        |
teams_memberships_list                  |        |
teams_members_remove                    |        |
teams_delete                            |        |
organizations_search                    |        |
organizations_list_suborganizations     |        |
organizations_suborg_report             |        |
organizations_list                      |        |
organizations_get                       |        |
organizations_create                    |        |
organizations_mark_internal             | REMOVED |
organizations_flag_malicious            | REMOVED |
components_create                       | REMOVED |
components_list                         | REMOVED |
components_search                       | REMOVED |
components_delete                       | REMOVED |
extensions_list                         |        |
scm_branches_list                       |        |
scm_gh_app_registrations_list          |        |
scm_repositories_sync                   |        |
resources_list                          |        |
properties_list                         |        |
endpoint_list                           |        |
controllers_list                        |        |
controllers_data_get                    |        |
automation_jobs_list                    |        |
automation_trigger                      |        |
automation_trigger_by_branch            |        |
automation_rerun                        |        |
automation_stop                         |        |
automation_approve_manual_gate          |        |
automation_reject_manual_gate           |        |
repositories_list                       |        |
repositories_search                     |        |
branches_list                           |        |
runs_list                               |        |
logs_list                               |        |
actions_list                            |        |
workflow_list                           |        |
workflow_get_content                    |        |
workflow_schema_get                     |        |
workflow_validate                       |        |
workflow_update_content                 |        |
workflow_trigger                        |        |
flags_environments_list                 |        |
flags_applications_list                 |        |
flags_add                               |        |
flags_list                              |        |
flags_get                               |        |
flags_get_by_name                       |        |
flags_update_defaultValue               |        |
flags_flag_usage_per_environment        |        |
flags_sdk_key_get                       | REMOVED |
flags_delete                            |        |
flags_configurations_list               |        |
flag_configuration_get                  |        |
flag_configuration_conditions_set       |        |
flags_configuration_state_update        |        |
flag_approval_requests_list             |        |
flag_target_groups_add                  |        |
flag_target_groups_get                  |        |
flag_target_groups_get_by_name          |        |
flag_target_groups_list                 |        |
flag_target_groups_flag_usage_per_env   |        |
flag_target_groups_list_with_flags_usage|        |
flag_target_groups_target_group_usage   |        |
flag_serve_to_target_group              |        |
flag_target_groups_delete               |        |
flag_custom_properties_add              |        |
flag_custom_properties_get              |        |
flag_custom_properties_get_by_name      |        |
flag_custom_properties_list             |        |
flag_custom_properties_flag_usage_per_env|       |
flag_custom_properties_target_group_usage|       |
flag_custom_properties_delete           |        |
security_findings_summary_get           |        |
security_issues_open_get                |        |
security_issues_all_get                 |        |
security_filter_tools_list              |        |
security_filters_list                   |        |
api_tokens_list                         |        |
saml_connections_list                   |        |
saml_email_domains_list                 |        |
report_drilldown_get                    |        |
rbac_permissions_list                   |        |
rbac_roles_list                         |        |
rbac_role_create                        |        |
rbac_role_get                           |        |
rbac_authorizations_list                |        |
rbac_authorization_check_bulk           |        |
rbac_authorization_create               |        |
rbac_role_delete                        |        |
security_configuration_get              |        |
security_configuration_hierarchy_get    |        |
security_configuration_set              |        |
security_sla_configuration_get          |        |
security_sla_configuration_set          |        |
security_sla_configuration_remove       |        |
security_tenant_sla_configuration_remove|        |
security_plugin_activate                |        |
security_plugin_config_get              |        |
security_plugin_config_set              |        |
security_plugin_deactivate              |        |
security_implicit_scans_set             |        |
services_list                           |        |
services_add                            |        |
services_get                            |        |
services_delete                         |        |
endpoint_get                            | REMOVED |
endpoint_add                            |        |
endpoint_disable                        | REMOVED |
endpoint_scm_connector_prepare          |        |
ticketing_webhook_url_get               |        |
search_resources                        |        |
search_runs                             |        |
properties_get                          |        |
properties_add                          |        |
property_delete                         |        |
resources_get                           |        |
```
