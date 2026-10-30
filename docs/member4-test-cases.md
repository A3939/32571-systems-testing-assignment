# Member 4 (Tanut, 25677093, GitHub `zethio44`): T007, T011, T012

Target: https://opencart.abstracta.us (OpenCart 2.3, shared public demo).
Issues: [#17 T007](https://github.com/A3939/32571-systems-testing-assignment/issues/17), [#22 T011](https://github.com/A3939/32571-systems-testing-assignment/issues/22), [#23 T012](https://github.com/A3939/32571-systems-testing-assignment/issues/23).

| Case | Function | Test file | Final result |
| --- | --- | --- | --- |
| T007 | F07 Wish list | `tests/test_wishlist.py` | 2 passed, 1 failed (defect D006) |
| T011 | F11 Edit account information | `tests/test_edit_account.py` | 3 passed |
| T012 | F12 Address book | `tests/test_address_book.py` | 3 passed |

Page objects: `pages/member4_account_pages.py`. Fixture: `logged_in_account` in `conftest.py`. It reuses the verified F01 registration (`registered_account`) and the F02 login flow, so each scenario gets its own new synthetic account and fresh browser and never depends on pytest order.

## How to run

```bash
python member4_run.py --browser edge            # all three cases, evidence archived per case
python run_tests.py --case member4 --browser edge   # quick run with the group dashboard
```

`member4_run.py` writes `evidence/t007|t011|t012/` (overview.html, report.html, results.xml, run.json, requirements-frozen.txt, screenshots/, steps/, source/). If a case folder already has a run, it moves it into `previous-runs/<archive time>/` first, so failed runs are kept.

## Environment (from run.json)

Windows 11 (10.0.26200) x64, Python 3.13.2, Selenium 4 + pytest 8.4 + pytest-html, Microsoft Edge 156.0.4314.42 with msedgedriver 156.0.4314.50 (resolved by Selenium Manager), headless, 1440×1000. The group default is Chrome. Edge was added as a `--browser` option because this machine has no Chrome.

## Scenarios

### T007 F07 Wish list
- **S01 Add a product.** Precondition: the new account's wish list has no rows. Open iPhone (id 40) and record model, availability and price as this customer sees them (F04 is the oracle). Click Add to Wish List. Expected: `Success: You have added iPhone to your wish list!`, header `Wish List (1)`, and the wish list has one iPhone row whose model/stock/price match the product page.
- **S02 Persistence and navigation.** Add iPhone and MacBook (header `Wish List (2)`). Log out, then open the wish list route: expected redirect to login. Log in again, open My Account, follow the wish-list link. Expected: route `account/wishlist`, both products, header `Wish List (2)`.
- **S03 Remove.** With iPhone and MacBook saved, remove iPhone. Expected: `Success: You have modified your wish list!`, only MacBook, `Wish List (1)`. Remove MacBook. Expected: same alert, no rows, the empty-list text `Your wish list is empty.`, and `Wish List (0)`.

### T011 F11 Edit account information
- **S01 Update.** Change first name, last name and telephone to Updated / Member Four / 0298765432. Expected: `Success: Your account has been successfully updated.` on `account/account`, and the edit form shows the saved values (email unchanged).
- **S02 Empty first name.** Expected: exactly one field message, `First Name must be between 1 and 32 characters!`. The page stays on `account/edit` and the saved details are unchanged.
- **S03 Invalid email (`member4-xxxx@`).** Layer 1: the `type="email"` field fails the browser's own validation and nothing is submitted. Layer 2: with browser validation switched off (a client that skips it), the server must return exactly `E-Mail Address does not appear to be valid!`. Expected: the saved email is unchanged.

### T012 F12 Address book
- **S01 Add a valid address.** Precondition: no saved addresses. New Address → Study Tester, 15 Broadway, Ultimo 2007, Australia / New South Wales. Expected: `Your address has been successfully added` on `account/address`, and one entry showing those values.
- **S02 Missing mandatory fields.** Submit the empty form. Expected: First Name, Last Name, Address 1, City and Region / State each show their message. Company and Address 2 show none. Nothing is saved.
- **S03 Edit then delete.** Add a default and a non-default address. Edit the non-default one: the form must keep the saved country/region. Change it to 1 Harris Street, Pyrmont. Expected: `Your address has been successfully updated` and the list shows the change. Delete it. Expected: `Your address has been successfully deleted` and one entry left. Trying to delete the last address must be refused with a `Warning:` alert.

## Execution history (30 October 2026, all runs kept)

| Run | Code | T007 | T011 | T012 | Kept in |
| --- | --- | --- | --- | --- | --- |
| 1 (18:19) | 44a3846 | 0/3 | 2/3 | 0/3 | `previous-runs/20261030-182615` |
| 2 (18:26) | 44a3846, same code repeated (the update had not been copied) | 0/3 | 2/3 | 0/3 | `previous-runs/20261030-183143` |
| 3 (18:31) | bd54898 | 1/3 | 3/3 | 2/3 | `previous-runs/20261030-183606` |
| **Final (18:36)** | **ac0f6b2** | **2/3** | **3/3** | **3/3** | `evidence/t0xx/` |

`previous-runs/` folder names are the time the run was archived, not the time it ran.

The non-passes in runs 1–3 were investigated one by one. Website defects:
- **D006** (F07, F12): an empty wish list and an empty address book show `Your shopping cart is empty!`, not the list's own empty message. Asserted in T007-S03. This is probably the same mis-mapped language string as D001.
- **D007** (F07, cosmetic): the My Account page labels the wish-list link `Wish List (%s)`, with the placeholder never filled in. Seen in screenshots, not asserted.

Automation issues (fixed; not defects):
1. The precondition "list is empty" was checked by the empty-state wording (hit D006) instead of the row count (T007-S01, T012-S01, T012-S02).
2. Expected the old OpenCart link text "Modify your wish list"; the link is now followed by its route (T007-S02).
3. T011-S03: the browser's HTML5 email check blocked submission, so no server message could appear. The test now checks both layers.
4. T007-S01 hard-coded $123.20, taken from the logged-out page. A logged-in customer without an address sees ex-tax prices ($101.00) on both the product page and the wish list, so the oracle is now the product page in the same session.
5. T012-S03 read and submitted the edit form while the AJAX region list was still loading (Country disabled, so it was not posted). This produced `Please select a country!` and PHP `Undefined index: country_id` notices in run 1. The form now waits for the list to load. Once it waits, the edit form keeps the saved values, so no defect is claimed.
