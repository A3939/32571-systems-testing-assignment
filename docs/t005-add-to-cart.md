# T005 — F05 Add product to cart

Tester: **Wanchai Sangkusolwong / 25654120 / Member 3 / wanchaiS**. Issue: [#15](https://github.com/A3939/32571-systems-testing-assignment/issues/15).

Target: product pages `product/product&product_id=48` (iPod Classic, no options) and `product_id=30` (Canon EOS 5D, required **Select** option), then `checkout/cart`, under https://opencart.abstracta.us/index.php?route= . Executed 29 October 2026, 22:44 AEDT, headless Chrome 156. [Environment/source hashes](../evidence/t005/run.json), [dependencies](../evidence/t005/requirements-frozen.txt), [JUnit](../evidence/t005/results.xml), [dashboard](../evidence/t005/overview.html), [full report](../evidence/t005/report.html).

Preconditions: product details (F04) are reachable. iPod Classic showed `Availability: 528` and Canon EOS 5D showed `Availability: 20` when the cases were designed. Each scenario starts in a fresh browser, so it starts with its own empty guest cart. No account is created and no order is placed.

| Scenario | Inputs | Steps | Expected result | Actual result | Outcome | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| T005-S01 Add an in-stock product | iPod Classic, default Qty 1 | Open product 48; confirm name and empty header cart; click Add to Cart; open cart | Alert `Success: You have added iPod Classic to your shopping cart!`; header `1 item(s) - $122.00`; cart lists only iPod Classic, Qty 1, unit and line total $122.00; no `***` stock warning | Matched | PASS | [Added](../evidence/t005/steps/test_t005_s01_add_simple_product-added.png), [cart](../evidence/t005/screenshots/20261029T114458128346-606cf23435.png) |
| T005-S02 Required option | Canon EOS 5D; Select left at `--- Please Select ---`, then `Red` | Click Add to Cart without an option; check header; choose Red; Add to Cart again; open cart | First attempt shows `Select required!` and the header stays `0 item(s) - $0.00`. Second attempt shows the success alert and header `1 item(s) - $98.00`; the cart row shows `Select: Red`, Qty 1, $98.00 | Matched | PASS | [Option required](../evidence/t005/steps/test_t005_s02_required_option-option-required.png), [cart](../evidence/t005/screenshots/20261029T114505558118-c1fcbe8ad4.png) |
| T005-S03 Quantity 0 | iPod Classic, Qty `0` | Enter 0 in Qty; click Add to Cart; capture the response; open cart | The add is rejected, or at least no success confirmation appears; the cart stays empty | Cart stayed empty (`0 item(s) - $0.00`, `Your shopping cart is empty!`), but the product page showed **`Success: You have added iPod Classic to your shopping cart!`** | **FAIL — defect D002** | [Success alert with 0 items](../evidence/t005/steps/test_t005_s03_zero_quantity-add-response.png), [empty cart](../evidence/t005/screenshots/20261029T114512880250-b04eddd410.png) |

Result: **2 passed, 1 failed, 0 errors, 0 skipped in 21.68 s**.

## Defects and observations

- **D002 — False success message for an invalid quantity (T005-S03, medium).** Quantity 0 shows the success confirmation, but nothing is added. Exploration on 29 October showed the same behaviour for quantity -1. A shopper is told the item is in the cart when it is not.
- **D003 — Add-to-cart confirmation can disappear (intermittent, low).** Changing Qty and clicking Add to Cart fires two AJAX requests. If the quantity-change response arrives second, it removes the success alert. This was reproduced live in 1 of 6 probes. Root cause and timeline: [investigation](../evidence/t005/investigation-alert-race.md). `set_quantity` now waits for that request to finish, so S03 measures the quantity rule rather than the race.
- **D004 — Cart page heading is wrong (found in evidence review, low).** With items in the cart, the cart page `<h1>` reads `Use Gift Certificate (n.nnkg)` instead of `Shopping Cart (n.nnkg)`. With an empty cart it reads `Shopping Cart`. It is visible in every non-empty cart screenshot, e.g. [S01 cart](../evidence/t005/screenshots/20261029T114458128346-606cf23435.png). This was not a scripted assertion.
- **D005 — iPhone availability contradicts the cart (exploratory, medium).** The iPhone page shows `Availability: In Stock`. Adding one iPhone flags the cart row `***` with `Products marked with *** are not available in the desired quantity or not in stock!` [Product page](../evidence/t005/exploratory/iphone-product-in-stock.png), [cart](../evidence/t005/exploratory/iphone-cart-not-in-stock.png). [INFERENCE] Stock on this shared demo is probably at or below 0, with the out-of-stock status label configured as "In Stock". Checkout is not blocked.

Source: [tests](../tests/test_add_to_cart.py), [page objects](../pages/cart_page.py), [base page](../pages/base_page.py), [fixtures](../conftest.py). Tested snapshots and full source screenshots: [tests](../evidence/t005/source/tests__test_add_to_cart.png), [cart page objects](../evidence/t005/source/pages__cart_page.png), [base page](../evidence/t005/source/pages__base_page.png), [fixtures](../evidence/t005/source/conftest.png).

```bash
python -m pytest tests/test_add_to_cart.py --headless --screenshots=all --evidence-dir=evidence/t005 --dashboard=evidence/t005/overview.html --html=evidence/t005/report.html --self-contained-html --junitxml=evidence/t005/results.xml
```

The failing scenario is the intended detection of D002, not an automation error. The [AI assistance](wanchai-test-cases.md#ai-assistance) used for this case is recorded in the case index.
