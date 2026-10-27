# 32571 Systems Testing — Python + Selenium

Team Selenium tests for OpenCart Abstracta, using Python 3.11+, Selenium 4 and pytest. Member 1 is Aditya Girishkumar Patel (25723634 / `A3939`): F01/T001 registration (#11), F02/T002 authentication including logout (#12), and F09/T009 password reset requests (#19). Search belongs to Member 2; its OpenCart migration is tracked in PR #24.

## Setup (macOS / Linux)

Install Python 3.11+ and Chrome or Firefox, then:

```bash
git clone https://github.com/A3939/32571-systems-testing-assignment.git
cd 32571-systems-testing-assignment
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

Windows PowerShell, after cloning and entering the repository:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

If activation is restricted, run `.\.venv\Scripts\python.exe -m pytest` directly. Selenium Manager resolves browser drivers automatically; initial use requires network access to browser-driver downloads. Do not install TestCafe or Node.js for this suite.

## Run

Run from the repository root:

```bash
python -m pytest --collect-only -q
python -m pytest -m search
python -m pytest --headless --html=reports/report.html --self-contained-html --junitxml=reports/results.xml
python -m pytest --browser firefox --headless
python -m pytest -m registration --allow-account-creation
python -m pytest tests/test_login.py --allow-account-creation --headless --screenshots=all
python -m pytest tests/test_password_reset.py --allow-account-creation --headless --screenshots=all
```

Run evidence into a fresh folder, for example:

```bash
python -m pytest tests/test_registration.py --allow-account-creation --headless --screenshots=all --evidence-dir=reports/t001-new --dashboard=reports/t001-new/overview.html --html=reports/t001-new/report.html --self-contained-html --junitxml=reports/t001-new/results.xml
```

Account creation is skipped unless explicitly enabled because it creates a new persistent demo account every run. Tests use synthetic data. The authentication lifecycle and positive password-reset case each prepare a unique synthetic account and log out during setup. Enable them with `--allow-account-creation`; they need no `.env` credentials and never depend on a registration test running first. Each test has a fresh browser.

`--base-url` overrides `BASE_URL` from `.env` for a compatible deployment. Default: https://opencart.abstracta.us . Browser sessions are fresh for each test and closed afterwards. Explicit waits handle page updates; no fixed sleeps.

## Structure

- `conftest.py`: browser fixtures, options, isolated account setup and screenshot hook.
- `pages/`: reusable selectors and page actions.
- `tests/`: assertions, test data and scenario IDs.
- `docs/test-plan.md`: scenario allocation, dependencies and reporting guidance.
- `docs/t001-registration.md`: registration case table, real results and linked evidence.
- `docs/t002-authentication.md`: login/logout lifecycle and rejection cases.
- `docs/t009-password-reset.md`: password reset request UI cases.
- `docs/aditya-test-cases.md`: your three cases and a combined run command.
- `evidence/`: reviewed, archived OpenCart runs; choose a new folder for each rerun.
- `reports/`: generated HTML, JUnit XML and PNG evidence (gitignored).

## Team workflow

Each member should implement three function-based cases, each with three scenarios, using unique IDs. Use the ownership recorded in the GitHub issues. Create a branch such as `feature/aditya-registration`, add page methods and tests, document scenarios and results, run tests and open a pull request. Keep assertions in tests and shared browser interactions in page objects.

Use `--screenshots=all` for successful as well as failed scenario evidence. Screenshots are embedded in the HTML report and saved under `reports/screenshots/`. Keep each final evidence run in a separate folder before rerunning. Screenshots may show account data; review before sharing. HTML reports may contain assertion details. Neither reports nor `.env` are committed automatically.

## Troubleshooting and evidence

- No tests found: check you are in this repository and run `python -m pytest --collect-only -q`.
- Import error: use the activated environment and install `requirements.txt`.
- Driver startup error: check installed browser, network access, and any stale driver on PATH.
- Timeout: inspect the screenshot and live page, then verify selectors in `pages/`; do not replace a meaningful assertion with a generic element-exists check.
- Demo data can change. Search examples assume iPhone/MacBook remain in the catalogue.
- Skipped cases are not passes. Complete account configuration and rerun before collecting final results.

Dependency ranges allow compatible updates; record `python -m pip freeze` with your final evidence for reproducibility. This project does not automatically run public-site browser tests on every commit.

Reference: https://www.selenium.dev/documentation/selenium_manager/

## Readable results dashboard

Every test run now creates `reports/overview.html` automatically. Open it on macOS:

```bash
python -m pytest --screenshots=all
open reports/overview.html
```

The dashboard has status totals, function/status filters, search, expected results, plain-language outcomes, next steps and expandable screenshots/diagnostics. It works offline and can be printed to PDF. Only selected scenarios are counted; skipped tests are never counted as passes. A lockout warning, when observed, is flagged for review without changing the pytest result. Errors mean setup/cleanup failed. Other failed checks still need investigation before being called website defects.

The existing `--html=reports/report.html --self-contained-html` output remains available for the detailed pytest report. `--dashboard=reports/my-run.html` changes the new dashboard path. Reports overwrite the previous file at the same path; archive important runs before rerunning. Add new scenario descriptions to `SCENARIOS` in `reporting/dashboard.py`. Configured test email/password values are redacted from dashboard text; images and the separate pytest report are not automatically redacted.

### KPI layout

The overview uses a compact two-column dashboard: outcome counts by function, stacked status bars, longest scenario times, pass share, and average duration by function. Durations include setup and cleanup; skipped/not-run scenarios are excluded from duration averages and attempted-scenario pass share. Charts always describe the whole selected run; filters affect scenario details only. Severity, confirmed defects and weekly trends are not inferred from test failures.
