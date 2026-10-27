# T002 — F02 Authentication: login and logout

Tester: **Aditya Girishkumar Patel / 25723634 / Member 1 / A3939**. Issue: [#12](https://github.com/A3939/32571-systems-testing-assignment/issues/12). Registration prerequisites are documented in [T001](t001-registration.md).

Target routes: `account/login`, `account/account`, `account/logout` under https://opencart.abstracta.us/index.php?route= . Executed 27 October 2026 (Australia/Sydney), headless Chrome. [Environment/source hashes](../evidence/t002/run.json), [dependencies](../evidence/t002/requirements-frozen.txt), [JUnit with recorded step URLs](../evidence/t002/results.xml), [dashboard](../evidence/t002/overview.html), [full report](../evidence/t002/report.html).

Preconditions: registration validated in T001; fresh browser per scenario. The positive scenario's fixture independently creates a unique `uts-<uuid>@example.com` account with a random synthetic password, verifies registration confirmation and logs out before the login test. It requires `--allow-account-creation`. No personal credentials or test-order dependency. Negative cases run without account creation. A setup failure is an ERROR, not a successful login/logout case. Local form/environment checks are validated; overall G03/G05 approval remains with the group.

| Scenario | Inputs | Steps | Expected result and rationale | Actual result | Outcome | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| T002-S01 | Dedicated fixture account, valid password | Log in; open protected account; log out; reopen protected account; log in again | Credentials grant account access and logout link; logout confirms sign-out; protected account requires login; same credentials authenticate again. Session termination must revoke protected access without deleting the account. | All five checkpoints matched; URLs recorded in JUnit | PASS | [Login](../evidence/t002/steps/test_t002_s01_valid_login-login.png), [account access](../evidence/t002/steps/test_t002_s01_valid_login-account-access.png), [logout](../evidence/t002/steps/test_t002_s01_valid_login-logout.png), [protected route](../evidence/t002/steps/test_t002_s01_valid_login-protected-route.png), [fresh login](../evidence/t002/steps/test_t002_s01_valid_login-fresh-login.png) |
| T002-S02 | Unique `unknown-<uuid>@example.com`, invalid synthetic password | Submit login, capture rejection, attempt protected account | Credentials warning and login route; protected access still requires authentication | Credentials warning appeared; protected route returned to login | PASS | [Rejection](../evidence/t002/steps/test_t002_s02_unknown_account-rejection.png), [protected route](../evidence/t002/screenshots/20261027T043936274860-985c921c31.png) |
| T002-S03 | Empty email and password | Submit blank form, capture rejection, attempt protected account | Credentials rejection and login route; no authenticated account access | Credentials warning appeared; protected route returned to login; no lockout warning observed | PASS | [Rejection](../evidence/t002/steps/test_t002_s03_empty_credentials-rejection.png), [protected route](../evidence/t002/screenshots/20261027T043942661643-fc87b2e2f9.png) |

Result: **3 passed, 0 failed, 0 errors, 0 skipped in 27.68 s**. No website defect or lockout was observed. The full authentication lifecycle occupies one scenario, as specified by #12. It is not counted as three standalone logout scenarios.

Source: [tests](../tests/test_login.py), [page objects](../pages/account_page.py), [isolated account and checkpoint fixtures](../conftest.py). Tested source snapshots: [tests](../evidence/t002/source/tests__test_login.py), [page objects](../evidence/t002/source/pages__account_page.py), [fixtures](../evidence/t002/source/conftest.py). Complete source screenshots: [tests](../evidence/t002/source/tests__test_login.png), [page objects](../evidence/t002/source/pages__account_page.png), [fixtures](../evidence/t002/source/conftest.png). The archived metadata identifies the base commit and tested file hashes; this PR contains the implementation and archive together.

```bash
python -m pytest tests/test_login.py --allow-account-creation --headless --screenshots=all --evidence-dir=evidence/t002 --dashboard=evidence/t002/overview.html --html=evidence/t002/report.html --self-contained-html --junitxml=evidence/t002/results.xml
```

Use a fresh folder for future runs. Screenshots show the actual Selenium browser at each checkpoint; source screenshots display the escaped, snapshotted test source. Four offline reporter checks and diff/compilation checks pass.

AI assistance: same user request recorded in [T001](t001-registration.md): clean the repository, migrate to OpenCart Abstracta, complete issues #11/#12/#19, create one PR per issue. Codex implemented the isolated fixture/lifecycle checks, executed them and drafted this table. CodeRabbit was signed out; direct review was used.

This PR links the completed case/evidence for consolidation in #6 and source submission in #10. Transfer the table/screenshots to Section 6; overall group approval and report submission are outside these observed browser outcomes.
