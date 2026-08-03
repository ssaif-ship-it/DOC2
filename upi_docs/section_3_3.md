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