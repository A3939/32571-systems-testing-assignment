# T005 investigation — Add to Cart confirmation can disappear (observation O-01 / defect D003)

Found while debugging the first dry run of T005-S03 on 29 October 2026. That run timed out after 15 s with no success alert and no validation message, although the quantity-0 request had been sent. A rerun reached the expected assertion. The timeout came from a race on the site, not from a slow server.

## Cause (from the live page source)

The product page binds two AJAX handlers:

```js
$('select[name=\'recurring_id\'], input[name="quantity"]').change(function(){ $.ajax({url:'index.php?route=product/product/getRecurringDescription', ...
  success:function(json){ $('.alert-dismissible, .text-danger').remove(); ... } }) })
$('#button-cart').on('click', function(){ $.ajax({url:'index.php?route=checkout/cart/add', ... }) })
```

A shopper who edits **Qty** and then clicks **Add to Cart** triggers both. The click blurs the field, which fires `change`, so the two requests leave within a millisecond of each other. If `getRecurringDescription` responds last, its success handler deletes the `alert-success alert-dismissible` confirmation that `cart/add` has just inserted. It also deletes any `.text-danger` validation message.

## Probe (fresh headless Chrome session per attempt, iPod Classic, jQuery ajaxSend/ajaxComplete log)

| Attempt | Qty | Confirmation visible | Timeline relative to the `cart/add` send |
| --- | --- | --- | --- |
| 0 | 0 | yes, 0.7 s | `cart/add` done +575 ms; `getRecurringDescription` done earlier |
| 1 | 1 | yes, 0.9 s | `cart/add` done last |
| 2 | 0 | yes, 1.1 s | `cart/add` done last |
| 3 | 1 | yes, 0.9 s | `cart/add` done last |
| **4** | **0** | **no, still absent after 40 s** | `cart/add` done +681 ms → `getRecurringDescription` done **+684 ms** (removes the alert) |
| 5 | 1 | yes, 0.9 s | `cart/add` done last |

In attempt 4 the item was still processed server-side, and `common/cart/info` refreshed the header. The shopper saw no confirmation.

## Effect on the automation

`ProductPurchasePage.set_quantity` now tabs out of the field and waits for `jQuery.active === 0` before Add to Cart is clicked. This makes T005-S03 deterministic: it tests what the site does with quantity 0 rather than which response wins the race. The race remains a site defect. It is recorded as D003 (intermittent, low severity) in the report and was not counted as a scenario outcome.
