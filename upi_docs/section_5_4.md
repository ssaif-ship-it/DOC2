Every payment failure on the UPI network or card rails returns a raw, technical error string from the issuing bank or switch, such as `U30|DEBIT HAS BEEN FAILED|Z9|INSUFFICIENT FUNDS IN CUSTOMER (REMITTER) ACCOUNT`, `ZM`, `U69`, or `EPI401`. Displaying these raw codes directly to customers leads to confusion, unnecessary support tickets, and cart abandonment.

This guide details how to translate raw error payloads into plain-language, action-oriented customer messages that drive retries, protect checkout conversion, and maintain trust.

---

## 1. The Three-Layer Error Model

Every payment failure undergoes a three-stage translation process. Only the third stage should ever be rendered on customer-facing screens:

| Layer | Audience / Target | Example Payload |
| :-- | :-- | :-- |
| **1. Raw Bank / Network Code** | Internal logs, gateway routing, switch recon | `U30\|DEBIT HAS BEEN FAILED\|Z9\|INSUFFICIENT FUNDS` |
| **2. Normalized Gateway Code** | Merchant APIs, webhooks, analytics dashboards | `error_code: "TRANSACTION_DECLINED"`, `error_reason: "debit_failed"`, `error_source: "bank"` |
| **3. Customer-Facing Message** | Checkout UI, mobile app modals, SMS / Email | *"Your payment failed due to insufficient balance. Please add funds and try again, or use a different account."* |

### Cashfree Normalized Payload Structure

Cashfree automatically abstracts raw bank responses inside the `error_details` object:

```json
{
  "error_details": {
    "error_code": "TRANSACTION_DECLINED",
    "error_description": "payment has been declined",
    "error_reason": "debit_failed",
    "error_source": "bank",
    "error_code_raw": "Z9",
    "error_description_raw": "INSUFFICIENT FUNDS IN CUSTOMER (REMITTER) ACCOUNT"
  }
}
