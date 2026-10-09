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

The report plugin was exercised with synthetic pass, failure, skip, setup-error and teardown-error scenarios. Totals and cleanup-error precedence were verified. Four offline unit checks passed for rendering totals, HTML escaping, credential redaction, lockout guidance and an empty run. These are reporter checks, not passes against the public website. Run `python -m unittest discover -s qa` to repeat the offline checks.

KPI layout update: existing four reporter tests pass. Additional checks verified distribution percentages, exclusion of skipped cases from timing averages/pass share, and zero-data handling. Browser preview could not run because the browser binary was unavailable; no visual-browser verification is claimed.
