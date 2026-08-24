# Report Generation

`generate_report.py` reads one or more DeepEval JSON output files, merges them, and writes a self-contained HTML dashboard to `reports/`.

---

## Pipeline Overview

```mermaid
flowchart TD
    A([pytest run\n20 tests]) --> B["reports/test_run_*.json\n(one per test)"]

    B --> C["python utils/generate_report.py"]

    subgraph LOAD [Load & Parse]
        C --> D["glob reports/*.json\nor explicit paths from argv"]
        D --> E["load_json_files()\n• parse verboseLogs → sub-scores\n• accumulate totals across files\n• sort by order field"]
    end

    subgraph RENDER [Render]
        E --> F["embed as JS const REPORT = {...}\ninside HTML template"]
        F --> G["write reports/report_YYYYMMDD_HHMMSS.html\n(self-contained, no CDN)"]
    end

    G --> H([open in any browser\nworks offline])
```

---

## JSON Parsing — What Gets Extracted

```mermaid
flowchart LR
    J["test_run_*.json"] --> P["parse_verbose_logs(verboseLogs)"]

    P --> S1["primitive_usage_score"]
    P --> S2["arg_correctness_score"]
    P --> S3["tools_called  [list of names]"]

    J --> F1["testPassed / testFailed\nrunDuration"]
    J --> F2["testFile, success\nmetricsData[].reason\nactualOutput, input"]
```

`verboseLogs` is a raw string emitted by DeepEval's MCPUseMetric — the regex extractor pulls the numeric sub-scores and tool names out of it even when the schema changes between versions.

---

## Multi-File Merge

```mermaid
flowchart TD
    A["reports/test_run_001.json\nscore=0.9"] & B["reports/test_run_002.json\nscore=0.4"] & C["reports/test_run_003.json\nscore=1.0"] --> D

    D["load_json_files(paths)"]
    D --> E["merged list of test rows\nsorted by order field"]
    D --> F["aggregated totals\npassed / failed / duration\nsource file count"]
    E & F --> G["REPORT = {rows, totals, sources}"]
    G --> H["HTML template\nrun-meta subtitle:\n'3 source files · 20 tests'"]
```

Pass explicit paths for a targeted merge, or omit arguments to merge everything in `reports/`:

```bash
python utils/generate_report.py                          # all reports/*.json
python utils/generate_report.py reports/test_run_01.json # single file
python utils/generate_report.py reports/a.json reports/b.json  # two files
```

---

## HTML Dashboard Structure

```mermaid
flowchart TD
    HTML["report.html\n(self-contained)"]

    HTML --> TH["Theme toggle\n☽ / ☀\nstored in localStorage"]
    HTML --> SC["Summary cards\nTotal · Passed · Failed\nPass Rate · Duration"]
    HTML --> FT["Filter toolbar\nAll / Passed / Failed\n+ text search\n+ source-file dropdown"]
    HTML --> RT["Results table\none row per test\nID · Input · Tools Called · Score · Status"]

    RT --> OV["Detail overlay\n(click any row)"]
    OV --> OV1["Primitive Usage Score"]
    OV --> OV2["Argument Correctness Score"]
    OV --> OV3["Tools called list"]
    OV --> OV4["Eval reason (judge explanation)"]
    OV --> OV5["Agent final answer"]
    OV --> OV6["Raw verboseLogs"]
```

---

## Theme System

```mermaid
flowchart LR
    LS["localStorage\n'deepeval-theme'"] --> AT

    SM["System\nprefers-color-scheme"] --> AT

    AT["applyTheme()\ndocument.documentElement\n.setAttribute('data-theme', theme)"]

    AT --> DK["data-theme='dark'\n☀ button shown"]
    AT --> LT["data-theme='light'\n☽ button shown"]

    BTN["User clicks toggle"] --> NEXT["flip theme\nsave to localStorage"]
    NEXT --> AT
```

Priority order: saved localStorage preference → system preference (`prefers-color-scheme: dark`) → light fallback.

---

## Output Files

| File pattern | Created by | Contents |
|---|---|---|
| `reports/test_run_YYYYMMDD_HHMMSS.json` | `evaluate()` in each test | One test result per file |
| `reports/evaluation_YYYYMMDD_HHMMSS.html` | DeepEval `DisplayConfig` | DeepEval's own per-run HTML |
| `reports/report_YYYYMMDD_HHMMSS.html` | `generate_report.py` | **Merged dashboard** — this is the main report |

---

## Related Files

| File | Role |
|------|------|
| `utils/generate_report.py` | Report generator — `parse_verbose_logs()`, `load_json_files()`, HTML template |
| `tests/test_smoke.py` | Writes JSON via `DisplayConfig` after each test |
| `reports/` | Runtime output directory (git-ignored) |
