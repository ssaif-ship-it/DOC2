UPI AutoPay offers a mandate service that allows users to set up recurring payments (Standing Instructions) for use cases like subscriptions, utility bills, insurance premiums, and EMI repayments[cite: 1]. While mandate creation is a one-time activity, it allows the user's account to be debited automatically as per the agreed terms, without the user needing to authenticate subsequent transactions (within specific limits)[cite: 1]. Mandates are supported on all valid UPI IDs and are revocable by the user[cite: 1].

### Mandate Creation Modes
AutoPay mandates can be created via three primary modes[cite: 1]:
*   **QR Scanning (Payer-initiated):** Merchant initiated QR scanning via the Payer App[cite: 1].
*   **Intent Call (Payer-initiated):** Merchant initiated Intent Call to the Payer App, often used for in-app or WhatsApp promotional flows[cite: 1].
*   **Collect Request (Payee-initiated):** Merchant initiated Collect request pushed directly to the Payer's UPI app[cite: 1].

### Key Mandate Attributes
When creating a mandate, the following core attributes must be defined[cite: 1]:
*   **Validity Date:** This includes the start date and the end date, signifying the total validity period of the mandate (which can be a maximum of up to 30 years)[cite: 1].
*   **Amount Rule (MAX vs. EXACT):** 
    *   `MAX`: The payee can debit any value up to the specified amount per debit (e.g., variable utility bills)[cite: 1].
    *   `EXACT`: The payee can only debit the exact specified amount[cite: 1].
*   **Recurrence Pattern (Frequency):** Specifies when the debit will be initiated. Allowed frequencies are: Daily, Weekly, Fortnightly, Monthly, Bimonthly, Quarterly, Half-yearly, Yearly, or "As presented"[cite: 1].

### Execution Limits & AFA (UPI PIN) Rules
The requirement for an Additional Factor of Authentication (AFA), which is the UPI PIN, depends on the transaction amount and the Merchant Category Code (MCC):
*   **Transactions ≤ ₹15,000:** The first execution can happen instantly without AFA, and subsequent transactions can be performed without AFA[cite: 1].
*   **Select MCCs (Extended Limits):** For specific MCCs (as per OC 151A), the maximum execution amount without AFA is extended up to ₹1,00,000[cite: 1].
*   **Transactions > ₹15,000 (or > ₹1 Lakh for select MCCs):** Every mandate execution exceeding these thresholds must be accompanied by a UPI PIN[cite: 1].
*   **Deferred Executions:** If the user is not willing to have an instant first debit (i.e., the execution happens on a deferred date or more than 5 minutes after creation), AFA is always required for the first execution, regardless of the amount[cite: 1]. 

### Pre-Debit Notification (PDN) Guidelines
*   **24-Hour Rule:** It is the liability of the Payee PSP to communicate the execution date, time, and details (UMN, Merchant Name, etc.) to the Payer PSP and Issuer Bank so that the customer is notified at least 24 hours prior to execution[cite: 1].
*   **PDN Exemptions:** A 24-hour PDN is *not* required for:
    *   Daily mandates[cite: 1].
    *   Mandates where execution happens within 5 minutes of creation[cite: 1].
    *   Mandates where execution happens on the same date as creation[cite: 1].
    *   Auto Top-Up for NETC FASTag (MCC 4784) and RuPay NCMC (MCC 7412)[cite: 1].