The NPCI has launched EMI on UPI using the Contextual Payments Framework. This feature enables eligible merchants to offer real-time EMI options for customers paying via RuPay Credit Cards on standard UPI QR codes and Intent links.

By providing instant EMI capabilities natively at checkout, merchants address cart abandonment, lower barriers for high-ticket purchases, and leverage marketing and funding support driven by NPCI.

---

## 1. Context, Market Opportunity & Strategic Objectives

Across ~3,498 merchants currently processing transactions from RuPay credit card users, Cashfree has identified an immediate target pool of ~495 eligible merchants, representing a potential GMV of ₹126M+ with an average order value (AOV) exceeding ₹3,000.

**Business Impact & Value Proposition:**
*   **Conversion Uplift:** Presenting flexible affordability options directly on product pages and checkouts increases conversion rates by 30% and reduces customer drop-offs by 30%.
*   **Higher AOV:** Customers are empowered to purchase higher ticket-size items, driving a 40% to 60% increase in Average Order Value.
*   **Zero Merchant Risk:** Upfront settlement guarantees the merchant receives the full transaction amount (less subvention discount where applicable), while the issuing bank bears the repayment risk.

### Key Success Metrics

| Goal Category | Key Performance Indicator (KPI) | Target Benchmark |
| :--- | :--- | :--- |
| **Expand Feature Reach** | Number of active merchants enabled with `upi_cc_emi` | Target eligible merchant pool |
| **Drive Merchant Adoption** | Average number of EMI offers created per merchant / month | Increase offer creation rate |
| **Drive Consumer Usage** | Average EMI amount availed per merchant / month | GMV growth in orders >₹3,000 |
| **Improve User Visibility** | Percentage of QR scans where EMI options are displayed | Maximize eligible RuPay scans |

---

## 2. Operational Scope & Phase 1 Constraints

To ensure switch stability and comply with initial NPCI rollout guidelines, Phase 1 operates under the following scope constraints:

*   **Supported Issuing Banks (Phase 1):** Real-time Contextual EMI is strictly supported for **SBI RuPay Credit Cards** and **HDFC RuPay Credit Cards**.
*   **Offer Combination Limits:** Combining flat discounts with EMI offers (e.g., ₹5,000 flat discount + No-Cost EMI) is not supported in Phase 1.
*   **Product SKU Filtering (`prodCode`):** Specific product-level SKU validation (`prodCode`) is bypassed at the switch level initially; all cart items are treated as EMI-eligible by default.
*   **Third-Party App Rendering:** Rendering of the EMI selection screens on user devices depends on support within individual UPI PSP apps (Google Pay, PhonePe, Paytm, CRED).

**Flow Restrictions (Strict Enforcement):**
*   ❌ **Collect Requests:** Contextual EMI is strictly prohibited for Collect requests.
*   ✅ **Supported Flow Types:** Enabled exclusively for UPI Intent Links and Dynamic QR Codes.

---

## 3. Contextual Payment Protocol & Technical API Flow

Contextual payment routing enables real-time negotiation between the Payer PSP app, NPCI Switch, and the Cashfree Acquirer Switch.

> *(Insert Technical Flow Architecture Diagram / Sequence Image Here)*

### Step-by-Step API Execution Sequence

**1. Payload & Link Generation (Merchant / Cashfree PG):**
*   Enable the new payment method tag: `upi_cc_emi`.
*   The generated Intent URL or Dynamic QR code appends the contextual metadata flag: `ctxtCode: "03"` (or `"C03"` designated for EMI).
*   Optional payload parameter: `prodCode` (Unique product identifier reserved for SKU-level filtering in future phases).

**2. Handling `ReqGetContext` API (Acquirer Switch):**
*   When a customer scans the QR or triggers the Intent deep link, the Payer PSP sends a `ReqGetContext` call via NPCI to Cashfree.
*   To maintain sub-10ms response times, Cashfree's low-latency switch validates:
    *   Merchant enablement and active configurations.
    *   Card BIN eligibility against supported issuers (SBI, HDFC).
    *   Configured EMI plans (e.g., 3, 6, 9, 12, 18 months) replicated at the switch level.
*   Cashfree responds with `RespGetContext` containing index-wise EMI plan breakdowns and subvention details.

**3. Validation of `ReqAuthDetails`:**
*   When the customer selects an EMI plan and enters their UPI PIN, Cashfree receives `ReqAuthDetails`.
*   Cashfree validates that:
    *   `ctxtCode` equals `"03"`.
    *   `offerId` is valid for the specific user, product amount, and card BIN.
*   Cashfree responds with `RespAuthDetails` authorizing execution upon successful verification.

---

## 4. Affordability Engine & Subvention Calculations

Merchants can configure both No-Cost EMI and Low-Cost EMI structures via the Cashfree Dashboard or API.

### Mechanics of No-Cost EMI
In a No-Cost EMI model, the customer pays only the product sticker price ($A$), split equally over $N$ months. The merchant absorbs the interest by offering an upfront discount equivalent to the total interest charged by the bank.

### Mathematical Amortization & Settlement Model
The monthly installment ($EMI$) paid by the customer is calculated using the standard amortized equation:

$$EMI = \frac{P \times R \times (1+R)^N}{(1+R)^N - 1}$$

Where:
*   $A$ = Order Amount / Product Sticker Price (paid by customer)
*   $P$ = Adjusted Base Principal (settled upfront to merchant)
*   $R$ = Monthly Interest Rate charged by issuing bank ($\text{Annual Rate} / 12 / 100$)
*   $N$ = Repayment Tenure in months
*   $EMI$ = Monthly Installment Amount, where $EMI = \frac{A}{N}$ for No-Cost EMI

Solving for the net Principal amount ($P$):

$$P = \frac{EMI \times [(1+R)^N - 1]}{R \times (1+R)^N}$$

### Standard Calculation Example: ₹10,000 Order on a 3-Month No-Cost EMI at 16% p.a. Bank Interest

| Parameter | Symbol / Formula | Numerical Value | Description |
| :--- | :--- | :--- | :--- |
| **Order Amount (Sticker Price)** | $A$ | ₹10,000 | Total amount paid by customer over $N$ months |
| **Tenure** | $N$ | 3 Months | Chosen repayment duration |
| **Bank Interest Rate** | $Annual\ R$ | 16% p.a. | Bank's credit card interest rate |
| **Monthly EMI Amount** | $EMI = A / N$ | ₹3,333 | Fixed monthly amount paid by customer |
| **Adjusted Principal Base** | $P$ | ₹9,739 | Calculated base amount using formula above |
| **Merchant Subvention Discount** | $A - P$ | ₹261 | Upfront discount absorbed by merchant |
| **Subvention Percentage** | `%` | 2.61% | Total subvention percentage cost to merchant |
| **Processing Fee** | `-` | ₹199 | One-time charge levied by issuing bank to user |
| **Upfront Settlement Amount** | $Net$ | ₹9,739 | Amount settled to merchant ($A - \text{Discount}$) |

### Low-Cost EMI Setup
For Low-Cost EMI, the merchant specifies a capped interest subvention percentage (partial interest discount), and the customer pays the remaining balance interest.

---

## 5. Integration Journeys & Touchpoints

### A. Merchant Dashboard Journey
1.  Log in to Cashfree Merchant Dashboard.
2.  Go to **Offers & Affordability > Create Offer**.
3.  Select Offer Type: **RuPay Credit Card EMI**.
4.  Select Issuing Banks: **SBI** and **HDFC**.
5.  Set tenure rules (3, 6, 9, 12, 18 months) and subvention type (No-Cost or Low-Cost).
6.  Save and enable the RuPay UPI Contextual Flag. Rule configurations are instantly replicated to the switch engine.

### B. API Integration Touchpoints
*   **Create Offer API:** Send `offer_type: "EMI"` with `payment_methods: ["upi_cc_emi"]` and bank subvention rules.
*   **Order Creation API:** Request contextual Intent link / QR by specifying `payment_method: "upi_cc_emi"`. The API attaches the context payload automatically:

```json
{
  "order_id": "order_99887766",
  "order_amount": 10000.00,
  "order_currency": "INR",
  "payment_method": {
    "upi": {
      "channel": "intent",
      "ctxtCode": "03",
      "prodCode": "SKU-44321"
    }
  }
}