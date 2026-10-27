# Test plan

Target: https://opencart.abstracta.us/. Aditya (Member 1 / A3939) owns F01/T001 registration (#11), F02/T002 authentication including logout (#12), and F09/T009 password reset request (#19). This plan states expected behaviour; actual results live in the individual case documents. Search remains Member 2 work (PR #24). The [Member 1 index](member-1-test-cases.md) links completed case tables and evidence.

| Function / case | Scenario | Expected result |
| --- | --- | --- |
| F01 Registration / T001 | S01 Valid unique email, matching passwords, policy checked | Success route, explicit account-created message and authenticated sidebar |
| F01 Registration / T001 | S02 Mismatched passwords | Specific confirmation error |
| F01 Registration / T001 | S03 Policy unchecked | Specific privacy-policy warning |
| F02 Authentication / T002 | S01 Authentication lifecycle | Login, account access, logout, protected-route rejection and fresh login |
| F02 Authentication / T002 | S02 Random unregistered email | Credentials warning |
| F02 Authentication / T002 | S03 Empty credentials | Credentials warning |
| F03 Search / T003 | S01 iPhone | Matching product title |
| F03 Search / T003 | S02 MacBook | Matching product title |
| F03 Search / T003 | S03 Unique nonexistent term | No-result message and no cards |

| F09 Password reset request / T009 | S01 Dedicated registered email | Confirmation on login route; request UI only |
| F09 Password reset request / T009 | S02 Unknown synthetic email | Documented unknown-email warning; no success |
| F09 Password reset request / T009 | S03 Empty email | Request rejection; no success |

URLs use `/index.php?route=` and `account/register`, `account/login`, `account/logout`, `account/account`, `account/forgotten` or `product/search` on the configured base URL.

Schedule registration validation before login validation as the assignment requests. For positive account scenarios, prepare dedicated synthetic accounts independently of pytest ordering. Tests use fresh browsers and do not depend on pytest execution order. Search can be tested independently and in parallel by another team member. Do not add parallel execution against shared account state without designing isolation.

For the group report complete website overview, roles, function dependencies, member details/allocation, a Gantt chart, environment details, individual test-case tables, real result statistics, defects/reflections, and presentation details. Preserve source code and describe AI prompts used. A pytest skip means not executed, not a pass. Setup/teardown errors must be distinguished from assertion failures. Confirm failures manually before labelling them website defects; timeouts, network errors and changed selectors can be automation issues.
