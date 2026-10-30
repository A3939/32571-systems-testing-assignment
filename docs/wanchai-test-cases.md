# Wanchai test cases

Wanchai Sangkusolwong / 25654120 / GitHub `wanchaiS` (Member 3) owns these three function-based cases on **https://opencart.abstracta.us/**:

| Issue | Function / case | Scenarios | Result | Section 6 table and evidence |
| --- | --- | --- | --- | --- |
| [#15](https://github.com/A3939/32571-systems-testing-assignment/issues/15) | F05 / T005 Add product to cart | In-stock product; required option; quantity 0 | 2 pass, 1 fail (D002) | [T005](t005-add-to-cart.md) |
| [#16](https://github.com/A3939/32571-systems-testing-assignment/issues/16) | F06 / T006 Update and remove cart items | Increase quantity; remove one of two products; quantity 0 | 3 pass | [T006](t006-cart-update.md) |
| [#21](https://github.com/A3939/32571-systems-testing-assignment/issues/21) | F10 / T010 Checkout form validation | Empty cart; blank guest details; invalid then corrected email | 3 pass | [T010](t010-checkout-validation.md) |

Totals: **9 scenarios — 8 passed, 1 failed, 0 errors, 0 skipped**. Defects: D002 (scripted, T005-S03), D003 (intermittent race found while debugging), D004 (cart heading, found in evidence review) and D005 (iPhone stock label, exploratory). See [T005](t005-add-to-cart.md#defects-and-observations).

Dependencies: F05 needs product details (F04) to be reachable. F06 and F10 need F05, so their positive setup goes through the `ipod_in_cart` fixture. That fixture uses the T005 add-to-cart flow and verifies it. Each scenario runs in a fresh browser with its own guest cart. No accounts are created, no orders are placed, and the tests do not depend on run order.

```bash
python3 run_tests.py --case add-to-cart     # or cart-update, checkout
```

## AI assistance

Prompt (Wanchai, 29 October 2026, to Claude, an AI coding agent working in this repository): *"Read Assessment Task 3.pdf. This is the website we chose: https://opencart.abstracta.us/. This is the GitHub repo we contribute to … and this is the current state of our report …"*. In follow-up answers Wanchai chose the Member 3 slot (F05/F06/F10). He asked for the three cases end to end plus drafts of the group report sections, delivered as a fork and pull request.

The agent explored the live site, wrote the page objects and tests in the repository's existing conventions, executed and archived the runs, investigated the two unexpected failures (D003, and the T010 automation timing issue) and drafted these documents. Expected results were taken from observed OpenCart behaviour and the site's own messages before any assertion was run. They were not adjusted to make a failing scenario pass.
