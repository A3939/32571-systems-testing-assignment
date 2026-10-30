# 32571 Systems Testing — OpenCart

Python 3.11+, Selenium 4 and pytest tests for **https://opencart.abstracta.us/**.

Aditya Girishkumar Patel (25723634 / GitHub `A3939`) owns these three cases, each with three scenarios:

| Case | Function | Issue | Results and assignment evidence |
| --- | --- | --- | --- |
| T001 / F01 | Registration | [#11](https://github.com/A3939/32571-systems-testing-assignment/issues/11) | [Registration report](docs/t001-registration.md) |
| T002 / F02 | Authentication, including login and logout | [#12](https://github.com/A3939/32571-systems-testing-assignment/issues/12) | [Authentication report](docs/t002-authentication.md) |
| T009 / F09 | Password reset request | [#19](https://github.com/A3939/32571-systems-testing-assignment/issues/19) | [Password reset report](docs/t009-password-reset.md) |

Search belongs to Member 2 and is excluded from the Aditya runner. Its OpenCart migration is tracked in PR #24.

## Member 4 cases (Tanut, GitHub `zethio44`)

| Case | Function | Issue | Details |
| --- | --- | --- | --- |
| T007 / F07 | Wish list | [#17](https://github.com/A3939/32571-systems-testing-assignment/issues/17) | [Member 4 test cases](docs/member4-test-cases.md) |
| T011 / F11 | Edit account information | [#22](https://github.com/A3939/32571-systems-testing-assignment/issues/22) | [Member 4 test cases](docs/member4-test-cases.md) |
| T012 / F12 | Address book | [#23](https://github.com/A3939/32571-systems-testing-assignment/issues/23) | [Member 4 test cases](docs/member4-test-cases.md) |

Run them with `python member4_run.py --browser edge` (archives evidence per case) or `python run_tests.py --case member4`. `--browser` also accepts `edge`.

## First-time setup

Install Python 3.11+ and Chrome or Firefox. From the repository folder on macOS/Linux:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
cp .env.example .env
```

Windows PowerShell:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Copy `.env.example` only when creating your local `.env`; keep any existing settings. The base URL is:

```dotenv
BASE_URL=https://opencart.abstracta.us
```

Selenium Manager resolves browser drivers automatically. Its initial driver download needs network access. The runner uses the repository's `.venv` automatically, so activating it is optional.

## Run tests and open the report with one command

From the repository root on macOS/Linux:

```bash
python3 run_tests.py
```

On Windows:

```powershell
py -3 run_tests.py
```

The script:

1. Runs Aditya's nine scenarios in headless Chrome.
2. Enables creation of dedicated synthetic accounts for the positive scenarios.
3. Captures scenario screenshots and login/logout checkpoints.
4. Saves the report and images in a new dated folder under `reports/runs/`.
5. Opens that run's report in your default browser when testing finishes, including when scenarios fail.

Earlier runs are preserved. The script returns pytest's exit code, so failed tests still produce a failing command status. Collection-only runs do not generate or open a report. If automatic browser opening is unavailable, the script prints the report's location.

### Run options

| Command | Purpose |
| --- | --- |
| `python3 run_tests.py --case registration` | Run the three registration scenarios and open their report |
| `python3 run_tests.py --case authentication` | Run the three login/logout scenarios and open their report |
| `python3 run_tests.py --case password-reset` | Run the three reset-request scenarios and open their report |
| `python3 run_tests.py --headed` | Watch the browser while all nine scenarios run |
| `python3 run_tests.py --browser firefox` | Use Firefox |
| `python3 run_tests.py --no-open` | Run and save results without opening a browser tab |
| `python3 run_tests.py --collect-only -q` | List the nine scenarios without executing them |
| `python3 run_tests.py --help` | Show script options |

Extra pytest options are forwarded. For example, `python3 run_tests.py --case registration -k t001_s02` selects only the password-mismatch scenario. Replace `python3` with `py -3` in these examples on Windows.

The runner enables account creation automatically. Each full run creates three disposable synthetic accounts: one for registration, one for authentication setup and one for password-reset setup. Tests do not need personal login credentials or depend on another test running first. Password-reset testing makes one request to its dedicated account; email delivery and completing the password change are outside scope.

## Folder structure

```text
.
├── run_tests.py                  # Run Aditya's cases and open their report
├── README.md
├── requirements.txt             # Python dependencies
├── pytest.ini                   # Test discovery and markers
├── conftest.py                  # Browser/account fixtures and screenshots
├── .env.example                 # Shareable configuration example
├── .env                         # Local configuration; excluded from Git
├── pages/                       # Reusable Selenium page interactions
│   ├── base_page.py
│   ├── account_page.py
│   ├── password_reset_page.py
│   └── search_page.py
├── tests/                       # Assignment browser tests
│   ├── test_registration.py     # T001: three scenarios
│   ├── test_login.py            # T002: three scenarios, including logout
│   ├── test_password_reset.py   # T009: three request-UI scenarios
│   └── test_search.py           # Member 2's scenarios
├── reporting/                   # Code and assets that generate reports
│   ├── dashboard.py             # Collect pytest outcomes and timings
│   ├── html_report.py           # Render report pages
│   ├── kpi.py                   # Summary counts and charts
│   ├── output.py                # Organize run folders and latest link
│   └── assets/                 # Report CSS and JavaScript
├── docs/                        # Written assignment cases and test plan
│   ├── aditya-test-cases.md
│   ├── test-plan.md
│   ├── t001-registration.md
│   ├── t002-authentication.md
│   └── t009-password-reset.md
├── reports/                     # Generated local results; excluded from Git
│   ├── latest.html              # Shortcut to the newest default run
│   └── runs/
│       └── <date-time>/         # A separate folder for each run
│           ├── overview.html   # Open this run directly
│           ├── overview-pages/ # Required companion pages and shared assets
│           ├── overview-report.zip
│           ├── screenshots/    # Scenario images and observation JSON
│           └── steps/          # Login/logout checkpoint images
└── evidence/                    # Reviewed assignment archives committed to Git
    ├── t001/
    ├── t002/
    └── t009/
```

Python package folders also contain `__init__.py` files. `.venv/` holds the local Python environment and is excluded from Git.

### What each folder is for

- **`pages/`** contains clicks, field entry, navigation and waits shared by tests.
- **`tests/`** contains the assignment scenarios and assertions about expected behaviour.
- **`reporting/`** contains the source code that generates the dashboard; it is needed to run the current suite.
- **`reports/runs/`** stores new local test results. A run adds a new directory and preserves previous runs.
- **`evidence/`** stores the reviewed submission snapshots, including original results, source screenshots and environment details. Normal runs do not update these archives or the written case tables.
- **`docs/`** explains the case inputs, preconditions, expected outcomes, recorded results and evidence links.

The optional reporter-development tests have been removed; `tests/` contains the website tests only.

## Viewing and sharing reports

The script opens the report automatically. To reopen the newest default run on macOS:

```bash
open reports/latest.html
```

On Linux or Windows, open `reports/latest.html` in your browser. To view an older run, open its `reports/runs/<date-time>/overview.html`.

The report includes Overview, Scenarios, Evidence and Run details pages with filters, search, screenshots and printing. Keep `overview.html` beside its `overview-pages/` directory. To share the generated HTML report, send `overview-report.zip` and extract it before opening. Scenario images are embedded in the report's Evidence page; raw images and observations also stay in the run folder.

Default runs update the `latest.html` shortcut. Explicit `--evidence-dir` or `--dashboard` paths are supported through the runner, but custom paths are reused as requested and do not update that shortcut. The script still opens the actual custom report. Use a fresh directory when choosing a custom path.

The extra pytest-html and JUnit formats are optional. To keep all output together for a custom run:

```bash
python3 run_tests.py --evidence-dir=reports/runs/custom-run --html=reports/runs/custom-run/details.html --self-contained-html --junitxml=reports/runs/custom-run/results.xml
```

## Direct pytest use

After activating `.venv`, pytest can still be used directly:

```bash
python -m pytest --collect-only -q
python -m pytest tests/test_registration.py --allow-account-creation --headless --screenshots=all
```

Direct pytest runs also generate a dated report, but do not open it automatically. Without `--allow-account-creation`, the three positive account scenarios are skipped. Skips are not passes.

## Troubleshooting

- **Missing dependencies:** install `requirements.txt` into `.venv` using the setup commands above.
- **Browser startup failure:** check that Chrome/Firefox is installed and Selenium Manager can download its driver.
- **Failed scenario:** open its screenshot and diagnostics; check selectors, prerequisites and the live page before claiming a website defect.
- **No automatic report tab:** open the report path printed by the script, or `reports/latest.html` for a default run.
- **Incorrect target:** check `BASE_URL` in `.env`, or pass `--base-url=https://opencart.abstracta.us` to the runner.

Browser sessions are isolated and closed after each test. Configured email/password values are redacted from readable-report text; screenshots and optional pytest-html output should be reviewed before sharing. Group prerequisite sign-off, final report consolidation and assignment submission remain separate from executing the tests.
