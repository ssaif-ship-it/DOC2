# 4.3 Single Block Multiple Debits (SBMD), UPI Reserve Pay & One-Time Mandates (OTM)

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

## 3. Single Block Multiple Debits (SBMD) / UPI Reserve Pay

SBMD is an extension of OTM. It allows a merchant to block a maximum ceiling amount once and execute multiple partial debits against that single block over time — until the funds are exhausted, revoked, or expired.

Unlike traditional AutoPay, where individual recurring debits can fail due to low balance, SBMD guarantees that every debit execution is backed by pre-reserved funds.

### SBMD Purpose Codes & Vertical Specifications

#### Purpose Code 76 — Secondary Market Trading

Designed specifically for equity, derivative, and commodity broking under MCC 6211.

- **Flagship Use Case:** Investors block funds in their bank account against the Clearing Corporation (CC). As trades are executed by the broker throughout the day, the CC debits the block to settle trade obligations.
- **Maximum Transaction Limit:** Exceptional cap of ₹5,00,000 per block (aligned with RBI-approved ASBA limits).
- **Mandate Initiation:** Payer-Initiated strictly (Intent, QR, SDK). Collect mode is strictly prohibited.
- **Mandate Operations:** `CREATE` and `REVOKE` only. `MODIFY` is not permitted.
- **Revocable Flag:** Must be set to `N` (Non-revocable by customer inside TPAP apps). Revocation can only be triggered via merchant/CC interfaces.
- **Transaction Reference (`tr`) Format:** Must strictly follow the hyphen-separated structure:

  ```text
  TMCODE-SEGMENTCODE-UCCCODE-brokerref
  ```

  e.g., `12345-123-1122334456-brokerref`, where TM Code is 5 digits, Segment Code is 3 digits, and UCC is 12 digits.

- **Funding Sources:** Savings Accounts, Current Accounts, Overdraft Accounts.

#### Purpose Code 77 — Online Goods & Services

Designed for general e-commerce, quick commerce, travel, and mobility platforms.

- **Use Cases:** Quick commerce, online food delivery, travel bookings, cab aggregators, EV charging stations, in-app wallets (without preloading), and Pay-on-Delivery.
- **Maximum Transaction Limit:** Block capped at standard network limits of ₹10,00,000 (or standard ₹1,00,000 P2M depending on tier).
- **Block Validity:** Up to 90 days.
- **Mandate Initiation:** Payer-initiated (Intent, QR, SDK) or Payee-initiated (Collect mode permitted).
- **Mandate Operations:** `CREATE`, `MODIFY`, `REVOKE`. Modification is allowed strictly for the amount field.
- **Funding Sources:** Savings Accounts, Current Accounts, Overdrafts, RuPay Credit Cards on UPI, and Pre-Sanctioned Credit Lines.

#### Purpose Codes 78 & 79

Reserved by NPCI for upcoming product extensions and industry verticals.

### SBMD Use Case Deep Dives

| Vertical | Example |
| :--- | :--- |
| **Secondary Markets** | Investor blocks ₹5L against CC; broker debits per trade. |
| **Quick Commerce** | User blocks ₹2,000; mini-orders debit without PIN re-entry. |
| **Travel Bookings** | User blocks ₹10,000; flight, hotel, and cab debit as booked. |
| **In-App Wallets** | Funds stay in customer's bank; debited only on usage. |

## 4. Consumer Branding: UPI Reserve Pay

**UPI Reserve Pay** is NPCI's official consumer-facing brand name for SBMD. While technical specifications, APIs, and switch routing use "SBMD", customer-facing interfaces inside TPAP apps (Google Pay, PhonePe, Paytm, CRED) display "UPI Reserve Pay".

**In-App Messaging Example:** *"UPI Reserve Pay mandate — ₹10,000 blocked for [Merchant Name]"*

> **Merchant UX Best Practice:** Use "UPI Reserve Pay" in checkout banners and tooltips to build consumer familiarity with fund-blocking mechanics.

## 5. End-to-End Lifecycle & Architecture

The SBMD lifecycle operates across three distinct phases, separating authorization from physical fund transfer:

```text
[ Phase 1: Block ]  ---> Customer approves PIN ---> Bank liens funds ---> Mandate Active
[ Phase 2: Debit ]  ---> Merchant sends ReqPay  ---> Bank lifts lien ---> Debits exact amount
[ Phase 3: Release] ---> Expiry / Revoke API    ---> Bank drops lien ---> Unused balance freed
```

### Phase 1: Block (Mandate Creation)

1. Customer initiates mandate creation via Intent, QR, SDK, or Collect (Purpose Code 77 only).
2. The issuing bank prompts the user for their 4-digit or 6-digit UPI PIN.
3. Upon PIN validation, the issuing bank places a lien on the requested amount.
4. The switch returns confirmation back to the merchant.

**Sample Intent deep link structure for SBMD:**

```text
upi://mandate?ver=01&pn=MerchantName&cu=INR&amrule=MAX&block=Y
&purpose=77&mc=5552&mode=13&recur=ASPRESENTED&am=10000.00
&orgid=000000&rev=N&share=N&tn=Description&validitystart=27072026
&validityend=25102026&pa=merchant@bank&tr=REFERENCE123&txnType=CREATE
```

- `block=Y` — Triggers account lien.
- `recur=ASPRESENTED` — Configures multi-debit capability.
- `purpose=76 / 77` — Enforces industry-specific rules and ceilings.
- `amrule=MAX` — Declares amount as a maximum cap.

### Phase 2: Debit (Execution)

1. Merchant issues a `ReqPay` execution API call referencing the Unique Mandate Number (UMN) and required debit amount (≤ remaining lien).
2. The remitter bank verifies the digital signature attached to the mandate.
3. The bank temporarily lifts the lien, debits the exact requested execution amount, and re-applies the lien to any remaining unused balance:

   ```text
   Remaining Balance = Original Block − Σ(Successful Debits)
   ```

> **Mandatory Execution Rule:** Member banks are strictly prohibited from declining SBMD execution requests. All eligibility and status checks must be completed during initial mandate creation.

> **Timeout & Retries (Retail 77):** If an execution times out, it is treated as an immediate decline and reversed in real-time. Merchants can retry execution up to 3 times in 24 hours.

### Phase 3: Release (Unblock / Revoke)

Unutilized funds are released back to the customer's available balance under three conditions:

1. **Mandate Expiration:** Mandate validity period lapses (e.g., 90 days for retail).
2. **Explicit Revocation:** Merchant issues a `ReqMandate` (`type=REVOKE`) call.
3. **Exhaustion:** The blocked funds reach a zero balance through execution.

> **Revocation Rule:** Customers cannot directly revoke SBMD mandates inside their UPI apps. Revocation must be initiated by the merchant on behalf of the customer.

## 6. Merchant Integration API Workflow

```text
[ 1. Create Order ] --> [ 2. Order Pay (sbmd: true) ] --> [ 3. PIN Block Auth ]
                                                                   |
                                                                   v
[ 6. Settlement ]   <-- [ 5. Capture Execution ]     <-- [ 4. Check Balance ]
```

1. **Create Order** (`POST /orders`): Initialize a standard order payload.
2. **Order Pay** (`POST /orders/{order_id}/pay`): Set `authorize_only: true`, pass authorization metadata (block amount, start/end dates), and set `sbmd: true`.
3. **Customer Authorization:** Customer approves the request via UPI PIN.
4. **Check Mandate Status:** Query active lien amount and remaining available balance via API.
5. **Capture / Execution:** Issue capture requests with the execution amount. Multiple captures can be executed against the same mandate reference.
6. **Void / Revoke:** Trigger the Void API to release remaining blocked funds and terminate the mandate.

## 7. Edge Cases & Operational Guardrails

- **Deemed / Timeout Mandate Creation:** If mandate creation succeeds at the bank but times out at the gateway, funds may be locked while showing `USER_DROPPED` at the merchant end. Merchants should poll mandate status before triggering fresh creation requests, and enforce auto-void scripts on expired pending mandates.
- **Multiple Captures on Legacy OMS:** Standard e-commerce systems often assume a 1:1 relationship between orders and payments. Integrating SBMD requires updating internal ledgers to track multiple execution IDs and settlement events against a single initial parent order ID.
- **VPA Formatting Errors:** Ensure strict VPA syntax validation before triggering Collect mandates to prevent upstream switch rejections (`PAYER_PSP_NOT_REGISTERED`).
- **Refund Handling:** Refunds can only be executed on captured/debited funds. To return locked, un-captured money, use the Void/Revoke API, not the Refund API.

## 8. Go-Live & Onboarding Checklist

- [ ] **MID & MCC Configuration:** Confirm your MCC matches the purpose code (6211 for Purpose Code 76; relevant retail MCCs for 77). Obtain a dedicated SBMD-enabled Merchant ID (MID).
- [ ] **Integration Testing:**
  - [ ] Verify successful mandate block creation.
  - [ ] Execute full single capture (execution = block).
  - [ ] Execute partial multiple captures (exec₁ + exec₂ < block).
  - [ ] Validate that execution exceeding remaining lien is rejected.
  - [ ] Execute Void/Revoke API and confirm instant lien release.
- [ ] **Reconciliation & Webhook Handlers:** Subscribe to `MANDATE_CREATED`, `EXECUTION_SUCCESS`, `EXECUTION_FAILED`, and `MANDATE_REVOKED` webhooks.
- [ ] **Customer Communication:** Ensure checkout screens explicitly inform users that funds will be reserved in their account and debited upon fulfillment.