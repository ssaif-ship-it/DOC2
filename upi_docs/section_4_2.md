# 4.2 UPI AutoPay Interoperability & Migration Flow

UPI AutoPay is the recurring payments framework built on the Unified Payments Interface (UPI)[cite: 1]. It supports subscriptions, loan EMIs, insurance premiums, utility bills, and similar recurring payment types[cite: 1]. 

By default, most payment service providers (PSPs) bind AutoPay mandates to the gateway that originally created them[cite: 1]. When you switch your acquiring bank or payment gateway, those mandates become invalid and your customers must set them up again[cite: 1]. 

UPI AutoPay Interoperability removes this dependency[cite: 1]. It allows you to move mandates across payment gateways without interruption, and gives your customers greater visibility and control over their recurring payments[cite: 1].

---

## 1. The Core Concept: MIC Mapping

Cashfree validates merchants using a persistent Merchant Identifier Code (MIC) rather than your Payee UPI ID[cite: 1]. 

*   The MIC is a 20-character hexadecimal code derived from your corporate PAN using SHAKE-256 hashing[cite: 1].
*   The MIC remains consistent regardless of which payment gateway or bank you use[cite: 1].

**Use Cases for Interoperability:**
*   Migrate your payment processing from one gateway to another without disrupting recurring mandates[cite: 1].
*   Keep subscriptions, loan EMIs, and insurance collections active when you switch settlement partners[cite: 1].
*   Maintain payment continuity during merchant migration, acquisitions, or platform changes[cite: 1].

---

## 2. What This Means For You

If you have active UPI AutoPay mandates with another payment aggregator, you can migrate your processing to Cashfree without disrupting your customers' mandates[cite: 1].

| Aspect | Before interoperability | After interoperability |
| :--- | :--- | :--- |
| **Switching payment gateways** | Mandates break and users must re-create[cite: 1] | Mandates migrate seamlessly[cite: 1] |
| **Mandate visibility for users** | Only within the originating UPI app[cite: 1] | Viewable across any UPI app[cite: 1] |
| **Dynamic routing for mandate executions** | Not allowed[cite: 1] | Now allowed[cite: 1] |
| **User re-authentication needed?** | Yes, required if gateway changes[cite: 1] | No, existing UPI PIN suffices[cite: 1] |

---

## 3. Eligibility for Mandate Migration

Because this is new functionality that has not yet been widely adopted, not all banks and UPI apps have implemented the required changes[cite: 1]. You can migrate mandates only when all three entities—the payee PSP (the PSP collecting payments on your behalf), the payer PSP (the customer's UPI app), and the remitting bank—have implemented the interoperability framework[cite: 1].

### Eligible Remitting Banks
You can migrate mandates only when the customer's bank account is held at one of these banks[cite: 1]:

| Bank name | Status |
| :--- | :--- |
| **HDFC Bank** | Live on UPI interoperability[cite: 1] |
| **Punjab National Bank (PNB)** | Live on UPI interoperability[cite: 1] |
| **IndusInd Bank** | Live on UPI interoperability[cite: 1] |
| **Yes Bank** | Live on UPI interoperability[cite: 1] |
| **IDFC FIRST Bank** | Live on UPI interoperability[cite: 1] |
| **Cosmos Bank** | Live on UPI interoperability[cite: 1] |

### Eligible Payer PSPs (UPI Apps)
Your customer's UPI app must also be certified for interoperability[cite: 1]. The following payer PSPs are currently eligible:

| UPI app or PSP | UPI handle |
| :--- | :--- |
| **Paytm** | `@ptyes`[cite: 1] |
| **BHIM** | `@upi`[cite: 1] |
| **INDmoney** | `@inhdfc`[cite: 1] |

> **Note:** You can migrate a mandate only when both the remitting bank and the payer PSP are on these lists[cite: 1]. Mandates linked to banks not in this list are not yet eligible, but Cashfree updates this list as more banks complete certification[cite: 1].

---

## 4. How Mandate Migration Works

The following steps describe the migration flow involving your existing payment aggregator (PA1), Cashfree, and NPCI's UPI switch[cite: 1]. 

### Step 1: Migrate mandates to the interoperability framework
Before Cashfree executes your mandates, your existing mandates, which were created under the old framework using purpose code `14`, must be upgraded to the interoperability framework by PA1[cite: 1].
*   PA1 initiates a `ReqMandate` API call with `type='UPDATE'` and purpose code `AZ` for each eligible mandate[cite: 1].
*   PA1 updates the `sid` tag in the mandate with your Merchant Identifier Code (MIC)[cite: 1].

### Step 2: Receive mandate details from PA1
Once PA1 moves eligible mandates to the interoperability framework, it shares a list of migrated mandates with you containing[cite: 1]:
*   **UMN (Unique Mandate Number):** The primary identifier for the mandate[cite: 1].
*   **MIC (Merchant Identifier Code):** The 20-character hexadecimal code derived from your corporate PAN using SHAKE-256 hashing[cite: 1].
*   **SeqNum (Sequence Number):** The current sequence number of the mandate, required for pre-debit notifications and execution ordering[cite: 1].
*   **Metadata:** Other mandate metadata required for execution, including mandate max amount, frequency, start date, and end date[cite: 1].

### Step 3: Share mandate details with Cashfree
After you receive the mandate data from PA1, share it with Cashfree to let Cashfree take over mandate execution for your customers[cite: 1]. You are responsible for ensuring the mandate data from PA1 is accurate[cite: 1]. Any discrepancy in MIC, UMN, or SeqNum causes mandate execution to fail[cite: 1].

### Step 4: Cashfree validates and begins execution
Once Cashfree receives your mandate data, Cashfree validates the mandate and begins execution[cite: 1]:
*   Cashfree maps the MIC against your Payee UPI ID[cite: 1].
*   Cashfree associates the new payee with all migrated mandates[cite: 1].
*   Cashfree begins executing mandates on the specified due dates[cite: 1].

---

## 5. What is Required From You

These merchant actionables describe the steps you must complete before Cashfree can begin executing migrated mandates[cite: 1].

| Action | Description |
| :--- | :--- |
| **Request SID updation from PA1** | Formally ask PA1 to initiate the interoperability migration using `ReqMandate` with purpose code `AZ` for all eligible mandates[cite: 1]. This is a prerequisite; Cashfree cannot execute mandates until this is done[cite: 1]. |
| **Collect mandate data file from PA1** | After migration is complete, collect the mandate data file from PA1 containing UMN, MIC, SeqNum, mandate max amount, frequency, start date, and end date for every migrated mandate[cite: 1]. |
| **Share mandate data with Cashfree** | Provide the mandate data file to Cashfree's onboarding and integrations team for validation and ingestion[cite: 1]. |
| **Coordinate go-live date** | Agree on a go-live date with Cashfree[cite: 1]. Ensure PA1 stops executing the same UMN once Cashfree takes over to avoid duplicate debits[cite: 1]. |

---

## 6. Migration Checklist & Considerations

To track your migration progress, ensure you have:
*   Identified all active UPI AutoPay mandates on your current payment aggregator and confirmed the source UPI app and remitting bank for each[cite: 1].
*   Filtered your active mandate list by eligible remitting banks (HDFC Bank, PNB, IndusInd Bank, Yes Bank, IDFC FIRST Bank, and Cosmos Bank)[cite: 1].
*   Filtered mandates by eligible payer PSPs[cite: 1].
*   Formally asked PA1 to initiate the `ReqMandate` updates with `type='UPDATE'` and purpose code `AZ`[cite: 1].
*   Collected the data file containing all required metadata before sharing it with Cashfree[cite: 1].
*   Shared the mandate data with Cashfree promptly so mandates can move to production smoothly[cite: 1].
*   Confirmed the go-live date with Cashfree and arranged a clean cutover where PA1 stops executing migrated mandates before Cashfree begins[cite: 1].

**Current Limitations and Risks:**
*   **POC stage:** Interoperability is in an early proof-of-concept phase[cite: 1]. Complete full testing before live migration[cite: 1].
*   **SeqNum Conflicts:** If PA1 and Cashfree execute the same UMN once Cashfree takes over, you risk duplicate debits[cite: 1].
*   **Limited Coverage:** Only 6 remitting banks and 3 payer PSPs are currently eligible[cite: 1]. Mandates outside this scope cannot migrate yet[cite: 1].