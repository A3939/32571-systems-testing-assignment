# Starter test plan

These are proposed tests, not recorded passes. Assign owners before submission.

| Function / case | Scenario | Expected result |
| --- | --- | --- |
| F01 Registration / T001 | S01 Valid unique email, matching passwords, policy checked | Account-created heading |
| F01 Registration / T001 | S02 Mismatched passwords | Specific confirmation error |
| F01 Registration / T001 | S03 Policy unchecked | Specific privacy-policy warning |
| F02 Login / T002 | S01 Existing demo account | Account page and heading |
| F02 Login / T002 | S02 Random unregistered email | Credentials warning |
| F02 Login / T002 | S03 Empty credentials | Credentials warning |
| F03 Search / T003 | S01 iPhone | Matching product title |
| F03 Search / T003 | S02 MacBook | Matching product title |
| F03 Search / T003 | S03 Unique nonexistent term | No-result message and no cards |

URLs: `/index.php?route=account/register`, `account/login`, and `product/search` on the configured base URL.

Schedule registration validation before login validation as the assignment requests. For valid login, register a dedicated account manually after checking registration, then set local environment credentials. Tests use fresh browsers and do not depend on pytest execution order. Search can be tested independently and in parallel by another team member. Do not add parallel execution against shared account state without designing isolation.

For the group report complete website overview, roles, function dependencies, member details/allocation, a Gantt chart, environment details, individual test-case tables, real result statistics, defects/reflections, and presentation details. Preserve source code and describe AI prompts used. A pytest skip means not executed, not a pass. Setup/teardown errors must be distinguished from assertion failures. Confirm failures manually before labelling them website defects; timeouts, network errors and changed selectors can be automation issues.
