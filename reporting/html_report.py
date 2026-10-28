"""Offline HTML pages for the readable pytest report."""
import base64
from collections import Counter
import hashlib
from html import escape
import os
from pathlib import Path
from urllib.parse import quote, urlencode
from zipfile import ZIP_DEFLATED, ZipFile

from reporting.kpi import panels

STATUSES = ("Passed", "Failed", "Error", "Skipped", "Not run")
PAGES = {
    "overview": ("Overview", "A clear view of this test run."),
    "scenarios": ("Scenarios", "Review expected results and recorded outcomes."),
    "evidence": ("Evidence", "Inspect screenshots and diagnostic messages."),
    "run-details": ("Run details", "Check the environment, run settings and collection issues."),
}
ASSETS = Path(__file__).with_name("assets")


def clean(value):
    value = str(value)
    for key in ("TEST_PASSWORD", "TEST_EMAIL"):
        secret = os.getenv(key)
        if secret:
            value = value.replace(secret, "[redacted]")
    return value


def e(value):
    return escape(clean(value), quote=True)


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


def scenario_id(row):
    return "scenario-" + hashlib.sha256(row["nodeid"].encode()).hexdigest()[:16]


def status_class(status):
    return status.lower().replace(" ", "-") if status in STATUSES else "not-run"


def badge(status):
    return f'<span class="badge {status_class(status)}"><span aria-hidden="true">●</span> {e(status)}</span>'


def screenshot(row):
    image = row.get("evidence", "")
    if not isinstance(image, str):
        return ""
    try:
        decoded = base64.b64decode(image, validate=True)
    except ValueError:
        return ""
    if not decoded.startswith(b"\x89PNG\r\n\x1a\n"):
        return ""
    return f"data:image/png;base64,{image}"


def toolbar(rows):
    statuses = "".join(f'<option>{e(status)}</option>' for status in STATUSES)
    groups = "".join(f'<option>{e(group)}</option>' for group in sorted({row["group"] for row in rows}))
    return f'''<form class="toolbar" id="filters" role="search">
<label class="search">Search scenarios<input id="query" type="search" placeholder="Search by name, case ID or function"></label>
<label>Status<select id="status"><option value="">All statuses</option>{statuses}</select></label>
<label>Function<select id="group"><option value="">All functions</option>{groups}</select></label>
<button type="reset" class="button quiet">Reset</button></form>
<p class="filter-summary" id="visible" aria-live="polite">{len(rows)} scenarios</p>'''


def overview(rows, links, issues):
    counts = Counter(row["status"] for row in rows)
    cards = "".join(
        f'<a class="metric" href="{e(links["scenarios"] + "?" + urlencode({"status": status}))}">'
        f'<span>{status}</span><strong class="{status_class(status)}">{counts[status]}</strong>'
        '<small>View scenarios <span aria-hidden="true">↗</span></small></a>'
        for status in STATUSES
    )
    review = counts["Failed"] + counts["Error"]
    if not rows:
        notice = '<strong>No scenarios selected.</strong> This report does not claim a successful test run.'
    elif review:
        notice = f'<strong>{review} checks need investigation.</strong> Open the scenarios to compare outcomes and evidence.'
    elif counts["Passed"] == len(rows):
        notice = f'<strong>All {len(rows)} selected scenarios passed.</strong> Open Evidence to review the captured screenshots.'
    else:
        unfinished = counts["Skipped"] + counts["Not run"]
        notice = f'<strong>{unfinished} scenarios were skipped or not run.</strong> No pass is claimed for these scenarios.'
    issue_link = (
        f'<a href="{e(links["run-details"])}#run-issues">{len(issues)} run / collection issues</a>' if issues else ""
    )
    chart_rows = [{**row, **{key: clean(row[key]) for key in ("group", "title", "case")}} for row in rows]
    return f'''<div class="section-heading"><h2>Run summary</h2><span class="muted">{len(rows)} selected scenarios</span></div>
<div class="metrics">{cards}</div><div class="notice">{notice} {issue_link}</div>
{panels(chart_rows)}<p class="caption">Charts describe the whole selected run. Filters on the Scenarios and Evidence pages apply to individual checks.</p>'''


def scenarios(rows, links):
    cards = []
    for row in rows:
        meaning, action = explanation(row)
        anchor = scenario_id(row)
        alert = f'<p class="alert">{e(row["alert"])}</p>' if row.get("alert") else ""
        cards.append(f'''<article class="scenario-card" data-scenario data-status="{e(row['status'])}" data-group="{e(row['group'])}" id="{anchor}">
<div class="rowhead"><div><p class="eyebrow">{e(row['group'])} / {e(row['case'])}</p><h2>{e(row['title'])}</h2></div>{badge(row['status'])}</div>
<div class="columns"><section><h3>Expected result</h3><p>{e(row['expected'])}</p></section>
<section><h3>Recorded outcome</h3><p>{e(meaning)}</p>{alert}</section><section><h3>Next step</h3><p>{e(action)}</p></section></div>
<footer><span>{row['duration']:.2f}s · <code>{e(row['nodeid'])}</code></span><a href="{e(links['evidence'])}#{anchor}">View evidence <span aria-hidden="true">→</span></a></footer></article>''')
    empty = '<div class="empty-state"><h2>No scenarios selected</h2><p>Run the intended tests to populate this report.</p></div>' if not rows else ""
    return toolbar(rows) + "".join(cards) + empty + '<div id="empty" class="empty-state" hidden>No scenarios match these filters.</div>'


def evidence(rows, links):
    cards = []
    for row in rows:
        anchor = scenario_id(row)
        image = screenshot(row)
        if image:
            visual = f'''<button type="button" class="screenshot" data-zoom aria-label="Enlarge screenshot: {e(row['title'])}">
<img src="{image}" alt="Browser evidence for {e(row['title'])}" loading="lazy"><span>Enlarge screenshot ↗</span></button>
<a class="download-image" href="{image}" download="{anchor}.png">Download screenshot</a>'''
        else:
            visual = '<div class="missing-image"><span aria-hidden="true">▧</span><strong>Screenshot unavailable</strong><p>No valid PNG was captured for this scenario. Use <code>--screenshots=all</code> to capture executed checks.</p></div>'
        notes = "\n".join(row["notes"]) or "No diagnostic message recorded."
        alert = f'<p class="alert">{e(row["alert"])}</p>' if row.get("alert") else ""
        cards.append(f'''<article class="evidence-card" data-scenario data-status="{e(row['status'])}" data-group="{e(row['group'])}" id="{anchor}">
<div class="rowhead"><div><p class="eyebrow">{e(row['group'])} / {e(row['case'])}</p><h2>{e(row['title'])}</h2></div>{badge(row['status'])}</div>
{visual}<details class="diagnostics"{' open' if row['status'] in ('Failed', 'Error') else ''}><summary>Diagnostic message</summary>{alert}<pre>{e(notes)}</pre></details>
<footer><span>{row['duration']:.2f}s</span><a href="{e(links['scenarios'])}#{anchor}">View scenario →</a></footer></article>''')
    captured = sum(bool(screenshot(row)) for row in rows)
    return (f'<p class="page-note">{captured} of {len(rows)} scenarios have screenshots. Images show the browser at capture time.</p>'
            + toolbar(rows) + '<div class="evidence-grid">' + "".join(cards) + '</div>'
            + ('<div class="empty-state"><h2>No scenario evidence</h2><p>No scenarios were selected in this run.</p></div>' if not rows else "")
            + '<div id="empty" class="empty-state" hidden>No evidence matches these filters.</div>'
            + '''<dialog id="image-dialog" aria-labelledby="image-title"><div class="dialog-header"><h2 id="image-title">Scenario screenshot</h2><button type="button" class="button" id="close-image">Close</button></div><img id="full-image" alt=""></dialog>''')


def run_details(rows, metadata, details, issues):
    fields = {"Run summary": metadata, "Selected scenarios": str(len(rows)), **(details or {})}
    entries = "".join(f'<div><dt>{e(key)}</dt><dd>{e(value)}</dd></div>' for key, value in fields.items())
    issue_cards = "".join(f'<details open class="issue"><summary>Run issue {number}</summary><pre>{e(issue)}</pre></details>' for number, issue in enumerate(issues, 1))
    if not issues:
        issue_cards = '<p class="muted">No collection issues were recorded.</p>'
    return f'''<div class="details-grid"><section class="panel"><h2>Environment and execution</h2><dl class="run-details">{entries}</dl></section>
<section class="panel"><h2>Understanding the results</h2><div class="guide"><p><strong>Passed</strong> — the automated assertions succeeded.</p><p><strong>Failed</strong> — a check failed; investigate before calling it a website defect.</p><p><strong>Error</strong> — setup or cleanup failed.</p><p><strong>Skipped / not run</strong> — no pass is claimed.</p><p>Durations include setup and cleanup. Pass share excludes skipped and not-run scenarios.</p><p>Screenshots can contain account details. Review images before sharing the report.</p></div></section></div>
<section class="panel" id="run-issues"><h2>Run and collection issues</h2>{issue_cards}</section>'''


def render(rows, metadata, issues=(), *, page="overview", links=None, details=None, asset_prefix=None):
    """Render one report page; inline assets when no asset prefix is supplied."""
    if page not in PAGES:
        raise ValueError(f"Unknown report page: {page}")
    links = links or {name: f"{name}.html" for name in PAGES}
    title, subtitle = PAGES[page]
    if page == "overview":
        body = overview(rows, links, issues)
    elif page == "scenarios":
        body = scenarios(rows, links)
    elif page == "evidence":
        body = evidence(rows, links)
    else:
        body = run_details(rows, metadata, details, issues)
    navigation = "".join(
        f'<a href="{e(links[name])}"' + (' aria-current="page"' if name == page else '')
        + f'><span class="nav-number" aria-hidden="true">0{number}</span>{label}</a>'
        for number, (name, (label, _)) in enumerate(PAGES.items(), 1)
    )
    if asset_prefix is None:
        styles = f'<style>{(ASSETS / "report.css").read_text(encoding="utf-8")}</style>'
        script = f'<script>{(ASSETS / "report.js").read_text(encoding="utf-8")}</script>'
    else:
        styles = f'<link rel="stylesheet" href="{e(asset_prefix)}report.css">'
        script = f'<script src="{e(asset_prefix)}report.js" defer></script>'
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title} · System test report</title>{styles}</head>
<body><a class="skip-link" href="#main">Skip to content</a><aside class="sidebar"><a class="brand" href="{e(links['overview'])}"><span class="brand-mark" aria-hidden="true">✓</span><span>Test report<small>32571 · Systems testing</small></span></a>
<p class="nav-label">This test run</p><nav aria-label="Report pages">{navigation}</nav><div class="sidebar-note"><span class="live-dot" aria-hidden="true"></span> Saved report<p>Measured outcomes from one test run.</p></div></aside>
<main id="main"><div class="topbar"><span>Reports <span aria-hidden="true">/</span> <strong>{title}</strong></span><div class="actions"><button type="button" class="button quiet" data-print>Print page</button></div></div>
<header class="page-header"><p class="eyebrow">Test execution report</p><h1>{title}</h1><p>{subtitle}</p><p class="run-metadata">{e(metadata)}</p></header>
{body}<div class="report-footer"><span>32571 · Systems testing</span><span>Saved report · {len(rows)} selected scenarios</span></div></main>{script}</body></html>'''


def write_report(path, rows, metadata, issues=(), *, details=None):
    """Write four linked pages, shared local assets and a portable ZIP."""
    path = Path(path)
    companion = path.with_name(f"{path.stem}-pages")
    assets = companion / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    archive = path.with_name(f"{path.stem}-report.zip")
    output = []
    for filename in ("report.css", "report.js"):
        target = assets / filename
        target.write_bytes((ASSETS / filename).read_bytes())
        output.append(target)
    for page in PAGES:
        target = path if page == "overview" else companion / f"{page}.html"
        page_prefix = quote(companion.name) + "/" if page == "overview" else ""
        links = {name: f"{page_prefix}{name}.html" for name in PAGES}
        links["overview"] = ("" if page == "overview" else "../") + quote(path.name)
        asset_prefix = page_prefix + "assets/"
        target.write_text(render(rows, metadata, issues, page=page, links=links,
                                 details=details, asset_prefix=asset_prefix), encoding="utf-8")
        output.append(target)
    with ZipFile(archive, "w", compression=ZIP_DEFLATED) as bundle:
        for filename in output:
            bundle.write(filename, filename.relative_to(path.parent))
    return path
