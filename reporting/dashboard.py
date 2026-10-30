"""Collect real pytest outcomes and generate the offline report pages."""
from datetime import datetime
from pathlib import Path
import platform
import time

import pytest

from reporting.html_report import clean, explanation, render, write_report
from reporting.output import write_latest_report

SCENARIOS = {
    "test_t001_s01_valid_registration": ("Registration", "T001 · S01", "Register with valid details", "The success route shows the account-created confirmation and authenticated sidebar."),
    "test_t001_s02_password_mismatch": ("Registration", "T001 · S02", "Reject mismatched passwords", "A password-confirmation error appears."),
    "test_t001_s03_policy_required": ("Registration", "T001 · S03", "Require privacy-policy acceptance", "Registration is rejected with a privacy-policy warning."),
    "test_t002_s01_valid_login": ("Authentication", "T002 · S01", "Login and logout lifecycle", "Login grants account access; logout protects it; a fresh login succeeds."),
    "test_t002_s02_unknown_account": ("Authentication", "T002 · S02", "Reject an unknown account", "An invalid-credentials warning appears."),
    "test_t002_s03_empty_credentials": ("Authentication", "T002 · S03", "Reject empty credentials", "An invalid-credentials warning appears, with no active lockout."),
    "test_t003_existing_product[T003-S01-iPhone]": ("Search", "T003 · S01", "Search for iPhone", "At least one product title contains iPhone."),
    "test_t003_existing_product[T003-S02-MacBook]": ("Search", "T003 · S02", "Search for MacBook", "At least one product title contains MacBook."),
    "test_t003_s03_no_results": ("Search", "T003 · S03", "Search for a nonexistent product", "A no-results message appears and there are no result cards."),
    "test_t009_s01_registered_email": ("Password reset", "T009 · S01", "Request reset for a registered account", "A reset-request confirmation appears on the login route; email delivery is outside scope."),
    "test_t009_s02_unregistered_email": ("Password reset", "T009 · S02", "Reject an unregistered reset email", "The documented unknown-email warning appears, with no success confirmation."),
    "test_t009_s03_empty_email": ("Password reset", "T009 · S03", "Reject an empty reset email", "The request is rejected on the forgotten-password form, without a success confirmation."),
    "test_t007_s01_add_product_to_wishlist": ("Wish list", "T007 · S01", "Add a product to the wish list", "Success alert, header Wish List (1) and the iPhone row with model, stock and price."),
    "test_t007_s02_wishlist_persists_after_logout": ("Wish list", "T007 · S02", "Wish list persists after logout and login", "Wish list is protected after logout; after login both products are reached from My Account."),
    "test_t007_s03_remove_products_from_wishlist": ("Wish list", "T007 · S03", "Remove products from the wish list", "Each removal shows the modified alert; the list ends empty with Wish List (0)."),
    "test_t011_s01_update_name_and_telephone": ("Edit account", "T011 · S01", "Update name and telephone", "Success alert on My Account; the edit form shows the saved values."),
    "test_t011_s02_empty_first_name_rejected": ("Edit account", "T011 · S02", "Reject an empty first name", "Only the first-name message appears and saved details are unchanged."),
    "test_t011_s03_invalid_email_rejected": ("Edit account", "T011 · S03", "Reject an invalid email", "Only the email message appears and the saved email is unchanged."),
    "test_t012_s01_add_valid_address": ("Address book", "T012 · S01", "Add a valid address", "Added alert; the address book lists the saved address fields."),
    "test_t012_s02_missing_mandatory_fields": ("Address book", "T012 · S02", "Reject missing mandatory fields", "Field messages for each mandatory field; nothing is saved."),
    "test_t012_s03_edit_then_delete_address": ("Address book", "T012 · S03", "Edit then delete an address", "Updated and deleted alerts; the only remaining address cannot be deleted."),
}


def pytest_addoption(parser):
    parser.addoption("--dashboard", help="Report entry page (default: a new folder under reports/runs)")


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


def pytest_sessionfinish(session, exitstatus):
    if session.config.option.collectonly:
        return
    data = session.config._dashboard
    rows = list(data["rows"].values())
    for row in rows:
        item = row.pop("item", None)
        if item:
            row["evidence"] = getattr(item, "_dashboard_screenshot", "")
    metadata = (f"{datetime.now().astimezone().strftime('%d %b %Y, %H:%M %Z')} · "
                f"{platform.system()} · Python {platform.python_version()} · "
                f"{time.monotonic()-data['started']:.1f}s · pytest exit code {exitstatus}")
    path = Path(session.config.getoption("--dashboard"))
    details = {
        "Generated": datetime.now().astimezone().strftime("%d %b %Y, %H:%M %Z"),
        "Operating system": f"{platform.system()} {platform.release()}",
        "Architecture": platform.machine(),
        "Python": platform.python_version(),
        "Pytest": pytest.__version__,
        "Browser": session.config.getoption("--browser"),
        "Headless": "Yes" if session.config.getoption("--headless") else "No",
        "Base URL": session.config.getoption("--base-url"),
        "Duration": f"{time.monotonic() - data['started']:.1f}s",
        "Pytest exit code": str(exitstatus),
        "Selected paths": ", ".join(session.config.args),
    }
    write_report(path, rows, metadata, _collection_issues, details=details)
    write_latest_report(session.config, path)
    _collection_issues.clear()


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    if not config.option.collectonly:
        terminalreporter.write_sep("-", f"Readable dashboard: {config.getoption('--dashboard')}")
