# Domain: Reports & Analytics
**Tools covered (4):** `controllers_data_get`, `controllers_list`, `organizations_suborg_report`, `report_drilldown_get`
**Total prompts:** 12 (4 positive, 4 negative, 4 edge)

> **Cross-domain tools used for setup:** `user_whoami` (default), `organizations_list` (default), `organizations_list_suborganizations` (default)

---

## Test Execution Tracker

| ID | Type | Category | Expected Tools | Timeout | Status | Notes |
|----|------|----------|----------------|---------|--------|-------|
| RA-P01 | Positive | Chain | `organizations_list` → `controllers_list` | 20s | ⬜ | |
| RA-P02 | Positive | Chain | `organizations_list` → `controllers_list` → `controllers_data_get` | 30s | ⬜ | |
| RA-P03 | Positive | Chain | `organizations_list_suborganizations` → `organizations_suborg_report` ×4 | 60s | ⬜ | All widget IDs |
| RA-P04 | Positive | Chain | `organizations_list` → `controllers_list` → `report_drilldown_get` | 30s | ⬜ | |
| RA-N01 | Negative | Selection | `controllers_data_get` (nil controller ID) | 15s | ⬜ | |
| RA-N02 | Negative | Selection | `organizations_suborg_report` (nil org ID) | 15s | ⬜ | |
| RA-N03 | Negative | Selection | `report_drilldown_get` (nil controller ID) | 15s | ⬜ | |
| RA-N04 | Negative | Selection | `controllers_list` (nil org ID) | 15s | ⬜ | |
| RA-E01 | Edge | Chain | `organizations_list_suborganizations` → `organizations_suborg_report` (multiple sub-orgs) | 60s | ⬜ | |
| RA-E02 | Edge | Chain | `organizations_list` → `controllers_list` → `controllers_data_get` (multiple controllers) | 60s | ⬜ | |
| RA-E03 | Edge | Chain | `organizations_list` → `controllers_list` → `report_drilldown_get` (empty drilldown) | 30s | ⬜ | |
| RA-E04 | Edge | Chain | `organizations_list_suborganizations` → `organizations_suborg_report` (leaf node suborg) | 30s | ⬜ | |

---

## Diagnostic Categories

| Category | Definition | Failure Indicates |
|----------|-----------|-------------------|
| **Selection** | Single tool call from natural language | AI picked the wrong tool from 131 options |
| **Chain** | 2–4 tools called in sequence | Wrong tool order, missed step, or incorrect data passed between steps |
| **Stress** | 5+ tools OR repeated calls OR large payloads | Timeout, session limit, or token exhaustion |

---

## Test Setup

> Resolve all IDs at runtime.
> Call `organizations_list` for org ID; `organizations_list_suborganizations` for sub-org IDs.
> Nil UUID for negative tests: `00000000-0000-0000-0000-000000000099`

---

## POSITIVE TEST CASES

---

### RA-P01 — List Controllers for Organization
**Discovery:** `Chain` | **Expected:** `organizations_list → controllers_list` | **Timeout:** `20s`

```
Call organizations_list to get the org ID.
Call controllers_list for that organization.
Report: total controller count, each controller's id, name, and type.
If no controllers exist, record "0 controllers — empty result OK".
```

---

### RA-P02 — Get Report Data for a Controller
**Discovery:** `Chain` | **Expected:** `organizations_list → controllers_list → controllers_data_get` | **Timeout:** `30s`

```
1. Call organizations_list to get the org ID.
2. Call controllers_list to get a controller ID.
3. Call controllers_data_get for that controller.
Report: all report data fields returned (widget ID, data points, time range).
If no controllers exist, record "No controllers found — test skipped".
```

---

### RA-P03 — Sub-Organization Report for Multiple Widget IDs
**Discovery:** `Chain` | **Expected:** `organizations_list_suborganizations → organizations_suborg_report ×4` | **Timeout:** `60s`

```
Call organizations_list_suborganizations to get a sub-org ID.
For the first sub-org found, call organizations_suborg_report with each of these widget IDs:
- ci1
- ci2
- ci3
- ci4
For each call, report: the widget title and data returned. Note which widgets return data vs empty data vs errors.
```

---

### RA-P04 — Get Report Drilldown for a Controller
**Discovery:** `Chain` | **Expected:** `organizations_list → controllers_list → report_drilldown_get` | **Timeout:** `30s`

```
1. Call organizations_list to get the org ID.
2. Call controllers_list to get a controller ID.
3. Call report_drilldown_get for that controller.
Report: the drilldown data fields returned.
If no drilldown data is available, record the response as-is (empty drilldown is acceptable).
```

---

## NEGATIVE TEST CASES

---

### RA-N01 — Get Controller Data with Non-Existent Controller ID
**Discovery:** `Selection` | **Expected:** `controllers_data_get` | **Timeout:** `15s`

```
Call controllers_data_get with a nil controller ID: 00000000-0000-0000-0000-000000000099.
Record the exact error message and HTTP status code. Expected: 404 or 400.
```

---

### RA-N02 — Sub-Org Report with Non-Existent Org ID
**Discovery:** `Selection` | **Expected:** `organizations_suborg_report` | **Timeout:** `15s`

```
Call organizations_suborg_report with a nil org ID: 00000000-0000-0000-0000-000000000099 and widget "ci1".
Record the exact error message and HTTP status code. Expected: 404 or 400.
```

---

### RA-N03 — Report Drilldown with Non-Existent Controller ID
**Discovery:** `Selection` | **Expected:** `report_drilldown_get` | **Timeout:** `15s`

```
Call report_drilldown_get with a nil controller ID: 00000000-0000-0000-0000-000000000099.
Record the exact error message and HTTP status code. Expected: 404 or 400.
```

---

### RA-N04 — List Controllers for Non-Existent Org
**Discovery:** `Selection` | **Expected:** `controllers_list` | **Timeout:** `15s`

```
Call controllers_list with a nil org ID: 00000000-0000-0000-0000-000000000099.
Record the exact error message and HTTP status code. Expected: 404 or 400.
```

---

## EDGE CASES

---

### RA-E01 — Sub-Org Report for Multiple Sub-Organizations
**Discovery:** `Chain` | **Expected:** `organizations_list_suborganizations → organizations_suborg_report (multiple sub-orgs)` | **Timeout:** `60s`

```
Call organizations_list_suborganizations to get all sub-orgs.
For the first 3 sub-orgs, call organizations_suborg_report with widget "ci1" for each.
Report: the data returned per sub-org. Note any sub-org that returns empty data vs actual data.
Verify: the tool does not fail even when some sub-orgs have no data.
```

---

### RA-E02 — Get Report Data for All Controllers
**Discovery:** `Chain` | **Expected:** `organizations_list → controllers_list → controllers_data_get (multiple)` | **Timeout:** `60s`

```
1. Call organizations_list to get the org ID.
2. Call controllers_list to get all controllers.
3. For each controller (up to 5), call controllers_data_get.
4. Report: which controllers return data vs empty, and any error responses.
Verify the tool handles multiple sequential calls without degradation.
```

---

### RA-E03 — Report Drilldown Returns Empty for Controller with No Drilldown
**Discovery:** `Chain` | **Expected:** `organizations_list → controllers_list → report_drilldown_get` | **Timeout:** `30s`

```
1. Call controllers_list to get all controllers.
2. Call report_drilldown_get for each controller (up to 3).
3. Verify: empty drilldown data is returned without an error.
Record which controllers have drilldown data and which return empty.
```

---

### RA-E04 — Sub-Org Report for a Leaf Node Sub-Organization
**Discovery:** `Chain` | **Expected:** `organizations_list_suborganizations → organizations_suborg_report (leaf node)` | **Timeout:** `30s`

```
1. Call organizations_list_suborganizations to get all sub-orgs.
2. Identify a leaf-node sub-org (one with no children).
3. Call organizations_suborg_report for that leaf sub-org with widget "ci1".
4. Verify: a leaf-node sub-org can return report data without error.
If no leaf node is found, use the deepest available sub-org.
```
