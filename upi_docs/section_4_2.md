UPI AutoPay is the recurring payments framework built on the Unified Payments Interface (UPI). It supports subscriptions, loan EMIs, insurance premiums, utility bills, and similar recurring payment types.

By default, most payment service providers (PSPs) bind AutoPay mandates to the gateway that originally created them. When you switch your acquiring bank or payment gateway, those mandates become invalid and your customers must set them up again.

**UPI AutoPay Interoperability** removes this dependency. It allows you to move mandates across payment gateways without interruption, and gives your customers greater visibility and control over their recurring payments.

## 1. The Core Concept: MIC Mapping

Instead of validating recurring payments using a rigid Payee UPI ID, Cashfree validates merchants using a persistent **Merchant Identifier Code (MIC)**.

*   The MIC is a 20-character hexadecimal code derived from your corporate PAN using SHAKE-256 hashing.
*   The MIC remains permanently consistent regardless of which payment gateway or bank you use to process payments.

**Key Features:**

*   **Acquiring-side interoperability:** A different payment aggregator or acquiring bank can execute mandates on behalf of the one that originally created them.
*   **Payer-side interoperability:** Users can view active mandates across UPI apps and port mandates without disrupting recurring debits.
*   **Gateway migration support:** You can change payment gateways without forcing customers to recreate mandates.

**Use Cases:**

*   Migrate your payment processing from one gateway to another without disrupting recurring mandates.
*   Keep subscriptions, loan EMIs, and insurance premium collections active when you switch settlement partners.
*   Support recurring utility bill payments across multiple UPI apps and remitting banks.
*   Maintain recurring payment continuity during merchant migration, acquisitions, or platform changes.

## 2. Before vs. After Interoperability

If you have active UPI AutoPay mandates with another payment aggregator, you can migrate your processing to Cashfree without disrupting your customers’ mandates.

## 3. Eligibility for Mandate Migration

Because this is new functionality that has not yet been widely adopted, not all banks and UPI apps have implemented the required changes. You can migrate mandates only when the remitting bank and the payer's UPI app are certified.

**Eligible Remitting Banks (Customer's Bank):**
You can migrate mandates only when the customer’s bank account is held at one of these banks:
*   HDFC Bank
*   Punjab National Bank (PNB)
*   IndusInd Bank
*   Yes Bank
*   IDFC FIRST Bank
*   Cosmos Bank

**Eligible Payer PSPs (Customer's UPI App):**
Your customer’s UPI app must also be certified for interoperability. The following payer PSPs are currently eligible:
*   Paytm (`@ptyes`)
*   BHIM (`@upi`)
*   INDmoney (`@inhdfc`)

> **Note:** Mandates linked to banks or apps not on these lists are not yet eligible for migration. Cashfree updates these lists as more entities complete certification.

## 4. How Mandate Migration Works

The following steps describe the migration flow involving your existing payment aggregator (PA1), Cashfree, and NPCI’s UPI switch.

### Step 1: Migrate mandates to the interoperability framework
Before Cashfree executes your mandates, your existing mandates (created under the old framework using purpose code `14`) must be upgraded to the interoperability framework by PA1.
*   PA1 initiates a `ReqMandate` API call with `type='UPDATE'` and purpose code `AZ` for each eligible mandate.
*   PA1 updates the `sid` tag in the mandate with your Merchant Identifier Code (MIC).

> **Note:** Customers do not need to enter their UPI PIN for this upgrade.

### Step 2: Receive mandate details from PA1
Once PA1 moves eligible mandates to the interoperability framework, it shares a list of migrated mandates with you containing:
*   **UMN (Unique Mandate Number):** The primary identifier for the mandate.
*   **MIC:** Your 20-character hexadecimal code (SHAKE-256 hashed).
*   **SeqNum (Sequence Number):** The current sequence number of the mandate, required for pre-debit notifications and execution ordering.
*   **Metadata:** Mandate max amount, frequency, start date, and end date.

### Step 3: Share mandate details with Cashfree
After you receive the mandate data from PA1, share it with Cashfree. This handoff lets Cashfree take over mandate execution for your customers. You are responsible for ensuring the mandate data from PA1 is accurate. Any discrepancy in MIC, UMN, or SeqNum causes mandate execution to fail.

### Step 4: Cashfree validates and begins execution
Once Cashfree receives your mandate data, we validate the mandate and begin execution:
*   Cashfree maps the MIC against your Payee UPI ID.
*   Cashfree associates the new payee with all migrated mandates.
*   Cashfree begins executing mandates on the specified due dates.

## 5. Merchant Migration Checklist

To ensure a smooth, clean cutover without dropping active subscriptions or causing duplicate debits, follow this checklist:

1.  **Filter by Eligibility:** Work with PA1 to identify which of your existing mandates are on eligible remitting banks and the 3 eligible payer PSPs.
2.  **Request SID Updation:** Formally ask PA1 to initiate the interoperability migration (`ReqMandate` with `type='UPDATE'` and purpose code `AZ`) for all eligible mandates. Cashfree cannot execute mandates until this is done.
3.  **Collect Data:** Collect all required mandate metadata (UMN, MIC, SeqNum, amount, frequency, dates) from PA1.
4.  **Share with Cashfree:** Provide the mandate data file to Cashfree’s onboarding and integrations team for validation and ingestion.
5.  **Coordinate the Go-Live Date:** Agree on an exact cutover date with Cashfree.
6.  **Prevent SeqNum Conflicts:** You must ensure PA1 stops executing the same UMN once Cashfree takes over. If PA1 and Cashfree execute the same mandate at the same time, you risk duplicate debit attempts.