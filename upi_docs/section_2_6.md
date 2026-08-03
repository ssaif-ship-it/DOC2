# Standards & Onboarding Requirements


To maintain the integrity of the UPI ecosystem and comply with RBI and NPCI guidelines, strict standards dictate how merchants are classified, verified, and permitted to transact. These onboarding guardrails are not mere formalities; they directly dictate your transaction limits, allowed payment flows, and settlement cycles.

### Merchant Category Code (MCC) Assignments

Every merchant onboarded to accept UPI payments must be assigned a **Merchant Category Code (MCC)**. This 4-digit number classifies the primary type of goods or services provided.

The MCC dictates the fundamental rules of engagement for your UPI integration:

* **Transaction Limits:** Standard P2M transactions are capped at ₹1 Lakh. However, specific MCCs (like `6211` for Capital Markets or `8099` for Education) are granted exceptions allowing up to ₹5 Lakhs per transaction.
* **Permitted Payment Instruments:** Certain MCCs are blocked from accepting UPI payments funded by Credit Cards or Prepaid Wallets (PPIs) due to risk profiles or interchange fee constraints.
* **AutoPay Limits:** The maximum threshold for auto-debit without an additional PIN (AFA) varies by MCC (e.g., standard is ₹15,000, but mutual funds/insurance can be up to ₹1 Lakh).

> **Note:** It is critical to accurately declare your business operations during onboarding to ensure the correct MCC is assigned.

> **Note:** More details about MCC in 3.2

### Third-Party Verification (TPV)

Third-Party Verification (TPV) is a stringent compliance requirement designed to ensure that funds deposited into an investment account originate *only* from a bank account pre-registered and verified against that specific investor's profile.

* **Applicability:** TPV is heavily enforced for Capital Markets, Broking, and Mutual Funds (primarily **MCC 6211** and **6012**).

**How it Works in UPI:**

1. **Initiation:** When the merchant creates the UPI payment request, they must pass the verified customer's bank account number and IFSC code in the payload.
2. **Validation:** Before presenting the PIN screen, the Payer PSP queries the Remitter Bank to verify the underlying account details.
3. **Enforcement:** If the user attempts to pay using a UPI ID linked to a non-registered bank account (e.g., paying from a spouse's account), the transaction is blocked at the bank level, failing with a specific TPV error code (e.g., `U19`).

### SEBI Valid Handles (Capital Markets Mandatory Requirement)

In a major move to combat impersonation fraud in the securities market, the Securities and Exchange Board of India (SEBI) mandated the use of standardized, validated UPI handles for all registered intermediaries (brokers, mutual funds, portfolio managers) effective **October 1, 2025**.

If you operate in the Capital Markets space (MCC 6211), you must comply with the `@valid` handle framework.

**Key Features of SEBI Valid Handles:**

* **Standardized Structure:** Your UPI ID must follow the structure: `[custom_prefix].[intermediary_type]@valid[bank_name]`.
  * *Example (Broker):* `groww.brk@validhdfc`
  * *Example (Mutual Fund):* `nippon.mf@validicici`
* **Exclusive Designation:** The `@valid` suffix is restricted exclusively to SEBI-registered intermediaries operating under MCC 6211. It cannot be issued to any other merchant type.
* **Visual Trust Indicators:** When a retail investor initiates a payment to a `@valid` handle, their UPI App will natively display a distinctive "thumbs-up inside a green triangle" icon.
* **SEBI Check Verification:** Investors can independently verify your `@valid` handle through the "SEBI Check" tool on the SEBI portal or Saarthi app before transferring funds.

> **Warning:** Merchants attempting to collect capital market investments without transitioning to the `@valid` infrastructure face regulatory action and blocked payment flows.

# UPI Payment Products & Merchant Onboarding Guide

A complete reference for choosing the right UPI payment product and getting a Cashfree merchant account from signup to go-live.

---

## Product Comparison at a Glance

<div class="upi-product-table" style="overflow-x:auto; border:1px solid #E5E7EB; border-radius:0.5rem; box-shadow:0 1px 2px rgba(0,0,0,0.05); margin:1.5rem 0;">
<style>
.upi-product-table table { width:100%; font-size:14px; text-align:left; border-collapse:collapse; }
.upi-product-table thead th { background:#F4F0FA; color:#5A28A3; font-weight:600; padding:12px 16px; }
.upi-product-table tbody td { padding:12px 16px; border-top:1px solid #E5E7EB; color:#4B5563; }
.upi-product-table tbody tr:hover td { background:#F9FAFB; }
.upi-product-table .badge { display:inline-block; padding:2px 10px; border-radius:9999px; font-size:12px; font-weight:500; }
</style>
<table>
  <thead>
    <tr>
      <th>Product</th>
      <th>Best for</th>
      <th>Integration effort</th>
      <th>Customer action</th>
      <th>Where</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="font-weight:600;color:#111827;">UPI Intent</td>
      <td>Mobile app/web checkout</td>
      <td><span class="badge" style="background:#EFF6FF;color:#1D4ED8;">Low (API)</span></td>
      <td>Tap app → PIN</td>
      <td><span class="badge" style="background:#EEF2FF;color:#4338CA;">Online</span></td>
    </tr>
    <tr>
      <td style="font-weight:600;color:#111827;">UPI Collect</td>
      <td>Desktop web, known VPA</td>
      <td><span class="badge" style="background:#EFF6FF;color:#1D4ED8;">Low (API)</span></td>
      <td>Type VPA → approve in app</td>
      <td><span class="badge" style="background:#EEF2FF;color:#4338CA;">Online</span></td>
    </tr>
    <tr>
      <td style="font-weight:600;color:#111827;">Flash UPI</td>
      <td>High-volume repeat apps</td>
      <td><span class="badge" style="background:#FFFBEB;color:#B45309;">Medium (SDK)</span></td>
      <td>PIN only (no app switch)</td>
      <td><span class="badge" style="background:#EEF2FF;color:#4338CA;">Online (in-app)</span></td>
    </tr>
    <tr>
      <td style="font-weight:600;color:#111827;">Static QR</td>
      <td>Physical stores, no-tech</td>
      <td><span class="badge" style="background:#F0FDF4;color:#15803D;">Zero (print QR)</span></td>
      <td>Scan → type amount → PIN</td>
      <td><span class="badge" style="background:#F3F4F6;color:#374151;">Offline</span></td>
    </tr>
    <tr>
      <td style="font-weight:600;color:#111827;">Dynamic QR</td>
      <td>Delivery, desktop, invoices</td>
      <td><span class="badge" style="background:#FFFBEB;color:#B45309;">Medium (API)</span></td>
      <td>Scan → PIN (amount pre-filled)</td>
      <td><span class="badge" style="background:#F0FDFA;color:#0F766E;">Offline/Online</span></td>
    </tr>
    <tr>
      <td style="font-weight:600;color:#111827;">SoftPOS</td>
      <td>Field agents, delivery, retail</td>
      <td><span class="badge" style="background:#EFF6FF;color:#1D4ED8;">Low (app install)</span></td>
      <td>Scan QR / Tap card / Pay link</td>
      <td><span class="badge" style="background:#F3F4F6;color:#374151;">Offline</span></td>
    </tr>
  </tbody>
</table>
</div>




