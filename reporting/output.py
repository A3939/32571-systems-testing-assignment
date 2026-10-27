"""Keep generated reports and screenshots together for each test run."""
from datetime import datetime
from html import escape
from pathlib import Path
from urllib.parse import quote


def configure_report_paths(config):
    if config.option.collectonly:
        return
    dashboard = config.getoption("--dashboard")
    evidence = config.getoption("--evidence-dir")
    config._automatic_report_run = not dashboard and not evidence
    if config._automatic_report_run:
        directory = Path("reports/runs") / datetime.now().astimezone().strftime("%Y%m%d-%H%M%S-%f")
    else:
        directory = Path(evidence) if evidence else Path(dashboard).parent
    config.option.evidence_dir = evidence or str(directory)
    config.option.dashboard = dashboard or str(directory / "overview.html")


def write_latest_report(config, report):
    if not getattr(config, "_automatic_report_run", False):
        return
    latest = Path("reports/latest.html")
    target = escape(quote(Path(report).relative_to(latest.parent).as_posix()), quote=True)
    latest.write_text(
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<title>Latest test run</title>'
        f'<meta http-equiv="refresh" content="0;url={target}"></head>'
        f'<body><p><a href="{target}">Open the latest test report</a></p></body></html>',
        encoding="utf-8",
    )
