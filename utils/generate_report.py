#!/usr/bin/env python3
"""
DeepEval HTML Report Generator
Reads one or more reports/*.json files and produces a self-contained HTML dashboard.

Usage:
    python generate_report.py                      # reads all reports/*.json
    python generate_report.py reports/foo.json     # explicit file(s)
"""

import glob
import json
import os
import re
import sys
from datetime import datetime


# ---------------------------------------------------------------------------
# Data extraction
# ---------------------------------------------------------------------------

def _re_float(pattern, text, default=None):
    m = re.search(pattern, text)
    return float(m.group(1)) if m else default


def _re_text(pattern, text, default=""):
    m = re.search(pattern, text, re.DOTALL)
    return m.group(1).strip() if m else default


def parse_verbose_logs(logs: str) -> dict:
    tools = re.findall(r"MCPToolCall\(name='([^']+)'", logs)
    prim_score = _re_float(r"Primitive Usage Score:\s*([\d.]+)", logs)
    arg_score = _re_float(r"Argument Correctness Score:\s*([\d.]+)", logs)
    prim_reason = _re_text(
        r"Primitive Usage Reason:\s*(.+?)(?:\nArgument Correctness Score:|\Z)", logs
    )
    return {
        "tools_called": tools,
        "primitive_usage_score": prim_score,
        "arg_correctness_score": arg_score,
        "primitive_usage_reason": prim_reason,
    }


def load_json_files(paths: list[str]) -> dict:
    all_test_cases = []
    total_passed = 0
    total_failed = 0
    total_duration = 0.0
    all_metrics_scores = []
    multi_source = len(paths) > 1

    for path in paths:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        source_name = os.path.basename(path)
        total_passed += data.get("testPassed", 0)
        total_failed += data.get("testFailed", 0)
        total_duration += data.get("runDuration", 0.0)
        all_metrics_scores.extend(data.get("metricsScores", []))

        for tc in data.get("testCases", []):
            enriched = dict(tc)
            enriched["_source"] = source_name if multi_source else None

            for md in enriched.get("metricsData", []):
                logs = md.get("verboseLogs", "")
                md["_parsed"] = parse_verbose_logs(logs)

            all_test_cases.append(enriched)

    # Sort by original order field
    all_test_cases.sort(key=lambda t: t.get("order", 0))

    # Aggregate metrics scores by metric name
    metrics_map: dict[str, dict] = {}
    for ms in all_metrics_scores:
        name = ms["metric"]
        if name not in metrics_map:
            metrics_map[name] = {"metric": name, "passes": 0, "fails": 0, "errors": 0, "scores": []}
        metrics_map[name]["passes"] += ms.get("passes", 0)
        metrics_map[name]["fails"] += ms.get("fails", 0)
        metrics_map[name]["errors"] += ms.get("errors", 0)
        metrics_map[name]["scores"].extend(ms.get("scores", []))

    # Derive threshold and eval model from first test case
    threshold = 0.7
    eval_model = ""
    if all_test_cases and all_test_cases[0].get("metricsData"):
        md0 = all_test_cases[0]["metricsData"][0]
        threshold = md0.get("threshold", 0.7)
        eval_model = md0.get("evaluationModel", "")

    return {
        "testCases": all_test_cases,
        "metricsScores": list(metrics_map.values()),
        "testPassed": total_passed,
        "testFailed": total_failed,
        "runDuration": total_duration,
        "multi_source": multi_source,
        "threshold": threshold,
        "evalModel": eval_model,
        "sources": [os.path.basename(p) for p in paths],
    }


# ---------------------------------------------------------------------------
# HTML template
# ---------------------------------------------------------------------------

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>DeepEval Report</title>
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --bg:        #0d1117;
  --surface:   #161b27;
  --surface2:  #1e2438;
  --border:    #2a3150;
  --text:      #e2e8f0;
  --muted:     #8892a4;
  --accent:    #4f8ef7;
  --green:     #22c55e;
  --green-bg:  #0d2e1a;
  --red:       #ef4444;
  --red-bg:    #2d1111;
  --amber:     #f59e0b;
  --amber-bg:  #2d2005;
  --radius:    10px;
  --shadow:    0 4px 24px rgba(0,0,0,.5);
}

body {
  background: var(--bg);
  color: var(--text);
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  font-size: 14px;
  line-height: 1.6;
  min-height: 100vh;
  transition: background .2s, color .2s;
}

.theme-toggle {
  width: 32px; height: 32px;
  border-radius: 8px;
  border: 1px solid var(--border);
  background: var(--surface2);
  color: var(--muted);
  cursor: pointer;
  font-size: 15px;
  display: flex; align-items: center; justify-content: center;
  transition: all .15s;
  flex-shrink: 0;
}
.theme-toggle:hover { border-color: var(--accent); color: var(--accent); }

/* ── Layout ─────────────────────────────────────────── */
.page { max-width: 1400px; margin: 0 auto; padding: 28px 24px 60px; }

/* ── Header ─────────────────────────────────────────── */
.header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 28px;
}
.header-left h1 {
  font-size: 22px;
  font-weight: 700;
  color: var(--text);
  letter-spacing: -0.3px;
}
.header-left .subtitle {
  font-size: 12px;
  color: var(--muted);
  margin-top: 3px;
}
.header-right { display: flex; gap: 8px; flex-wrap: wrap; align-items: center; }
.badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: .3px;
}
.badge-blue   { background: rgba(79,142,247,.15); color: var(--accent); border: 1px solid rgba(79,142,247,.3); }
.badge-muted  { background: var(--surface2); color: var(--muted); border: 1px solid var(--border); }

/* ── Summary cards ──────────────────────────────────── */
.cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(170px, 1fr));
  gap: 14px;
  margin-bottom: 28px;
}
.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 18px 20px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  transition: border-color .2s;
}
.card:hover { border-color: var(--accent); }
.card-label {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: .8px;
  color: var(--muted);
  font-weight: 600;
}
.card-value {
  font-size: 30px;
  font-weight: 700;
  line-height: 1;
}
.card-sub {
  font-size: 11px;
  color: var(--muted);
}
.card-green .card-value { color: var(--green); }
.card-red   .card-value { color: var(--red); }
.card-blue  .card-value { color: var(--accent); }
.card-amber .card-value { color: var(--amber); }

/* pass-rate card with inline bar */
.rate-bar {
  height: 5px;
  border-radius: 3px;
  background: var(--border);
  overflow: hidden;
  margin-top: 4px;
}
.rate-bar-fill {
  height: 100%;
  border-radius: 3px;
  background: linear-gradient(90deg, var(--green), #16a34a);
  transition: width .6s ease;
}

/* ── Toolbar ─────────────────────────────────────────── */
.toolbar {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 16px;
}
.filter-group { display: flex; gap: 4px; }
.filter-btn {
  padding: 6px 14px;
  border-radius: 6px;
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--muted);
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all .15s;
}
.filter-btn:hover { border-color: var(--accent); color: var(--text); }
.filter-btn.active { background: var(--accent); border-color: var(--accent); color: #fff; }

.search-wrap { flex: 1; min-width: 200px; max-width: 380px; position: relative; }
.search-wrap svg {
  position: absolute;
  left: 10px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--muted);
  pointer-events: none;
}
#search {
  width: 100%;
  padding: 7px 12px 7px 34px;
  border-radius: 6px;
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--text);
  font-size: 13px;
  outline: none;
  transition: border-color .15s;
}
#search:focus { border-color: var(--accent); }

#source-filter {
  padding: 6px 12px;
  border-radius: 6px;
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--text);
  font-size: 12px;
  cursor: pointer;
  outline: none;
}

.result-count { margin-left: auto; font-size: 12px; color: var(--muted); }

/* ── Table ───────────────────────────────────────────── */
.table-wrap {
  overflow-x: auto;
  border-radius: var(--radius);
  border: 1px solid var(--border);
}
table {
  width: 100%;
  border-collapse: collapse;
  min-width: 680px;
}
thead th {
  background: var(--surface2);
  padding: 11px 14px;
  text-align: left;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: .6px;
  color: var(--muted);
  border-bottom: 1px solid var(--border);
  white-space: nowrap;
}
tbody tr {
  border-bottom: 1px solid var(--border);
  cursor: pointer;
  transition: background .12s;
}
tbody tr:last-child { border-bottom: none; }
tbody tr:hover { background: var(--surface2); }
tbody tr.hidden { display: none; }
td {
  padding: 12px 14px;
  vertical-align: middle;
}
.td-num { color: var(--muted); font-size: 12px; width: 36px; }
.td-input {
  max-width: 340px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-size: 13px;
}
.td-score {
  font-size: 13px;
  font-weight: 700;
  white-space: nowrap;
}
.score-pass { color: var(--green); }
.score-partial { color: var(--amber); }
.score-fail { color: var(--red); }

.pill {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 3px 9px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 700;
  white-space: nowrap;
}
.pill-pass { background: var(--green-bg); color: var(--green); border: 1px solid rgba(34,197,94,.25); }
.pill-fail { background: var(--red-bg);   color: var(--red);   border: 1px solid rgba(239,68,68,.25); }

.tools-list { display: flex; flex-wrap: wrap; gap: 4px; }
.tool-chip {
  display: inline-block;
  padding: 2px 7px;
  background: rgba(79,142,247,.1);
  border: 1px solid rgba(79,142,247,.25);
  color: var(--accent);
  border-radius: 4px;
  font-size: 10px;
  font-family: 'SFMono-Regular', 'Consolas', monospace;
  white-space: nowrap;
}
.tools-more { font-size: 10px; color: var(--muted); padding: 2px 4px; }
.td-dur { color: var(--muted); font-size: 12px; white-space: nowrap; }
.td-source { font-size: 11px; color: var(--muted); white-space: nowrap; }

.empty-state {
  text-align: center;
  padding: 40px;
  color: var(--muted);
  font-size: 13px;
}

/* ── Overlay ─────────────────────────────────────────── */
.overlay-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,.65);
  backdrop-filter: blur(3px);
  z-index: 100;
  opacity: 0;
  pointer-events: none;
  transition: opacity .2s;
}
.overlay-backdrop.visible {
  opacity: 1;
  pointer-events: all;
}
.overlay {
  position: fixed;
  top: 0;
  right: 0;
  width: min(740px, 100vw);
  height: 100vh;
  background: var(--surface);
  border-left: 1px solid var(--border);
  box-shadow: -8px 0 40px rgba(0,0,0,.6);
  z-index: 101;
  display: flex;
  flex-direction: column;
  transform: translateX(100%);
  transition: transform .25s cubic-bezier(.4,0,.2,1);
  overflow: hidden;
}
.overlay.visible { transform: translateX(0); }

.overlay-header {
  padding: 20px 22px 16px;
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: flex-start;
  gap: 12px;
  background: var(--surface2);
}
.overlay-title {
  flex: 1;
  font-size: 15px;
  font-weight: 600;
  line-height: 1.5;
  word-break: break-word;
}
.overlay-close {
  width: 28px; height: 28px;
  border-radius: 6px;
  border: 1px solid var(--border);
  background: transparent;
  color: var(--muted);
  cursor: pointer;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  margin-top: 1px;
  transition: all .15s;
}
.overlay-close:hover { background: var(--red-bg); color: var(--red); border-color: var(--red); }

.overlay-body {
  flex: 1;
  overflow-y: auto;
  padding: 20px 22px 30px;
  display: flex;
  flex-direction: column;
  gap: 22px;
}

/* score mini-cards */
.score-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}
.score-card {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 14px 16px;
}
.score-card-label {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: .7px;
  color: var(--muted);
  font-weight: 700;
  margin-bottom: 6px;
}
.score-card-value {
  font-size: 24px;
  font-weight: 700;
}

/* section block */
.section { display: flex; flex-direction: column; gap: 8px; }
.section-label {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: .7px;
  color: var(--muted);
  font-weight: 700;
}
.section-text {
  font-size: 13px;
  line-height: 1.7;
  color: var(--text);
}

.tools-big { display: flex; flex-wrap: wrap; gap: 6px; }
.tool-chip-big {
  padding: 4px 10px;
  background: rgba(79,142,247,.1);
  border: 1px solid rgba(79,142,247,.3);
  color: var(--accent);
  border-radius: 6px;
  font-size: 12px;
  font-family: 'SFMono-Regular', 'Consolas', monospace;
}

/* agent output */
.agent-output {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 14px 16px;
  font-size: 12px;
  font-family: 'SFMono-Regular', 'Consolas', monospace;
  color: #a0aec0;
  white-space: pre-wrap;
  word-break: break-word;
  max-height: 260px;
  overflow-y: auto;
  line-height: 1.65;
}

/* details/summary for verbose logs */
details {
  border: 1px solid var(--border);
  border-radius: 8px;
  overflow: hidden;
}
details summary {
  padding: 10px 14px;
  background: var(--surface2);
  cursor: pointer;
  font-size: 12px;
  font-weight: 600;
  color: var(--muted);
  list-style: none;
  display: flex;
  align-items: center;
  gap: 6px;
  user-select: none;
}
details summary::-webkit-details-marker { display: none; }
details summary::before {
  content: '▶';
  font-size: 9px;
  transition: transform .15s;
}
details[open] summary::before { transform: rotate(90deg); }
details summary:hover { color: var(--text); }
.verbose-pre {
  padding: 12px 14px;
  font-size: 11px;
  font-family: 'SFMono-Regular', 'Consolas', monospace;
  color: var(--muted);
  white-space: pre-wrap;
  word-break: break-word;
  max-height: 360px;
  overflow-y: auto;
  line-height: 1.6;
  background: var(--bg);
}

/* scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--muted); }

/* ── Light theme ─────────────────────────────────────── */
[data-theme="light"] {
  --bg:        #f5f7fa;
  --surface:   #ffffff;
  --surface2:  #eef1f6;
  --border:    #d1d9e6;
  --text:      #1a202c;
  --muted:     #64748b;
  --accent:    #2563eb;
  --green:     #16a34a;
  --green-bg:  #dcfce7;
  --red:       #dc2626;
  --red-bg:    #fee2e2;
  --amber:     #d97706;
  --amber-bg:  #fef3c7;
}

/* responsive */
@media (max-width: 600px) {
  .score-cards { grid-template-columns: 1fr 1fr; }
  .cards       { grid-template-columns: repeat(2, 1fr); }
}
</style>
</head>
<body>

<div class="page">

  <!-- Header -->
  <div class="header">
    <div class="header-left">
      <h1>DeepEval Test Report</h1>
      <div class="subtitle" id="run-meta"></div>
    </div>
    <div class="header-right">
      <button class="theme-toggle" id="theme-toggle" title="Toggle theme" aria-label="Toggle theme">&#9728;</button>
      <div id="header-badges"></div>
    </div>
  </div>

  <!-- Summary Cards -->
  <div class="cards" id="summary-cards"></div>

  <!-- Toolbar -->
  <div class="toolbar">
    <div class="filter-group">
      <button class="filter-btn active" data-filter="all">All</button>
      <button class="filter-btn" data-filter="pass">Passed</button>
      <button class="filter-btn" data-filter="fail">Failed</button>
    </div>
    <div class="search-wrap">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
      </svg>
      <input id="search" type="text" placeholder="Search test inputs…" autocomplete="off"/>
    </div>
    <select id="source-filter" style="display:none"></select>
    <span class="result-count" id="result-count"></span>
  </div>

  <!-- Table -->
  <div class="table-wrap">
    <table id="results-table">
      <thead>
        <tr id="table-head"></tr>
      </thead>
      <tbody id="table-body"></tbody>
    </table>
  </div>

</div>

<!-- Overlay backdrop -->
<div class="overlay-backdrop" id="backdrop"></div>

<!-- Detail overlay -->
<div class="overlay" id="overlay">
  <div class="overlay-header">
    <div class="overlay-title" id="ov-title"></div>
    <button class="overlay-close" id="overlay-close" aria-label="Close">&times;</button>
  </div>
  <div class="overlay-body" id="overlay-body"></div>
</div>

<script>
// ── Data ──────────────────────────────────────────────────────────────────
const REPORT = __REPORT_DATA__;

// ── Helpers ───────────────────────────────────────────────────────────────
function esc(s) {
  return String(s ?? '')
    .replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')
    .replace(/"/g,'&quot;').replace(/'/g,'&#39;');
}

function scoreColor(score, threshold) {
  if (score === null || score === undefined) return '';
  if (score >= threshold) return 'score-pass';
  if (score > 0) return 'score-partial';
  return 'score-fail';
}

function scoreFmt(score) {
  if (score === null || score === undefined) return '—';
  return score.toFixed(2);
}

function durFmt(s) {
  return s != null ? s.toFixed(1) + 's' : '—';
}

// ── Summary cards ─────────────────────────────────────────────────────────
function buildSummary() {
  const { testPassed, testFailed, runDuration, threshold, evalModel, sources, metricsScores } = REPORT;
  const total = testPassed + testFailed;
  const rate  = total > 0 ? Math.round((testPassed / total) * 100) : 0;

  // header meta
  document.getElementById('run-meta').textContent =
    `Generated ${new Date().toLocaleString()}  ·  ${total} test${total !== 1 ? 's' : ''}  ·  ${sources.length} source file${sources.length !== 1 ? 's' : ''}`;

  // badges
  const badgeArea = document.getElementById('header-badges');
  const metricName = metricsScores[0]?.metric ?? 'Metric';
  badgeArea.innerHTML = `
    <span class="badge badge-blue">${esc(metricName)} ≥ ${threshold}</span>
    <span class="badge badge-muted" title="${esc(evalModel)}">${esc(evalModel.split('/').pop())}</span>
  `;

  // cards
  const cards = document.getElementById('summary-cards');
  cards.innerHTML = `
    <div class="card">
      <div class="card-label">Total Tests</div>
      <div class="card-value card-blue" style="color:var(--text)">${total}</div>
    </div>
    <div class="card card-green">
      <div class="card-label">Passed</div>
      <div class="card-value">${testPassed}</div>
    </div>
    <div class="card card-red">
      <div class="card-label">Failed</div>
      <div class="card-value">${testFailed}</div>
    </div>
    <div class="card card-blue">
      <div class="card-label">Pass Rate</div>
      <div class="card-value">${rate}%</div>
      <div class="rate-bar"><div class="rate-bar-fill" style="width:${rate}%"></div></div>
    </div>
    <div class="card card-amber">
      <div class="card-label">Run Duration</div>
      <div class="card-value" style="font-size:22px">${durFmt(runDuration)}</div>
    </div>
  `;
}

// ── Table ─────────────────────────────────────────────────────────────────
const multiSource = REPORT.multi_source;
const threshold   = REPORT.threshold;

function buildTableHead() {
  const head = document.getElementById('table-head');
  const cols = ['#','Test Input','Status','Score','Prim Use','Arg Correct','Tools Called','Duration'];
  if (multiSource) cols.push('Source');
  head.innerHTML = cols.map(c => `<th>${c}</th>`).join('');
}

function toolsHtml(tools, max=3) {
  if (!tools || tools.length === 0) return '<span style="color:var(--muted);font-size:11px">—</span>';
  const shown = tools.slice(0, max);
  const rest  = tools.length - max;
  let h = shown.map(t => `<span class="tool-chip">${esc(t)}</span>`).join('');
  if (rest > 0) h += `<span class="tools-more">+${rest}</span>`;
  return `<div class="tools-list">${h}</div>`;
}

function buildTableRows() {
  const tbody = document.getElementById('table-body');
  const rows  = REPORT.testCases;

  if (!rows.length) {
    tbody.innerHTML = `<tr><td colspan="9" class="empty-state">No test cases found.</td></tr>`;
    return;
  }

  tbody.innerHTML = rows.map((tc, idx) => {
    const md     = tc.metricsData?.[0] ?? {};
    const parsed = md._parsed ?? {};
    const score  = md.score;
    const prim   = parsed.primitive_usage_score;
    const arg    = parsed.arg_correctness_score;
    const tools  = parsed.tools_called ?? [];
    const pass   = tc.success;

    const statusCell = pass
      ? `<span class="pill pill-pass">✓ Pass</span>`
      : `<span class="pill pill-fail">✗ Fail</span>`;

    const scoreCell  = `<span class="td-score ${scoreColor(score, threshold)}">${scoreFmt(score)}</span>`;
    const primCell   = `<span class="td-score ${scoreColor(prim,  threshold)}">${scoreFmt(prim)}</span>`;
    const argCell    = `<span class="td-score ${scoreColor(arg,   threshold)}">${scoreFmt(arg)}</span>`;

    const sourceTd = multiSource ? `<td class="td-source">${esc(tc._source ?? '')}</td>` : '';
    const filterAttr = pass ? 'pass' : 'fail';

    return `<tr data-idx="${idx}" data-filter="${filterAttr}" data-input="${esc(tc.input ?? '')}">
      <td class="td-num">${idx + 1}</td>
      <td class="td-input" title="${esc(tc.input)}">${esc(tc.input)}</td>
      <td>${statusCell}</td>
      <td>${scoreCell}</td>
      <td>${primCell}</td>
      <td>${argCell}</td>
      <td>${toolsHtml(tools)}</td>
      <td class="td-dur">${durFmt(tc.runDuration)}</td>
      ${sourceTd}
    </tr>`;
  }).join('');

  // click handler
  tbody.querySelectorAll('tr').forEach(row => {
    row.addEventListener('click', () => openOverlay(parseInt(row.dataset.idx)));
  });
}

// ── Filter / search ───────────────────────────────────────────────────────
let activeFilter = 'all';
let activeSearch = '';
let activeSource = '';

function applyFilters() {
  const rows = document.querySelectorAll('#table-body tr[data-filter]');
  let visible = 0;
  rows.forEach(row => {
    const f = row.dataset.filter;
    const input = (row.dataset.input ?? '').toLowerCase();
    const src   = row.querySelector('.td-source')?.textContent ?? '';

    const filterOk = activeFilter === 'all' || activeFilter === f;
    const searchOk = !activeSearch || input.includes(activeSearch.toLowerCase());
    const sourceOk = !activeSource || src === activeSource;

    const show = filterOk && searchOk && sourceOk;
    row.classList.toggle('hidden', !show);
    if (show) visible++;
  });

  const total = REPORT.testCases.length;
  document.getElementById('result-count').textContent =
    visible === total ? `${total} tests` : `${visible} / ${total} tests`;
}

document.querySelectorAll('.filter-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    activeFilter = btn.dataset.filter;
    applyFilters();
  });
});

document.getElementById('search').addEventListener('input', e => {
  activeSearch = e.target.value;
  applyFilters();
});

// Source filter (multi-file)
function buildSourceFilter() {
  const sel = document.getElementById('source-filter');
  if (!multiSource) return;
  sel.style.display = '';
  const sources = ['', ...REPORT.sources];
  sel.innerHTML = sources.map(s =>
    `<option value="${esc(s)}">${s ? esc(s) : 'All sources'}</option>`
  ).join('');
  sel.addEventListener('change', e => {
    activeSource = e.target.value;
    applyFilters();
  });
}

// ── Overlay ───────────────────────────────────────────────────────────────
const overlay   = document.getElementById('overlay');
const backdrop  = document.getElementById('backdrop');
const ovClose   = document.getElementById('overlay-close');

function openOverlay(idx) {
  const tc     = REPORT.testCases[idx];
  const md     = tc.metricsData?.[0] ?? {};
  const parsed = md._parsed ?? {};
  const score  = md.score;
  const prim   = parsed.primitive_usage_score;
  const arg    = parsed.arg_correctness_score;
  const tools  = parsed.tools_called ?? [];
  const pass   = tc.success;

  // title
  document.getElementById('ov-title').innerHTML =
    `<span class="pill ${pass ? 'pill-pass' : 'pill-fail'}" style="margin-right:8px">${pass ? '✓ Pass' : '✗ Fail'}</span>${esc(tc.input)}`;

  // body sections
  const reasonText = (md.reason ?? '').replace(/^\[\s*/,'').replace(/\s*\]$/,'').trim();
  const primReason  = parsed.primitive_usage_reason ?? '';
  const verboseLogs = md.verboseLogs ?? '';
  const actualOut   = tc.actualOutput ?? '';

  document.getElementById('overlay-body').innerHTML = `
    <!-- Score breakdown -->
    <div class="score-cards">
      <div class="score-card">
        <div class="score-card-label">Overall Score</div>
        <div class="score-card-value ${scoreColor(score, threshold)}">${scoreFmt(score)}</div>
        <div style="font-size:11px;color:var(--muted);margin-top:4px">threshold ${threshold}</div>
      </div>
      <div class="score-card">
        <div class="score-card-label">Primitive Use</div>
        <div class="score-card-value ${scoreColor(prim, threshold)}">${scoreFmt(prim)}</div>
        <div style="font-size:11px;color:var(--muted);margin-top:4px">tool selection</div>
      </div>
      <div class="score-card">
        <div class="score-card-label">Arg Correctness</div>
        <div class="score-card-value ${scoreColor(arg, threshold)}">${scoreFmt(arg)}</div>
        <div style="font-size:11px;color:var(--muted);margin-top:4px">argument quality</div>
      </div>
    </div>

    ${tools.length ? `
    <!-- Tools called -->
    <div class="section">
      <div class="section-label">MCP Tools Called</div>
      <div class="tools-big">${tools.map(t => `<span class="tool-chip-big">${esc(t)}</span>`).join('')}</div>
    </div>` : ''}

    ${reasonText ? `
    <!-- Eval reason -->
    <div class="section">
      <div class="section-label">Evaluation Reason</div>
      <div class="section-text">${esc(reasonText)}</div>
    </div>` : ''}

    ${primReason ? `
    <!-- Prim usage reason -->
    <details>
      <summary>Primitive Usage Reasoning</summary>
      <div class="verbose-pre">${esc(primReason)}</div>
    </details>` : ''}

    ${actualOut ? `
    <!-- Agent response -->
    <div class="section">
      <div class="section-label">Agent Response</div>
      <div class="agent-output">${esc(actualOut)}</div>
    </div>` : ''}

    ${verboseLogs ? `
    <!-- Verbose logs -->
    <details>
      <summary>Raw Verbose Logs</summary>
      <div class="verbose-pre">${esc(verboseLogs)}</div>
    </details>` : ''}
  `;

  overlay.classList.add('visible');
  backdrop.classList.add('visible');
  document.body.style.overflow = 'hidden';
}

function closeOverlay() {
  overlay.classList.remove('visible');
  backdrop.classList.remove('visible');
  document.body.style.overflow = '';
}

ovClose.addEventListener('click', closeOverlay);
backdrop.addEventListener('click', closeOverlay);
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeOverlay(); });

// ── Theme toggle ──────────────────────────────────────────────────────────
const THEME_KEY = 'deepeval-theme';
const toggleBtn = document.getElementById('theme-toggle');

function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  toggleBtn.textContent = theme === 'light' ? '☽' : '☀';
  toggleBtn.title = theme === 'light' ? 'Switch to dark mode' : 'Switch to light mode';
}

const saved = localStorage.getItem(THEME_KEY);
const systemDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
applyTheme(saved ?? (systemDark ? 'dark' : 'light'));

toggleBtn.addEventListener('click', () => {
  const next = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
  localStorage.setItem(THEME_KEY, next);
  applyTheme(next);
});

// ── Init ──────────────────────────────────────────────────────────────────
buildSummary();
buildTableHead();
buildTableRows();
buildSourceFilter();
applyFilters();
</script>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def resolve_input_files(args: list[str]) -> list[str]:
    if args:
        return sorted(args)
    # Auto-detect: all *.json in reports/ that aren't the output
    base = os.path.join(os.path.dirname(__file__), "reports")
    found = sorted(glob.glob(os.path.join(base, "*.json")))
    # Exclude the deepeval lock file
    found = [f for f in found if not f.endswith(".test_run.lock")]
    if not found:
        raise FileNotFoundError(f"No JSON files found in {base}")
    return found


def main():
    input_files = resolve_input_files(sys.argv[1:])
    print(f"Loading {len(input_files)} file(s):")
    for f in input_files:
        print(f"  {f}")

    data = load_json_files(input_files)

    # Embed data into HTML
    data_json = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    html = HTML_TEMPLATE.replace("__REPORT_DATA__", data_json)

    # Write output
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = os.path.join(os.path.dirname(__file__), "reports")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"report_{ts}.html")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

    total = data["testPassed"] + data["testFailed"]
    rate  = round(data["testPassed"] / total * 100) if total else 0
    print(f"\nReport written: {out_path}")
    print(f"  {data['testPassed']}/{total} passed ({rate}%)  |  {data['testFailed']} failed  |  {data['runDuration']:.1f}s total")


if __name__ == "__main__":
    main()
