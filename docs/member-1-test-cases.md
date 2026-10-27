# Member 1 case index

Aditya Girishkumar Patel / 25723634 / GitHub `A3939` owns these three function-based cases on **https://opencart.abstracta.us/**:

| Issue | Function / case | Scenarios | Section 6 table and evidence |
| --- | --- | --- | --- |
| [#11](https://github.com/A3939/32571-systems-testing-assignment/issues/11) | F01 / T001 Registration | Valid unique registration; password mismatch; policy omitted | [T001](t001-registration.md) |
| [#12](https://github.com/A3939/32571-systems-testing-assignment/issues/12) | F02 / T002 Authentication including logout | Full authentication lifecycle; unknown account; empty credentials | [T002](t002-authentication.md) |
| [#19](https://github.com/A3939/32571-systems-testing-assignment/issues/19) | F09 / T009 Password reset request | Registered email; unknown email; empty email | [T009](t009-password-reset.md) |

Logout belongs to the T002 lifecycle. T009 is password reset request, as the current issue allocation specifies. Search is Member 2 work; its OpenCart selector changes remain in PR #24.

Each case has three scenarios. Each browser session is fresh; positive authentication/reset cases prepare a dedicated synthetic account through their own fixture. No test depends on another test having run first. The positive reset case makes one request; email delivery and completing the password reset are outside scope.

For another full Member 1 run, select all three files and use a new archive directory:

```bash
python -m pytest tests/test_registration.py tests/test_login.py tests/test_password_reset.py --allow-account-creation --headless --screenshots=all --evidence-dir=reports/member1-new --dashboard=reports/member1-new/overview.html --html=reports/member1-new/report.html --self-contained-html --junitxml=reports/member1-new/results.xml
```

Without `--allow-account-creation`, the three positive scenarios are skipped, never counted as passes. Negative scenarios do not require a registered account. Keep original evidence before retests. The case documents record actual outcomes, source links/screenshots, environment metadata, independent expected results and AI assistance. Group prerequisite sign-off, Section 6 consolidation (#6), individual source submission (#10) and final assignment submission remain group/member actions.
