# T001 — F01 User registration

Tester: **Aditya Girishkumar Patel / 25723634 / Member 1 / A3939**. Issue: [#11](https://github.com/A3939/32571-systems-testing-assignment/issues/11).

Target: https://opencart.abstracta.us/index.php?route=account/register . Executed 27 October 2026 (Australia/Sydney), headless Chrome. [Environment and source hashes](../evidence/t001/run.json), [dependencies](../evidence/t001/requirements-frozen.txt), [JUnit](../evidence/t001/results.xml), [dashboard](../evidence/t001/overview.html), [full report](../evidence/t001/report.html).

Preconditions: new browser per scenario; registration URL and six form fields reachable; native `input[name="agree"]` checkbox verified. Local environment, collection and offline reporter checks passed. [Form screenshot](../evidence/t001/registration-form.png). Group-wide G03/G05 sign-off and report consolidation remain group responsibilities; these results only validate the prerequisites used here. No pytest ordering dependency. One disposable synthetic account is created per enabled positive run.

| Scenario | Inputs | Steps | Independently justified expected result | Actual result | Outcome | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| T001-S01 | Unique `uts-<uuid>@example.com`; Study / Tester; 0412345678; matching synthetic passwords; policy checked | Open registration, complete six fields, accept policy, submit | `account/success`, explicit account-created confirmation and visible authenticated logout link | Success route and confirmation appeared; authenticated sidebar available; heading is `Account` | PASS | [Screenshot](../evidence/t001/screenshots/20261027T043722053473-2e76396642.png) |
| T001-S02 | Fresh unique synthetic email; mismatched passwords; policy checked | Complete form, accept policy, submit | Confirmation-specific validation; remain on registration; no authenticated sidebar | Password confirmation error appeared; registration retained; no logout link | PASS | [Screenshot](../evidence/t001/screenshots/20261027T043726678696-13e4f366ad.png) |
| T001-S03 | Fresh unique synthetic email; matching passwords; policy unchecked | Complete form and submit without accepting policy | Privacy-policy warning; remain on registration; no authenticated sidebar | Privacy-policy warning appeared; registration retained; no logout link | PASS | [Screenshot](../evidence/t001/screenshots/20261027T043731599894-2e525b58fe.png) |

Final result: **3 passed, 0 failed, 0 errors, 0 skipped in 16.33 s**. No email delivery is claimed. Synthetic addresses use the reserved example.com domain; personal account credentials were not used.

Expected outcomes follow the form's password-confirmation and privacy-policy labels and the standard OpenCart registration contract: valid accepted details create an account, contradictory passwords and omitted mandatory agreement do not. The [upstream success text](https://github.com/opencart/opencart/blob/2.3.0.2/upload/catalog/language/en-gb/account/success.php) and [registration validation text](https://github.com/opencart/opencart/blob/2.3.0.2/upload/catalog/language/en-gb/account/register.php) are reference contracts, not a claim about this deployment's exact version.

The [initial migration run](../evidence/t001/initial-heading-check/results.xml) recorded **2 passed / 1 failed in 29.48 s**. It still expected the old site's exact success heading. The captured [original success screenshot](../evidence/t001/initial-heading-check/screenshots/20261027T043621924540-2e76396642.png) shows the new site uses `Account` above a clear successful-registration confirmation and authenticated sidebar. Investigation classified this as a stale automation assumption, not failed account creation. The final assertion verifies route, explicit success text and authenticated state. The original results/screenshots were preserved before the retest, which created one additional disposable account. No website defect is asserted.

Source: [tests](../tests/test_registration.py), [page object](../pages/account_page.py), [fixtures](../conftest.py). Exact tested snapshots and complete source screenshots: [tests](../evidence/t001/source/tests__test_registration.py), [tests screenshot](../evidence/t001/source/tests__test_registration.png), [page object screenshot](../evidence/t001/source/pages__account_page.png), [fixtures screenshot](../evidence/t001/source/conftest.png). `run.json` records the base commit and SHA-256 of each tested source; this PR's commit contains the implementation and evidence together.

```bash
python -m pytest tests/test_registration.py --allow-account-creation --headless --screenshots=all --evidence-dir=evidence/t001 --dashboard=evidence/t001/overview.html --html=evidence/t001/report.html --self-contained-html --junitxml=evidence/t001/results.xml
python -m unittest discover -s qa
python -m pytest --collect-only -q
```

Use a new evidence directory on any future run; the committed archive is the original recorded run. Source screenshots were captured by rendering the escaped source snapshots in Chrome, without executing the displayed source. All three scenario result images are actual Selenium browser screenshots.

AI assistance/prompt record: the user requested repository cleanup, migration to `https://opencart.abstracta.us/`, completion of Member 1 issues #11/#12/#19 and a PR for each. Codex inspected issues and live forms, adapted selectors/assertions, ran Selenium, investigated the heading mismatch and drafted this table. No reviewer prompt was executed. CodeRabbit CLI 0.7.0 was present but signed out; direct source review and local checks were used.

The case and evidence are linked through this issue-specific PR for consolidation in #6 and source submission in #10. Transfer this table and screenshots to Section 6 of the group report; group prerequisite approval is not implied.
