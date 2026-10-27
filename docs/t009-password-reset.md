# T009 — F09 Password reset request

Tester: **Aditya Girishkumar Patel / 25723634 / Member 1 / A3939**. Issue: [#19](https://github.com/A3939/32571-systems-testing-assignment/issues/19). Uses the isolated registration fixture; see the [registration case](t001-registration.md) and [authentication case](t002-authentication.md).

Target: https://opencart.abstracta.us/index.php?route=account/forgotten . Executed 27 October 2026 (Australia/Sydney), headless Chrome. [Environment/source hashes](../evidence/t009/run.json), [dependencies](../evidence/t009/requirements-frozen.txt), [JUnit](../evidence/t009/results.xml), [dashboard](../evidence/t009/overview.html), [full report](../evidence/t009/report.html).

Preconditions: registration has been validated; forgotten-password route displays the reset-request instructions and email field. Each scenario starts in a fresh browser. The positive scenario independently prepares a unique synthetic registered account and logs out before requesting reset. It requires `--allow-account-creation` and sends exactly one request to that account. Negative cases do not create accounts. A fixture failure is an ERROR. Local form/environment prerequisites were checked; group-wide G03/G05 approval remains with the group.

| Scenario | Inputs | Steps | Independently justified expected result | Actual result | Outcome | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| T009-S01 | Dedicated registered `uts-<uuid>@example.com` email | Open reset form while logged out, submit registered email once | Confirmation of the reset request on `account/login`, with login fields visible and no authenticated sidebar | Confirmation appeared on login route; email/password fields visible; no authenticated logout link | PASS | [Screenshot](../evidence/t009/screenshots/20261027T044139480356-2d702a394c.png) |
| T009-S02 | Unique unregistered `unknown-<uuid>@example.com` | Open reset form, submit email | Documented unknown-email warning on `account/forgotten`; no success confirmation | Unknown-email warning appeared, form retained, no success alert | PASS | [Screenshot](../evidence/t009/screenshots/20261027T044143938043-0e41cefb34.png) |
| T009-S03 | Empty email | Open reset form, submit without email | Request rejected on forgotten-password form, with no success confirmation | Same unknown-email warning appeared, form retained, no success alert | PASS | [Screenshot](../evidence/t009/screenshots/20261027T044148186888-e2d5e9f9e3.png) |

Result: **3 passed, 0 failed, 0 errors, 0 skipped in 21.79 s**. These results verify the **request UI only**. Email delivery, opening a reset link and completing a password change were not tested. The on-screen message does not prove delivery. The dedicated account received one reset request; there were no retries or repeated reset requests to it.

The expected contract was selected before execution from the visible form instructions and [OpenCart's forgotten-password controller](https://github.com/opencart/opencart/blob/3.0.2.0/upload/catalog/controller/account/forgotten.php) and [language file](https://github.com/opencart/opencart/blob/3.0.2.0/upload/catalog/language/en-gb/account/forgotten.php). They describe a registered-email confirmation/redirect and an unknown-email warning. This is a reference implementation, not an assertion of the deployment's exact version. The live site matched that contract, including rejection of an empty email. This deployment exposes a specific unknown-email warning; it does not use the generic confirmation contemplated as an alternative in #19. No website defect is asserted.

Source: [tests](../tests/test_password_reset.py), [page object](../pages/password_reset_page.py), [account fixture](../conftest.py). Exact tested snapshots: [tests](../evidence/t009/source/tests__test_password_reset.py), [page object](../evidence/t009/source/pages__password_reset_page.py), [fixtures](../evidence/t009/source/conftest.py). Complete source screenshots: [tests](../evidence/t009/source/tests__test_password_reset.png), [page object](../evidence/t009/source/pages__password_reset_page.png), [fixtures](../evidence/t009/source/conftest.png). The archive records the base commit and tested SHA-256 hashes; the containing PR commit includes source and evidence together.

```bash
python -m pytest tests/test_password_reset.py --allow-account-creation --headless --screenshots=all --evidence-dir=evidence/t009 --dashboard=evidence/t009/overview.html --html=evidence/t009/report.html --self-contained-html --junitxml=evidence/t009/results.xml
```

Choose a fresh evidence directory for future runs. All result images are actual Selenium browser screenshots. Source screenshots display the escaped tested source snapshots. Four offline reporter checks pass; twelve browser scenarios collect (nine Member 1 cases and three Member 2 search examples); Python compilation and diff checks pass. Search tests were not rerun here because their OpenCart changes are in Member 2 PR #24.

AI assistance: the user requested repository cleanup, OpenCart migration, completion of Member 1 issues #11/#12/#19 and separate PRs. Codex inspected the issue and live form, checked the upstream contract, implemented tests/page object, ran the three scenarios once and drafted this report. CodeRabbit was signed out, so direct source review was used.

This PR links the completed table, code and evidence for group consolidation (#6) and individual source submission (#10). Transfer the table/screenshots to Section 6. Group sign-off and final report submission are not implied by these browser results.
