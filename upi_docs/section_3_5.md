## 3.3 Investment Category Onboarding

To comply with SEBI guidelines, onboarding investment category merchants such as Stock Brokers, Mutual Funds, Online Bond Platform Providers (OBPPs), and Investment Advisers/Research Analysts (IA/RAs) requires configuring standardized, exclusive Valid UPI Handles. All merchants in this category must be onboarded under **MCC 6211 (Security Brokers/Dealers)**.

A critical component of this onboarding is **Third-Party Validation (TPV)**. TPV ensures that payments are exclusively accepted from the investor’s pre-registered bank account, reducing failed or non-compliant transactions.

*   **Standard TPV:** Supported by ICICI, YES, HDFC, and AXIS banks.
*   **Multibank TPV:** Allows merchants to pass up to 5 registered accounts per request, granting users flexibility. This is supported by ICICI and HDFC.
*   **Recurring Payments:** TPV is fully supported for UPI Mandates and OTMs.

---

### Valid Handle Formats

The format of the SEBI-mandated UPI handle depends on the transaction type. The suffix `cf` is used for standard handles, while `cfp` is required if the merchant needs AutoPay/subscription support.

*   **One-Time Payments:** `MerchantName.cf.brk@[bank_identifier]`
*   **UPI AutoPay:** `MerchantName.cfp.brk@[bank_identifier]`

---

### Beneficiary & Settlement Configuration

Properly configuring the beneficiary account and settlement flags is a strict compliance requirement. Failure to enable Direct Settlement (DS) where required will result in double settlement and financial loss.

| Intermediary Type | Beneficiary Account | TPV Required | Direct Settlement (DS) |
| :--- | :--- | :--- | :--- |
| **Stock Brokers** | Broker's own designated bank account | Yes | **ON** |
| **Mutual Funds (MF)** | ICCL / NCCL Bank Accounts | Yes | **ON** |
| **OBPPs** | ICCL / NCCL Bank Accounts | Yes | **ON** |
| **IA / RA** | Cashfree Payments' Axis Escrow Account | No | **OFF** |

---

### Bank-Specific Procurement Workflows

The process for acquiring and mapping the Valid Handle varies depending on the chosen acquiring bank:

*   **Axis Bank (API-Based):** The most streamlined route. Handles are procured via internal API integration. The Banking Ops team uploads the specified DMO format file in Retool. 
    > *Note: Terminals are created in a non-TPV state by default and must be manually updated to enable TPV.*
*   **HDFC Bank (File-Based by Cashfree):** A manual process. Cashfree Banking Ops prepares the required onboarding files (including a covering letter on letterhead) and submits them directly to the HDFC onboarding team. The Bank Ops team manually adds the credentials to the system once provided by HDFC.
*   **ICICI Bank (File-Based by Merchant):** The merchant is responsible for filling, signing, sealing, and submitting the UPI Onboarding Form directly to their ICICI point of contact (Mutual Funds must also get signatures from ICCL/NCCL). Once ICICI maps the VPA to Cashfree's parent MID, Bank Ops configures the credentials, ensuring the `isDMO` flag is set to `true`.