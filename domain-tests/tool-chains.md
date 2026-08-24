# CloudBees MCP — Tool Chaining Scenario Prompts

Each prompt below exercises multiple tools in sequence.
Copy and paste any prompt directly into Claude Code with the CloudBees MCP server connected.

---

## Diagnostic Categories

| Category | Definition | Failure Indicates |
|----------|-----------|-------------------|
| **Selection** | Single tool call from natural language | AI picked the wrong tool from 84+ options |
| **Chain** | 2–4 tools called in sequence | Wrong tool order, missed step, or incorrect data passed between steps |
| **Stress** | 5+ tools OR repeated calls OR large payloads | Timeout, session limit, or token exhaustion |

---

## WRITE TOOL COVERAGE AUDIT

Out of 84 total tools, **26 are write operations** (POST / DELETE / UPDATE).
The scenarios below are explicitly designed to exercise all 27.

| Write Tool | Type | Covered In |
|------------|------|------------|
| `user_set_timezone` | POST | WR-01 |
| `components_create` | POST | WR-02 |
| `components_delete` | DELETE | WR-02 |
| `teams_create` | POST | CD-07, WR-03 |
| `teams_delete` | DELETE | CD-07, WR-03 |
| `teams_invite_create` | POST | CD-07, WR-03 |
| `teams_invite_delete` | DELETE | CD-07, WR-03 |
| `teams_members_add` | POST | CD-07, WR-03 |
| `teams_members_remove` | DELETE | CD-07, WR-03 |
| `automation_trigger` | POST | WR-04 |
| `automation_trigger_by_branch` | POST | WR-04 |
| `automation_rerun` | POST | WR-04 |
| `automation_stop` | POST | WR-04 |
| `automation_approve_manual_gate` | POST | WR-05 |
| `automation_reject_manual_gate` | POST | WR-05 |
| `workflow_validate` | POST | WR-06 |
| `workflow_update_content` | POST | WR-06 |
| `workflow_trigger` | POST | WR-06 |
| `flags_add` | POST | CD-06, WR-07 |
| `flags_delete` | DELETE | CD-06, WR-07 |
| `flags_configuration_state_update` | POST | CD-06, WR-07 |
| `flags_update_defaultValue_string` | POST | WR-07 |
| `flag_target_groups_add` | POST | CD-06, WR-08 |
| `flag_target_groups_delete` | DELETE | CD-06, WR-08 |
| `flag_custom_properties_add` | POST | CD-06, WR-09 |
| `flag_custom_properties_delete` | DELETE | CD-06, WR-09 |

---

## WRITE OPERATION SCENARIOS

---

### WR-01 — User Timezone Update and Verification

**Discovery:** `Chain` | **Expected:** `user_whoami → user_preferences_get → user_set_timezone → user_preferences_get` | **Timeout:** `45s`

```
Get my current user identity. Then get my user preferences to see my current preferences including timezone. Then set my timezone to "America/New_York". Then get my user preferences again to verify the timezone was updated. Report: original timezone value, the update call response, and the new timezone value after the change. If the update fails, capture the exact error response including status code.
```

---

### WR-02 — Component Create, Verify, and Delete Lifecycle

**Discovery:** `Stress` | **Expected:** `endpoint_list → repositories_search → components_create → components_list → components_search → branches_list → components_delete` | **Timeout:** `120s`

```
List all endpoints and pick the GitHub endpoint named "User/rjain0404" (id: 413e7e54-...). Search repositories for "deploy-app-prod" to get its URL. Create a new component named "mcp-test-component-DATE" using that repository URL, endpoint ID, organization ID 6c5eeb79-4606-4c39-bd5c-c2323336caad, and defaultBranch "main". Then list all components and confirm the new component appears. Search for it by name. List its branches. Finally delete the component. Report: the created componentId, confirmation it appeared in list and search, its branches, and confirmation of deletion.
```

---

### WR-03 — Full Team Lifecycle: Create, Invite, Add Member, Remove Member, Delete

**Discovery:** `Stress` | **Expected:** `users_list → teams_create → teams_invite_create → teams_invites_list → teams_invite_delete → teams_members_add → teams_get_by_id → teams_members_remove → teams_delete` | **Timeout:** `120s`

```
List all users and pick Chitra Perumal (cperumal@cloudbees.com). Create a new team called "wr03-lifecycle-team-DATE". Invite Chitra by email to the team. List pending invites and confirm the invite appears. Delete the invite. Add Chitra as a direct member using her userId. Get the team by ID and confirm her userId appears in userIds. Attempt to remove Chitra from the team — capture the exact response whether it succeeds or fails with 400. Delete the team. Report the result of every step especially the remove step.
```

---

### WR-04 — CI/CD Pipeline Trigger, Monitor, Rerun, and Stop Lifecycle

**Discovery:** `Stress` | **Expected:** `repositories_search → branches_list → automation_trigger_by_branch → runs_list → logs_list → automation_rerun → automation_stop` | **Timeout:** `120s`

```
Search for a repository named "go" under the aspm-sv-qa endpoint. List its branches and pick the master branch. Trigger a CI run on the master branch. Capture the runId from the response. List recent runs to confirm the triggered run appears. Retrieve logs for that run. Then rerun it and capture the new runId. Finally stop the rerun. Report: the original runId, whether the run appeared in the runs listing, the log output, the rerun runId, and the stop response.
```

---

### WR-05 — Manual Gate: Trigger a Pipeline, Approve the Gate, Then Reject on a Second Run

**Discovery:** `Stress` | **Expected:** `repositories_search → automation_trigger_by_branch → runs_list → automation_jobs_list → automation_approve_manual_gate → automation_trigger_by_branch → automation_reject_manual_gate → automation_stop` | **Timeout:** `120s`

```
Search for a repository that has a pipeline with a manual gate configured. Trigger it on its default branch. List runs and find the run that is paused at a manual gate. List jobs for that run to find the gateId. Approve the manual gate. Then trigger a second run of the same pipeline. When it reaches the manual gate, reject it instead. Stop the rejected run. Report: first run outcome after approval, second run outcome after rejection, and exact responses from both gate operations. If no manual gate pipeline exists, document the skip reason.
```

---

### WR-06 — Full Workflow Lifecycle: List, Read, Validate, Update, Trigger

**Discovery:** `Stress` | **Expected:** `workflow_list → workflow_get_content → workflow_schema_get → workflow_validate → workflow_update_content → workflow_get_content → workflow_trigger → workflow_update_content` | **Timeout:** `120s`

```
List all workflows and pick the first one. Get its full content. Get the workflow schema. Validate the workflow content against the schema and report whether it is valid. Add a comment "# mcp-test-DATE" to the top of the workflow content and update it. Get the content again to confirm the update was saved. Trigger the workflow and capture the runId. Finally restore the original workflow content. Report the result of each write step.
```

---

### WR-07 — Feature Flag Full Write Lifecycle Including Default Value Update

**Discovery:** `Stress` | **Expected:** `flags_environments_list → flags_applications_list → flags_add → flags_get_by_name → flags_configurations_list → flag_configuration_get → flags_configuration_state_update → flags_update_defaultValue → flag_configuration_get → flags_configuration_state_update → flags_delete` | **Timeout:** `120s`

```
List all feature flag environments and pick the first one. List all applications and pick the first one. Create a new String type feature flag named "wr07-test-flag-DATE" with description "WR-07 write test". Get the flag by name to confirm creation. List its configurations. Get the config for the first environment. Enable the flag in that environment. Update the default value to "enabled" (use String type flag to avoid the bug seen with Boolean flags). Get the configuration again to verify the default value was updated. Disable the flag. Delete the flag. Report the result of every write step, especially whether the default value update succeeds on a String type flag.
```

---

### WR-08 — Target Group Write Lifecycle: Create with Conditions, Verify, Update Usage, Delete

**Discovery:** `Stress` | **Expected:** `flags_applications_list → flag_target_groups_add → flag_target_groups_get_by_name → flag_target_groups_list → flag_target_groups_flag_usage_per_environment → flag_target_groups_list_with_flags_usage → flag_target_groups_target_group_usage → flag_target_groups_delete` | **Timeout:** `120s`

```
List all feature flag applications and pick the first one. Create a target group named "wr08-beta-users-DATE" with a condition that matches users where the property "plan" equals "beta" using the conditions object: {"property": {"name": "plan", "operator": "eq", "operands": ["beta"]}}. Get the target group by name to verify the conditions were saved correctly. List all target groups and confirm it appears. Check flag usage per environment (expect empty). List all target groups with flag usage. Check target group nesting usage. Delete the target group. Report: whether the conditions were persisted correctly in the get response, and the deletion confirmation.
```

---

### WR-09 — Custom Property Write Lifecycle Across All Types

**Discovery:** `Stress` | **Expected:** `flags_applications_list → flag_custom_properties_add (×3) → flag_custom_properties_list → flag_custom_properties_get_by_name → flag_custom_properties_flag_usage_per_environment → flag_custom_properties_target_group_usage → flag_custom_properties_delete (×3)` | **Timeout:** `120s`

```
List all feature flag applications and pick the first one. Create three custom properties in it: (1) name "wr09-bool-prop-DATE" type Boolean, (2) name "wr09-string-prop-DATE" type String, (3) name "wr09-number-prop-DATE" type Number. List all custom properties and confirm all three appear. Get each one by name. Check flag usage per environment and target group usage for the String property. Delete all three properties. Report: whether all three were created with the correct types, whether they all appeared in the list, and deletion confirmations.
```

---

### WR-10 — Cascaded Write + Read: Create Flag with Target Group and Custom Property, Wire Them Together

**Discovery:** `Stress` | **Expected:** `flags_applications_list → flags_environments_list → flag_custom_properties_add → flag_target_groups_add → flags_add → flags_configuration_state_update → flag_target_groups_flag_usage_per_environment → flag_custom_properties_flag_usage_per_environment → flags_configuration_state_update → flags_delete → flag_target_groups_delete → flag_custom_properties_delete` | **Timeout:** `120s`

```
List all feature flag applications and environments. Pick the first application and environment. Create a custom property named "wr10-user-tier-DATE" of type String. Create a target group named "wr10-premium-users-DATE" with condition matching users where "wr10-user-tier-DATE" equals "premium": {"property": {"name": "wr10-user-tier-DATE", "operator": "eq", "operands": ["premium"]}}. Create a Boolean feature flag named "wr10-premium-feature-DATE". Enable the flag in the first environment. Check target group flag usage per environment for the target group (may be empty since flag does not reference the TG explicitly). Check custom property flag usage per environment for the custom property. Then clean up: disable and delete the flag, delete the target group, delete the custom property. Report the full chain result. This tests the full three-way write relationship between flags, target groups, and custom properties.
```

---

### WR-11 — Multi-Step Update: Change Flag State Across Multiple Environments

**Discovery:** `Stress` | **Expected:** `flags_applications_list → flags_environments_list → flags_add → flags_configuration_state_update (×N) → flags_configurations_list → flags_configuration_state_update → flags_configurations_list → flags_delete` | **Timeout:** `120s`

```
List all feature flag applications and environments. If there is more than one environment, pick the application that has the most environments. Create a new Boolean flag named "wr11-multi-env-flag-DATE". Enable the flag in each available environment one by one. After enabling all, list the flag's configurations to verify all environments show enabled=true. Then disable the flag in only the first environment. List configurations again and confirm that the first environment shows enabled=false while the others remain enabled=true. This is a "configuration drift" test. Finally disable all and delete the flag. Report the enabled/disabled state at each verification step.
```

---

## SECURITY INTELLIGENCE

---

### SC-01 — Find the Component with the Most Vulnerabilities Across All Sub-Orgs

**Discovery:** `Stress` | **Expected:** `organizations_list_suborganizations → components_list → branches_list → security_findings_summary_get (×N)` | **Timeout:** `120s`

```
List all sub-organizations. For each sub-org, list all components. For every component that has a non-empty defaultBranch, get the branch ID and get its security findings summary. Rank all components by total vulnerability count (descending) and separately by VERY_HIGH count (descending). Present two leaderboards: one for most total findings and one for most critical findings. Include the sub-org name, component name, scanner tools used, and last scanned date in the output.
```

---

### SC-02 — Find All Components That Have Never Been Scanned

**Discovery:** `Stress` | **Expected:** `organizations_list_suborganizations → components_list → branches_list → security_findings_summary_get (×N)` | **Timeout:** `120s`

```
List all sub-organizations and their components. For each component with a valid defaultBranch, get its security findings summary. Identify and list all components where the response returns zero total findings or returns an error, and flag those separately. Also list any components that have an empty defaultBranch (which would block scanning entirely). Present the results as: (1) components never scanned, (2) components with empty defaultBranch, and (3) components with zero findings (may have been scanned but found nothing).
```

---

### SC-03 — SLA Breach Report: Find All BREACHED High/Critical Issues Across a Component

**Discovery:** `Chain` | **Expected:** `components_search → branches_list → security_issues_open_get` | **Timeout:** `45s`

```
Search for the component named "go" in the aspm-automation-organization. Get its branch ID. Get the open security issues for the master branch. Filter all issues where sla.status = "BREACHED". For each breached issue, show: the vulnerability name, severity, first identified date, SLA due date, triage status, and how many days overdue it is (calculate from today's date 2026-06-10). Sort by most days overdue first.
```

---

### SC-04 — Security Risk by Sub-Org: Which Sub-Org Has the Highest Aggregate Risk Score?

**Discovery:** `Stress` | **Expected:** `organizations_list_suborganizations → components_list → branches_list → security_findings_summary_get (×N)` | **Timeout:** `120s`

```
List all sub-organizations. For each sub-org, list its components. Get the security findings summary for each component with a valid branch. Aggregate the findings at the sub-org level by summing: VERY_HIGH (weight 4), HIGH (weight 3), MEDIUM (weight 2), LOW (weight 1). Compute a weighted risk score per sub-org. Rank sub-orgs by this weighted risk score. Present a table showing each sub-org, its component count, total raw findings count, and weighted risk score.
```

---

### SC-05 — Scanner Coverage Audit: Which Scanners Are Used Across Which Components?

**Discovery:** `Stress` | **Expected:** `components_list → branches_list → security_findings_summary_get (×N)` | **Timeout:** `120s`

```
List all components across all sub-organizations. For each component with a valid defaultBranch, get its security findings summary. Extract the list of scanner tools used for each component. Build a matrix showing: which scanners (Gosec, Trivy, Snyk SCA, Snyk SAST, Snyk IaC, Checkmarx, Njsscan, Gitleaks, Grype, FindSecBugs, Checkov, SonarQube) are active on which components. Then answer: (1) which components have only 1 scanner, (2) which have the most scanners, (3) which scanners appear most frequently across all components.
```

---

### SC-06 — Multi-Branch Security Delta: Compare Vulnerabilities Across Branches of the Same Component

**Discovery:** `Chain` | **Expected:** `components_search → branches_list → security_findings_summary_get (×2)` | **Timeout:** `45s`

```
Find the component named "resolvedFindings-feb" in the aspm-automation-sub-org. List all its branches. For each branch, get its security findings summary. Compare the vulnerability counts across branches: which branch has the most findings, which has the fewest, and what is the delta in VERY_HIGH and HIGH counts between the main/default branch and any other branches. This shows whether non-default branches are more or less secure than the default.
```

---

### SC-07 — Triage Status Distribution: How Many Issues Are Unreviewed vs In-Review vs Fix-Required?

**Discovery:** `Stress` | **Expected:** `components_list → security_findings_summary_get (×3) → security_issues_open_get (×3)` | **Timeout:** `120s`

```
Pick the 3 components with the highest total vulnerability counts from all sub-orgs (use the component listing and security findings summaries to identify them). For each of those 3 components, get their open security issues. Aggregate the triage status counts across all issues: how many are UNREVIEWED, IN_REVIEW, FIX_REQUIRED, RISK_ACCEPTED, FALSE_POSITIVE. Present a triage health dashboard showing these counts per component and a combined total. Highlight any component where more than 80% of issues are still UNREVIEWED.
```

---

### SC-08 — Security Findings by Severity Trend: Which Components Have the Most HIGH Issues Within SLA?

**Discovery:** `Stress` | **Expected:** `components_list → branches_list → security_issues_open_get (×N)` | **Timeout:** `120s`

```
List all components. For each component with a valid defaultBranch, get its open security issues. From the results, separate all HIGH severity issues into two groups: (1) within SLA (sla.status = "WITHIN") and (2) breached SLA (sla.status = "BREACHED"). Rank components by count of HIGH-severity BREACHED issues. This identifies which components need the most urgent remediation attention right now.
```

---

## FEATURE FLAGS

---

### FL-01 — Flag Health Check: Which Flags Are Enabled vs Disabled Across All Applications?

**Discovery:** `Stress` | **Expected:** `flags_environments_list → flags_applications_list → flags_list (×N) → flags_configurations_list (×N)` | **Timeout:** `120s`

```
List all feature flag environments and all feature flag applications. For each application, list all flags. For each flag, list its configurations. Build a health summary showing per application: total flags, how many are enabled in each environment, how many are disabled, and how many have never been configured in any environment. Identify any flags that exist but have zero configurations (orphaned flags).
```

---

### FL-02 — Flag Usage Audit: Find All Flags With Zero Usage Across All Environments

**Discovery:** `Stress` | **Expected:** `flags_applications_list → flags_list (×N) → flags_flag_usage_per_environment (×N)` | **Timeout:** `120s`

```
List all feature flag applications. For each application, list all flags. For each flag, check its usage per environment. Find all flags where usage is empty or zero across all environments — these are flags that have been created but are not being evaluated anywhere. List them by application. These are candidates for cleanup or investigation.
```

---

### FL-03 — SDK Key Inventory: Get All SDK Keys Across All Environments and Applications

**Discovery:** `Stress` | **Expected:** `flags_environments_list → flags_applications_list → flags_sdk_key_get (×N)` | **Timeout:** `90s`

```
List all feature flag environments and all feature flag applications. For each combination of application and environment, get the SDK key. Compile a complete SDK key inventory table showing: application name, environment name, and SDK key. This is useful for auditing which SDK keys are active and whether all apps are properly configured for each environment.
```

---

### FL-04 — Target Group Impact Analysis: Which Target Groups Are Used by the Most Flags?

**Discovery:** `Stress` | **Expected:** `flags_applications_list → flag_target_groups_list_with_flags_usage → flag_target_groups_flag_usage_per_environment` | **Timeout:** `90s`

```
List all feature flag applications. For each application, list all target groups with their flags usage data. Rank target groups by the number of flags that reference them (flagUsage count). For the top 3 most-used target groups, check their flag usage per environment to get a per-environment breakdown. This shows which target groups have the highest blast radius if modified or deleted.
```

---

### FL-05 — Custom Properties Coverage: Which Applications Use Custom Properties and Which Don't?

**Discovery:** `Chain` | **Expected:** `flags_applications_list → flag_custom_properties_list (×N)` | **Timeout:** `60s`

```
List all feature flag applications. For each application, list all custom properties. Build a coverage report showing: which applications have custom properties defined, how many each has, what types they are (Boolean, String, Number, etc.), and which applications have zero custom properties. Applications with no custom properties may be missing user targeting capabilities.
```

---

### FL-06 — Flag Configuration State Drift: Are Flags Consistently Enabled Across All Environments?

**Discovery:** `Stress` | **Expected:** `flags_applications_list → flags_list (×N) → flags_configurations_list (×N)` | **Timeout:** `120s`

```
List all feature flag applications and their flags. For each flag, list its configurations. Identify flags where the enabled state is inconsistent across environments — for example, enabled in one environment but disabled in another. List these "drifted" flags by application. This is useful for detecting flags that were partially rolled out and never fully enabled or cleaned up.
```

---

### FL-07 — Pending Approvals Audit: Review All Flags Awaiting Approval With Their Current Config

**Discovery:** `Chain` | **Expected:** `flags_applications_list → flag_approval_requests_list → flag_configuration_get` | **Timeout:** `45s`

```
List all feature flag applications. For each application, list pending flag approval requests. For any pending approval requests found, get the current configuration of the flag being changed. Present a summary of: which applications have pending approvals, what the flag names are, what change is being requested, and what the current configuration state is.
```

---

## ORGANIZATIONS & TEAMS

---

### OT-01 — Full Organization Hierarchy Map with CI Metrics

**Discovery:** `Stress` | **Expected:** `organizations_list_suborganizations → organizations_suborg_report (×N)` | **Timeout:** `90s`

```
List all sub-organizations. Build a hierarchy tree showing the parent-child org relationships. Then for the top-level org and each direct child sub-org, get the sub-organization report with widget IDs ci1 through ci4 to get: project types (ci1), run counts (ci2), success rates (ci3), and duration metrics (ci4). Present the org hierarchy alongside its CI metrics.
```

---

### OT-02 — Team Membership Audit: Which Users Belong to No Custom Teams?

**Discovery:** `Chain` | **Expected:** `users_list → teams_get` | **Timeout:** `30s`

```
List all users in the organization. List all teams. For each user, check which teams include their userId in the userIds array. Identify users who are only in predefined system teams (type = PREDEFINED) but are not members of any user-defined team (type = USERDEFINED). These users may be under-onboarded or belong to a different access model than expected.
```

---

### OT-03 — Org Risk Profile: Combine Team, Endpoint, and Security Data Per Sub-Org

**Discovery:** `Stress` | **Expected:** `organizations_list_suborganizations → components_list → security_findings_summary_get (×N) → endpoint_list` | **Timeout:** `120s`

```
List all sub-organizations. For each sub-org, list its components and get the security findings summary for each. Also list all endpoints to see which SCM integrations are configured. Build a risk profile per sub-org showing: number of components, total findings (by severity), list of active scanners, and which SCM endpoints are in use. Rank sub-orgs by total VERY_HIGH + HIGH findings.
```

---

### OT-04 — New User Onboarding Check: Verify a User's Access Is Correctly Set Up

**Discovery:** `Chain` | **Expected:** `users_list → user_preferences_get → teams_get` | **Timeout:** `30s`

```
List all users. For the user named "Menaga QAUser" (mmuthuramalingam+qauser@beescloud.com), find their userId. Get their user preferences. List all teams and see which teams include their userId. Report: (1) which teams they belong to, (2) whether they are in any user-defined teams, (3) what their current preferences are (theme, onboarding status). This is a standard new-user access verification check.
```

---

## REPOSITORY & COMPONENT INTELLIGENCE

---

### RI-01 — Find All Repositories With No Linked Component (Orphaned Repos)

**Discovery:** `Chain` | **Expected:** `repositories_list → components_list` | **Timeout:** `30s`

```
List all repositories for the organization. List all components. Cross-reference: find all repositories where the serviceId field is empty (no linked component). These are repositories that are visible to CloudBees but have not been onboarded as components. List them grouped by SCM endpoint (GitHub, GitLab, Bitbucket), showing repo name, URL, and defaultBranch.
```

---

### RI-02 — Component Property Inheritance Audit

**Discovery:** `Stress` | **Expected:** `components_list → properties_list (×N)` | **Timeout:** `90s`

```
List all components in the aspm-automation-organization. For each component, list its properties. Identify: (1) components that have their own component-level properties (source = COMPONENT), (2) components that only inherit properties from the org level (source = INHERITED), and (3) components with no properties at all. List any secret properties (isSecret = true) by component, showing only the name (never the value).
```

---

### RI-03 — Branch Coverage Report: Which Components Have Multiple Branches Being Tracked?

**Discovery:** `Stress` | **Expected:** `components_list → branches_list (×N)` | **Timeout:** `90s`

```
List all components across all sub-organizations. For each component, list its branches. Identify: (1) components with only 1 branch, (2) components with 2–4 branches, (3) components with 5+ branches. For components with multiple branches, list the branch names. This reveals which components have comprehensive branch coverage in the platform vs those that only track a single branch.
```

---

### RI-04 — SCM Endpoint Coverage: Which Endpoints Have the Most and Fewest Components?

**Discovery:** `Chain` | **Expected:** `endpoint_list → components_list` | **Timeout:** `30s`

```
List all endpoints. List all components. Group components by their endpointId. For each endpoint, count how many components use it. Show: endpoint name, type (GitHub/GitLab/Bitbucket), number of linked components. Identify any endpoints with zero linked components (configured but unused) and endpoints with the most components.
```

---

## IDENTITY & ACCESS

---

### IA-01 — Full Identity Snapshot: Who Am I and What Do I Have Access To?

**Discovery:** `Stress` | **Expected:** `user_whoami → user_preferences_get → teams_get → api_tokens_list → organizations_list_suborganizations` | **Timeout:** `60s`

```
Get my identity. Get my user preferences. List all teams and find which teams include my userId. List all API tokens (names and expiry only). List all sub-organizations to see the org hierarchy I have access to. Compile a complete identity snapshot: who I am, my preferences, my team memberships, my API tokens, and the org structure visible to me.
```

---

### IA-02 — SAML & Auth Configuration Audit

**Discovery:** `Chain` | **Expected:** `saml_connections_list → saml_email_domains_list → api_tokens_list → users_list` | **Timeout:** `45s`

```
List all SAML connections to check if SAML SSO is configured. List all SAML email domains. List all API tokens in use. List all users to get the user count and login types. Compile an authentication configuration summary: is SAML enabled, which domains are SAML-managed, how many API tokens are active, and what login types are in use (password, Google OAuth, etc.). Flag any users who are using password login in an org that also has Google OAuth configured.
```

---

## CROSS-DOMAIN CHAINED SCENARIOS

---

### CD-01 — End-to-End Secure Component Onboarding Checklist

**Discovery:** `Stress` | **Expected:** `repositories_search → components_list → branches_list → security_findings_summary_get → properties_list` | **Timeout:** `90s`

```
Search for a repository named "VulnerableGoRepo4GH" in the repositories. Find the component linked to it (if any) using the component listing and cross-referencing by repository URL. Get its branches. Get its security findings summary to check if it has been scanned. List its properties to check if it has any secrets configured. Report a full onboarding health card: is the component registered, is it being scanned, how many findings does it have, and does it have its required properties configured.
```

---

### CD-02 — Feature Flag + Security Cross-Reference: Do Flag-Enabled Apps Have Clean Security Posture?

**Discovery:** `Stress` | **Expected:** `flags_applications_list → flags_list → flags_configurations_list → components_list → branches_list → security_findings_summary_get` | **Timeout:** `120s`

```
List all feature flag applications. For each application, list its flags and their configurations. Identify applications that have at least one enabled flag (enabled = true). For each such application, find the linked component (match by repositoryUrl or name). Get the security findings summary for that component. Report: for each application with enabled feature flags, what is its current security posture (total findings, VERY_HIGH count)? Flag any app that has enabled feature flags AND has VERY_HIGH severity security findings.
```

---

### CD-03 — Organization Health Dashboard: Combine People, Code, and Security Signals

**Discovery:** `Stress` | **Expected:** `user_whoami → organizations_list_suborganizations → users_list → teams_get → components_list → security_findings_summary_get → api_tokens_list → saml_connections_list` | **Timeout:** `120s`

```
Generate a comprehensive organization health dashboard by calling: get my identity (confirm auth), list sub-organizations (org structure — count sub-orgs), list all users (total user count), list all teams (number of teams), list all components (total components and how many have a valid defaultBranch), get the security findings summary for 3–5 key components (aggregate total findings), list API tokens (active token count), list SAML connections (is SSO enabled). Present a single-page health card with: org structure summary, people metrics, component count, security risk summary, and auth configuration status.
```

---

### CD-04 — Target Group + Flag + Security Blast Radius: What Would Happen If a Target Group Changed?

**Discovery:** `Stress` | **Expected:** `flags_applications_list → flag_target_groups_list_with_flags_usage → flag_target_groups_flag_usage_per_environment → flags_get → components_list → security_findings_summary_get` | **Timeout:** `120s`

```
List all feature flag applications. For each application, list all target groups with their flags usage and find the target group with the highest number of flags using it (highest blast radius). Check its flag usage per environment to see which environments it affects. List each flag that uses this target group. For each such flag, get its details. Then find the component linked to this application and report its current security findings summary. This gives the full blast radius: if this target group was deleted or modified, how many flags, environments, and what security risk context applies.
```

---

### CD-05 — Stale Component Scan Audit: Which Components Haven't Been Scanned in Over 30 Days?

**Discovery:** `Stress` | **Expected:** `components_list → branches_list → security_findings_summary_get (×N)` | **Timeout:** `120s`

```
List all components across all sub-organizations. For each component with a valid defaultBranch, get its security findings summary. From each response, extract the lastScanned timestamp. Today's date is 2026-06-10. Identify all components where lastScanned is more than 30 days ago (before 2026-05-11) or where lastScanned is null/empty. Group them into: (1) not scanned in 30–60 days, (2) not scanned in 60–90 days, (3) not scanned in 90+ days, (4) never scanned. This is a security hygiene report.
```

---

### CD-06 — Full Feature Flag Lifecycle Validation (S5 Scenario)

**Discovery:** `Stress` | **Expected:** `flags_environments_list → flags_applications_list → flags_add → flags_get_by_name → flags_configurations_list → flag_configuration_get → flags_configuration_state_update → flags_flag_usage_per_environment → flags_sdk_key_get → flags_configuration_state_update → flags_delete` | **Timeout:** `120s`

```
Run a complete feature flag lifecycle test: (1) list all environments and pick the first one, (2) list all applications and pick the first one, (3) create a new boolean flag named "lifecycle-test-flag-DATE" in that application, (4) retrieve the flag by name and confirm the id matches, (5) list its configurations and get the config for the first environment, (6) enable the flag in that environment, (7) check usage per environment (expect empty), (8) get the SDK key for the environment, (9) disable the flag, (10) delete the flag. Report pass/fail for each step and confirm the flag is gone after deletion.
```

---

### CD-07 — Team Lifecycle + Membership Validation (S2 Scenario)

**Discovery:** `Stress` | **Expected:** `users_list → teams_create → teams_invite_create → teams_invites_list → teams_members_add → teams_get_by_id → teams_members_remove → teams_delete` | **Timeout:** `120s`

```
Run a complete team lifecycle test: (1) list all users and pick one who is not the current user, (2) create a new team named "lifecycle-test-team-DATE", (3) create an invite for that user's email to the team, (4) list invites and confirm the invite appears, (5) add the user as a direct member using their userId, (6) get the team by ID and confirm the userId appears in userIds, (7) attempt to remove the user from the team and capture the exact response (this is expected to fail with 400 — document the response), (8) delete the team. Report the result of each step clearly, especially step 7.
```

---

### CD-08 — Endpoint + Repository + Component Traceability Chain

**Discovery:** `Stress` | **Expected:** `endpoint_list → repositories_list → repositories_search → components_search → branches_list → security_findings_summary_get` | **Timeout:** `90s`

```
List all configured endpoints. For the GitHub endpoint named "AA-Prod-ASPM" (id: 33591c6d-...), list all repositories connected to it. Search for a repository named "vulnado-new". Find its linked component using a component search. Get the component's branches. Get the security findings summary for the default branch. Present a full traceability chain: Endpoint → Repository → Component → Branch → Security Findings summary. This validates the entire onboarding chain from SCM integration to security visibility.
```

---

## Summary Table

### Read-Only Scenarios (GET chains)

| # | Prompt ID | Domain | Tools in Chain | Complexity |
|---|-----------|--------|---------------|------------|
| 1 | SC-01 | Security | org_list → comp_list → branches → findings_summary | High |
| 2 | SC-02 | Security | org_list → comp_list → branches → findings_summary | High |
| 3 | SC-03 | Security | comp_list → branches → issues_open | Medium |
| 4 | SC-04 | Security | org_list → comp_list → branches → findings_summary | High |
| 5 | SC-05 | Security | comp_list → branches → findings_summary | High |
| 6 | SC-06 | Security | comp_list → branches → findings_summary (multi-branch) | Medium |
| 7 | SC-07 | Security | comp_list → branches → issues_open | Medium |
| 8 | SC-08 | Security | comp_list → branches → issues_open | Medium |
| 9 | FL-01 | Flags | apps → flags_list → configs_list | Medium |
| 10 | FL-02 | Flags | apps → flags_list → usage_per_env | Medium |
| 11 | FL-03 | Flags | envs → apps → sdk_key | Low |
| 12 | FL-04 | Flags | apps → tg_list_with_usage → tg_flag_usage_per_env | Medium |
| 13 | FL-05 | Flags | apps → custom_props_list | Low |
| 14 | FL-06 | Flags | apps → flags_list → configs_list | Medium |
| 15 | FL-07 | Flags | apps → approval_requests → flag_config_get | Medium |
| 16 | OT-01 | Orgs | org_list → suborg_report (multi-widget) | Medium |
| 17 | OT-02 | Teams | users_list → teams_get | Low |
| 18 | OT-03 | Orgs | org_list → comp_list → findings_summary → endpoint_list | High |
| 19 | OT-04 | Teams/Users | users_list → preferences → teams_get | Low |
| 20 | RI-01 | Repos | repositories_list → components_list | Low |
| 21 | RI-02 | Components | comp_list → properties_list | Low |
| 22 | RI-03 | Components | comp_list → branches_list | Low |
| 23 | RI-04 | Endpoints | endpoint_list → comp_list | Low |
| 24 | IA-01 | Identity | whoami → preferences → teams → tokens → org_list | Low |
| 25 | IA-02 | Auth | saml_connections → saml_domains → tokens → users_list | Low |
| 26 | CD-01 | Cross-domain | repos_search → comp_list → branches → findings → properties | High |
| 27 | CD-02 | Cross-domain | flag_apps → flags → configs → comp_list → branches → findings | High |
| 28 | CD-03 | Cross-domain | whoami → org_list → users → teams → comp_list → findings → tokens | High |
| 29 | CD-04 | Cross-domain | flag_apps → tg_list_usage → tg_flag_usage → flags_get → comp → findings | High |
| 30 | CD-05 | Security | comp_list → branches → findings_summary (date filter) | High |
| 31 | CD-06 | Flags | Full flag lifecycle (10 tools) | Medium |
| 32 | CD-07 | Teams | Full team lifecycle (8 tools) | Medium |
| 33 | CD-08 | Repos | endpoint → repos → comp_search → branches → findings | Medium |

### Write Operation Scenarios (POST / DELETE chains)

| # | Prompt ID | Domain | Write Tools Exercised | Also Covers (GET) | Complexity |
|---|-----------|--------|-----------------------|-------------------|------------|
| 34 | WR-01 | Identity | `user_set_timezone` | whoami, preferences_get | Low |
| 35 | WR-02 | Components | `components_create`, `components_delete` | endpoint_list, repos_search, comp_list, comp_search, branches_list | Medium |
| 36 | WR-03 | Teams | `teams_create`, `teams_invite_create`, `teams_invite_delete`, `teams_members_add`, `teams_members_remove`, `teams_delete` | users_list, teams_get_by_id, invites_list | Medium |
| 37 | WR-04 | CI/CD | `automation_trigger_by_branch`, `automation_rerun`, `automation_stop` | repos_search, branches_list, runs_list, logs_list | High |
| 38 | WR-05 | CI/CD | `automation_approve_manual_gate`, `automation_reject_manual_gate`, `automation_trigger_by_branch`, `automation_stop` | runs_list, automation_jobs_list | High |
| 39 | WR-06 | Workflows | `workflow_validate`, `workflow_update_content`, `workflow_trigger` | workflow_list, workflow_get_content, workflow_schema_get | High |
| 40 | WR-07 | Flags | `flags_add`, `flags_configuration_state_update`, `flags_update_defaultValue_string`, `flags_delete` | flags_environments_list, flags_applications_list, flags_get_by_name, flags_configurations_list, flag_configuration_get | Medium |
| 41 | WR-08 | Target Groups | `flag_target_groups_add`, `flag_target_groups_delete` | apps_list, tg_get_by_name, tg_list, tg_flag_usage_per_env, tg_list_with_usage, tg_target_group_usage | Medium |
| 42 | WR-09 | Custom Props | `flag_custom_properties_add` (x3 types), `flag_custom_properties_delete` (x3) | apps_list, cp_list, cp_get_by_name, cp_flag_usage, cp_tg_usage | Medium |
| 43 | WR-10 | Flags + TG + CP | `flag_custom_properties_add`, `flag_target_groups_add`, `flags_add`, `flags_configuration_state_update`, `flags_delete`, `flag_target_groups_delete`, `flag_custom_properties_delete` | apps_list, envs_list, tg_flag_usage, cp_flag_usage | High |
| 44 | WR-11 | Flags | `flags_add`, `flags_configuration_state_update` (x3), `flags_delete` | apps_list, envs_list, flags_configurations_list | Medium |

### Write Tool Coverage Summary

| Write Tool | Covered In | Status |
|------------|------------|--------|
| `user_set_timezone` | WR-01 | Done |
| `components_create` | WR-02 | Done |
| `components_delete` | WR-02 | Done |
| `teams_create` | WR-03, CD-07 | Done |
| `teams_delete` | WR-03, CD-07 | Done |
| `teams_invite_create` | WR-03, CD-07 | Done |
| `teams_invite_delete` | WR-03, CD-07 | Done |
| `teams_members_add` | WR-03, CD-07 | Done |
| `teams_members_remove` | WR-03, CD-07 | Done |
| `automation_trigger_by_branch` | WR-04, WR-05 | Done |
| `automation_trigger` | WR-04 | Done |
| `automation_rerun` | WR-04 | Done |
| `automation_stop` | WR-04, WR-05 | Done |
| `automation_approve_manual_gate` | WR-05 | Done |
| `automation_reject_manual_gate` | WR-05 | Done |
| `workflow_validate` | WR-06 | Done |
| `workflow_update_content` | WR-06 | Done |
| `workflow_trigger` | WR-06 | Done |
| `flags_add` | WR-07, WR-10, WR-11, CD-06 | Done |
| `flags_delete` | WR-07, WR-10, WR-11, CD-06 | Done |
| `flags_configuration_state_update` | WR-07, WR-10, WR-11, CD-06 | Done |
| `flags_update_defaultValue_string` | WR-07 | Done |
| `flag_target_groups_add` | WR-08, WR-10, CD-06 | Done |
| `flag_target_groups_delete` | WR-08, WR-10, CD-06 | Done |
| `flag_custom_properties_add` | WR-09, WR-10, CD-06 | Done |
| `flag_custom_properties_delete` | WR-09, WR-10, CD-06 | Done |

**Total prompts: 44 | Read scenarios: 33 | Write scenarios: 11 | All 26 write tools covered**
