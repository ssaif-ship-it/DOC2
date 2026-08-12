UPI AutoPay is a recurring payments framework built on the Unified Payments Interface (UPI). It lets your customer set up a mandate (a Standing Instruction) once, and after that one-time authorization, their account can be debited automatically for every subsequent cycle without them opening their UPI app again, within the limits described below. It is commonly used for subscriptions, loan EMIs, insurance premiums, and utility bills.

Merchants can initiate mandate creation via three modes: **QR Scanning**, **Intent Deep Links**, or **Collect Requests**.

<video src="https://github.com/user-attachments/assets/cc00d497-1171-4b8d-be57-edde6a77320c" autoplay loop muted playsinline width="100%">
  Your browser does not support the video tag.
</video>

## 1. The First Decision: Periodic or On-Demand

Before you create a mandate, decide which of the two AutoPay types fits your billing model. Everything else in this section, frequency, amount rule, and retries, follows from this choice.

| Type | How it works | Best for |
| :-- | :-- | :-- |
| **Periodic** | You register a fixed frequency (Daily, Monthly, Yearly, and so on) when creating the mandate. Cashfree automatically schedules and triggers the debit on each due date, you don't call an API to fire it. | Subscriptions, EMIs, insurance premiums, anything with a predictable billing calendar. |
| **On-Demand** | The mandate is created without a fixed schedule. You trigger each charge yourself, whenever it's due, by raising a charge through the API. | Usage-based billing, ad-hoc top-ups, or any case where you don't know the next debit date in advance. |

## 2. Frequencies (Periodic Mandates Only)

If you chose Periodic, you must register one of the following frequencies at mandate creation: Daily, Weekly, Fortnightly, Monthly, Bimonthly, Quarterly, Half-yearly, Yearly, or **As Presented**.

**As Presented is a special case.** Unlike the others, it has no fixed date or fixed amount, a debit is raised whenever you present the next bill (for example, a variable utility bill). Because the amount and date both vary, NPCI sets a lower per-mandate registration ceiling for As Presented mandates than for fixed-frequency ones, and that ceiling also varies by merchant category (MCC). For most categories it is ₹25,000 per mandate; a handful of categories are allowed higher. See [4.4 MCC-Specific Limits](#doc-4-4) for the full table before you register a mandate, this is a ceiling on what you can register the mandate for, not a monthly cap on how much you collect.

## 3. Amount Rules: Exact or Max

Alongside frequency, every mandate also carries an amount rule:

| Amount Rule | Description |
| :-- | :-- |
| **EXACT** | You are authorized to debit the exact amount specified (e.g., exactly ₹1,000 for a fixed subscription). |
| **MAX** | You are authorized to debit up to a ceiling per cycle (e.g., up to ₹5,000 for a variable utility bill). If you collect less than the ceiling in one cycle, you cannot carry the difference forward and collect it in a later cycle. |

> **For MAX mandates specifically:** the moment your customer approves the mandate in their UPI app, a ₹1 debit is triggered right away as a verification check, before any of your real recurring debits begin. *(Flagged for you to confirm from your test account: does Cashfree refund this ₹1 automatically, and does it show up separately in settlement, or does it just get treated as a normal transaction?)*

## 4. How Much Can Go Through Without a PIN

NPCI limits how much can be automatically debited before the customer has to re-enter their UPI PIN, this is their Additional Factor of Authentication, or AFA. Most merchants get a standard ceiling of ₹15,000 per debit; a short list of high-value categories (credit card bills, insurance premiums, mutual funds, and a few others) get a higher ₹1,00,000 ceiling instead. Above whichever ceiling applies to your category, the customer has to enter their PIN for that specific cycle.

The exact ceiling for your category, and the matching registration limits, are in **[4.4 MCC-Specific Limits](#doc-4-4)**, check that table rather than assuming ₹15,000 applies to you by default.

**First execution is a special case:** if it happens within 5 minutes of mandate creation, the PIN the customer just entered to create the mandate covers it too, no separate PIN entry. If the first debit is scheduled for later instead, it always needs a fresh PIN entry regardless of amount, this one time, even if it's below ₹15,000.

## 5. The Pre-Debit Notification (PDN)

Before every execution, you must send a Pre-Debit Notification (PDN) to the customer's UPI app, at least 24 hours ahead of the debit.

*   **The amount cannot change after the PDN is sent.** If the amount you actually debit differs from the amount stated in the PDN, the issuing bank declines the transaction on amount-match grounds. This is not a retry situation, correct the amount and notify again for the next attempt.
*   **If the PDN itself fails to reach the customer** (a delivery failure on the bank's or PSP's side), the debit is blocked for that cycle. This is also not something you retry directly, the execution simply cannot proceed without a delivered PDN.

> **Exemptions:** PDNs are not required for Daily frequency mandates, same-day executions, or auto-replenishment use cases like NETC FASTag (MCC 4784) and RuPay NCMC (MCC 7412).

## 6. Denied Payments and Retries

A debit can fail even after the PDN goes through successfully, and what you do next depends entirely on why it failed. Don't treat every failure the same way, only one of the four cases below is something you actually retry, and even then, only for Periodic subscriptions, On-Demand has no fixed cycle to retry within, you just raise a new charge yourself whenever you're ready.

| What happened | What you do about it |
| :-- | :-- |
| **Customer-side and temporary:** low balance, a brief network issue at the customer's bank, an inactive-but-not-closed account | **Retry it, Periodic only.** The subscription moves to ON HOLD, and you call the Retry API. Up to **3 retry attempts**, no more than **1 per day**, and it must succeed before the current cycle expires. A successful retry reactivates the subscription. |
| **The account or mandate itself is broken:** closed/invalid account, a mandate already cancelled or deactivated, a name mismatch | **Don't retry, it won't work.** The customer needs to set up a brand new mandate. |
| **Blocked by something outside normal banking:** a court order, a frozen account, KYC pending on the customer's side | **Retrying won't fix this.** Follow up with the customer directly instead. |
| **This was the mandate's very first debit, and it failed for any reason above** | **The whole mandate is cancelled**, not just this one cycle. This is the one exception to the SeqNum-skipping rule below. |

See **[4.4 MCC-Specific Limits](#doc-4-4)** for the full limits reference, registration ceilings and PIN thresholds by category, that the rest of this section points back to.

## 7. Tracking Executions: SeqNum

Every mandate execution is tracked using a sequential number (SeqNum), month one is `SeqNum: 1`, month two is `SeqNum: 2`, and so on.

If a cycle's execution is ultimately not recovered, whether retries were exhausted, the cycle expired, or the failure was non-recoverable, that SeqNum stands cancelled. You skip it and move to the next sequence number (e.g., `SeqNum: 3`) for the following cycle. A missed SeqNum does not pause or restart the sequence.

## 8. Pause & Revoke (The Loan Exception)

Customers can pause or permanently revoke their active mandates directly from their UPI app. Any attempt to debit a paused or revoked mandate results in an immediate technical decline.

**The MCC 7322 Exception:** To protect lenders, merchants operating under **MCC 7322 (Debt Collection / Loans)** can set the **Revocable Flag to `N`** during mandate creation. This removes the Pause and Cancel buttons from the customer's UPI app for that mandate. The borrower cannot cancel it themselves, only the lender can cancel a non-revocable mandate, by contacting the acquiring bank directly.
