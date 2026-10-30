#!/usr/bin/env python3
"""Member 4 (Tanut): run T007, T011 and T012 and archive the evidence like the other members.

Usage:  python member4_run.py [--browser edge|chrome|firefox] [--case t007|t011|t012] [--headed]

For each case it writes evidence/<case>/: overview.html, report.html, results.xml, run.json,
requirements-frozen.txt, screenshots/, steps/ and source/ (exact tested source).
An existing evidence folder is moved to evidence/<case>/previous-runs/<time> first,
so earlier runs (including failures) are never overwritten.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import platform
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CASES = {
    "t007": ["tests/test_wishlist.py"],
    "t011": ["tests/test_edit_account.py"],
    "t012": ["tests/test_address_book.py"],
}
SHARED = ["pages/member4_account_pages.py", "pages/account_page.py", "pages/base_page.py", "conftest.py"]
TESTER = "Tanut / 25677093 / zethio44"
KEEP = ("previous-runs",)


def archive_previous(folder):
    if not folder.exists() or not any(p.name not in KEEP for p in folder.iterdir()):
        return
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    target = folder / "previous-runs" / stamp
    target.mkdir(parents=True)
    for item in list(folder.iterdir()):
        if item.name not in KEEP:
            shutil.move(str(item), str(target / item.name))
    print(f"Archived earlier run to {target.relative_to(ROOT)}")


def browser_versions(browser):
    try:
        from selenium import webdriver
        options = {"chrome": webdriver.ChromeOptions, "edge": webdriver.EdgeOptions,
                   "firefox": webdriver.FirefoxOptions}[browser]()
        options.add_argument("-headless" if browser == "firefox" else "--headless=new")
        driver = {"chrome": webdriver.Chrome, "edge": webdriver.Edge, "firefox": webdriver.Firefox}[browser](options=options)
        caps = driver.capabilities
        driver.quit()
        key = {"chrome": "chrome", "edge": "msedge", "firefox": "moz:geckodriverVersion"}[browser]
        drv = caps.get(key, {}).get(f"{'chromedriver' if browser == 'chrome' else 'msedgedriver'}Version") if browser != "firefox" else caps.get(key)
        return caps.get("browserName"), caps.get("browserVersion"), drv
    except Exception as exc:  # metadata only; never block the run
        return browser, f"unknown ({exc.__class__.__name__})", "unknown"


def git(*args):
    try:
        return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    except OSError:
        return "unknown"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--browser", choices=["chrome", "edge", "firefox"], default="edge")
    parser.add_argument("--case", choices=["all", *CASES], default="all")
    parser.add_argument("--headed", action="store_true")
    args = parser.parse_args()

    cases = CASES if args.case == "all" else {args.case: CASES[args.case]}
    name, version, driver = browser_versions(args.browser)
    freeze = subprocess.run([sys.executable, "-m", "pip", "freeze"], capture_output=True, text=True).stdout
    summary = {}
    for case, tests in cases.items():
        folder = ROOT / "evidence" / case
        archive_previous(folder)
        folder.mkdir(parents=True, exist_ok=True)
        rel = folder.relative_to(ROOT).as_posix()
        command = [sys.executable, "-m", "pytest", *tests, "--allow-account-creation",
                   f"--browser={args.browser}", "--screenshots=all",
                   f"--evidence-dir={rel}", f"--dashboard={rel}/overview.html",
                   f"--html={rel}/report.html", "--self-contained-html",
                   f"--junitxml={rel}/results.xml"]
        if not args.headed:
            command.append("--headless")
        print(f"\n=== {case.upper()} ===\n" + " ".join(command), flush=True)
        started = datetime.now(timezone.utc)
        status = subprocess.run(command, cwd=ROOT).returncode
        sources = [*tests, *SHARED]
        (folder / "source").mkdir(exist_ok=True)
        for src in sources:
            shutil.copy2(ROOT / src, folder / "source" / src.replace("/", "__"))
        (folder / "requirements-frozen.txt").write_text(freeze)
        (folder / "run.json").write_text(json.dumps({
            "captured_utc": started.isoformat(),
            "target": "https://opencart.abstracta.us",
            "tester": TESTER,
            "platform": platform.platform(),
            "machine": platform.machine(),
            "python": platform.python_version(),
            "source_commit": git("rev-parse", "HEAD"),
            "uncommitted_changes": bool(git("status", "--porcelain", "--", *sources)),
            "source_sha256": {s: hashlib.sha256((ROOT / s).read_bytes()).hexdigest() for s in sources},
            "browser": f"{name} {version}",
            "driver": driver,
            "headless": not args.headed,
            "command": " ".join(Path(c).name if i == 0 else c for i, c in enumerate(command)),
            "pytest_exit_code": status,
        }, indent=2) + "\n")
        summary[case] = status
    print("\nExit codes (0 = all passed, 1 = some failed):", summary)
    return max(summary.values())


if __name__ == "__main__":
    raise SystemExit(main())
