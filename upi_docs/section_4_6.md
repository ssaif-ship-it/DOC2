# 4.6 UPI Global & Reserve Pay

As the Unified Payments Interface (UPI) expands beyond domestic instant transfers, two key extensions enable merchants and users to handle cross-border payments and pre-authorized reserved balances: UPI Global and UPI Reserve Pay.

---

## 1. UPI Global (Cross-Border Transactions)

UPI Global, managed by NPCI International Payments Limited (NIPL), extends UPI infrastructure to international markets. It operates across two primary models: Outbound Payments (Indian travelers paying abroad) and Inbound Payments (NRIs and international visitors paying Indian merchants).

### A. Inbound Merchant Acceptance (NRI & International Numbers)
Merchants processing payments in India can accept UPI payments from Non-Resident Indians (NRIs) and Persons of Indian Origin (PIOs) holding NRE (Non-Resident External) or NRO (Non-Resident Ordinary) accounts linked to foreign mobile numbers.

*   **Supported Country Codes:** United States (+1), Canada (+1), United Kingdom (+44), United Arab Emirates (+971), Singapore (+65), Australia (+61), Saudi Arabia (+966), Oman (+968), Qatar (+974), Hong Kong (+852).
*   **SIM Binding Rule:** Unlike domestic users who require an active Indian (+91) SIM, international users undergo strict international SIM binding with their remitting bank's mobile banking application.
*   **Merchant Impact:** No separate API or QR integration is required. Standard Cashfree Dynamic QRs and Intent links natively accept payments from linked international handles provided the acquiring bank supports international NRE/NRO routing.

### B. Outbound Cross-Border QR Payments
Indian travelers using domestic UPI apps (Google Pay, PhonePe, Paytm, BHIM) can scan localized QR codes at international merchant establishments.

*   **Partner Networks:** Liquid Group & SGQR (Singapore), PayNet (Malaysia), PromptPay (Thailand), NeOPAY (UAE), NCM (Nepal), Bhutan, France (Eiffel Tower & select merchants), Sri Lanka, and Mauritius.

**Transaction Flow & FX Conversion:**
1.  Customer scans foreign QR using their Indian UPI App.
2.  The UPI Switch queries NIPL's FX engine in real time to fetch the live exchange rate.
3.  The UPI app displays the localized foreign currency amount alongside the exact equivalent in Indian Rupees (INR).
4.  The customer enters their standard UPI PIN.
5.  The remitting bank debits the customer's account in INR, while NIPL settles the local foreign currency to the acquiring overseas entity.

---

## 2. UPI Reserve Pay (Pre-Authorization & Lien Framework)

UPI Reserve Pay is NPCI's standardized umbrella solution for fund reservation (pre-authorization) across e-commerce, travel, ride-hailing, and financial markets. It unifies One-Time Mandates (OTM) and Single Block Multiple Debits (SBMD) into a unified checkout architecture.

### Key Mechanics of UPI Reserve Pay
Instead of deducting money immediately during checkout, UPI Reserve Pay places a lien (hold) on the requested funds directly inside the customer's savings or current bank account.

```text
+-------------------+      1. Reserve Request (Lien)      +-------------------+
|  Customer Account |  =================================> | Merchant / App    |
|  (Funds Locked)   |                                     | (Fulfillment)     |
+-------------------+      2. Executed Debit (Partial/Full)+-------------------+
        ||                                                         ||
        \/                                                         \/
   Unused Balance Released automatically upon expiration or explicit Revoke API call
