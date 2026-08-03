To maintain the security of the payment ecosystem and mitigate fraud, the National Payments Corporation of India (NPCI) and participating banks enforce strict transaction and velocity limits on the UPI network.

As a merchant, it is crucial to understand both the baseline network limits and your specific Merchant Category Code (MCC) limits. Attempting to collect amounts above these thresholds—or using restricted payment flows—will result in immediate technical declines.

### 1. The 24-Hour New User Velocity Rule (Anti-Fraud)

One of the most common reasons for unexpected payment failures on high-value orders is the NPCI's 24-hour cooling-off period. To prevent account takeover fraud, the NPCI heavily restricts transaction capabilities when a user's UPI profile undergoes a major state change (e.g., first-time registration, device binding/new phone, or UPI PIN reset).

**The Restriction:** For the first **24 hours** following any of these triggers, the user's UPI transaction limit is strictly capped at **₹5,000**. Normal limits are automatically restored after the 24-hour window expires.

### 2. Standard & MCC-Specific Limits

By default, the standard retail limit for a P2M (Person-to-Merchant) transaction is **₹1 Lakh**. However, the NPCI recognizes that certain critical industries require higher ceilings, while high-risk categories face strict flow limitations (such as completely blocking "pull"/Collect requests).

The table below acts as your master reference for daily transaction limits and flow blocks enforced by the NPCI switch, based on your merchant category:

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
    .upi-constraints {
      margin-top: 24px;
      padding: 16px;
      background-color: #f8f9fa;
      border-left: 4px solid #1a73e8;
      border-radius: 0 4px 4px 0;
    }
    .upi-constraints h4 {
      margin: 0 0 10px 0;
      font-size: 16px;
      color: #1a73e8;
    }
    .upi-constraints ul {
      margin: 0;
      padding-left: 20px;
      font-size: 14px;
    }
    .upi-constraints li {
      margin-bottom: 8px;
    }
    .upi-constraints li:last-child {
      margin-bottom: 0;
    }
  </style>

  <table class="upi-limits-table">
    <thead>
      <tr>
        <th>Limit Tier</th>
        <th>Sector / Category</th>
        <th>Covered Services</th>
        <th>Associated MCC Codes</th>
        <th>Daily Limit</th>
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
        <td>Credit Cards, Insurance, Securities, LIC, Banking, Debt Collection</td>
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

  <div class="upi-constraints">
    <h4>Key Merchant &amp; User Velocity Constraints</h4>
    <ul>
      <li><strong>24-Hour Security Cap:</strong> Profile updates (new registration, device binding, or UPI PIN reset) cap transactions at <strong>₹5,000 total</strong> for the first 24 hours.</li>
      <li><strong>Volume Cap:</strong> Standard Default merchants (₹100k tier) are subject to a maximum <strong>20 transactions daily</strong> per rolling 24 hours.</li>
      <li><strong>Bank-Level Overrides:</strong> Remitter banks reserve authority to apply lower internal spending limits (e.g., ₹50,000 daily) regardless of category cap allowance.</li>
    </ul>
  </div>
</div>

> **Note:** The Standard Default tier is additionally subject to a 20-transaction daily limit per rolling 24 hours, and the ₹5,000 new-user cap described above still applies within its 24-hour window regardless of MCC.

> **Note:** While the NPCI sets the maximum ceilings above, individual **Remitter Banks** reserve the right to set *lower* internal limits based on their own risk policies (e.g., a specific bank might cap daily UPI spends at ₹50,000 regardless of your MCC).