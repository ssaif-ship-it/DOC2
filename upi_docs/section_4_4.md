Your AutoPay mandate limits depend entirely on your Merchant Category Code (MCC). Two numbers matter every time you create a mandate: how much you can register it for, and how much can be auto-debited before your customer has to re-enter their UPI PIN, the AFA threshold introduced in [4.1](#doc-4-1). Find your category in the table below before you register your first mandate.

## 1. Key Terminology & Mechanics

### Max Creation Limit (Registration Cap)

The maximum upper bound allowed when registering a mandate. The merchant can never execute a debit that exceeds the registered Creation Limit on any billing cycle.

### Billing Frequency Types

<!-- Claude, updated for Saif: switched this column and bullet from NPCI's "As Presented" label to Cashfree's own "On-Demand" plan type name, per your instruction that this is what Cashfree uses. This also lines up with the research already in 4.1's comment: Cashfree's Subscriptions Overview page assigns As Presented's defining behaviour, debiting a variable amount whenever a bill is generated, to On-Demand, not Periodic. The NPCI mandate creation frequency itself is still "As Presented" under the hood, this change is about which label merchants see in this doc. -->

*   **On-Demand:** Debits are triggered whenever an invoice is generated (for example, utility bills, credit card statements). Because billing dates and amounts vary, stricter creation caps apply.
*   **All Others:** Predefined recurring intervals (for example, Daily, Monthly, Half-Yearly, Yearly). Higher creation limits are permitted due to the predictable billing cadence.

### AFA (Additional Factor of Authentication) Exemption Threshold

The monetary ceiling up to which recurring auto-debits process silently in the background without requiring your customer to re-enter their UPI PIN, already introduced in [4.1](#doc-4-1):

*   **Transaction at or below the AFA Threshold:** Processed via automated clearing (subject to mandatory pre-debit notifications).
*   **Transaction > AFA Threshold:** Fails auto-debit or requires a mandatory step-up authentication flow (SMS/Email payment link with OTP) prior to debit execution.

<table>
  <thead>
    <tr>
      <th>MCC</th>
      <th>MCC DESC</th>
      <th>Max Creation Limit Freq= On-Demand</th>
      <th>Max Creation Limit Freq= All Others</th>
      <th>Value Below Which AFA Isn't Required</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>4722</td>
      <td>Travel agencies and tour operators</td>
      <td>₹25,000</td>
      <td>₹5,00,000</td>
      <td>₹15,000</td>
    </tr>
    <tr>
      <td>5413</td>
      <td>Credit Card Bill Payments</td>
      <td>₹1,00,000</td>
      <td>₹5,00,000</td>
      <td>₹1,00,000</td>
    </tr>
    <tr>
      <td>5944</td>
      <td>Jewellery, watch, clock and silverware shops</td>
      <td>₹25,000</td>
      <td>₹2,00,000</td>
      <td>₹15,000</td>
    </tr>
    <tr>
      <td>5960</td>
      <td>Direct marketing insurance services</td>
      <td>₹1,00,000</td>
      <td>₹5,00,000</td>
      <td>₹1,00,000</td>
    </tr>
    <tr>
      <td>6012</td>
      <td>Financial institutions merchandise and services</td>
      <td>₹1,00,000</td>
      <td>₹5,00,000</td>
      <td>₹1,00,000</td>
    </tr>
    <tr>
      <td>6211</td>
      <td>Securities brokers and dealers</td>
      <td>₹1,00,000</td>
      <td>₹5,00,000</td>
      <td>₹1,00,000</td>
    </tr>
    <tr>
      <td>6300</td>
      <td>Insurance sales, underwriting and premiums</td>
      <td>₹1,00,000</td>
      <td>₹5,00,000</td>
      <td>₹1,00,000</td>
    </tr>
    <tr>
      <td>6381</td>
      <td>Insurance Premiums</td>
      <td>₹1,00,000</td>
      <td>₹1,00,000</td>
      <td>₹1,00,000</td>
    </tr>
    <tr>
      <td>6399</td>
      <td>Insurance, Not Elsewhere Classified</td>
      <td>₹1,00,000</td>
      <td>₹1,00,000</td>
      <td>₹1,00,000</td>
    </tr>
    <tr>
      <td>6529</td>
      <td>LIC</td>
      <td>₹1,00,000</td>
      <td>₹5,00,000</td>
      <td>₹1,00,000</td>
    </tr>
    <tr>
      <td>7322</td>
      <td>Debt collection agencies</td>
      <td>₹25,000</td>
      <td>₹5,00,000</td>
      <td>₹15,000</td>
    </tr>
    <tr>
      <td>7409</td>
      <td>Digital Account Opening</td>
      <td>₹25,000</td>
      <td>₹2,00,000</td>
      <td>₹15,000</td>
    </tr>
    <tr>
      <td>7410</td>
      <td>Digital banking related services (excluding CASA account opening)</td>
      <td>₹25,000</td>
      <td>₹5,00,000</td>
      <td>₹15,000</td>
    </tr>
    <tr>
      <td>9311</td>
      <td>Tax payments</td>
      <td>₹25,000</td>
      <td>₹5,00,000</td>
      <td>₹15,000</td>
    </tr>
    <tr>
      <td>9400</td>
      <td>PMNRF</td>
      <td>₹25,000</td>
      <td>₹2,00,000</td>
      <td>₹15,000</td>
    </tr>
    <tr>
      <td>All Other MCCs</td>
      <td>All Other MCCs</td>
      <td>₹25,000</td>
      <td>₹1,00,000</td>
      <td>₹15,000</td>
    </tr>
  </tbody>
</table>
<!-- Claude, flagging for Saif: MCC 6381 and 6399 originally carried the parenthetical "(no longer valid for first presentment work)" in the MCC description column. I could not confirm what this means, my best guess is that the lower All Others limit for these two codes does not apply to a mandate's very first debit and only takes effect from the second cycle onward, but that is a guess, not a confirmed fact, so I removed the phrase from the visible table rather than publish a footnote based on it. Confirm the real meaning before adding anything back. -->
