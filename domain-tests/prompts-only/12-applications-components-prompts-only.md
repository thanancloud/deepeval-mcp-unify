# Applications & Components — Prompts Only

---

## POSITIVE TEST CASES

### AC-P01 — List Repositories for an Organization

```
List all organizations to get the current org.
List all repositories for that organization.
Report: total repository count, each repo's name, SCM provider (GitHub, etc.), and URL.
```

---

### AC-P02 — Search Repositories by Partial Name

```
List all repositories to get the first repository's name.
Extract a 3–5 character partial string from that name.
Search repositories using that partial string.
Verify the known repository appears in the search results.
Report: total results found, and whether the expected repo is present.
```

---

### AC-P03 — List Branches for a Component

```
List all services to find a component (type=COMPONENT).
List all active branches for that component using its organization.
Report: total branch count, each branch's name, last commit hash, and author.
```

---

### AC-P04 — List GitHub App Registrations

```
List all organizations to get the org.
List all registered GitHub Apps for that organization.
Report: each registered GitHub App's name and app URL.
If no registrations exist, record "0 GitHub App registrations — empty result OK".
```

---

### AC-P05 — List SCM Branches via SCM Provider

```
1. List all organizations to get the org.
2. List all endpoints for the org to find SCM connector endpoints.
3. From the results, get an SCM connector endpoint ID.
4. List all repositories to get a repository.
5. List branches from the SCM provider for that repository using the connector endpoint ID.
Report: branch names returned from the SCM provider directly.
If no SCM connector is found, record "No SCM connector endpoint found — test skipped".
```

---

### AC-P06 — Trigger SCM Repository Sync

```
1. List all organizations to get the org.
2. List registered GitHub Apps to confirm an SCM integration exists.
3. If an integration exists, trigger an asynchronous repository sync for the org.
4. Report the response (job ID, status, or acknowledgement).
5. List repositories after a brief moment — verify the sync was initiated.
If no SCM integration exists, record "No SCM integration found — test skipped".
```

---

## NEGATIVE TEST CASES

### AC-N01 — Repository Search with No Matching Results

```
Search repositories using "xyzzy-repo-no-match-9999999".
Record the exact response. Expected: empty results array or 0 results — NOT an error.
```

---

### AC-N02 — List Branches for Non-Existent Component

```
Attempt to list branches for a nil component ID: 00000000-0000-0000-0000-000000000099.
Record the exact error message and HTTP status code. Expected: 404 or 400.
```

---

### AC-N03 — SCM Branches List with Invalid Endpoint ID

```
Attempt to list SCM branches using a nil connector endpoint ID: 00000000-0000-0000-0000-000000000099 and repository name "fake-repo".
Record the exact error message and HTTP status code. Expected: 404 or 400.
```

---

### AC-N04 — SCM Repository Sync with Non-Existent Org

```
Attempt to trigger a repository sync for a nil org ID: 00000000-0000-0000-0000-000000000099.
Record the exact error message and HTTP status code. Expected: 404 or 400.
```

---

### AC-N05 — List Repositories for Non-Existent Org

```
Attempt to list repositories for a nil org ID: 00000000-0000-0000-0000-000000000099.
Record the exact error message and HTTP status code. Expected: 404 or 400.
```

---

### AC-N06 — List GitHub App Registrations for Non-Existent Org

```
Attempt to list GitHub App registrations for a nil org ID: 00000000-0000-0000-0000-000000000099.
Record the exact error message and HTTP status code. Expected: 404 or 400.
```

---

## EDGE CASES

### AC-E01 — Exact Name Match in Repository Search

```
List repositories to get an exact repository name.
Search repositories using the full exact name.
Verify: exactly one result is returned matching that name.
Compare: does the exact-match search return the same repository object as the list?
```

---

### AC-E02 — List Branches for Component with Single Branch

```
List all services to find components.
Identify a component likely to have only one branch (e.g., a simple or new service).
List branches for that component.
Verify: at least one branch is returned and the call does not error on small branch counts.
```

---

### AC-E03 — Verify Default Branch Is Listed for Every Component

```
List all services to get up to 3 components.
For each component, list its branches.
Verify: for each component, at least one branch is listed. Note if any component returns an empty branch list.
Report: which components have branches and which (if any) return empty.
```

---

### AC-E04 — Repository Count Before and After Sync

```
1. List all organizations to get the org.
2. List repositories — record the total count (before sync).
3. Trigger a repository sync.
4. List repositories again — record the new total count (after sync).
Report: did the count change? Were any new repositories added?
Note: the sync is asynchronous — a count change is possible but not guaranteed immediately.
```

---

### AC-E05 — SCM Branches for Repository with Many Branches

```
1. List all organizations to get the org.
2. List endpoints to get an SCM connector endpoint ID.
3. List repositories to find a repository (prefer one expected to have many branches).
4. List branches from the SCM provider for that repository.
Report: total branch count returned, whether pagination is indicated in the response.
If no SCM connector, record "No SCM connector — test skipped".
```

---

### AC-E06 — Cross-Verify Repositories via List and Search

```
1. List all services to get a component's associated repository name (if available).
2. List all repositories — find that repository in the full list.
3. Search repositories with the same repository name.
4. Verify: the repository appears in both results and the data is consistent (same name, same URL).
Report any fields that differ between the list and search responses.
```
