# 1.3 Standards & Onboarding Requirements

To maintain the integrity of the UPI ecosystem and comply with RBI and NPCI guidelines, strict standards dictate how merchants are classified, verified, and permitted to transact. These onboarding guardrails are not mere formalities; they directly dictate your transaction limits, allowed payment flows, and settlement cycles.

### Merchant Category Code (MCC) Assignments

Every merchant onboarded to accept UPI payments must be assigned a **Merchant Category Code (MCC)**. This 4-digit number classifies the primary type of goods or services provided.

The MCC dictates the fundamental rules of engagement for your UPI integration:

* **Transaction Limits:** Standard P2M transactions are capped at ₹1 Lakh. However, specific MCCs (like `6211` for Capital Markets or `8099` for Education) are granted exceptions allowing up to ₹5 Lakhs per transaction.
* **Permitted Payment Instruments:** Certain MCCs are blocked from accepting UPI payments funded by Credit Cards or Prepaid Wallets (PPIs) due to risk profiles or interchange fee constraints.
* **AutoPay Limits:** The maximum threshold for auto-debit without an additional PIN (AFA) varies by MCC (e.g., standard is ₹15,000, but mutual funds/insurance can be up to ₹1 Lakh).

> **Note:** It is critical to accurately declare your business operations during onboarding to ensure the correct MCC is assigned.

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