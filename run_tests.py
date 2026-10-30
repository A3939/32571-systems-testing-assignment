#!/usr/bin/env python3
"""Run the OpenCart scenarios for T001/T002/T009 (Aditya) and T005/T006/T010 (Wanchai) and open the report."""
import argparse
import os
from pathlib import Path
import sys
import webbrowser


ROOT = Path(__file__).resolve().parent
CASES = {
    "registration": "tests/test_registration.py",
    "authentication": "tests/test_login.py",
    "password-reset": "tests/test_password_reset.py",
    "add-to-cart": "tests/test_add_to_cart.py",
    "cart-update": "tests/test_cart_update.py",
    "checkout": "tests/test_checkout.py",
}


class RunReport:
    path = None

    def pytest_sessionfinish(self, session, exitstatus):
        if not session.config.option.collectonly:
            path = session.config.getoption("--dashboard")
            if path:
                self.path = Path(path).resolve()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", choices=["all", *CASES], default="all")
    parser.add_argument("--headed", action="store_true", help="Show the browser during testing")
    parser.add_argument("--browser", choices=["chrome", "firefox"], default="chrome")
    parser.add_argument("--no-open", action="store_true", help="Save the report without opening it")
    args, pytest_options = parser.parse_known_args(argv)

    try:
        import pytest
    except ImportError:
        print("Install dependencies first: python -m pip install -r requirements.txt", file=sys.stderr)
        return 4

    os.chdir(ROOT)
    paths = list(CASES.values()) if args.case == "all" else [CASES[args.case]]
    options = [*paths, "--allow-account-creation", "--screenshots=all", f"--browser={args.browser}"]
    if not args.headed:
        options.append("--headless")
    report = RunReport()
    status = int(pytest.main([*options, *pytest_options], plugins=[report]))
    if report.path and report.path.is_file() and status in (0, 1, 2):
        print(f"\nReport: {report.path}", flush=True)
        if not args.no_open:
            try:
                opened = webbrowser.open(report.path.as_uri())
            except (webbrowser.Error, OSError):
                opened = False
            if not opened:
                print("Could not open the browser automatically. Open the report path above.", file=sys.stderr)
    return status


if __name__ == "__main__":
    # Use the repository environment even when the terminal has not activated it.
    environment = ROOT / ".venv"
    python = environment / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    if python.is_file() and Path(sys.prefix).resolve() != environment.resolve():
        os.execv(str(python), [str(python), str(Path(__file__).resolve()), *sys.argv[1:]])
    raise SystemExit(main())
