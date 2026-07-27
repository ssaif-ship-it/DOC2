This guide outlines standard non-technical business failures, network response codes, error normalization rules, and subscription-specific AutoPay errors in UPI processing. It helps engineering, finance, and customer support teams distinguish between recoverable user errors, mandate state blocks, bank outages, and compliance guardrails to optimize checkout and recurring billing retry paths.

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

| NPCI Code | Gateway Error Code | Root Cause / Business Context | Category | Recommended Action / UI Guidance |
| :--- | :--- | :--- | :--- | :--- |
| **ZA** | `INSUFFICIENT_FUNDS` | Remitter account balance is lower than transaction amount. | User Error | Prompt user to choose another bank account, RuPay Credit Card, or alternative payment method. Do not retry automatically. |
| **ZM** | `INCORRECT_PIN` | Customer entered an incorrect 4-digit or 6-digit UPI PIN. | User Error | Prompt customer to re-enter PIN carefully or reset UPI PIN in their UPI app. |
| **Z6** | `PIN_ATTEMPTS_EXCEEDED` | Customer entered an incorrect UPI PIN 3 consecutive times; account blocked for 24h. | User Error | Instruct customer to wait 24 hours or reset PIN using their debit card in their UPI app. |
| **ZK** | `ACCOUNT_BLOCKED` | Customer's bank account is frozen, inactive, or restricted by the issuing bank. | Compliance / Risk | Advise customer to contact their issuing bank to remove account blocks. |
| **U16** | `TRANSACTION_LIMIT_EXCEEDED` | Transaction exceeds daily per-transaction cap (₹1,00,000 standard P2M or ₹5,00,000 special MCC cap). | Limit Error | Request customer to split order amount or use NetBanking / Credit Card. |
| **U30** | `NEW_USER_VELOCITY_CAP` | Customer registered, changed device, or reset PIN within the last 24 hours (capped at ₹5,00,000 → ₹5,000). | Anti-Fraud Cap | Show message: "UPI limit capped at ₹5,000 for 24 hours following phone/PIN setup. Please pay using NetBanking." |
| **U19** | `TPV_ACCOUNT_MISMATCH` | Paid account does not match registered investor account details (MCC 6211 Capital Markets). | Compliance Block | Inform user that payment must originate strictly from their pre-registered bank account. |
| **U01** | `VPA_NOT_FOUND` | Virtual Payment Address (VPA / UPI ID) entered does not exist or handle is deleted. | Input Error | Prompt user to re-check and type a valid UPI handle (e.g., name@upi). |
| **U69** | `COLLECT_BLOCKED_FOR_MCC` | Collect request initiated for an MCC restricted to Intent/QR only (Gaming 5816, Wallet 6540, Rent 6513). | Integration Block | Switch checkout implementation to UPI Intent or Dynamic QR flow. |
| **U14** | `ENCRYPTION_ERROR` | Device Common Library (CL) token expired or cryptographic handshake failed. | Technical | Ask user to retry transaction or restart their UPI app. |
| **U66** | `CBS_UNREACHABLE` | Remitter bank Core Banking System (CBS) is temporarily down or timed out. | Network Failure | Automatically retry via secondary acquiring route or show bank outage status. |

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

## 4. AutoPay & Recurring Mandate Specific Errors

Recurring mandates have their own set of error codes due to lifecycle constraints, pre-debit notifications, and sequential debit ordering.

### 4.1 Master AutoPay Error Code Reference

| Error Code | Gateway Error Code | Context / Root Cause | Operational Handling & Retry Rules |
| :--- | :--- | :--- | :--- |
| **M1** | `MANDATE_NOT_FOUND` | UMN (Unique Mandate Number) is invalid or does not exist in switch records. | Do not retry. Prompt user to re-authorize a fresh AutoPay mandate setup. |
| **M2** | `MANDATE_EXPIRED` | The end date of the mandate has lapsed. | Block automatic debits. Require customer to set up a new subscription mandate. |
| **MD / M3** | `MANDATE_REVOKED` | Customer explicitly cancelled/revoked the mandate inside their UPI App. | Mandate terminal state. Mark subscription as `CANCELLED` in merchant database; trigger re-activation email. |
| **MP** | `MANDATE_PAUSED` | Customer temporarily paused the mandate in their UPI App. | Do not execute. Wait until customer unpauses, or send a push notification to resume subscription. |
| **M5** | `SEQ_NUM_MISMATCH` | Execution submitted with an out-of-sync SeqNum (e.g. sent SeqNum: 4 when bank expected 3). | Re-synchronize SeqNum against last successful webhook or query Mandate Details API before retrying. |
| **M6** | `DUPLICATE_EXECUTION` | An execution attempt for the current SeqNum was already processed or is pending. | Check transaction status via API; do not trigger another debit for this cycle. |
| **PDN_MISSING** | `PRE_DEBIT_NOTIF_REQUIRED` | Debit initiated without delivering a Pre-Debit Notification 24h prior. | Issuer bank automatically rejects debit. Schedule PDN immediately and queue debit 24 hours later. |
| **MF** | `RECURRING_DEBIT_FAILED` | Debit failed due to remitter side reasons (ZA Insufficient Funds or ZK Account Blocked). | Retries permitted: Max 9 retries (10 total) for this SeqNum with at least 1 hour cooling-off period. |

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