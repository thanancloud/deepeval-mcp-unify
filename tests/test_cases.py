"""
Smoke test cases drawn verbatim from domain-tests/smoke.md.
REMOVED tools are excluded. Write-lifecycle tools appear in their natural
prompt order (create → use → delete) as separate cases.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class EvalCase:
    id: str
    prompt: str
    expected_tool_names: list[str]
    timeout_seconds: int


SMOKE_CASES: list[EvalCase] = [
    # ── Identity & User Preferences ───────────────────────────────────────────
    EvalCase(
        id="smoke-1",
        prompt="Who am I on CloudBees? Show my full profile.",
        expected_tool_names=["user_whoami"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-2",
        prompt="Show my CloudBees user preferences.",
        expected_tool_names=["user_preferences_get"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-3",
        prompt="Set my CloudBees timezone to UTC.",
        expected_tool_names=["user_set_timezone"],
        timeout_seconds=15,
    ),
    # ── Users ─────────────────────────────────────────────────────────────────
    EvalCase(
        id="smoke-4",
        prompt="List all users in the CloudBees organization.",
        expected_tool_names=["users_list"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-5",
        prompt="Search for my own user details using my email address.",
        expected_tool_names=["users_get"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-6",
        prompt="Get user details for user ID f3039d4a-7c3a-11f0-9a1c-42010a83ae54.",
        expected_tool_names=["users_get_by_id"],
        timeout_seconds=15,
    ),
    # ── Teams lifecycle ───────────────────────────────────────────────────────
    EvalCase(
        id="smoke-7",
        prompt="Create a team named 'smoke-test-team-01'.",
        expected_tool_names=["teams_create"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-8",
        prompt="List all teams and find the one named 'smoke-test-team-01'.",
        expected_tool_names=["teams_get"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-9",
        prompt=(
            "Get team details using the teamId from the team named 'smoke-test-team-01' "
            "that was just created."
        ),
        expected_tool_names=["teams_get_by_id"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-10",
        prompt="Invite the first user in the users list to smoke-test-team-01.",
        expected_tool_names=["teams_invite_create"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-11",
        prompt="List all pending invites for smoke-test-team-01.",
        expected_tool_names=["teams_invites_list"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-12",
        prompt="Delete the invite we just created for smoke-test-team-01.",
        expected_tool_names=["teams_invite_delete"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-13",
        prompt="Add the first user in the users list to smoke-test-team-01 as a member.",
        expected_tool_names=["teams_members_add"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-14",
        prompt="List all memberships in smoke-test-team-01.",
        expected_tool_names=["teams_memberships_list"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-15",
        prompt="Remove the first user from smoke-test-team-01.",
        expected_tool_names=["teams_members_remove"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-16",
        prompt="Delete smoke-test-team-01.",
        expected_tool_names=["teams_delete"],
        timeout_seconds=15,
    ),
    # ── Organizations ─────────────────────────────────────────────────────────
    EvalCase(
        id="smoke-17",
        prompt="Search for organizations with 'cloudbees' in the name.",
        expected_tool_names=["organizations_search"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-18",
        prompt="List all sub-organizations under the current organization.",
        expected_tool_names=["organizations_list_suborganizations"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-19",
        prompt="Get the sub-org report (widget ci1) for the first sub-organization.",
        expected_tool_names=["organizations_suborg_report"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-20",
        prompt="List all organizations accessible to me.",
        expected_tool_names=["organizations_list"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-21",
        prompt="Get the organization with ID 6c5eeb79-4606-4c39-bd5c-c2323336caad.",
        expected_tool_names=["organizations_get"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-22",
        prompt=(
            "Create a sub-organization with displayName 'smoke-org-01' and domainName "
            "'smoke-org-01' under parent 6c5eeb79-4606-4c39-bd5c-c2323336caad."
        ),
        expected_tool_names=["organizations_create"],
        timeout_seconds=15,
    ),
    # ── Components & SCM ─────────────────────────────────────────────────────
    EvalCase(
        id="smoke-29",
        prompt="List all available extensions for the organization.",
        expected_tool_names=["extensions_list"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-30",
        prompt=(
            "List branches from the SCM provider for the VulnerableGoRepo4GH repository "
            "(endpoint 413e7e54-f227-44dc-9b0d-d793e7c6f5d4, "
            "url https://github.com/rjain0404/VulnerableGoRepo4GH.git)."
        ),
        expected_tool_names=["scm_branches_list"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-31",
        prompt="List registered GitHub App registrations for the organization.",
        expected_tool_names=["scm_gh_app_registrations_list"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-32",
        prompt="Trigger a sync of repositories from the SCM provider for the organization.",
        expected_tool_names=["scm_repositories_sync"],
        timeout_seconds=15,
    ),
    # ── Resources, Properties, Endpoints ─────────────────────────────────────
    EvalCase(
        id="smoke-33",
        prompt="List all available resources in CloudBees.",
        expected_tool_names=["resources_list"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-34",
        prompt=(
            "List all properties for the 'go' component "
            "(95fdf71c-de53-43e4-b5dc-bec7170becd6)."
        ),
        expected_tool_names=["properties_list"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-35",
        prompt="List all configured endpoints.",
        expected_tool_names=["endpoint_list"],
        timeout_seconds=15,
    ),
    # ── Controllers ───────────────────────────────────────────────────────────
    EvalCase(
        id="smoke-36",
        prompt="List all CloudBees controllers.",
        expected_tool_names=["controllers_list"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-37",
        prompt="Get data for the first controller in the list.",
        expected_tool_names=["controllers_data_get"],
        timeout_seconds=15,
    ),
    # ── CI/CD Automation ──────────────────────────────────────────────────────
    EvalCase(
        id="smoke-38",
        prompt="List all automation jobs.",
        expected_tool_names=["automation_jobs_list"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-39",
        prompt="Trigger the first automation job.",
        expected_tool_names=["automation_trigger"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-40",
        prompt="Trigger the first automation job on its default branch.",
        expected_tool_names=["automation_trigger_by_branch"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-41",
        prompt="Rerun the most recent run of the first automation job.",
        expected_tool_names=["automation_rerun"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-42",
        prompt="Stop the run we just triggered.",
        expected_tool_names=["automation_stop"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-43",
        prompt="Check if any job has a pending manual gate and approve it.",
        expected_tool_names=["automation_approve_manual_gate"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-44",
        prompt="Check if any job has a pending manual gate and reject it.",
        expected_tool_names=["automation_reject_manual_gate"],
        timeout_seconds=15,
    ),
    # ── Repositories, Branches, Runs, Logs, Actions ───────────────────────────
    EvalCase(
        id="smoke-45",
        prompt="List all repositories in the organization.",
        expected_tool_names=["repositories_list"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-46",
        prompt="Search repositories for 'test'.",
        expected_tool_names=["repositories_search"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-47",
        prompt="List branches for the first repository's linked component.",
        expected_tool_names=["branches_list"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-48",
        prompt="List recent runs for the first automation job.",
        expected_tool_names=["runs_list"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-49",
        prompt="List logs for the most recent run.",
        expected_tool_names=["logs_list"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-50",
        prompt="List all available CloudBees actions.",
        expected_tool_names=["actions_list"],
        timeout_seconds=15,
    ),
    # ── Workflows ─────────────────────────────────────────────────────────────
    EvalCase(
        id="smoke-51",
        prompt="List all workflows.",
        expected_tool_names=["workflow_list"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-52",
        prompt="Get the content of the first workflow.",
        expected_tool_names=["workflow_get_content"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-53",
        prompt="Get the workflow schema.",
        expected_tool_names=["workflow_schema_get"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-54",
        prompt="Validate the content of the first workflow.",
        expected_tool_names=["workflow_validate"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-55",
        prompt="Add a comment '# smoke test' to the first workflow and save.",
        expected_tool_names=["workflow_update_content"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-56",
        prompt="Trigger the first workflow.",
        expected_tool_names=["workflow_trigger"],
        timeout_seconds=15,
    ),
    # ── Feature Flags — Core ──────────────────────────────────────────────────
    EvalCase(
        id="smoke-58",
        prompt="List all feature flag environments.",
        expected_tool_names=["flags_environments_list"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-59",
        prompt="List all feature flag applications.",
        expected_tool_names=["flags_applications_list"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-60",
        prompt="Create a boolean feature flag named 'smoke-flag-01'.",
        expected_tool_names=["flags_add"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-61",
        prompt="List all feature flags in the first application.",
        expected_tool_names=["flags_list"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-62",
        prompt="Get the smoke-flag-01 flag details by its ID.",
        expected_tool_names=["flags_get"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-63",
        prompt="Get the flag named 'smoke-flag-01' by name.",
        expected_tool_names=["flags_get_by_name"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-64",
        prompt="Update smoke-flag-01 default value to 'false'.",
        expected_tool_names=["flags_update_defaultValue"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-65",
        prompt="Show usage of smoke-flag-01 per environment.",
        expected_tool_names=["flags_flag_usage_per_environment"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-67",
        prompt="Delete smoke-flag-01.",
        expected_tool_names=["flags_delete"],
        timeout_seconds=15,
    ),
    # ── Feature Flags — Configuration ─────────────────────────────────────────
    EvalCase(
        id="smoke-68",
        prompt=(
            "List all flag configurations for the first application "
            "and first environment."
        ),
        expected_tool_names=["flags_configurations_list"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-69",
        prompt="Get the configuration for smoke-flag-01 in the first environment.",
        expected_tool_names=["flag_configuration_get"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-70",
        prompt="Enable smoke-flag-01 in the first environment.",
        expected_tool_names=["flags_configuration_state_update"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-71",
        prompt=(
            "Set targeting conditions on smoke-flag-01 in the first environment, "
            "linking to smoke-tg-01 with flagValue=true."
        ),
        expected_tool_names=["flag_configuration_conditions_set"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-73",
        prompt="List all pending flag approval requests.",
        expected_tool_names=["flag_approval_requests_list"],
        timeout_seconds=15,
    ),
    # ── Feature Flags — Target Groups ─────────────────────────────────────────
    EvalCase(
        id="smoke-74",
        prompt="Create a target group named 'smoke-tg-01'.",
        expected_tool_names=["flag_target_groups_add"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-75",
        prompt="Get the smoke-tg-01 target group by its ID.",
        expected_tool_names=["flag_target_groups_get"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-76",
        prompt="Get the target group named 'smoke-tg-01' by name.",
        expected_tool_names=["flag_target_groups_get_by_name"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-77",
        prompt="List all target groups in the first application.",
        expected_tool_names=["flag_target_groups_list"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-78",
        prompt="Check flag usage per environment for smoke-tg-01.",
        expected_tool_names=["flag_target_groups_flag_usage_per_environment"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-79",
        prompt="List all target groups with their flag usage data.",
        expected_tool_names=["flag_target_groups_list_with_flags_usage"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-80",
        prompt="Get overall usage for smoke-tg-01.",
        expected_tool_names=["flag_target_groups_target_group_usage"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-80a",
        prompt=(
            "Serve value true to smoke-tg-01 for smoke-flag-01 in the first environment "
            "with enableIfDisabled=true."
        ),
        expected_tool_names=["flag_serve_to_target_group"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-81",
        prompt="Delete smoke-tg-01.",
        expected_tool_names=["flag_target_groups_delete"],
        timeout_seconds=15,
    ),
    # ── Feature Flags — Custom Properties ─────────────────────────────────────
    EvalCase(
        id="smoke-82",
        prompt="Create a string custom property named 'smoke-prop-01'.",
        expected_tool_names=["flag_custom_properties_add"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-83",
        prompt="Get the smoke-prop-01 custom property by its ID.",
        expected_tool_names=["flag_custom_properties_get"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-84",
        prompt="Get the custom property named 'smoke-prop-01' by name.",
        expected_tool_names=["flag_custom_properties_get_by_name"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-85",
        prompt="List all custom properties in the first application.",
        expected_tool_names=["flag_custom_properties_list"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-86",
        prompt="Check flag usage per environment for smoke-prop-01.",
        expected_tool_names=["flag_custom_properties_flag_usage_per_environment"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-87",
        prompt="Get target group usage for smoke-prop-01.",
        expected_tool_names=["flag_custom_properties_target_group_usage"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-88",
        prompt="Delete smoke-prop-01.",
        expected_tool_names=["flag_custom_properties_delete"],
        timeout_seconds=15,
    ),
    # ── Security ──────────────────────────────────────────────────────────────
    EvalCase(
        id="smoke-89",
        prompt="Get the security findings summary for the 'go' component.",
        expected_tool_names=["security_findings_summary_get"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-90",
        prompt="List all open security issues for the 'go' component.",
        expected_tool_names=["security_issues_open_get"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-91",
        prompt=(
            "List all security issues (open and resolved) for the first sub-org."
        ),
        expected_tool_names=["security_issues_all_get"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-92",
        prompt=(
            "List all security filter tools for the first feature flag application."
        ),
        expected_tool_names=["security_filter_tools_list"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-93",
        prompt=(
            "List all application security filters for the first feature flag application."
        ),
        expected_tool_names=["security_filters_list"],
        timeout_seconds=15,
    ),
    # ── Auth & SAML ───────────────────────────────────────────────────────────
    EvalCase(
        id="smoke-94",
        prompt="List all API tokens.",
        expected_tool_names=["api_tokens_list"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-95",
        prompt="List all SAML connections.",
        expected_tool_names=["saml_connections_list"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-96",
        prompt="List all SAML email domains.",
        expected_tool_names=["saml_email_domains_list"],
        timeout_seconds=15,
    ),
    # ── Reports ───────────────────────────────────────────────────────────────
    EvalCase(
        id="smoke-97",
        prompt="Get a drill-down report for security findings.",
        expected_tool_names=["report_drilldown_get"],
        timeout_seconds=15,
    ),
    # ── RBAC ──────────────────────────────────────────────────────────────────
    EvalCase(
        id="smoke-98",
        prompt="List all available RBAC permissions for the organization.",
        expected_tool_names=["rbac_permissions_list"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-99",
        prompt="List all RBAC roles in the organization.",
        expected_tool_names=["rbac_roles_list"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-100",
        prompt="Create a custom RBAC role named 'smoke-rbac-role-01'.",
        expected_tool_names=["rbac_role_create"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-101",
        prompt="Get the details of the 'smoke-rbac-role-01' role by its ID.",
        expected_tool_names=["rbac_role_get"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-102",
        prompt="List all RBAC authorizations in the organization.",
        expected_tool_names=["rbac_authorizations_list"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-103",
        prompt=(
            "Check if the current user has read and write permissions in the organization."
        ),
        expected_tool_names=["rbac_authorization_check_bulk"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-105",
        prompt="Delete the 'smoke-rbac-role-01' role.",
        expected_tool_names=["rbac_role_delete"],
        timeout_seconds=15,
    ),
    # ── Security Advanced ─────────────────────────────────────────────────────
    EvalCase(
        id="smoke-106",
        prompt="Get the security configuration for the organization.",
        expected_tool_names=["security_configuration_get"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-107",
        prompt="Get the security configuration hierarchy for the organization.",
        expected_tool_names=["security_configuration_hierarchy_get"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-108",
        prompt=(
            "Toggle the first boolean security configuration field to its current "
            "value (no-op update to verify write works)."
        ),
        expected_tool_names=["security_configuration_set"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-109",
        prompt="Get the SLA configuration for the organization.",
        expected_tool_names=["security_sla_configuration_get"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-110",
        prompt="Set the LOW severity SLA window to 90 days.",
        expected_tool_names=["security_sla_configuration_set"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-111",
        prompt=(
            "Remove the custom SLA configuration for the first sub-organization."
        ),
        expected_tool_names=["security_sla_configuration_remove"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-112",
        prompt="Remove the tenant-level SLA configuration for the organization.",
        expected_tool_names=["security_tenant_sla_configuration_remove"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-113",
        prompt="Activate the first available security plugin for the organization.",
        expected_tool_names=["security_plugin_activate"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-114",
        prompt="Get the configuration for the first available security plugin.",
        expected_tool_names=["security_plugin_config_get"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-115",
        prompt="Update a non-critical config field on the first security plugin.",
        expected_tool_names=["security_plugin_config_set"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-116",
        prompt="Deactivate the security plugin we just activated.",
        expected_tool_names=["security_plugin_deactivate"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-117",
        prompt="Enable implicit security scans for the organization.",
        expected_tool_names=["security_implicit_scans_set"],
        timeout_seconds=15,
    ),
    # ── Services & Endpoints ──────────────────────────────────────────────────
    EvalCase(
        id="smoke-118",
        prompt="List all services in the organization.",
        expected_tool_names=["services_list"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-119",
        prompt="Create a service named 'smoke-service-01'.",
        expected_tool_names=["services_add"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-120",
        prompt="Get the details of the 'smoke-service-01' service by its ID.",
        expected_tool_names=["services_get"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-121",
        prompt="Delete the 'smoke-service-01' service.",
        expected_tool_names=["services_delete"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-122",
        prompt=(
            "Add a new GitHub endpoint named 'smoke-endpoint-01' "
            "(use placeholder credentials)."
        ),
        expected_tool_names=["endpoint_add"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-123",
        prompt="Prepare a GitHub SCM connector for the organization.",
        expected_tool_names=["endpoint_scm_connector_prepare"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-126",
        prompt="Get the ticketing webhook URL for the organization.",
        expected_tool_names=["ticketing_webhook_url_get"],
        timeout_seconds=15,
    ),
    # ── Search, Properties & Resources ───────────────────────────────────────
    EvalCase(
        id="smoke-127",
        prompt="Search for resources containing 'go' in the organization.",
        expected_tool_names=["search_resources"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-128",
        prompt="Search for recent pipeline runs in the organization (last 7 days).",
        expected_tool_names=["search_runs"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-129",
        prompt=(
            "Get the first property for the 'go' component by its property ID."
        ),
        expected_tool_names=["properties_get"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-130",
        prompt=(
            "Add a string property 'SMOKE_TEST_PROP' with value 'smoke-value' "
            "to the 'go' component."
        ),
        expected_tool_names=["properties_add"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-131",
        prompt="Delete the 'SMOKE_TEST_PROP' property we just added.",
        expected_tool_names=["property_delete"],
        timeout_seconds=15,
    ),
    EvalCase(
        id="smoke-132",
        prompt=(
            "Get the details of the master branch resource for the 'go' component "
            "by its resource ID."
        ),
        expected_tool_names=["resources_get"],
        timeout_seconds=15,
    ),
]
