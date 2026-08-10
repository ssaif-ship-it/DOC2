To comply with SEBI guidelines, onboarding investment category merchants such as Stock Brokers, Mutual Funds, Online Bond Platform Providers (OBPPs), and Investment Advisers/Research Analysts (IA/RAs) requires configuring standardized, exclusive Valid UPI Handles. All merchants in this category must be onboarded under **MCC 6211 (Security Brokers/Dealers)**.

A critical component of this onboarding is **Third-Party Validation (TPV)**. TPV ensures that payments are exclusively accepted from the investor's pre-registered bank account, reducing failed or non-compliant transactions.

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

<style>
  .onboarding-table-container {
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    margin: 20px 0;
    overflow-x: auto;
  }

  .onboarding-table {
    border-collapse: collapse;
    width: 100%;
    max-width: 900px;
    background-color: #ffffff;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
    border-radius: 8px;
    overflow: hidden;
  }

  .onboarding-table thead {
    background-color: #1a365d;
    color: #ffffff;
  }

  .onboarding-table th {
    text-align: left;
    padding: 16px 20px;
    font-size: 14px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .onboarding-table td {
    padding: 16px 20px;
    font-size: 14px;
    color: #2d3748;
    border-bottom: 1px solid #e2e8f0;
  }

  .onboarding-table tbody tr:nth-child(even) {
    background-color: #f7fafc;
  }

  .onboarding-table tbody tr:hover {
    background-color: #edf2f7;
    transition: background-color 0.2s ease;
  }

  .onboarding-table tbody tr:last-child td {
    border-bottom: none;
  }

  .intermediary-type {
    font-weight: 600;
    color: #1a202c;
  }

  /* Status Badges */
  .badge {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
    text-align: center;
    min-width: 30px;
  }

  .badge-positive {
    background-color: #c6f6d5;
    color: #22543d;
  }

  .badge-negative {
    background-color: #fed7d7;
    color: #742a2a;
  }
</style>

<div class="onboarding-table-container">
  <table class="onboarding-table">
    <thead>
      <tr>
        <th>Intermediary Type</th>
        <th>Beneficiary Account</th>
        <th>TPV Required</th>
        <th>Direct Settlement (DS)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td class="intermediary-type">Stock Brokers</td>
        <td>Broker's own designated bank account</td>
        <td><span class="badge badge-positive">Yes</span></td>
        <td><span class="badge badge-positive">ON</span></td>
      </tr>
      <tr>
        <td class="intermediary-type">Mutual Funds (MF)</td>
        <td>ICCL / NCCL Bank Accounts</td>
        <td><span class="badge badge-positive">Yes</span></td>
        <td><span class="badge badge-positive">ON</span></td>
      </tr>
      <tr>
        <td class="intermediary-type">OBPPs</td>
        <td>ICCL / NCCL Bank Accounts</td>
        <td><span class="badge badge-positive">Yes</span></td>
        <td><span class="badge badge-positive">ON</span></td>
      </tr>
      <tr>
        <td class="intermediary-type">IA / RA</td>
        <td>Cashfree Payments' Axis Escrow Account</td>
        <td><span class="badge badge-negative">No</span></td>
        <td><span class="badge badge-negative">OFF</span></td>
      </tr>
    </tbody>
  </table>
</div>

---

### Bank-Specific Procurement Workflows

The process for acquiring and mapping the Valid Handle varies depending on the chosen acquiring bank:

*   **Axis Bank (API-Based):** The most streamlined route. Handles are procured via internal API integration. The Banking Ops team uploads the specified DMO format file in Retool.

    > *Note: Terminals are created in a non-TPV state by default and must be manually updated to enable TPV.*

*   **HDFC Bank (File-Based by Cashfree):** A manual process. Cashfree Banking Ops prepares the required onboarding files (including a covering letter on letterhead) and submits them directly to the HDFC onboarding team. The Bank Ops team manually adds the credentials to the system once provided by HDFC.

*   **ICICI Bank (File-Based by Merchant):** The merchant is responsible for filling, signing, sealing, and submitting the UPI Onboarding Form directly to their ICICI point of contact (Mutual Funds must also get signatures from ICCL/NCCL). Once ICICI maps the VPA to Cashfree's parent MID, Bank Ops configures the credentials, ensuring the `isDMO` flag is set to `true`.
