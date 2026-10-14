To maintain the security of the payment ecosystem and mitigate fraud, the National Payments Corporation of India (NPCI) and participating banks enforce strict transaction and velocity limits on the UPI network.

As a merchant, you need to understand both the baseline network limits and your specific Merchant Category Code (MCC) limits. Attempting to collect amounts above these thresholds, or using restricted payment flows, will result in immediate technical declines.

### Standard & MCC-Specific Limits

By default, the standard retail limit for a P2M (Person-to-Merchant) transaction is **₹1 Lakh**. However, the NPCI recognizes that certain critical industries require higher ceilings. High-risk categories also face flow restrictions, covered in the constraints below.

The table below is your master reference for per transaction limits, based on your merchant category:

<div class="upi-table-wrapper" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #222; max-width: 100%; margin: 20px 0;">
  <style>
    .upi-limits-table {
      width: 100%;
      border-collapse: collapse;
      text-align: left;
      font-size: 14px;
      line-height: 1.5;
    }
    .upi-limits-table th,
    .upi-limits-table td {
      padding: 12px 14px;
      border-bottom: 1px solid #e0e0e0;
      vertical-align: middle;
    }
    .upi-limits-table th {
      background-color: #f5f7fa;
      color: #333;
      font-weight: 600;
      border-bottom: 2px solid #ccc;
    }
    .upi-limits-table tr:hover {
      background-color: #f9fbfd;
    }
    .mcc-code {
      font-family: SFMono-Regular, Consolas, 'Liberation Mono', Menlo, monospace;
      font-size: 13px;
      color: #444;
    }
    .tier-badge {
      font-weight: 600;
      color: #1a73e8;
    }
    .limit-amount {
      font-weight: 700;
      color: #0f9d58;
      white-space: nowrap;
    }
  </style>

  <table class="upi-limits-table">
    <thead>
      <tr>
        <th>Limit Tier</th>
        <th>Sector / Category</th>
        <th>Covered Services</th>
        <th>Associated MCC Codes</th>
        <th>Per Transaction Limit</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td rowspan="4" class="tier-badge">High Ceiling Tier</td>
        <td><strong>Medical &amp; Healthcare</strong></td>
        <td>Hospitals, Doctors, Dentists, Labs, Nursing, Optometrists, Vets</td>
        <td class="mcc-code">0742, 8011, 8021, 8031, 8041, 8042, 8049, 8050, 8062, 8071, 8099</td>
        <td class="limit-amount">₹500,000</td>
      </tr>
      <tr>
        <td><strong>Education</strong></td>
        <td>Schools, Colleges, Universities, Vocational, Business, Services</td>
        <td class="mcc-code">8211, 8220, 8241, 8244, 8249, 8299</td>
        <td class="limit-amount">₹500,000</td>
      </tr>
      <tr>
        <td><strong>Financial &amp; Insurance</strong></td>
        <td>Credit Cards, Insurance, Securities, LIC, Digital Banking (excluding savings and current account opening), Debt Collection</td>
        <td class="mcc-code">5413, 5960, 6012, 6211, 6300, 6529, 7322, 7410</td>
        <td class="limit-amount">₹500,000</td>
      </tr>
      <tr>
        <td><strong>Government &amp; Travel</strong></td>
        <td>Taxes, Travel Agencies, Tour Operators</td>
        <td class="mcc-code">4722, 9311</td>
        <td class="limit-amount">₹500,000</td>
      </tr>
      <tr>
        <td class="tier-badge">Intermediate Tier</td>
        <td><strong>Retail Luxury &amp; KYC</strong></td>
        <td>Jewellery, Watches, Silverware, Digital Account Opening</td>
        <td class="mcc-code">5944, 7409</td>
        <td class="limit-amount">₹200,000</td>
      </tr>
      <tr>
        <td class="tier-badge">Standard Baseline</td>
        <td><strong>General Retail &amp; P2P</strong></td>
        <td>P2P Transfers, Grocery, E-Commerce, Dining, Utilities, All Unspecified</td>
        <td class="mcc-code">P2P, RETAIL, ECOM, FOOD, UTIL, ALL</td>
        <td class="limit-amount">₹100,000</td>
      </tr>
    </tbody>
  </table>
</div>

These are per transaction limits. For some categories NPCI also sets a cumulative cap over any 24 hours, which your customer's issuing bank enforces:

* **₹10,00,000:** capital markets (6211), insurance (5960, 6300, 6529), travel (4722), debt collection (7322), and government e-marketplace earnest money deposit payments (9311).
* **₹6,00,000:** credit card bill payments (5413) and jewellery (5944).
* **₹5,00,000:** digital account opening for term deposits (7410).
* **₹2,00,000:** digital account opening, initial funding (7409).

The higher limits for these categories, and for tax payments (9311), apply only to merchants classified as Verified Merchants. If you are unsure whether your business qualifies, contact your Cashfree account manager.

<!--
Claude, updated for Saif (14 Oct): three changes here, per the verified MCC Limits sheet and the NPCI circular OC 185B (NPCI/UPI/2025-26/OC/185B, 28 August 2025, Annexure I, primary PDF read).
1. The column and intro line said Daily. The amounts in the table are per transaction limits. The cumulative 24 hour caps are separate and are listed in the note above, taken from Annexure I.
2. The Verified Merchant condition is condition 1 of OC 185B, and OC 185A applies it to tax payments (9311). Its definition sits in OC 100/2020-21, OC 163/2022-23, OC 163A/2023-24 and OC 190/2023-24, which have not been read, so the text above does not define it.
3. 7410 is described in the sheet as Digital banking related services (excluding CASA account opening), so the Covered Services cell no longer says plain Banking.
Left out on purpose: MCC 6012. OC 185B grants it the higher limit and a 5,00,000 cumulative cap only for FX retail through BBPS with purpose code BF or 01, while the sheet and the table list 6012 flat at 5,00,000. Decide whether to qualify it before adding it to the cumulative list. No cumulative cap is stated anywhere for the healthcare and education codes, so none is shown.
-->

  <div class="upi-constraints" style="margin-top: 24px; padding: 16px; background-color: #f8f9fa; border-left: 4px solid #1a73e8; border-radius: 0 4px 4px 0;">
    <h4 style="margin: 0 0 10px 0; font-size: 16px; color: #1a73e8;">Key Merchant &amp; User Velocity Constraints</h4>
    <ul style="margin: 0; padding-left: 20px; font-size: 14px;">
      <li style="margin-bottom: 8px;"><strong>24-Hour Security Cap:</strong> A major account state change, first-time registration, device binding to a new phone, an app reinstall, or a UPI PIN reset, triggers a cooling-off period to prevent account takeover fraud. The baseline is a cap of <strong>₹5,000</strong>, applied as both the per-transaction limit and the cumulative daily limit, for the first 24 hours. This is a floor, not a ceiling: individual banks and apps can apply stricter conditions on top of it, including a longer cooling-off window.</li>
<!-- Claude, updated for Saif: you added a line saying most other major banks follow the standard 24 hour cap regardless of OS, and asked if that is correct. It is not well supported by what I found. SBI's own page states a 5 day window for iOS, not 24 hours, and HDFC's page, via a Razorpay summary, states 72 hours for iOS, a different duration but still an OS split. Only Google Pay's page skips mentioning an OS difference, but it also does not say there is none. That is a mixed picture, not a clean confirmation that most banks skip the split, so I dropped that line rather than publish a claim the evidence does not back, and reframed the whole bullet as a floor that banks and apps can be stricter on top of, per your earlier instruction. I also could not find an NPCI circular establishing this 5,000 rupee, 24 hour figure as a universal rule, it is a widely cited industry baseline rather than a confirmed NPCI rule. -->
      <li style="margin-bottom: 8px;"><strong>Flow Restrictions:</strong> Collect and QR are both blocked for wallet loading (MCC 6540), real money gaming (MCC 5816), and real estate agents and managers (MCC 6513), restricting those categories to Intent only. Collect alone is blocked for credit card bill payments (MCC 5413), digital gold (MCC 5412), and MCC 7016.</li>
      <li style="margin-bottom: 8px;"><strong>Bank-Level Overrides:</strong> Remitter banks reserve authority to apply lower internal spending limits (e.g., ₹50,000 daily) regardless of category cap allowance.</li>
    </ul>
  </div>
