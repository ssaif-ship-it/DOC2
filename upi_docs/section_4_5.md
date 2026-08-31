## UPI OTM (One Time Mandate)

UPI OTM lets you block a specific amount in your customer's UPI linked bank account upfront, then charge it only after you have fulfilled the order, rather than debiting the full amount at the time of purchase. It works in two stages, authorization first, capture later.

*   **How it works:** You create the order through the Create Order API, then call Order Pay with `authorize_only` set to true. This blocks the funds without debiting them, and your customer approves it in their UPI app the same way as any other UPI payment, over Collect, Intent, or QR. Once you have fulfilled the order, call the Preauthorisation API with `action` set to `CAPTURE` to debit any amount up to the authorized value, you do not have to capture the full blocked amount. If you never capture, the block releases automatically once the mandate expires. You can also void the block before capture, or refund after.
*   **Best for:** Situations where you do not know the exact final amount at the time of purchase, or where you want to hold funds without charging them yet. Common examples include IPO fund reservations, insurance premiums pending underwriting, variable utility bills, healthcare provisional amounts, refundable rental deposits, travel and hospitality bookings, and high demand product launches with limited inventory.
*   **If a capture is delayed:** Error codes 59, K1, and VH are recoverable, NPCI escalates them and settlement still lands within T+5 business days. Error code VO is not recoverable, and no further action is possible from Cashfree's side.

<!-- Claude, confirmed for Saif: rewritten against Cashfree's own public docs (cashfree.com/docs/payments/subscription/upi-otm). The use cases and the CAPTURE/void mechanics are sourced from there, not from the internal sales deck, deliberately left out that deck's pricing slab for OTM since it is commercial information and I could not verify it is meant to be public. -->

See the [API Reference](https://www.cashfree.com/docs/payments/subscription/upi-otm) for the full request and response shapes.

## UPI Reserve Pay (Single Block Multiple Debits)

UPI Reserve Pay, also called Single Block Multiple Debits (SBMD), lets you block a maximum amount once and then debit it in multiple parts over time, without your customer re-entering their UPI PIN for each individual debit. It combines the security of a one-time block with the flexibility of a recurring payment.

*   **How it works:** Your customer authorizes a single block, up to ₹10,000, valid for up to 90 days. You then debit against that reserved balance in portions, for example ₹3,000 and later ₹3,500, until it is exhausted or the mandate expires. Any unused balance releases automatically at expiry, or you can release it manually.
*   **Best for:** Try and buy or pay-on-delivery e-commerce, where you authorize an estimated amount and debit only confirmed purchases, in-app wallets, weekly or monthly subscriptions, travel and hospitality bookings where you block an estimate and debit the final bill, and securities trading, where a brokerage blocks a lump sum and debits as trades execute.
*   **Funding sources:** Reserve Pay works against savings accounts, RuPay credit cards, and credit lines linked to UPI, not only a savings account balance.

See the [Implementation Guide](https://www.cashfree.com/docs/payments/upi-reserve-pay/upi-reserve-pay) for the full integration steps.
