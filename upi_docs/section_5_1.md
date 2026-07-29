This guide explains how and when funds from customer payments reach your bank account, how settlement cycles (T+1, T+0) work in practice, and how to manage reconciliation, direct settlements, and risk holds.

## 1. Key Concepts & Terminology

### 1.1 Summary of Lifecycle Stages

| Stage | What Happens | Merchant Timing |
| :--- | :--- | :--- |
| **Authorization** | Issuing bank confirms fund availability and locks the payment amount. | Real-time at checkout. |
| **Capture** | Transaction is finalized for clearing (Cards) or confirmed successful (UPI/NetBanking). | Real-time at checkout. |
| **Settlement** | Funds move from customer banks to the Payment Aggregator’s nodal/escrow account (or your bank account directly). | T+0 to T+2 interbank clearing. |
| **Payout** | Net money is transferred from the aggregator/acquirer into your registered merchant bank account. | Scheduled based on your T+n cycle. |

### 1.2 Gross vs. Net Settlement

*   **Gross Settlement:** You receive 100% of customer payments upfront; gateway charges and taxes are invoiced separately (common for specific enterprise setups).
*   **Net Settlement (Default):** Merchant Discount Rates (MDR), GST (18%), refunds, and chargebacks are deducted prior to payout:

```Net Payout = Gross Sales - MDR Fees - GST - Refunds/Disputes```

### 1.3 Settlement Cycles Explained (T+n)

Cycles represent business days (n) elapsed after transaction capture day (T):

*   **T+0 (Same-Day / Instant):** Payouts are executed on the transaction date itself, either in fixed daily batches (e.g., 09:00, 17:00, 20:00 IST) or via rolling 15-minute execution windows.
*   **T+1 (Next Business Day - Default):** Payouts are executed on the first banking working day following T.
*   **T+2 / Extended:** Applied for international card transactions, specific alternative payment methods, or elevated risk categories.

---

## 2. End-to-End Fund Movement

### 2.1 Standard Aggregator Model vs. Direct Settlement Model

> **Standard Model:**  [Customer] ---> [Gateway/Acquirer] ---> [Aggregator Escrow] ---> [Merchant Bank]
> **Direct Model:**    [Customer] ---> [Gateway/Acquirer] -------------------------> [Merchant Bank]

<table>
  <thead>
    <tr>
      <th style="text-align: left;">Dimension</th>
      <th style="text-align: left;">Standard Aggregator Settlement</th>
      <th style="text-align: left;">Direct Settlement</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align: left;"><strong>Escrow Routing</strong></td>
      <td style="text-align: left;">Aggregator receives funds, nets fees, and dispatches single consolidated payouts.</td>
      <td style="text-align: left;">Acquiring bank credits your corporate current account directly.</td>
    </tr>
    <tr>
      <td style="text-align: left;"><strong>Fee Collection</strong></td>
      <td style="text-align: left;">Net settlement (fees automatically deducted prior to bank transfer).</td>
      <td style="text-align: left;">Gross transfer; charges billed separately via periodic debit mandates.</td>
    </tr>
    <tr>
      <td style="text-align: left;"><strong>Reconciliation</strong></td>
      <td style="text-align: left;">Simple 1:1 match per settlement batch UTR.</td>
      <td style="text-align: left;">Requires 3-way reconciliation (Gateway Records ↔ Bank MIS ↔ Bank Statement).</td>
    </tr>
    <tr>
      <td style="text-align: left;"><strong>Refunds</strong></td>
      <td style="text-align: left;">Fully automated via PG Refund APIs.</td>
      <td style="text-align: left;">Standard PG Refund APIs are blocked; refunds require direct payout execution.</td>
    </tr>
    <tr>
      <td style="text-align: left;"><strong>Ideal For</strong></td>
      <td style="text-align: left;">E-commerce, D2C, SaaS, Retail</td>
      <td style="text-align: left;">Broking (MCC 6211), Wealth Management, Mutual Funds</td>
    </tr>
  </tbody>
</table>
---

## 3. Cut-off Times, Weekends & Bank Holidays

### 3.1 Eligibility Cut-off Formula

Settlement eligibility is evaluated using strict business-day logic:

```Eligibility Cut-off = Date + (n - 1  days) + 23:59:59 IST```

If the resulting target date falls on an RBI banking holiday or non-working day, the execution date rolls forward to the next bank working day.

### 3.2 Practical Examples

*   **Standard T+1 Batch:** Transaction captured Thursday at 16:00 IST → Included in Friday’s scheduled payout batch (e.g., 14:00 IST).
*   **Weekend Rollover (T+1):** Transaction captured Friday at 18:00 IST → Target date is Saturday. Because banks are closed, payout moves to Monday's batch. (If Monday is a bank holiday, payout executes Tuesday).
*   **T+0 Instant Override:** 24x7 Instant Settlements execute continuously via IMPS/UPI rails regardless of bank holidays.

### 3.3 Payment Mode Level Configuration

You can configure distinct settlement schedules per payment method rather than enforcing a single global schedule across your entire account:

```text
[Merchant Account Config]
  ├── UPI Transactions        ===> T+0 (Instant / Same Day)
  ├── Domestic Cards & NetBank ===> T+1 (Next Working Day)
  └── International Cards      ===> T+5 (Extended Risk Window)