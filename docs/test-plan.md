# Test plan

These are expected behaviours, not recorded passes. Member 1 (GitHub `A3939`) owns registration, login and logout through issues #11, #12 and #19. Search is a separate team example. Individual case tables are in [member-1-test-cases.md](member-1-test-cases.md).

| Function / case | Scenario | Expected result |
| --- | --- | --- |
| F01 Registration / T001 | S01 Valid unique email, matching passwords, policy checked | Account-created heading |
| F01 Registration / T001 | S02 Mismatched passwords | Specific confirmation error |
| F01 Registration / T001 | S03 Policy unchecked | Specific privacy-policy warning |
| F02 Login / T002 | S01 Existing demo account | Account route and visible sidebar logout link |
| F02 Login / T002 | S02 Random unregistered email | Credentials warning |
| F02 Login / T002 | S03 Empty credentials | Credentials warning |
| F03 Search / T003 | S01 iPhone | Matching product title |
| F03 Search / T003 | S02 MacBook | Matching product title |
| F03 Search / T003 | S03 Unique nonexistent term | No-result message and no cards |
| F09 Logout / T009 | S01 Logout from authenticated session | Logout route, heading and confirmation text |
| F09 Logout / T009 | S02 Open protected account page after logout | Redirect to login with email/password fields |
| F09 Logout / T009 | S03 Login again after logout with same account | Account route and visible sidebar logout link |

URLs use `/index.php?route=` followed by `account/register`, `account/login`, `account/logout`, `account/account` (protected) or `product/search` on the configured base URL.

Schedule registration validation before login validation, then logout validation. For valid login, register a dedicated account manually after checking registration, then set local environment credentials. Validate the group prerequisites G03 (function catalogue) and G05 (environment) before the final evidence run. Tests use fresh browsers and do not depend on pytest execution order. Logout tests establish their own authenticated session; login failures during this setup are errors in the logout prerequisite, not successful logout tests. Search can be tested independently and in parallel by another team member. Do not add parallel execution against shared account state without designing isolation.

For the group report complete website overview, roles, function dependencies, member details/allocation, a Gantt chart, environment details, individual test-case tables, real result statistics, defects/reflections, and presentation details. Preserve source code and describe AI prompts used. A pytest skip means not executed, not a pass. Setup/teardown errors must be distinguished from assertion failures. Confirm failures manually before labelling them website defects; timeouts, network errors and changed selectors can be automation issues.
