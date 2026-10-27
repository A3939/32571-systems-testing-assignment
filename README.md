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

Run your nine Member 1 scenarios from the repository root:

```bash
python -m pytest tests/test_registration.py tests/test_login.py tests/test_password_reset.py --allow-account-creation --headless --screenshots=all
open reports/latest.html
```

Each run automatically gets a new folder under `reports/runs/`. Its report, screenshots and lifecycle checkpoints stay together. `reports/latest.html` opens the newest default run; earlier run folders are preserved. Collection-only commands create no reports.

Other useful commands:

```bash
python -m pytest --collect-only -q
python -m pytest tests/test_login.py --allow-account-creation --screenshots=all
python -m pytest tests/test_password_reset.py --allow-account-creation --headless --screenshots=all
python -m pytest -m search
```

Account creation is skipped unless explicitly enabled because it creates a new persistent demo account every run. Tests use synthetic data. The authentication lifecycle and positive password-reset case each prepare a unique synthetic account and log out during setup. Enable them with `--allow-account-creation`; they need no `.env` credentials and never depend on a registration test running first. Each test has a fresh browser.

`--base-url` overrides `BASE_URL` from `.env` for a compatible deployment. Default: https://opencart.abstracta.us . Browser sessions are fresh for each test and closed afterwards. Explicit waits handle page updates; no fixed sleeps.

## Structure

- `conftest.py`: browser fixtures, options, isolated account setup and screenshot hook.
- `pages/`: reusable selectors and page actions.
- `tests/`: browser scenarios; offline reporter checks are in `qa/`.
- `docs/test-plan.md`: scenario allocation, dependencies and reporting guidance.
- `docs/t001-registration.md`: registration case table, real results and linked evidence.
- `docs/t002-authentication.md`: login/logout lifecycle and rejection cases.
- `docs/t009-password-reset.md`: password reset request UI cases.
- `docs/aditya-test-cases.md`: your three cases and a combined run command.
- `evidence/`: reviewed, archived OpenCart runs; choose a new folder for each rerun.
- `reports/latest.html`: opens the newest generated report.
- `reports/runs/`: one folder per run with its report and screenshots (gitignored).

## Team workflow

Each member should implement three function-based cases, each with three scenarios, using unique IDs. Use the ownership recorded in the GitHub issues. Create a branch such as `feature/aditya-registration`, add page methods and tests, document scenarios and results, run tests and open a pull request. Keep assertions in tests and shared browser interactions in page objects.

Use `--screenshots=all` for successful as well as failed scenario evidence. Screenshots are embedded in the HTML report and saved inside that run’s `screenshots/` folder; lifecycle checkpoints go in `steps/`. Default runs are automatically separated into dated folders. Screenshots may show account data; review before sharing. HTML reports may contain assertion details. Neither reports nor `.env` are committed automatically.

## Troubleshooting and evidence

- No tests found: check you are in this repository and run `python -m pytest --collect-only -q`.
- Import error: use the activated environment and install `requirements.txt`.
- Driver startup error: check installed browser, network access, and any stale driver on PATH.
- Timeout: inspect the screenshot and live page, then verify selectors in `pages/`; do not replace a meaningful assertion with a generic element-exists check.
- Demo data can change. Search examples assume iPhone/MacBook remain in the catalogue.
- Skipped cases are not passes. Complete account configuration and rerun before collecting final results.

Dependency ranges allow compatible updates; record `python -m pip freeze` with your final evidence for reproducibility. This project does not automatically run public-site browser tests on every commit.

Reference: https://www.selenium.dev/documentation/selenium_manager/

Run offline reporter checks with `python -m unittest discover -s qa`.

## Readable results dashboard

Every default run saves its report and screenshots together in a new dated directory under `reports/runs/`. Open `reports/latest.html` to view the newest default run. Earlier runs are preserved, and collection-only commands create no output. Reviewed assignment archives in `evidence/` are separate.

The self-contained `overview.html` report contains actual outcomes, scenario descriptions, filters and embedded screenshots. Files in `screenshots/` and `steps/` belong to the same run. Skipped scenarios are not passes, and test failures do not establish website defects.

Use `--evidence-dir=reports/runs/my-run` to choose a custom output folder; choose a fresh name each time. `--dashboard=path/overview.html` overrides the report file, with screenshots beside it unless explicitly configured otherwise. Custom paths do not update the latest-run shortcut. Optional pytest-html and JUnit outputs should be given paths in the same run directory.

Configured email/password values are redacted from dashboard text. Images and the optional pytest-html report are not automatically redacted.
