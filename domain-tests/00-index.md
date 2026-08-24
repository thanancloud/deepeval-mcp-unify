# CloudBees MCP — Domain Test Suite Index

**Total tools:** 124 | **Total prompts across all domains:** 231 | **All write tools covered**

---

## Domain Files

| File | Domain | Tools | Prompts | Positive | Negative | Edge |
|------|--------|-------|---------|----------|----------|------|
| [01-security.md](01-security.md) | Security (Core) | 5 | 24 | 8 | 8 | 8 |
| [02-feature-flags.md](02-feature-flags.md) | Feature Flags | 30 | 36 | 12 | 12 | 12 |
| [03-orgs-teams.md](03-orgs-teams.md) | Orgs & Teams | 22 | 33 | 11 | 11 | 11 |
| [04-components-repos.md](04-components-repos.md) | Components & Repos | 19 | 36 | 12 | 12 | 12 |
| [05-automation-workflows.md](05-automation-workflows.md) | Automation & Workflows | 13 | 22 | 7 | 8 | 7 |
| [06-rbac.md](06-rbac.md) | RBAC | 7 | 24 | 8 | 8 | 8 |
| [07-security-advanced.md](07-security-advanced.md) | Security — Advanced (Config, Plugins, SLA) | 12 | 24 | 8 | 8 | 8 |
| [08-services-endpoints.md](08-services-endpoints.md) | Services, Endpoints & Ticketing | 9 | 24 | 8 | 8 | 8 |
| [09-search-properties.md](09-search-properties.md) | Search, Properties & Resources | 6 | 18 | 6 | 6 | 6 |
| **Total** | | **131** | **246** | **82** | **82** | **82** |

> **Note:** 8 tools are shared across the original 95 and new 27 — the distinct count is 122. The 130 in the table counts domain assignments, not unique tools.


---

## Tool Allocation Per Domain

### Security (5 tools)
`security_findings_summary_get` · `security_issues_open_get` · `security_issues_all_get` · `security_filter_tools_list` · `security_filters_list`

### Feature Flags (30 tools)
`flags_environments_list` · `flags_applications_list` · `flags_add` · `flags_list` · `flags_get` · `flags_get_by_name` · `flags_update_defaultValue` · `flags_flag_usage_per_environment` · `flags_delete` · `flags_configurations_list` · `flag_configuration_get` · `flags_configuration_state_update` · `flag_configuration_conditions_set` · `flag_approval_requests_list` · `flag_target_groups_add` · `flag_target_groups_delete` · `flag_target_groups_get` · `flag_target_groups_get_by_name` · `flag_target_groups_list` · `flag_target_groups_flag_usage_per_environment` · `flag_target_groups_list_with_flags_usage` · `flag_target_groups_target_group_usage` · `flag_serve_to_target_group` · `flag_custom_properties_add` · `flag_custom_properties_delete` · `flag_custom_properties_get` · `flag_custom_properties_get_by_name` · `flag_custom_properties_list` · `flag_custom_properties_flag_usage_per_environment` · `flag_custom_properties_target_group_usage`

### Orgs & Teams (22 tools)
`user_whoami` · `user_preferences_get` · `user_set_timezone` · `users_list` · `users_get` · `users_get_by_id` · `teams_create` · `teams_delete` · `teams_get` · `teams_get_by_id` · `teams_invite_create` · `teams_invite_delete` · `teams_invites_list` · `teams_members_add` · `teams_members_remove` · `teams_memberships_list` · `organizations_search` · `organizations_list_suborganizations` · `organizations_suborg_report` · `organizations_list` · `organizations_get` · `organizations_create`

### Components & Repos (19 tools)
`repositories_list` · `repositories_search` · `branches_list` · `runs_list` · `logs_list` · `actions_list` · `resources_list` · `properties_list` · `endpoint_list` · `controllers_list` · `controllers_data_get` · `report_drilldown_get` · `api_tokens_list` · `saml_connections_list` · `saml_email_domains_list` · `extensions_list` · `scm_branches_list` · `scm_gh_app_registrations_list` · `scm_repositories_sync`

### Automation & Workflows (13 tools)
`automation_jobs_list` · `automation_trigger` · `automation_trigger_by_branch` · `automation_rerun` · `automation_stop` · `automation_approve_manual_gate` · `automation_reject_manual_gate` · `workflow_list` · `workflow_get_content` · `workflow_schema_get` · `workflow_validate` · `workflow_update_content` · `workflow_trigger`

### RBAC (7 tools) — NEW
`rbac_roles_list` · `rbac_role_get` · `rbac_role_create` · `rbac_role_delete` · `rbac_permissions_list` · `rbac_authorizations_list` · `rbac_authorization_check_bulk`

### Security — Advanced (12 tools) — NEW
`security_configuration_get` · `security_configuration_hierarchy_get` · `security_configuration_set` · `security_plugin_activate` · `security_plugin_deactivate` · `security_plugin_config_get` · `security_plugin_config_set` · `security_sla_configuration_get` · `security_sla_configuration_set` · `security_sla_configuration_remove` · `security_tenant_sla_configuration_remove` · `security_implicit_scans_set`

### Services, Endpoints & Ticketing (7 tools) — NEW
`services_list` · `services_get` · `services_add` · `services_delete` · `endpoint_add` · `endpoint_scm_connector_prepare` · `ticketing_webhook_url_get`

### Search, Properties & Resources (6 tools) — NEW
`search_resources` · `search_runs` · `properties_add` · `properties_get` · `property_delete` · `resources_get`

---

## Write Tool Coverage (new tools)

| Write Tool | Domain File | Test IDs |
|------------|-------------|----------|
| `user_set_timezone` | Orgs & Teams | OT-P09, OT-N08 |
| `teams_create` | Orgs & Teams | OT-P06, OT-N06, OT-E02, OT-E03, OT-E08 |
| `teams_delete` | Orgs & Teams | OT-P06, OT-N06, OT-E02, OT-E03, OT-E08 |
| `teams_invite_create` | Orgs & Teams | OT-P06, OT-N03, OT-E03, OT-E08 |
| `teams_invite_delete` | Orgs & Teams | OT-P06, OT-E03 |
| `teams_members_add` | Orgs & Teams | OT-P06, OT-P07, OT-N06 |
| `teams_members_remove` | Orgs & Teams | OT-N06 (Bug #3) |
| `flags_add` | Feature Flags | FF-P01, FF-P02, FF-P06, FF-N01, FF-N02, FF-N03, FF-E01, FF-E02, FF-E07, FF-E08, FF-E10 |
| `flags_delete` | Feature Flags | FF-P01, FF-P02, FF-P06, FF-N01, FF-E01, FF-E07, FF-E08, FF-E10 |
| `flags_configuration_state_update` | Feature Flags | FF-P01, FF-P02, FF-N01, FF-N07, FF-E07 |
| `flags_update_defaultValue` | Feature Flags | FF-P02, FF-N02 |
| `flag_target_groups_add` | Feature Flags | FF-P03, FF-P09, FF-E03, FF-E09 |
| `flag_target_groups_delete` | Feature Flags | FF-P03, FF-P09, FF-E03, FF-E09 |
| `flag_configuration_conditions_set` | Feature Flags | FF-P11, FF-N11, FF-E11 |
| `flag_serve_to_target_group` | Feature Flags | FF-P12, FF-N12, FF-E12 |
| `flag_custom_properties_add` | Feature Flags | FF-P04, FF-E04 |
| `flag_custom_properties_delete` | Feature Flags | FF-P04, FF-E04 |
| `automation_trigger` | Automation & Workflows | AW-E03 |
| `automation_trigger_by_branch` | Automation & Workflows | AW-P06, AW-N07, AW-E05 |
| `automation_rerun` | Automation & Workflows | AW-P07, AW-E04 |
| `automation_stop` | Automation & Workflows | AW-N05 |
| `automation_approve_manual_gate` | Automation & Workflows | AW-P08, AW-N06 |
| `automation_reject_manual_gate` | Automation & Workflows | AW-E05 |
| `workflow_validate` | Automation & Workflows | AW-P03, AW-N02, AW-E01 |
| `workflow_update_content` | Automation & Workflows | AW-P04, AW-N03, AW-E02 |
| `workflow_trigger` | Automation & Workflows | AW-P05, AW-E03, AW-E06 |
| `organizations_create` | Orgs & Teams | OT-P10, OT-N10, OT-E10 |
| `scm_repositories_sync` | Components & Repos | CR-P10, CR-E10 |
| `rbac_role_create` | RBAC | RBAC-P03, RBAC-P06, RBAC-P08, RBAC-N04, RBAC-E02, RBAC-E04, RBAC-E07, RBAC-E08 |
| `rbac_role_delete` | RBAC | RBAC-P08, RBAC-N02, RBAC-E02, RBAC-E08 |
| `security_configuration_set` | Security Advanced | SA-P03, SA-N07, SA-E07, SA-E08 |
| `security_sla_configuration_set` | Security Advanced | SA-P05, SA-E01, SA-E02, SA-E08 |
| `security_sla_configuration_remove` | Security Advanced | SA-N06, SA-E02 |
| `security_tenant_sla_configuration_remove` | Security Advanced | SA-N08 |
| `security_plugin_activate` | Security Advanced | SA-P07, SA-N04, SA-E03 |
| `security_plugin_deactivate` | Security Advanced | SA-N05, SA-E04 |
| `security_plugin_config_set` | Security Advanced | SA-E03 |
| `security_implicit_scans_set` | Security Advanced | SA-P08, SA-E06, SA-E08 |
| `services_add` | Services & Endpoints | SE-P03, SE-N03, SE-E03, SE-E05, SE-E07 |
| `services_delete` | Services & Endpoints | SE-P03, SE-N02, SE-E03, SE-E07 |
| `endpoint_add` | Services & Endpoints | SE-P05, SE-P06, SE-N05, SE-E02, SE-E08 |
| `properties_add` | Search & Properties | SP-P04, SP-N05, SP-E03 |
| `property_delete` | Search & Properties | SP-P04, SP-N04, SP-E03 |

---

## Known Bugs Being Retested

| Bug | Tool | Domain File | Test ID |
|-----|------|-------------|---------|
| Bug #1 | `user_set_timezone` 400 Bad Request | Orgs & Teams | OT-P09, OT-N08 |
| Bug #2 | `teams_memberships_list` 501 Not Implemented | Orgs & Teams | OT-P07 |
| Bug #3 | `teams_members_remove` 400 Bad Request | Orgs & Teams | OT-N06 |
| Bug #4 | `flags_update_defaultValue` 400 on Boolean flag | Feature Flags | FF-N02 |
| Bug #5 | `security_issues_all_get` fails on empty-defaultBranch component | Security | SEC-N03 |

---

## Execution Order (Recommended)

Run domains in this order to minimize dependencies and catch foundation issues first:

```
1. Security (Core)        (read-only, safe, no cleanup needed)
2. Orgs & Teams           (includes known bugs — run early to retest)
3. Feature Flags          (write ops, full lifecycle — self-contained cleanup)
4. Components & Repos     (write ops, requires endpoint/repo data from org)
5. Automation & Workflows (requires live pipeline for most write tests)
6. RBAC                   (new — write ops, self-contained cleanup)
7. Security — Advanced    (new — config/plugin writes, restore originals)
8. Services & Endpoints   (new — write ops, cleanup required)
9. Search, Properties & Resources (new — mostly read-only, one lifecycle test)
```

---

## Environment Prerequisites

```
MCP Server:    https://mcp.saas-qa.beescloud.com/v1/mcp
Auth:          OAuth Bearer token (managed by Claude Code)
Org ID:        6c5eeb79-4606-4c39-bd5c-c2323336caad
App ID:        e1903ba8-9234-4ae2-ab5f-aa0962b5be2f  (for flag tests)
Env ID:        cde9e350-0523-4bc5-99d2-b5782c583723  (for flag tests)
Endpoint ID:   413e7e54-f227-44dc-9b0d-d793e7c6f5d4  (for component create)
Live pipeline: Required for Automation & Workflows write tests (AW-P05 to AW-P08, AW-E03 to AW-E06)
```
