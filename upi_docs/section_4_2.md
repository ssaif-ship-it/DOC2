By default, most payment service providers (PSPs) bind AutoPay mandates to the payment gateway that originally created them. Historically, if a merchant switched acquiring banks or gateways, those mandates became invalid, forcing customers to set them up again. 

**UPI AutoPay Interoperability** removes this dependency. It allows merchants to migrate active mandates across payment gateways without customer interruption or requiring a new UPI PIN authorization.

### 1. The Core Concept: MIC Mapping
The cornerstone of interoperability is the **Merchant Identifier Code (MIC)**. 
Instead of validating recurring payments using a rigid Payee UPI ID, the NPCI framework now identifies merchants using their MIC. 
* The MIC is derived from your corporate PAN.
* The MIC remains permanently consistent regardless of which payment gateway or bank you use to process payments.

### 2. Eligibility & Limitations
Because this interoperability framework is in an early Proof-of-Concept (POC) phase, mandate migration is only possible when the Payee PSP, the Payer PSP (UPI app), and the Remitting Bank are all certified for interoperability. 

<table class="w-full text-left border-collapse">
  <thead>
    <tr class="bg-gray-100">
      <th class="p-3 border-b-2 border-gray-300 font-bold">Category</th>
      <th class="p-3 border-b-2 border-gray-300 font-bold">Current Status / Requirement</th>
    </tr>
  </thead>
  <tbody>
    <tr class="hover:bg-gray-50">
      <td class="p-3 border-b border-gray-200"><strong>Eligible Remitting Banks</strong></td>
      <td class="p-3 border-b border-gray-200">Currently limited to 6 banks: HDFC, PNB, IndusInd, Yes Bank, IDFC FIRST, and Cosmos Bank.</td>
    </tr>
    <tr class="bg-gray-50 hover:bg-gray-100">
      <td class="p-3 border-b border-gray-200"><strong>Eligible Payer PSPs</strong></td>
      <td class="p-3 border-b border-gray-200">Currently limited to 3 supported UPI apps.</td>
    </tr>
    <tr class="hover:bg-gray-50">
      <td class="p-3 border-b border-gray-200"><strong>SeqNum Conflicts</strong></td>
      <td class="p-3 border-b border-gray-200">You must ensure the old PA stops execution. If both gateways execute simultaneously, duplicate debits will occur.</td>
    </tr>
  </tbody>
</table>

### 3. The Migration Flow
The following steps outline how active mandates are ported from your existing Payment Aggregator (PA1) to Cashfree.

**Step 1: The Old Gateway (PA1) Updates the Mandate**
* PA1 initiates a `ReqMandate` API call with `type='UPDATE'` and the purpose code `AZ` for each eligible mandate.
* PA1 updates the `sid` tag within the mandate payload using your Cashfree-registered Merchant Identifier Code (MIC).
* The customer **does not** need to enter their UPI PIN for this upgrade.

**Step 2: Cashfree Takes Over Execution**
* Once the NPCI switch processes the update, Cashfree receives your mandate data.
* Cashfree maps the MIC against your new Payee UPI ID on our platform.
* Cashfree associates the new payee details with all migrated mandates and begins executing them on their specified due dates.

### 4. Merchant Action Checklist
To ensure a smooth transition without dropping active subscriptions, follow this checklist:
* Inventory every active mandate before beginning the migration to prevent missing data.
* Coordinate the exact cut-off date with PA1 to stop them from initiating pre-debit notifications (PDNs) or executions.
* Confirm that your corporate PAN matches the one used to generate the MIC.