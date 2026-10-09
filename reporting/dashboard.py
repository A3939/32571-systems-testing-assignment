"""A self-contained, offline dashboard built from real pytest outcomes."""
import base64
from collections import Counter
from datetime import datetime, timezone
from html import escape
import os
from pathlib import Path
import platform
import time

import pytest
from reporting.kpi import panels, CSS

SCENARIOS = {
    "test_t001_s01_valid_registration": ("Registration", "T001 · S01", "Register with valid details", "A new account is created and the confirmation page appears."),
    "test_t001_s02_password_mismatch": ("Registration", "T001 · S02", "Reject mismatched passwords", "A password-confirmation error appears."),
    "test_t001_s03_policy_required": ("Registration", "T001 · S03", "Require privacy-policy acceptance", "Registration is rejected with a privacy-policy warning."),
    "test_t002_s01_valid_login": ("Login", "T002 · S01", "Log in with a registered account", "The account page opens and a logout link is visible."),
    "test_t002_s02_unknown_account": ("Login", "T002 · S02", "Reject an unknown account", "An invalid-credentials warning appears."),
    "test_t002_s03_empty_credentials": ("Login", "T002 · S03", "Reject empty credentials", "An invalid-credentials warning appears, with no active lockout."),
    "test_t003_existing_product[T003-S01-iPhone]": ("Search", "T003 · S01", "Search for iPhone", "At least one product title contains iPhone."),
    "test_t003_existing_product[T003-S02-MacBook]": ("Search", "T003 · S02", "Search for MacBook", "At least one product title contains MacBook."),
    "test_t003_s03_no_results": ("Search", "T003 · S03", "Search for a nonexistent product", "A no-results message appears and there are no result cards."),
}
STATUSES = ("Passed", "Failed", "Error", "Skipped", "Not run")


def clean(value):
    value = str(value)
    for key in ("TEST_PASSWORD", "TEST_EMAIL"):
        secret = os.getenv(key)
        if secret:
            value = value.replace(secret, "[redacted]")
    return value


def pytest_addoption(parser):
    parser.addoption("--dashboard", default="reports/overview.html", help="Readable report output path")


def pytest_configure(config):
    _collection_issues.clear()
    config._dashboard = {"rows": {}, "started": time.monotonic(), "issues": []}


def pytest_collection_finish(session):
    for item in session.items:
        name = item.nodeid.split("::")[-1]
        group, case, title, expected = SCENARIOS.get(name, (
            "Other", "Unmapped", name.replace("_", " "), "Not documented. Add this scenario to reporting/dashboard.py."))
        session.config._dashboard["rows"][item.nodeid] = dict(
            nodeid=item.nodeid, group=group, case=case, title=title, expected=expected,
            status="Not run", duration=0, evidence="", notes=[], alert="")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    row = item.config._dashboard["rows"].get(item.nodeid)
    if row is None:
        return
    row["duration"] += report.duration
    if report.failed:
        # Setup/teardown problems take priority over call outcomes.
        status = "Failed" if report.when == "call" else "Error"
        if row["status"] != "Error":
            row["status"] = status
        if call.excinfo:
            row["notes"].append(clean(f"{report.when}: {call.excinfo.typename}: {call.excinfo.value}"))
    elif report.skipped and row["status"] not in ("Failed", "Error"):
        row["status"] = "Skipped"
        reason = report.longrepr[-1] if isinstance(report.longrepr, tuple) else str(report.longrepr)
        row["notes"].append(clean(reason))
    elif report.when == "call" and report.passed:
        row["status"] = "Passed"
    browser = getattr(item, "_browser", None)
    if report.failed and report.when != "teardown" and browser:
        try:
            row["alert"] = clean(" | ".join(e.text for e in browser.find_elements(
                "css selector", ".alert-danger") if e.is_displayed()))
        except Exception:
            pass
    # Existing screenshot hook attaches its capture to the item; read at session end.
    row["item"] = item


def pytest_collectreport(report):
    if report.failed:
        # Collection errors also appear in pytest's terminal output.
        _collection_issues.append(clean(str(report.longrepr)))


_collection_issues = []


def explanation(row):
    if row["status"] == "Passed":
        return "All assertions completed successfully.", "Keep this run as evidence."
    if row["status"] == "Skipped":
        return "This scenario was intentionally not executed.", "Read the skip reason, satisfy its prerequisites, then rerun."
    if row["status"] == "Not run":
        return "No final result was recorded for this selected scenario.", "Check whether the run was interrupted or stopped early."
    if "exceeded allowed number of login attempts" in row.get("alert", "").lower():
        return "A login lockout warning was observed. Review as a blocked scenario.", "Wait for the stated lockout period, then rerun with the required preconditions. Pytest's failure is retained."
    if row["status"] == "Error":
        return "Test setup or cleanup failed.", "Check browser setup, fixtures and environment before judging the website."
    if any("TimeoutException" in note for note in row["notes"]):
        return "The expected page condition was not detected before the wait expired.", "Review the screenshot and page message. Check selectors, preconditions and the expected result."
    return "The automated check did not complete successfully.", "Compare the evidence with the expected behaviour before recording a website defect."


def render(rows, metadata, issues=()):
    e = lambda value: escape(clean(value), quote=True)
    counts = Counter(row["status"] for row in rows)
    cards = "".join(f'<div class="metric"><span>{s}</span><strong class="{s.lower().replace(" ", "-")}">{counts[s]}</strong></div>' for s in STATUSES)
    body = []
    for row in rows:
        meaning, action = explanation(row)
        status = row["status"]
        image = row.get("evidence", "")
        try:
            base64.b64decode(image, validate=True)
        except Exception:
            image = ""
        screenshot = (f'<details><summary>View screenshot</summary><img alt="Browser evidence for {e(row["title"])}" src="data:image/png;base64,{image}"></details>' if image else '<p class="muted">No screenshot captured. Use --screenshots=all to capture executed scenarios.</p>')
        notes = "\n".join(row["notes"]) or "No diagnostic message recorded."
        body.append(f'''<article data-status="{e(status)}" data-group="{e(row['group'])}">
<div class="rowhead"><div><p class="eyebrow">{e(row['group'])} / {e(row['case'])}</p><h2>{e(row['title'])}</h2></div><span class="badge {status.lower().replace(' ', '-')}">{e(status)}</span></div>
<div class="columns"><section><h3>Expected result</h3><p>{e(row['expected'])}</p></section><section><h3>Recorded outcome</h3><p>{e(meaning)}</p>{'<p class="alert">'+e(row['alert'])+'</p>' if row.get('alert') else ''}</section><section><h3>Next step</h3><p>{e(action)}</p></section></div>
<footer>{row['duration']:.2f}s · {e(row['nodeid'])}</footer>
<details><summary>Evidence and technical details</summary>{screenshot}<h3>Diagnostic message</h3><pre>{e(notes)}</pre></details></article>''')
    issue_html = ''.join(f'<details open class="notice"><summary>Run / collection issue</summary><pre>{e(issue)}</pre></details>' for issue in issues)
    groups = sorted({row['group'] for row in rows})
    options = ''.join(f'<option>{e(s)}</option>' for s in STATUSES)
    group_options = ''.join(f'<option>{e(g)}</option>' for g in groups)
    kpis = panels(rows)
    return '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>System test results</title><style>
:root{font-family:system-ui,-apple-system,sans-serif;color:#182637;background:#f2f5f8;line-height:1.55}*{box-sizing:border-box}body{margin:0}main{max-width:1180px;margin:auto;padding:40px 24px}header{margin-bottom:28px}.eyebrow{text-transform:uppercase;letter-spacing:.1em;font-size:11px;font-weight:750;color:#52657d;margin:0 0 7px}h1{font-size:38px;letter-spacing:-1.3px;margin:0}h2{font-size:20px;margin:0}h3{font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:#52657d;margin:0 0 8px}p{margin:6px 0 14px}.muted,footer{color:#607087;font-size:13px}.metrics{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin:24px 0}.metric,article{background:white;border:1px solid #dce3eb;border-radius:14px}.metric{padding:18px 22px}.metric span{display:block;font-size:13px;color:#52657d}.metric strong{font-size:32px}.passed{color:#126541}.failed{color:#b22c38}.error{color:#91450a}.skipped{color:#67569c}.not-run{color:#5b6470}.notice{background:#eaf0fa;border-left:4px solid #345dd1;padding:16px 20px;border-radius:6px;margin-bottom:24px;font-size:14px}.toolbar{display:flex;gap:12px;flex-wrap:wrap;align-items:end;margin-bottom:20px}label{font-size:12px;font-weight:650;display:grid;gap:5px}input,select,button{font:inherit;border:1px solid #c4ceda;border-radius:7px;padding:10px;background:white;color:#182637}input{min-width:250px}button{cursor:pointer}article{padding:24px;margin:16px 0}.rowhead{display:flex;justify-content:space-between;gap:16px;align-items:center}.badge{font-size:12px;font-weight:750;border:1px solid currentColor;border-radius:100px;padding:4px 12px;white-space:nowrap}.columns{display:grid;grid-template-columns:1fr 1fr 1fr;gap:28px;margin-top:24px;font-size:14px}footer{border-top:1px solid #e5eaf0;padding-top:12px;overflow-wrap:anywhere}details{margin-top:12px}summary{cursor:pointer;font-size:13px;font-weight:650;padding:5px 0}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f4f6f9;padding:14px;border-radius:8px;font-size:12px}img{max-width:100%;border:1px solid #dce3eb;border-radius:8px;margin-top:12px}.alert{color:#91450a}#empty{padding:30px;text-align:center} [hidden]{display:none!important}@media(max-width:700px){.metrics{grid-template-columns:repeat(2,1fr)}.columns{grid-template-columns:1fr;gap:12px}h1{font-size:30px}main{padding:24px 14px}}@media print{.toolbar{display:none}main{padding:0}article{break-inside:avoid}.metrics{grid-template-columns:repeat(5,1fr)}}
''' + CSS + '''</style></head><body><main><header><p class="eyebrow">32571 / System testing</p><h1>Software Testing KPI Dashboard</h1><p class="muted">''' + e(metadata) + f'''</p></header><div class="metrics">{cards}</div>{kpis}<div class="notice"><strong>{len(rows)} selected scenarios.</strong> Summary charts and totals describe the full selected run; filters below apply only to scenario details. Failed means an automated check failed; it does not establish a website defect. Errors are setup/cleanup problems. Skipped and not-run scenarios are not passes. A suspected lockout needs review; this report does not change pytest outcomes.</div>{issue_html}
<div class="toolbar"><label>Find a scenario<input id="query" placeholder="Search name, ID or function"></label><label>Status<select id="status"><option>All statuses</option>{options}</select></label><label>Function<select id="group"><option>All functions</option>{group_options}</select></label><button id="reset" type="button">Reset filters</button><button type="button" onclick="window.print()">Print / save PDF</button></div><p id="visible" class="muted" aria-live="polite"></p>{''.join(body)}<p id="empty" hidden>No scenarios match your filters.</p><p class="muted">Evidence is captured from the test run. Screenshots can contain account details; review before sharing. This dashboard complements your written assignment report.</p></main>''' + '''<script>
const query=document.querySelector('#query'),status=document.querySelector('#status'),group=document.querySelector('#group');
function filter(){let count=0;document.querySelectorAll('article').forEach(card=>{const show=card.textContent.toLowerCase().includes(query.value.toLowerCase())&&(status.value==='All statuses'||card.dataset.status===status.value)&&(group.value==='All functions'||card.dataset.group===group.value);card.hidden=!show;if(show)count++;});document.querySelector('#visible').textContent=count+' scenarios shown';document.querySelector('#empty').hidden=count!==0;}
[query,status,group].forEach(el=>el.addEventListener('input',filter));document.querySelector('#reset').onclick=()=>{query.value='';status.selectedIndex=0;group.selectedIndex=0;filter();};filter();
</script></body></html>'''


def pytest_sessionfinish(session, exitstatus):
    if session.config.option.collectonly:
        return
    data = session.config._dashboard
    rows = list(data["rows"].values())
    for row in rows:
        item = row.pop("item", None)
        if item:
            row["evidence"] = getattr(item, "_dashboard_screenshot", "")
    metadata = (f"{datetime.now(timezone.utc).strftime('%d %b %Y, %H:%M UTC')} · "
                f"{platform.system()} · Python {platform.python_version()} · "
                f"{time.monotonic()-data['started']:.1f}s · pytest exit code {exitstatus}")
    path = Path(session.config.getoption("--dashboard"))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render(rows, metadata, _collection_issues), encoding="utf-8")
    _collection_issues.clear()


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    if not config.option.collectonly:
        terminalreporter.write_sep("-", f"Readable dashboard: {config.getoption('--dashboard')}")
