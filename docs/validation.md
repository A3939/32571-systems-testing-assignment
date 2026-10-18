# Boilerplate validation

- Dependencies installed successfully using Python 3.12.
- Python compilation passed for page objects, tests and fixtures.
- pytest collected all nine scenarios successfully.
- Registration and login input selectors and search controls were inspected in live HTML.
- A headless search test run was attempted, but Chrome failed to create a session in the build environment (`SessionNotCreatedException`). No end-to-end pass is claimed.

Run the suite on your own machine with Chrome/Firefox, review the expected messages and catalogue assumptions, and record genuine results before submission. The two positive account scenarios require explicit account-creation enablement and configured login credentials respectively.

## Follow-up from local test output

The submitted run showed four passes, four failures and one skipped test. Live search HTML confirmed that results are under `#product-search .content-products`, not `#content`. Both product-card and empty-result assertions now use that results container, excluding unrelated recommendation cards. Login now waits for an authenticated account route or a visible error and verifies a logout link on success. This does not establish that supplied credentials are valid. The user's credentials were not used or committed. Python syntax was checked after the changes; a successful end-to-end rerun is still required locally.

## Readable dashboard checks

The report plugin was exercised with synthetic pass, failure, skip, setup-error and teardown-error scenarios. Totals and cleanup-error precedence were verified. Four offline unit checks passed for rendering totals, HTML escaping, credential redaction, lockout guidance and an empty run. These are reporter checks, not passes against the public website. Run `python -m unittest discover -s tests/reporting` to repeat the offline checks.

KPI layout update: existing four reporter tests pass. Additional checks verified distribution percentages, exclusion of skipped cases from timing averages/pass share, and zero-data handling. Browser preview could not run because the browser binary was unavailable; no visual-browser verification is claimed.

## Member 1 cases: 16 October 2026

Implemented F09/T009 logout with three independent authenticated-session scenarios and linked them to the dashboard. F01/T001 registration and F02/T002 login retain their scenario IDs and use readable page fixtures. The sidebar logout selector avoids a matching hidden menu item. The full suite now collects twelve website scenarios; Member 1's allocation selects nine. Four offline dashboard checks pass, Python compilation passes, and `git diff --check` passes.

A real headless Chrome run of registration, login and logout recorded **7 passed, 1 failed and 1 skipped** in 70.72 seconds. Both registration validation scenarios, positive/unknown-account login, and all three logout scenarios passed. Empty-credentials login failed because the website showed a login-attempt lockout warning asking to retry in 1 hour instead of the expected invalid-credentials warning. The expected behaviour was preserved; no website defect is confirmed. Successful account creation was skipped because `--allow-account-creation` was not enabled.

The [individual case tables](member-1-test-cases.md) include per-scenario outcomes and screenshots. The [archived dashboard](../reports/member-1/20261016-102552/overview.html) is accompanied by JUnit results, eight screenshots, dependency versions, environment metadata and copies of the tested source. These local evidence artifacts are gitignored. Full tester details, real source-code screenshots, prerequisite sign-off, the planned registration run and lockout follow-up remain necessary for final submission.
