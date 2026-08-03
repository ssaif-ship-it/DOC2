
## 1. Key Terminology & Mechanics

### Max Creation Limit (Registration Cap)
The maximum upper bound allowed when registering a mandate. The merchant can never execute a debit that exceeds the registered Creation Limit on any billing cycle.

### Billing Frequency Types
* **As Presented :** Debits are triggered on demand whenever an invoice is generated (e.g., utility bills, credit card statements). Because billing dates and amounts vary, stricter creation caps apply.
* **All Others (:** Predefined recurring intervals (e.g., Daily, Monthly, Half-Yearly, Yearly). Higher creation limits are permitted due to the predictable billing cadence.

### AFA Exemption Threshold
The monetary ceiling up to which recurring auto-debits process silently in the background without requiring user OTP/PIN verification:
* **Transaction ≤ AFA Threshold:** Processed seamlessly via automated clearing (subject to mandatory pre-debit notifications).
* **Transaction > AFA Threshold:** Fails auto-debit or requires a mandatory step-up authentication flow (SMS/Email payment link with OTP) prior to debit execution.

<table>
  <thead>
    <tr>
      <th>MCC</th>
      <th>MCC DESC</th>
      <th>Max Creation Limit Freq= As Presented</th>
      <th>Max Creation Limit Freq= All Others</th>
      <th>Value Below Which AFA Isn't Required</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>4722</td>
      <td>Travel agencies and tour operators</td>
      <td>25k (Rule 939)</td>
      <td>5 Lakh (Rule 1493)</td>
      <td>15K</td>
    </tr>
    <tr>
      <td>5413</td>
      <td>Credit Card Bill Payments</td>
      <td>1 Lakh (Rule 935)</td>
      <td>5 Lakh (Rule 1494)</td>
      <td>1 Lakh</td>
    </tr>
    <tr>
      <td>5944</td>
      <td>Jewellery, watch, clock and silverware shops</td>
      <td>25k (Rule 939)</td>
      <td>2 Lakh (Rule 1495)</td>
      <td>15K</td>
    </tr>
    <tr>
      <td>5960</td>
      <td>Direct marketing insurance services</td>
      <td>1 Lakh (Rule 935)</td>
      <td>5 Lakh (Rule 1493)</td>
      <td>1 Lakh</td>
    </tr>
    <tr>
      <td>6012</td>
      <td>Financial institutions merchandise and services</td>
      <td>1 Lakh (Rule 935)</td>
      <td>5 Lakh (Rule 1496)</td>
      <td>1 Lakh</td>
    </tr>
    <tr>
      <td>6211</td>
      <td>Securities brokers and dealers</td>
      <td>1 Lakh (Rule 935)</td>
      <td>5 Lakh (Rule 1493)</td>
      <td>1 Lakh</td>
    </tr>
    <tr>
      <td>6300</td>
      <td>Insurance sales, underwriting and premiums</td>
      <td>1 Lakh (Rule 935)</td>
      <td>5 Lakh (Rule 1493)</td>
      <td>1 Lakh</td>
    </tr>
    <tr>
      <td>6381</td>
      <td>Insurance Premiums, (no longer valid for first presentment work)</td>
      <td>1 Lakh (Rule 935)</td>
      <td>1 Lakh (Rule 936)</td>
      <td>1 Lakh</td>
    </tr>
    <tr>
      <td>6399</td>
      <td>Insurance, Not Elsewhere Classified (no longer valid for first presentment work)</td>
      <td>1 Lakh (Rule 935)</td>
      <td>1 Lakh (Rule 936)</td>
      <td>1 Lakh</td>
    </tr>
    <tr>
      <td>6529</td>
      <td>LIC</td>
      <td>1 Lakh (Rule 935)</td>
      <td>5 Lakh (Rule 1493)</td>
      <td>1 Lakh</td>
    </tr>
    <tr>
      <td>7322</td>
      <td>Debt collection agencies</td>
      <td>25K (Rule 1103)</td>
      <td>5 Lakh (Rule 1493)</td>
      <td>15K</td>
    </tr>
    <tr>
      <td>7409</td>
      <td>Digital Account Opening</td>
      <td>25k (Rule 939)</td>
      <td>2 Lakh (Rule 1498)</td>
      <td>15K</td>
    </tr>
    <tr>
      <td>7410</td>
      <td>Digital banking related services (excluding CASA account opening)</td>
      <td>25k (Rule 939)</td>
      <td>5 Lakh (Rule 1497)</td>
      <td>15K</td>
    </tr>
    <tr>
      <td>9311</td>
      <td>Tax payments</td>
      <td>25k (Rule 939)</td>
      <td>5 Lakh (Rule 1493)</td>
      <td>15K</td>
    </tr>
    <tr>
      <td>9400</td>
      <td>PMNRF</td>
      <td>25k (Rule 939)</td>
      <td>2 Lakh (Rule 934)</td>
      <td>15K</td>
    </tr>
    <tr>
      <td>All Other MCCs</td>
      <td>All Other MCCs</td>
      <td>25k (Rule 939)</td>
      <td>1 Lakh (Rule 936)</td>
      <td>15K</td>
    </tr>
  </tbody>
</table>