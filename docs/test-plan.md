# Test plan

Target: https://opencart.abstracta.us/. Aditya (Member 1 / A3939) owns F01/T001 registration (#11), F02/T002 authentication including logout (#12), and F09/T009 password reset request (#19). Wanchai (Member 3 / wanchaiS) owns F05/T005 add to cart (#15), F06/T006 update/remove cart items (#16) and F10/T010 checkout form validation (#21). This plan states expected behaviour; actual results live in the individual case documents. Search remains Member 2 work (PR #24). [Aditya’s case index](aditya-test-cases.md) and [Wanchai’s case index](wanchai-test-cases.md) link completed case tables and evidence.

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
| F05 Add to cart / T005 | S01 iPod Classic, Qty 1 | Success alert; header and cart show one item at $122.00; no stock warning |
| F05 Add to cart / T005 | S02 Canon EOS 5D without, then with, the required option | `Select required!` and nothing added; then success with `Select: Red` in the cart |
| F05 Add to cart / T005 | S03 Qty 0 | No success confirmation; cart stays empty |
| F06 Update/remove cart / T006 | S01 Qty 1 → 3 | Modified-cart alert; line and order totals $366.00 |
| F06 Update/remove cart / T006 | S02 Remove one of two products | Only that product removed; total back to $122.00 |
| F06 Update/remove cart / T006 | S03 Qty 1 → 0 | Item removed; empty-cart message |
| F09 Password reset request / T009 | S01 Dedicated registered email | Confirmation on login route; request UI only |
| F09 Password reset request / T009 | S02 Unknown synthetic email | Documented unknown-email warning; no success |
| F09 Password reset request / T009 | S03 Empty email | Request rejection; no success |
| F10 Checkout validation / T010 | S01 Checkout with an empty cart | Redirect to cart with empty-cart message |
| F10 Checkout validation / T010 | S02 Blank guest billing details | Eight field-specific messages; Step 2 stays open |
| F10 Checkout validation / T010 | S03 Invalid email, then corrected | Email message only; after correction, Delivery Method step opens; no order placed |

URLs use `/index.php?route=` and `account/register`, `account/login`, `account/logout`, `account/account`, `account/forgotten`, `product/search`, `product/product`, `checkout/cart` or `checkout/checkout` on the configured base URL.

Schedule registration validation before login validation as the assignment requests, and add to cart before cart update and checkout validation. For positive account scenarios, prepare dedicated synthetic accounts independently of pytest ordering; cart and checkout scenarios build their own guest cart through the verified add-to-cart flow. Tests use fresh browsers and do not depend on pytest execution order. Search can be tested independently and in parallel by another team member. Do not add parallel execution against shared account state without designing isolation.

Group schedule (report Section 4): [Gantt chart](schedule-gantt.png) ([SVG](schedule-gantt.svg)). Bars are planned windows, ◇ marks actual execution dates, and arrows are test dependencies.

For the group report complete website overview, roles, function dependencies, member details/allocation, a Gantt chart, environment details, individual test-case tables, real result statistics, defects/reflections, and presentation details. Preserve source code and describe AI prompts used. A pytest skip means not executed, not a pass. Setup/teardown errors must be distinguished from assertion failures. Confirm failures manually before labelling them website defects; timeouts, network errors and changed selectors can be automation issues.
