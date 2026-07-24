# 4.2 UPI AutoPay Interoperability & Migration Flow

UPI AutoPay is the recurring payments framework built on the Unified Payments Interface (UPI). It supports subscriptions, loan EMIs, insurance premiums, utility bills, and similar recurring payment types. 

By default, most payment service providers (PSPs) bind AutoPay mandates to the gateway that originally created them. When you switch your acquiring bank or payment gateway, those mandates become invalid and your customers must set them up again. 

UPI AutoPay Interoperability removes this dependency. It allows you to move mandates across payment gateways without interruption, and gives your customers greater visibility and control over their recurring payments.

---

## 1. The Core Concept: MIC Mapping

Cashfree validates merchants using a persistent Merchant Identifier Code (MIC) rather than your Payee UPI ID. 

*   The MIC is a 20-character hexadecimal code derived from your corporate PAN using SHAKE-256 hashing.
*   The MIC remains consistent regardless of which payment gateway or bank you use.

**Use Cases for Interoperability:**
*   Migrate your payment processing from one gateway to another without disrupting recurring mandates.
*   Keep subscriptions, loan EMIs, and insurance collections active when you switch settlement partners.
*   Maintain payment continuity during merchant migration, acquisitions, or platform changes.

---

## 2. What This Means For You

If you have active UPI AutoPay mandates with another payment aggregator, you can migrate your processing to Cashfree without disrupting your customers' mandates.

| Aspect | Before interoperability | After interoperability |
| :--- | :--- | :--- |
| **Switching payment gateways** | Mandates break and users must re-create | Mandates migrate seamlessly |
| **Mandate visibility for users** | Only within the originating UPI app | Viewable across any UPI app |
| **Dynamic routing for mandate executions** | Not allowed | Now allowed |
| **User re-authentication needed?** | Yes, required if gateway changes | No, existing UPI PIN suffices |

---

## 3. Eligibility for Mandate Migration

Because this is new functionality that has not yet been widely adopted, not all banks and UPI apps have implemented the required changes. You can migrate mandates only when all three entities—the payee PSP (the PSP collecting payments on your behalf), the payer PSP (the customer's UPI app), and the remitting bank—have implemented the interoperability framework.

### Eligible Remitting Banks
You can migrate mandates only when the customer's bank account is held at one of these banks:

| Bank name | Status |
| :--- | :--- |
| **HDFC Bank** | Live on UPI interoperability |
| **Punjab National Bank (PNB)** | Live on UPI interoperability |
| **IndusInd Bank** | Live on UPI interoperability |
| **Yes Bank** | Live on UPI interoperability |
| **IDFC FIRST Bank** | Live on UPI interoperability |
| **Cosmos Bank** | Live on UPI interoperability |

### Eligible Payer PSPs (UPI Apps)
Your customer's UPI app must also be certified for interoperability. The following payer PSPs are currently eligible:

| UPI app or PSP | UPI handle |
| :--- | :--- |
| **Paytm** | `@ptyes` |
| **BHIM** | `@upi` |
| **INDmoney** | `@inhdfc` |

> **Note:** You can migrate a mandate only when both the remitting bank and the payer PSP are on these lists. Mandates linked to banks not in this list are not yet eligible, but Cashfree updates this list as more banks complete certification.

---

## 4. How Mandate Migration Works

The following steps describe the migration flow involving your existing payment aggregator (PA1), Cashfree, and NPCI's UPI switch. 

### Step 1: Migrate mandates to the interoperability framework
Before Cashfree executes your mandates, your existing mandates, which were created under the old framework using purpose code `14`, must be upgraded to the interoperability framework by PA1.
*   PA1 initiates a `ReqMandate` API call with `type='UPDATE'` and purpose code `AZ` for each eligible mandate.
*   PA1 updates the `sid` tag in the mandate with your Merchant Identifier Code (MIC).

### Step 2: Receive mandate details from PA1
Once PA1 moves eligible mandates to the interoperability framework, it shares a list of migrated mandates with you containing:
*   **UMN (Unique Mandate Number):** The primary identifier for the mandate.
*   **MIC (Merchant Identifier Code):** The 20-character hexadecimal code derived from your corporate PAN using SHAKE-256 hashing.
*   **SeqNum (Sequence Number):** The current sequence number of the mandate, required for pre-debit notifications and execution ordering.
*   **Metadata:** Other mandate metadata required for execution, including mandate max amount, frequency, start date, and end date.

### Step 3: Share mandate details with Cashfree
After you receive the mandate data from PA1, share it with Cashfree to let Cashfree take over mandate execution for your customers. You are responsible for ensuring the mandate data from PA1 is accurate. Any discrepancy in MIC, UMN, or SeqNum causes mandate execution to fail.

### Step 4: Cashfree validates and begins execution
Once Cashfree receives your mandate data, Cashfree validates the mandate and begins execution:
*   Cashfree maps the MIC against your Payee UPI ID.
*   Cashfree associates the new payee with all migrated mandates.
*   Cashfree begins executing mandates on the specified due dates.

---

## 5. What is Required From You

These merchant actionables describe the steps you must complete before Cashfree can begin executing migrated mandates.

| Action | Description |
| :--- | :--- |
| **Request SID updation from PA1** | Formally ask PA1 to initiate the interoperability migration using `ReqMandate` with purpose code `AZ` for all eligible mandates. This is a prerequisite; Cashfree cannot execute mandates until this is done. |
| **Collect mandate data file from PA1** | After migration is complete, collect the mandate data file from PA1 containing UMN, MIC, SeqNum, mandate max amount, frequency, start date, and end date for every migrated mandate. |
| **Share mandate data with Cashfree** | Provide the mandate data file to Cashfree's onboarding and integrations team for validation and ingestion. |
| **Coordinate go-live date** | Agree on a go-live date with Cashfree. Ensure PA1 stops executing the same UMN once Cashfree takes over to avoid duplicate debits. |

---

## 6. Migration Checklist & Considerations

To track your migration progress, ensure you have:
*   Identified all active UPI AutoPay mandates on your current payment aggregator and confirmed the source UPI app and remitting bank for each.
*   Filtered your active mandate list by eligible remitting banks (HDFC Bank, PNB, IndusInd Bank, Yes Bank, IDFC FIRST Bank, and Cosmos Bank).
*   Filtered mandates by eligible payer PSPs.
*   Formally asked PA1 to initiate the `ReqMandate` updates with `type='UPDATE'` and purpose code `AZ`.
*   Collected the data file containing all required metadata before sharing it with Cashfree.
*   Shared the mandate data with Cashfree promptly so mandates can move to production smoothly.
*   Confirmed the go-live date with Cashfree and arranged a clean cutover where PA1 stops executing migrated mandates before Cashfree begins.

**Current Limitations and Risks:**
*   **POC stage:** Interoperability is in an early proof-of-concept phase. Complete full testing before live migration.
*   **SeqNum Conflicts:** If PA1 and Cashfree execute the same UMN once Cashfree takes over, you risk duplicate debits.
*   **Limited Coverage:** Only 6 remitting banks and 3 payer PSPs are currently eligible. Mandates outside this scope cannot migrate yet.