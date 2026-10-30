# T006 — F06 Update and remove cart items

Tester: **Wanchai Sangkusolwong / 25654120 / Member 3 / wanchaiS**. Issue: [#16](https://github.com/A3939/32571-systems-testing-assignment/issues/16).

Target: https://opencart.abstracta.us/index.php?route=checkout/cart . Executed 29 October 2026, 22:45 AEDT, headless Chrome 156. [Environment/source hashes](../evidence/t006/run.json), [dependencies](../evidence/t006/requirements-frozen.txt), [JUnit](../evidence/t006/results.xml), [dashboard](../evidence/t006/overview.html), [full report](../evidence/t006/report.html).

Preconditions: add to cart (F05/T005-S01) passes. Each scenario uses a fresh browser. The `ipod_in_cart` fixture adds one iPod Classic through the same add-to-cart flow and checks both the success alert and the `1 item(s) - $122.00` header before the scenario starts. A fixture failure is reported as an ERROR, not a FAIL. No account or order is created.

| Scenario | Inputs | Steps | Expected result | Actual result | Outcome | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| T006-S01 Increase quantity | Cart with iPod Classic ×1; new Qty 3 | Open cart; confirm Qty 1; type 3; click Update (refresh icon) | `Success: You have modified your shopping cart!`; Qty 3; line total $366.00; Sub-Total $300.00; Total $366.00; header `3 item(s) - $366.00` | Matched | PASS | [Before](../evidence/t006/steps/test_t006_s01_update_quantity-before-update.png), [after](../evidence/t006/screenshots/20261029T114522827562-2bcbefe07f.png) |
| T006-S02 Remove one of two products | Cart with iPod Classic ×1 plus Canon EOS 5D (Select: Red) ×1 | Add Canon EOS 5D with Red; open cart and confirm both rows; click Remove (×) on Canon EOS 5D | Only Canon EOS 5D disappears; iPod Classic stays at Qty 1; Total $122.00; header `1 item(s) - $122.00` | Matched | PASS | [Two products](../evidence/t006/steps/test_t006_s02_remove_one_product-two-products.png), [after remove](../evidence/t006/screenshots/20261029T114534240837-da2654ec28.png) |
| T006-S03 Quantity 0 removes the item | Cart with iPod Classic ×1; new Qty 0 | Open cart; type 0; click Update | The item is removed (OpenCart treats quantity ≤ 0 as removal); the cart shows `Your shopping cart is empty!` on `checkout/cart`; header `0 item(s) - $0.00` | Matched | PASS | [Before](../evidence/t006/steps/test_t006_s03_zero_quantity_removes_item-before-update.png), [empty cart](../evidence/t006/screenshots/20261029T114541750483-0f3f3a09d0.png) |

Result: **3 passed, 0 failed, 0 errors, 0 skipped in 28.48 s**.

The cart heading defect D004 (`Use Gift Certificate (n.nnkg)` instead of `Shopping Cart`) is visible in the S01 and S02 screenshots. It is recorded in [T005](t005-add-to-cart.md#defects-and-observations) and was not asserted here, so these outcomes reflect only the update and remove behaviour.

Source: [tests](../tests/test_cart_update.py), [page objects](../pages/cart_page.py), [base page](../pages/base_page.py), [`ipod_in_cart` fixture](../conftest.py). Tested snapshots and full source screenshots: [tests](../evidence/t006/source/tests__test_cart_update.png), [cart page objects](../evidence/t006/source/pages__cart_page.png), [base page](../evidence/t006/source/pages__base_page.png), [fixtures](../evidence/t006/source/conftest.png).

```bash
python -m pytest tests/test_cart_update.py --headless --screenshots=all --evidence-dir=evidence/t006 --dashboard=evidence/t006/overview.html --html=evidence/t006/report.html --self-contained-html --junitxml=evidence/t006/results.xml
```
