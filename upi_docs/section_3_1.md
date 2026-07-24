# 3.1 Transaction Limits & MCC Caps

To maintain the security of the payment ecosystem and mitigate fraud, the National Payments Corporation of India (NPCI) and participating banks enforce strict transaction and velocity limits on the UPI network.

As a merchant, it is crucial to understand both the baseline network limits and your specific Merchant Category Code (MCC) limits. Attempting to collect amounts above these thresholds—or using restricted payment flows—will result in immediate technical declines.

### 1. The 24-Hour New User Velocity Rule (Anti-Fraud)

One of the most common reasons for unexpected payment failures on high-value orders is the NPCI's 24-hour cooling-off period. To prevent account takeover fraud, the NPCI heavily restricts transaction capabilities when a user's UPI profile undergoes a major state change (e.g., first-time registration, device binding/new phone, or UPI PIN reset).

**The Restriction:** For the first **24 hours** following any of these triggers, the user's UPI transaction limit is strictly capped at **₹5,000**. Normal limits are automatically restored after the 24-hour window expires.

### 2. Standard & MCC-Specific Limits

By default, the standard retail limit for a P2M (Person-to-Merchant) transaction is **₹1 Lakh**. However, the NPCI recognizes that certain critical industries require higher ceilings, while high-risk categories face strict flow limitations (such as completely blocking "pull"/Collect requests).

The table below acts as your master reference for daily transaction limits and flow blocks enforced by the NPCI switch, based on your merchant category:

<div class="overflow-x-auto my-6">
  <table class="w-full text-sm text-left border-collapse border border-gray-200">
    <thead class="text-xs text-gray-700 uppercase bg-gray-50">
      <tr>
        <th class="px-6 py-3 border border-gray-200 bg-gray-100">Merchant Categories</th>
        <th class="px-6 py-3 border border-gray-200 bg-[#E6F4EA] text-[#004D40]">Transaction Daily Limits (₹)</th>
      </tr>
    </thead>
    <tbody>
      <tr class="bg-white border-b hover:bg-gray-50">
        <td class="px-6 py-4 font-medium text-gray-900 border border-gray-200">P2M Transactions</td>
        <td class="px-6 py-4 border border-gray-200">1,00,000</td>
      </tr>
      <tr class="bg-gray-50 border-b hover:bg-gray-100">
        <td class="px-6 py-4 font-medium text-gray-900 border border-gray-200">BFSI</td>
        <td class="px-6 py-4 border border-gray-200">2,00,000</td>
      </tr>
      <tr class="bg-white border-b hover:bg-gray-50">
        <td class="px-6 py-4 font-medium text-gray-900 border border-gray-200">Non-verified merchants</td>
        <td class="px-6 py-4 border border-gray-200">Collect payments up to 2,000</td>
      </tr>
      <tr class="bg-gray-50 border-b hover:bg-gray-100">
        <td class="px-6 py-4 font-medium text-gray-900 border border-gray-200">MCC 5413 (Credit Card Bill Payments), 5412 (Purchase of digital gold)</td>
        <td class="px-6 py-4 border border-gray-200">Completely blocked for collect payments</td>
      </tr>
      <tr class="bg-white border-b hover:bg-gray-50">
        <td class="px-6 py-4 font-medium text-gray-900 border border-gray-200">MCCs 6513 (Rent), 6540 (Wallet Load), and 5816 (Digital Gaming)</td>
        <td class="px-6 py-4 border border-gray-200">Blocked on QR code and collect</td>
      </tr>
      <tr class="bg-gray-50 border-b hover:bg-gray-100">
        <td class="px-6 py-4 font-medium text-gray-900 border border-gray-200">MCC 6211 for IPO and purchase of G-Sec through RBI Retail Direct Scheme (RDS)</td>
        <td class="px-6 py-4 font-bold border border-gray-200">5,00,000</td>
      </tr>
      <tr class="bg-white border-b hover:bg-gray-50">
        <td class="px-6 py-4 font-medium text-gray-900 border border-gray-200">Tax Payments, MCC - 9311</td>
        <td class="px-6 py-4 font-bold border border-gray-200">5,00,000</td>
      </tr>
      <tr class="bg-gray-50 hover:bg-gray-100">
        <td class="px-6 py-4 font-medium text-gray-900 border border-gray-200">Hospitals and Educational Services, MCC - 8011, 8021, 8031, 8041, 8042, 8049, 8050, 8062, 8071, 8099, 0742, 8211, 8220, 8241, 8244, 8249, 8299</td>
        <td class="px-6 py-4 font-bold border border-gray-200">5,00,000</td>
      </tr>
    </tbody>
  </table>
</div>

> **Note:** While the NPCI sets the maximum ceilings above, individual **Remitter Banks** reserve the right to set *lower* internal limits based on their own risk policies (e.g., a specific bank might cap daily UPI spends at ₹50,000 regardless of your MCC).
