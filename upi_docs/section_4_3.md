While standard UPI flows (Intent, Collect) transfer funds instantly, certain business models require a "pre-authorization" mechanism. You may need to secure a customer's financial commitment upfront, but only capture the funds when a service is fulfilled, an order is adjusted, or a trade is executed.

UPI solves this using the Mandate Block functionality. The customer pre-authorizes a transaction, which freezes the required funds in their bank account. The funds are only debited when the merchant initiates the execution at a later time.

There are two primary architectures for this: **One-Time Mandates (OTM)** and **Single Block Multiple Debits (SBMD) / UPI Reserve Pay**.

<img width="1299" height="698" alt="image" src="https://github.com/user-attachments/assets/cd8c7d17-91c1-46c5-a77e-cd4b60fd1dd1" />

## 1. One-Time Mandates (OTM)

A One-Time Mandate allows a merchant to block funds for a specific transaction and execute a single debit at a later time.

| Attribute | Details |
| :--- | :--- |
| **Purpose Code** | `01` |
| **Use Cases** | Hotel reservations, security deposits, or E-commerce Pay-on-Delivery (blocking funds at checkout, capturing exact amount upon delivery confirmation). |
| **Execution** | You can debit an amount up to the blocked amount. Once the single debit is executed, the mandate is permanently closed, and any remaining blocked funds are released. |
| **Revocation** | The Revoke action must be initiated by the Payee (Merchant) on behalf of the user/merchant request. |

---

## 2. Single Block Multiple Debits (SBMD) / UPI Reserve Pay

SBMD (recently rebranded by NPCI as UPI Reserve Pay) is a powerful extension of OTM. It allows a merchant to block a maximum amount once and then execute multiple partial debits against that single block over time, until the blocked funds are exhausted, the block is revoked, or it expires.

### SBMD Use Cases & Purpose Codes

**Secondary Market Trading (Purpose Code `76`)**
*   **The Flagship Use Case:** Investors can block funds in their own account against the Clearing Corporation (CC). As the broker executes trades, the CC debits the block to the extent of the successful trade obligations at the end of the day.
*   **Limit:** Exceptional maximum limit of ₹5,00,000 per transaction.
*   **MCC:** Must be `6211` (Securities Brokers/Dealers).

**Online Goods & Services (Purpose Code `77`)**
*   **Use Cases:** Quick commerce, online food delivery (debiting per order without frequent authentication), travel bookings (blocking an amount for flights/hotels and debiting per booking), cab aggregators, and EVs.
*   **Limits:** The block is limited to a maximum of ₹10,000 and can be valid for up to 90 days.
*   **Funding Sources:** Supported across Savings Accounts, Current Accounts, Overdrafts, RuPay Credit Cards, and pre-sanctioned Credit Lines.

### Execution Rules for SBMD

| Rule | Description |
| :--- | :--- |
| **Initiation** | Payer-initiated via Intent (`04`), SDK-UPI Plugin (`10`), or QR Scan (`13`). Collect mode is NOT allowed for creating SBMD blocks. |
| **Frequency** | ASPRESENTED (As and when presented). |
| **Revocation** | Like OTM, revocation is initiated by the Payee on behalf of the customer. The customer will not find a revoke option directly in their TPAP/UPI App for SBMD mandates. |

---

## 3. The Lifecycle & Architecture

The lifecycle follows three distinct phases, separating authorization from the actual transfer of funds:

### Phase 1: Block (Creation)
1. Customer initiates the mandate via Intent or QR.
2. The request goes to the Remitter Bank (or Credit Card Issuer).
3. The customer authorizes the request using their UPI PIN.
4. The Remitter Bank blocks the requested amount.

### Phase 2: Debit (Execution)
1. The Merchant/Clearing Corporation initiates a `ReqPay` (Collect) execution request for a specific amount.
2. The Remitter Bank validates the digital signature of the UPI mandate attached to the execution request.
3. If valid, the Remitter Bank temporarily removes the lien, debits the exact requested amount, and re-applies the lien to any remaining balance.
4. Confirmation is sent to the Acquiring Bank, and then to the Merchant.

> **Note on Retries (Retail):** If a debit timeouts for Purpose Code `77`, it is treated as a decline and reversed real-time. Acquiring entities may retry a maximum of 3 times in 24 hours.

### Phase 3: Release (Unblock/Revoke)
Any unutilized funds are automatically released back to the customer's available balance when the mandate expires (e.g., after 90 days for retail). Merchants can also manually trigger a revoke to release the funds early.
