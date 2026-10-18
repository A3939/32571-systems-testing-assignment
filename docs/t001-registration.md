# Section 6 — T001 / F01: user registration

Tester: **Aditya Girishkumar Patel** · Student ID: **25723634** · GitHub: `A3939`.

Issue: [#11](https://github.com/A3939/32571-systems-testing-assignment/issues/11). Function URL: [Register Account](https://ecommerce-playground.lambdatest.io/index.php?route=account/register).

## Preconditions and prerequisites

- G03: confirm F01 is user registration and the candidate URL exposes the registration form. The overall group catalogue/dependency-graph issue remains open; this case does not claim group sign-off.
- G05: verify the local Python/Selenium/pytest environment, Chrome startup, selectors, collection and reporting before running the scenarios. Record actual versions and smoke-check evidence.
- Begin every scenario logged out, in a new browser session. The function-scoped `driver` fixture opens and closes the browser for each test.
- Use a new UUID-based synthetic email for each scenario; no scenario reuses an account created by another test. No login fixture or pytest ordering is required.
- Enable `--allow-account-creation` for the planned run. S01 creates one persistent disposable account on the public demo. S02 and S03 keep all other inputs valid and vary one condition each.

Common input values: first name `Study`, last name `Tester`, telephone `0412345678`, password `Study!Pass123`, newsletter left at the form default (`No`). The run generated these unique synthetic addresses:

- E01 / S01: `uts-41d4ea04d94946bda64f8d0d9d7c037e@example.com`.
- E02 / S02: `uts-7f42a8d494ab4ec3948d3064185baa2e@example.com`.
- E03 / S03: `uts-942dd893992843e9b00d4e6ebb7a26b1@example.com`.

## Independently justified expected outcomes

Expected outcomes are specified before this run and are not inferred from its pass/fail results. A complete valid registration should create an account; password confirmation must equal the password; the configured policy agreement must be accepted before registration succeeds.

These rules have an independent upstream reference in OpenCart's [registration controller](https://github.com/opencart/opencart/blob/3.0.3.8/upload/catalog/controller/account/register.php): account creation follows successful validation, confirmation is compared against the password, and the configured agreement is checked. The [registration language file](https://github.com/opencart/opencart/blob/3.0.3.8/upload/catalog/language/en-gb/account/register.php) specifies the validation wording; the [success language file](https://github.com/opencart/opencart/blob/3.0.3.8/upload/catalog/language/en-gb/account/success.php) supplies the account-created heading. These are upstream references, not a claim that the deployed playground is exactly OpenCart 3.0.3.8. Live form labels, controls and policy presence are recorded in the preflight evidence.

## Section 6 test-case table

| Scenario | Inputs | Steps | Expected result | Actual result | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| T001-S01 | Common valid fields; email E01; confirmation `Study!Pass123`; policy accepted. | 1. Open registration in a fresh browser. 2. Fill all fields. 3. Accept policy. 4. Submit. | Registration succeeds and `Your Account Has Been Created!` appears as the page heading. | Account-created heading displayed at `account/success`. | Passed | [S01 screenshot][s01] |
| T001-S02 | Common valid fields; email E02; confirmation `Different!Pass123`; policy accepted. | 1. Open registration in a fresh browser. 2. Fill fields with the mismatched confirmation. 3. Accept policy. 4. Submit. | Registration is rejected; the confirmation field shows `Password confirmation does not match password!`. | Confirmation mismatch error displayed; route remained `account/register`. | Passed | [S02 screenshot][s02] |
| T001-S03 | Common valid fields; email E03; matching confirmation; policy unchecked. | 1. Open registration in a fresh browser. 2. Fill all fields. 3. Leave policy unchecked. 4. Submit. | Registration is rejected; a warning states that agreement to the Privacy Policy is required. | Privacy Policy agreement warning displayed; route remained `account/register`. | Passed | [S03 screenshot][s03] |

## Source and scenario mapping

Tested source commit: [`8bb366d36f8a4b078f0f21fddef791e84ab05ee7`](https://github.com/A3939/32571-systems-testing-assignment/commit/8bb366d36f8a4b078f0f21fddef791e84ab05ee7).

- [Registration tests](https://github.com/A3939/32571-systems-testing-assignment/blob/8bb366d36f8a4b078f0f21fddef791e84ab05ee7/tests/test_registration.py): `test_t001_s01_valid_registration`, `test_t001_s02_password_mismatch`, `test_t001_s03_policy_required`.
- [Registration page object](https://github.com/A3939/32571-systems-testing-assignment/blob/8bb366d36f8a4b078f0f21fddef791e84ab05ee7/pages/account_page.py).
- [Browser isolation and screenshot hook](https://github.com/A3939/32571-systems-testing-assignment/blob/8bb366d36f8a4b078f0f21fddef791e84ab05ee7/conftest.py) and [shared browser actions](https://github.com/A3939/32571-systems-testing-assignment/blob/8bb366d36f8a4b078f0f21fddef791e84ab05ee7/pages/base_page.py).

## Run details and evidence

Planned run: **18 October 2026, 15:02:10–15:02:29 AEDT**, Australia/Sydney. Scenario execution took **14.66 seconds: 3 passed, 0 failed, 0 errors, 0 skipped**. Setup, call and teardown all passed for each scenario. Exactly one valid account-creation scenario was executed; it was not retried.

Environment: headless Chrome `155.0.8059.84`, matching ChromeDriver `155.0.8059.84`, Python `3.12.14`, macOS `26.6.2`, ARM64. Exact dependencies are in [requirements-frozen.txt][dependencies]. Three different browser-session IDs and three different emails are recorded in [run.json][metadata], supporting scenario isolation. Instrumentation recorded inputs and browser observations without changing the test assertions.

The [live form verification][form-check] was recorded before execution, along with [form screenshot][form-shot], [policy control][policy-shot], [test collection][collection] and [four passing offline dashboard checks][dashboard-checks]. This validates the F01-specific URL/controls and local automation prerequisites. Broader G03/G05 group completion remains pending in GitHub.

Reports: [overview dashboard][overview], [pytest HTML report][html-report], and [JUnit results][xml]. Source screenshots: [complete registration tests][source-tests] and [RegistrationPage][source-page]. These are actual browser screenshots of the archived source rendered with original line numbers and commit/hash labels; they are not IDE screenshots. All three result screenshots and both full source screenshots were visually checked.

Archive: `reports/member-1/t001-20261018-150210/`. It includes exact tested sources, SHA256 hashes, commands, run metadata, scenario observations, dependency versions, prerequisite checks and the capture scripts. [Downloadable evidence ZIP][bundle] includes the case write-up. The earlier 16 October evidence is preserved unchanged. A separate [aborted preflight record][aborted] documents a source-view timeout before any scenario execution or account creation; full source captures were then completed without repeating registration.

No failures were observed in this registration run and no website defect is claimed. Successful registration is verified by the submitted form, success route and heading; email delivery and backend database state were outside this case's checks.

Reproduction command, using a new output folder each time:

```bash
python -m pytest tests/test_registration.py \
  --headless --allow-account-creation --screenshots=all \
  --dashboard=reports/member-1/t001-new-run/overview.html \
  --junitxml=reports/member-1/t001-new-run/results.xml \
  --html=reports/member-1/t001-new-run/report.html --self-contained-html
```

Do not reuse an existing evidence folder. Generated evidence is kept locally under gitignored `reports/`; the case write-up is tracked in `docs/`. Attach the evidence bundle to the issue/group submission so screenshots are available beyond this local checkout.

## Prompts used

- "Can we make code little bit more cleaner and more readable"
- "can you make it more easy folder structure"
- Supplied issues #11, #12 and #19 and asked to write or rewrite the corresponding work.
- Supplied #11's completion checklist and asked whether all its requirements could be achieved.
- Provided the tester name and student ID for the Section 6 table.

## Completion assessment

| Requirement from #11 | Evidence / status |
| --- | --- |
| Verified URL; three final scenarios, inputs, preconditions, steps and independent expected outcomes | Complete in this write-up; live form and upstream references linked above. |
| Selenium/pytest tests, page objects, isolated fixtures and T001-S01 through T001-S03 mapping | Complete at source commit `8bb366d`; no test-source changes were needed for this run. |
| Prerequisites validated before execution; no test-order dependency | F01-specific form/environment checks passed before execution. G03/G05 overall group sign-off is still pending. |
| Actual outcomes recorded honestly and failures investigated | Complete: all three scenarios passed, no skips; aborted preflight recorded separately without claiming a scenario result. |
| Scenario result screenshots and corresponding source-code screenshots | Complete: three result PNGs and two full source PNGs, visually checked and linked above. |
| Section 6 table with tester details and actual results | Complete in this document for Aditya Girishkumar Patel / 25723634; transfer it into the final group report. |
| Source-code links, commit/run details, prompts and archived evidence | Complete locally; source links verified on GitHub, old evidence preserved, new evidence bundled. |

Remaining submission actions: obtain group prerequisite sign-off, incorporate this table and images into the final report, and attach/link the evidence to #11 for consolidation. This write-up does not mark GitHub checkboxes or close any issue.

[s01]: ../reports/member-1/t001-20261018-150210/screenshots/T001-S01.png
[s02]: ../reports/member-1/t001-20261018-150210/screenshots/T001-S02.png
[s03]: ../reports/member-1/t001-20261018-150210/screenshots/T001-S03.png
[metadata]: ../reports/member-1/t001-20261018-150210/run.json
[dependencies]: ../reports/member-1/t001-20261018-150210/requirements-frozen.txt
[form-check]: ../reports/member-1/t001-20261018-150210/prerequisites/form.json
[form-shot]: ../reports/member-1/t001-20261018-150210/prerequisites/registration-form.png
[policy-shot]: ../reports/member-1/t001-20261018-150210/prerequisites/policy-control.png
[collection]: ../reports/member-1/t001-20261018-150210/prerequisites/collection.txt
[dashboard-checks]: ../reports/member-1/t001-20261018-150210/prerequisites/dashboard-checks.txt
[overview]: ../reports/member-1/t001-20261018-150210/overview.html
[html-report]: ../reports/member-1/t001-20261018-150210/report.html
[xml]: ../reports/member-1/t001-20261018-150210/results.xml
[source-tests]: ../reports/member-1/t001-20261018-150210/source-code-screenshots/registration-tests-full.png
[source-page]: ../reports/member-1/t001-20261018-150210/source-code-screenshots/registration-page-full.png
[bundle]: ../reports/member-1/t001-20261018-150210-evidence.zip
[aborted]: ../reports/member-1/t001-20261018-150059/aborted.json
