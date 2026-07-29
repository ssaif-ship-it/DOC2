While standard UPI flows (Intent, Collect) transfer funds instantly, certain business models require a pre-authorization mechanism. Merchants often need to secure a customer's financial commitment upfront, but only capture the funds when a service is fulfilled, an order is adjusted, or a trade is executed.

UPI addresses this through **Mandate Block (Lien)** functionality. The customer pre-authorizes a transaction, freezing the required funds directly within their bank account. The money is only debited when the merchant initiates execution at a later time. This completely eliminates custodial risk, keeping money safely in the customer's account until the exact moment of payment.

## 1. Mandate Architecture Comparison

| Feature / Attribute | One-Time Mandates (OTM) | UPI AutoPay | SBMD / UPI Reserve Pay |
| :--- | :--- | :--- | :--- |
| **Mandate Recurrence** | One-Time | Recurring | Recurring |
| **Blocking of Funds (Lien)** | ✅ Yes | ❌ No | ✅ Yes |
| **Execution Pattern** | Single debit | Multiple debits per cycle | Multiple debits against 1 block |
| **Debit Failure Risk** | Near Zero (Funds Blocked) | High (Balance dependent) | Near Zero (Funds Blocked) |
| **Purpose Codes** | 01 | SI / Various | 76 (Trading), 77 (Retail) |
| **PIN Authentication** | 1-Time at Block creation | 1-Time at Setup | 1-Time at Block creation |

## 2. One-Time Mandates (OTM)

A One-Time Mandate allows a merchant to block funds for a single transaction and execute a single debit at a later time.

### Key Specifications

- **Purpose Code:** `01`
- **Primary Use Cases:** Hotel reservations, security deposits, IPO subscriptions (ASBA), e-commerce Pay-on-Delivery, and train ticket booking (IRCTC).
- **Execution:** A single debit up to the blocked amount (execution ≤ blocked amount). Once executed, the mandate is permanently closed, and any residual balance is automatically unblocked.
- **Mandate Creation:** Payee-initiated (Collect mode) or Payer-initiated (Intent/QR).
- **Mandate Operations:** `CREATE`, `MODIFY`, `REVOKE`.
- **Max Validity:** Configured by merchant/acquirer (up to 30 years maximum).

### Execution Rules & Mechanics

1. **Order Creation:** Call `POST /orders` with `authorize_only: true` and pass an authorization object detailing block amount and validity windows.
2. **Authorization:** Customer enters their UPI PIN via Intent, Collect, or Dynamic QR → issuing bank places a lien on the requested amount.
3. **Capture:** Merchant calls the **Pre-Authorization Capture API** with the final execution amount (≤ blocked amount). The bank debits the customer and settles the money to the merchant.
4. **Void/Release:** If an order is cancelled or unfulfilled, the merchant calls the **Void API**, immediately releasing the lien back to the customer.

> **TDR Pricing Rule:** Transaction Discount Rate (TDR) is charged upon mandate creation success. Even if a mandate is voided without capture, creation cost pricing applies.

## 3. UPI Reserve Pay/ Single Block Multiple Debits (SBMD) 

