# T010 — F10 Checkout form validation

Tester: **Wanchai Sangkusolwong / 25654120 / Member 3 / wanchaiS**. Issue: [#21](https://github.com/A3939/32571-systems-testing-assignment/issues/21).

Target: https://opencart.abstracta.us/index.php?route=checkout/checkout (guest checkout, Step 2 Billing Details). Executed 29 October 2026, 22:45 AEDT, headless Chrome 156. [Environment/source hashes](../evidence/t010/run.json), [dependencies](../evidence/t010/requirements-frozen.txt), [JUnit](../evidence/t010/results.xml), [dashboard](../evidence/t010/overview.html), [full report](../evidence/t010/report.html).

Preconditions: add to cart (F05) passes. S02 and S03 start from the `ipod_in_cart` fixture, which adds one verified iPod Classic in a fresh browser. S01 deliberately starts with an empty cart. Scope is form validation only: no payment method is chosen and **no order is placed**. Guest data is synthetic: `study.tester@example.com`, 15 Broadway, Ultimo NSW 2007, Australia.

| Scenario | Inputs | Steps | Expected result | Actual result | Outcome | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| T010-S01 Empty cart | No products | Open `checkout/checkout` directly | Redirect to `checkout/cart` with `Your shopping cart is empty!`; no checkout options (`#button-account`) shown; header `0 item(s) - $0.00` | Matched | PASS | [Redirected cart](../evidence/t010/screenshots/20261029T114546995271-5348d3d20f.png) |
| T010-S02 Blank guest billing details | iPod Classic in cart; every Step 2 field left blank (country stays at default United Kingdom) | Choose Guest Checkout and Continue; submit Step 2 with no input | Exactly eight field messages: First Name, Last Name, E-Mail, Telephone, Address 1, City, Post Code and Region/State. Optional Company and Address 2 show none. Step 2 stays open | Exactly the eight expected messages; Step 2 remained the only open step | PASS | [Guest form](../evidence/t010/steps/test_t010_s02_blank_guest_details-guest-form.png), [errors](../evidence/t010/screenshots/20261029T114557379391-10e689ea99.png) |
| T010-S03 Invalid email, then corrected | Valid guest details with email `study.tester@`, then `study.tester@example.com` | Fill Step 2 with Australia / New South Wales; submit; check errors; correct the email; submit again | First submit: only `E-Mail address does not appear to be valid!`, and Step 2 stays open. Second submit: no field errors, and checkout advances to Step 4 Delivery Method (`Flat Shipping Rate`) | Matched | PASS | [Invalid email](../evidence/t010/steps/test_t010_s03_invalid_email_then_corrected-invalid-email.png), [delivery method](../evidence/t010/screenshots/20261029T114611559894-7a565845b9.png) |

Result: **3 passed, 0 failed, 0 errors, 0 skipped in 29.45 s**.

## Initial run (automation issue, preserved)

The [first recorded run](../evidence/t010/initial-country-race/results.xml) had **2 passed / 1 failed**. S03 raised `NotImplementedError: You may not select a disabled option` while choosing Australia. The guest form loads regions for the default country as soon as it opens and disables the Country list until they arrive (`beforeSend: ...prop('disabled', true)`). The test selected a country inside that window. This was classified as an automation timing issue, not a website defect: a person cannot pick from a disabled list either. `CheckoutPage.continue_as_guest` now waits for AJAX to finish before the form is used. The rerun above passed. [Original screenshot](../evidence/t010/initial-country-race/screenshots/20261029T114348159123-7a565845b9.png).

Source: [tests](../tests/test_checkout.py), [checkout page object](../pages/checkout_page.py), [cart page objects](../pages/cart_page.py), [base page](../pages/base_page.py), [fixtures](../conftest.py). Tested snapshots and full source screenshots: [tests](../evidence/t010/source/tests__test_checkout.png), [checkout page object](../evidence/t010/source/pages__checkout_page.png), [cart page objects](../evidence/t010/source/pages__cart_page.png), [base page](../evidence/t010/source/pages__base_page.png), [fixtures](../evidence/t010/source/conftest.png).

```bash
python -m pytest tests/test_checkout.py --headless --screenshots=all --evidence-dir=evidence/t010 --dashboard=evidence/t010/overview.html --html=evidence/t010/report.html --self-contained-html --junitxml=evidence/t010/results.xml
```
