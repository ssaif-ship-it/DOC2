## 1. Overview & Error Architecture

When a UPI transaction or recurring debit fails, the failure signal originates at one of three layers before being reported back to your application:

```text
[ Customer / UPI App ] ---> [ NPCI Switch / Remitter Bank ] ---> [ Gateway / Switch ] ---> [ Merchant Backend ]
       (User Error)                 (Bank/Network Error)             (Normalized API)            (Handled Code)
```

1. **User / Account Errors (Business Failures):** Actionable issues originating from customer state (e.g., entering an incorrect PIN, insufficient account balance, or breaching daily limits).
2. **Bank / Switch Errors (Technical Failures):** Infrastructure issues at the remitter bank's Core Banking System (CBS) or NPCI routing switch.
3. **Compliance & Policy Blocks:** Failures triggered by regulatory guardrails (e.g., TPV account mismatch, restricted MCC flow block, or 24-hour velocity caps).
4. **AutoPay & Mandate State Failures:** Failures specific to recurring mandate executions (e.g., paused/revoked mandates, missing 24h pre-debit notifications, or sequence number desynchronization).

### Gateway Error Payload Structure

To abstract bank-specific error strings across different acquirers, the gateway returns a standardized error contract in both API responses and webhooks:

```json
{
  "event": "PAYMENT_FAILED",
  "data": {
    "order_id": "order_99887766",
    "cf_payment_id": 18294021,
    "payment_status": "FAILED",
    "error_details": {
      "error_code": "INSUFFICIENT_FUNDS",
      "error_type": "USER_ERROR",
      "error_subcode": "ZA",
      "error_message": "The customer account has insufficient funds to complete the transaction.",
      "raw_bank_response": "ZA - REMITTER BANK INSUFFICIENT BALANCE"
    }
  }
}
```

## 2. Master NPCI Error Code & Business Failure Mapping

The table below maps standard NPCI error codes, raw bank responses, root causes, and recommended user/checkout actions:
# error codes table

# https://ssaif-ship-it.github.io/Error_codes/

## 3. High-Priority Business Scenarios & Edge Cases

### 3.1 Third-Party Verification (TPV) Failures (U19)

In investment and capital markets flows (MCC 6211 / 6012), regulatory mandates require validating the remitter account against customer record.

- **Trigger:** Customer initiates a payment using a UPI ID linked to Account A, but registered profile has Account B.
- **Gateway Action:** Transaction is aborted before money leaves the bank, failing with `TPV_ACCOUNT_MISMATCH`.
- **Handling:** Display explicit error banner detailing the expected account number last 4 digits:

  > Expected Account: `XXXX-XXXX-1234`

### 3.2 The 24-Hour Velocity Cooling-Off Rule (U30)

To prevent account takeover fraud, NPCI caps transactions at ₹5,000 for 24 hours after:

1. Initial UPI registration on a device.
2. Device binding/SIM change.
3. UPI PIN reset/change.

If an order is ₹15,000, NPCI will decline the transaction with code U30 even if the user has ample account balance. Checkouts should detect U30 and offer non-UPI fallback instruments.

### 3.3 Restricted Flow Errors (U69)

Attempting to send a "pull" (Collect) request for restricted business categories results in an immediate U69 rejection.

```text
[Merchant App] -- Collect Request (MCC 5816) --> [NPCI Switch] -- REJECT (U69: Collect Blocked) --> [Merchant]
```

To resolve this permanently, merchants operating in restricted MCCs must eliminate VPA entry screens and use **UPI Intent Deep Links** or **Dynamic QR Codes**.



## 5. AutoPay Pre-Debit Notification (PDN) & Retry Guardrails

### 5.1 The 24-Hour PDN Rule

For all AutoPay recurring debits exceeding same-day execution, merchants must notify the user's issuing bank via the Pre-Debit Notification (PDN) API at least 24 to 48 hours prior to execution.

```text
[Day T-1 (24h Prior)] ---> Send PDN Request ---> [Payer PSP / Issuer Bank] ---> SMS Sent to User
[Day T (Execution)]   ---> Trigger ReqPay API  ---> [Bank Validates PDN]     ---> Debit Executed
```

If PDN is not sent or fails delivery validation, the issuer bank drops the debit with error `PRE_DEBIT_NOTIF_REQUIRED`.

**Exemptions:** Daily frequency mandates, same-day instant first execution (≤ 5 mins from creation), FASTag auto-replenishment (MCC 4784), and Transit (MCC 7412).

### 5.2 AutoPay Retry Matrix (SeqNum Lifecycle Rules)

When a recurring debit fails due to temporary balance insufficiency (ZA) or CBS timeouts (U66):

- **Max Retry Limit:** A maximum of 9 retry attempts (10 total executions) is allowed for a single sequence number (SeqNum).
- **Cooling-off Window:** Each retry attempt must be spaced by a minimum interval of 1 hour.
- **SeqNum Progression:** If all 10 attempts fail or the execution window for that billing cycle closes, that SeqNum is marked `EXPIRED`/`CANCELLED`. The merchant must skip to the next sequence number (e.g., SeqNum: 2 → SeqNum: 3) for the following billing cycle.

## 6. Merchant Retry Matrix & Smart Logic

Not all errors should trigger an automated retry. The decision tree below details how checkout and recurring engines should handle specific failure states:

```text
                          [ Payment Failure Received ]
                                       |
          +----------------------------+----------------------------+
          |                                                         |
 [ User-Fixable / Terminal ]                              [ Technical / Network ]
(ZA, ZM, U01, U16, U19, U30, M1, MD, MP)                  (U66, U14, B1, Timeout, MF)
          |                                                         |
 Do NOT retry automatically.                               Can retry automatically!
 Show actionable UI alert or                               Route to backup acquirer node,
 update subscription status.                                or retry debit after 1h delay.
```

### Action Logic Summary

1. **INSUFFICIENT_FUNDS / INCORRECT_PIN:** Display inline prompt. Do **not** trigger background retries.
2. **CBS_UNREACHABLE / SYSTEM_TIMEOUT:** Gateway handles internal retry across healthy bank pipes. If terminal failure is reached, offer a 1-click retry button.
3. **MANDATE_REVOKED / MANDATE_PAUSED:** Instantly flag recurring subscription in backend CRM and request user to re-authorize mandate.
4. **TRANSACTION_LIMIT_EXCEEDED:** Do not offer retry with UPI. Instantly toggle checkout tab to Credit/Debit Cards or NetBanking.

## 7. Webhook Integration Checklist for Failure Handling

- [ ] **Subscribe to PAYMENT_FAILED Webhooks:** Ensure backend listens for terminal failure webhooks to release reserved inventory immediately.
- [ ] **Subscribe to MANDATE_NOTIFICATION Webhooks:** Capture real-time events for mandate revocation, pause, and execution failures.
- [ ] **Parse Subcode Metadata:** Store `error_subcode` and `raw_bank_response` in transaction logs for analytics and support debugging.
- [ ] **Filter Non-Actionable Alerts:** Do not trigger internal engineering alerts for customer-driven errors (ZA, ZM); monitor spike rates only for infrastructure errors (U66, B1).
- [ ] **Synchronize Order Lifecycle:** Ensure stock allocation is unblocked instantly when U19 (TPV Mismatch) or U69 (Collect Blocked) occurs.