To maintain the security of the payment ecosystem and mitigate fraud, the National Payments Corporation of India (NPCI) and participating banks enforce strict transaction and velocity limits on the UPI network.

As a merchant, it is crucial to understand both the baseline network limits and your specific Merchant Category Code (MCC) limits. Attempting to collect amounts above these thresholds—or using restricted payment flows—will result in immediate technical declines.

### 1. The 24-Hour New User Velocity Rule (Anti-Fraud)

One of the most common reasons for unexpected payment failures on high-value orders is the NPCI's 24-hour cooling-off period. To prevent account takeover fraud, the NPCI heavily restricts transaction capabilities when a user's UPI profile undergoes a major state change (e.g., first-time registration, device binding/new phone, or UPI PIN reset).

**The Restriction:** For the first **24 hours** following any of these triggers, the user's UPI transaction limit is strictly capped at **₹5,000**. Normal limits are automatically restored after the 24-hour window expires.

### 2. Standard & MCC-Specific Limits

By default, the standard retail limit for a P2M (Person-to-Merchant) transaction is **₹1 Lakh**. However, the NPCI recognizes that certain critical industries require higher ceilings, while high-risk categories face strict flow limitations (such as completely blocking "pull"/Collect requests).

The table below acts as your master reference for daily transaction limits and flow blocks enforced by the NPCI switch, based on your merchant category:

| Merchant Group | MCC Code | Description | Daily Limit |
|---|---|---|---|
| Standard Default | P2P | Person-to-Person Transfers | ₹100,000 |
| Standard Default | RETAIL | Local Merchant & Grocery Stores | ₹100,000 |
| Standard Default | ECOM | E-Commerce & Online Spends | ₹100,000 |
| Standard Default | FOOD | Restaurants & Dining | ₹100,000 |
| Standard Default | UTIL | Utility Bills & Recharges | ₹100,000 |
| Standard Default | ALL | All Other Unspecified MCC Codes | ₹100,000 |
| Medical & Healthcare | 8062 | Hospitals | ₹500,000 |
| Medical & Healthcare | 8011 | Doctors & Physicians | ₹500,000 |
| Medical & Healthcare | 8021 | Dentists | ₹500,000 |
| Medical & Healthcare | 8071 | Medical & Dental Labs | ₹500,000 |
| Medical & Healthcare | 8050 | Nursing Care | ₹500,000 |
| Medical & Healthcare | 8042 | Optometrists | ₹500,000 |
| Medical & Healthcare | 8031 | Osteopaths | ₹500,000 |
| Medical & Healthcare | 8041 | Chiropractors | ₹500,000 |
| Medical & Healthcare | 8049 | Podiatrists | ₹500,000 |
| Medical & Healthcare | 8099 | Other Medical Services | ₹500,000 |
| Medical & Healthcare | 0742 | Veterinary Services | ₹500,000 |
| Education | 8211 | Schools (Elementary & Secondary) | ₹500,000 |
| Education | 8220 | Colleges & Universities | ₹500,000 |
| Education | 8249 | Vocational & Trade Schools | ₹500,000 |
| Education | 8244 | Business Schools | ₹500,000 |
| Education | 8241 | Correspondence Schools | ₹500,000 |
| Education | 8299 | Educational Services | ₹500,000 |
| Financial, Credit & Insurance | 5413 | Credit Card Bill Payments | ₹500,000 |
| Financial, Credit & Insurance | 6300 | Insurance Underwriting & Premiums | ₹500,000 |
| Financial, Credit & Insurance | 6529 | LIC Payments | ₹500,000 |
| Financial, Credit & Insurance | 6211 | Securities Brokers & Dealers | ₹500,000 |
| Financial, Credit & Insurance | 6012 | Financial Institutions | ₹500,000 |
| Financial, Credit & Insurance | 5960 | Direct Marketing Insurance | ₹500,000 |
| Financial, Credit & Insurance | 7322 | Debt Collection Agencies | ₹500,000 |
| Financial, Credit & Insurance | 7410 | Digital Banking Services | ₹500,000 |
| Government, Travel & Public Services | 9311 | Tax Payments | ₹500,000 |
| Government, Travel & Public Services | 4722 | Travel Agencies & Tour Operators | ₹500,000 |
| Retail Luxury & Digital KYC | 5944 | Jewellery, Watch & Silverware Shops | ₹200,000 |
| Retail Luxury & Digital KYC | 7409 | Digital Account Opening | ₹200,000 |

> **Note:** The Standard Default tier is additionally subject to a 20-transaction daily limit per rolling 24 hours, and the ₹5,000 new-user cap described above still applies within its 24-hour window regardless of MCC.

> **Note:** While the NPCI sets the maximum ceilings above, individual **Remitter Banks** reserve the right to set *lower* internal limits based on their own risk policies (e.g., a specific bank might cap daily UPI spends at ₹50,000 regardless of your MCC).