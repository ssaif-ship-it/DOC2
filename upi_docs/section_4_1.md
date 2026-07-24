# 4.1 AutoPay

UPI AutoPay is a recurring payments framework built on the Unified Payments Interface (UPI). It allows users to set up mandates (Standing Instructions) for use cases like subscriptions, loan EMIs, insurance premiums, and utility bills. While mandate creation is a one-time activity requiring authentication, it allows the user's account to be debited automatically for subsequent cycles without manual intervention (within permitted limits).

Merchants can initiate mandate creation via three modes: **QR Scanning**, **Intent Deep Links**, or **Collect Requests**.

<video src="https://github.com/user-attachments/assets/7b85f9ad-0ca5-4efc-b045-7642565cc15c" autoplay loop muted playsinline width="100%">
  Your browser does not support the video tag.
</video>


## 1. Core Concepts: Amount Rules & Frequencies

When creating a mandate, you must define the specific rules that dictate how and when funds can be pulled.

| Amount Rule | Description |
| :--- | :--- |
| **EXACT** | You are authorized to debit the exact amount specified (e.g., exactly ₹1,000 for a fixed subscription). |
| **MAX** | You are authorized to debit up to a maximum ceiling limit per cycle (e.g., up to ₹5,000 for a variable utility bill). You must ensure any extra amount collected during the first execution is adjusted in subsequent executions. |

**Supported Frequencies:**
Daily, Weekly, Fortnightly, Monthly, Bimonthly, Quarterly, Half-yearly, Yearly, or As Presented.

> **Note on "As Presented":** To prevent misuse, unverified offline merchants using "As Presented" mandates are capped at a cumulative debit of ₹25,000 per month. This cap does not apply to verified online merchants.

---

## 2. AFA (UPI PIN) Limits & Execution Rules

The NPCI enforces strict limits on how much money can be automatically debited without the customer entering their Additional Factor of Authentication (AFA/UPI PIN).

| Limit Type | Threshold | Description |
| :--- | :--- | :--- |
| **Standard Limit** | ₹15,000 | For most retail merchants, recurring debits up to ₹15,000 execute automatically without a PIN. |
| **Extended Limit** | ₹1,00,000 | For specific high-value categories mandated by OC 151A (Mutual Funds, Insurance Premiums, Credit Card Bills), the automatic PIN-less limit is extended to ₹1,00,000. |
| **Over-Limit Executions** | Above limits | Any execution exceeding these thresholds requires the user to manually enter their UPI PIN for every single cycle. |

**Instant vs. Deferred First Execution:**
*   **Instant:** If the very first debit happens instantly (within 5 minutes of mandate creation), no additional PIN is required, as the creation PIN suffices.
*   **Deferred:** If the first execution is deferred to a later date, that specific first debit will always strictly require a UPI PIN, regardless of the amount.

---

## 3. The 24-Hour Pre-Debit Notification (PDN)

To ensure transparency, you must trigger a Pre-Debit Notification (PDN) to the Payer PSP and Issuer Bank.

*   This notification must be sent at least **24 to 48 hours before** the actual execution date to remind the user to maintain a sufficient balance.
*   If you fail to send the PDN, the customer's bank will proactively block the subsequent debit execution.

> **Exemptions:** PDNs are not required for Daily frequency mandates, same-day executions, or auto-replenishments like NETC FASTag (MCC 4784) and RuPay NCMC (MCC 7412).

---

## 4. Tracking, Retries, and SeqNum

Every mandate execution is tracked using a sequential number (SeqNum). For example, month one is `SeqNum: 1`, month two is `SeqNum: 2`.

| Action | Rule |
| :--- | :--- |
| **Retries** | If an execution fails (e.g., insufficient funds), you are allowed a maximum of **9 re-initiation attempts** (10 attempts total) for that specific SeqNum. |
| **Cooling Off** | There must be a minimum gap of **1 hour** between any retry attempts. |
| **Skipping** | If all 10 attempts fail, or if you miss a cycle, that specific SeqNum stands cancelled. You must skip it and use the next sequence number (e.g., `SeqNum: 3`) for the following execution. |

---

## 5. Pause & Revoke (The Loan Exception)

Users can pause or permanently revoke their active mandates directly from their UPI app. Any attempt to debit a paused or revoked mandate will result in an immediate technical decline.

**The MCC 7322 Exception:**
To protect lenders, merchants operating under **MCC 7322 (Debt Collection / Loans)** can pass a specific `revokeable=N` flag during mandate creation. This removes the "Revoke" and "Pause" buttons from the customer's UPI app. For these EMI mandates, the user cannot cancel the AutoPay themselves; they must contact the lending institution directly.