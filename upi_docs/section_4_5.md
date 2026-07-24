UPI Lite is an on-device wallet solution designed by NPCI to process low-value transactions seamlessly without cluttering bank passbooks or stressing core banking systems (CBS). By storing balance directly within the secure Common Library (CL) on the customer's phone, UPI Lite enables 1-click PIN-less payments for amounts up to ₹200.

---

## 1. Enablement & Initial Top-Up Flow

### Product View & User Journey
*   **Discovery & Opt-In:** The customer sees an activation prompt/banner on the app's home screen and taps "Set-up now".
*   **Bank Selection & Consent:** The app displays linked bank accounts eligible for UPI Lite. The customer selects an account, reviews features, and agrees to the Terms & Conditions.
*   **Top-Up Amount:** The customer enters an initial top-up amount (recommended presets: ₹500, ₹1,000, ₹2,000).
*   **Authentication:** The customer enters their UPI PIN via the NPCI Common Library (CL) overlay screen.
*   **Confirmation:** Upon success, a "Money added Successfully!" screen displays the updated balance (up to ₹2,000), and an SMS notification is triggered by the PSP.

### Mandatory Business & Security Validations
*   **Device Integrity:** The app must verify that the device is not rooted or jailbroken. Activation is strictly blocked on compromised devices.
*   **Single Active Wallet Limit:** The Common Library can only hold balance for one UPI Lite account at a time.
*   **Maximum Stored Value:** The initial top-up cannot exceed the maximum stored value limit of ₹2,000.
*   **Issuer Eligibility:** The app must filter and present only issuing banks that are live on the UPI Lite network.

### Technical Architecture & API Sequence
**Phase 1: Service Enablement (Registration & Key Sharing)**
*   **Eligibility Query:** Payer PSP calls `RespListAccPvd` to check if the selected issuing bank account supports UPI Lite.
*   **Keypair Generation:** Upon user consent, the app invokes the device Common Library (CL) to generate a cryptographic key pair. The CL returns the Public Key to the app.
*   **Registration Call:** The Payer PSP initiates a `ReqListKeys` call (with `type="GetLite"`) to the UPI network, passing the Public Key to the NPCI Auth Engine.
*   **LRN Allocation:** The NPCI Auth Engine stores the Public Key, registers the device, and returns `RespListKeys` containing a unique LITE Reference Number (LRN) for the user's Lite account.

**Phase 2: Initial Top-Up (Fund Transfer)**
*   **Cryptogram Generation:** The app captures the top-up amount and UPI PIN. The CL constructs a secure credential block containing the UPI PIN and an Authentication Request Cryptogram (ARQC).
*   **Top-up Execution (`ReqPay`):** Payer PSP executes `ReqPay` with Purpose Code `41` (Enablement + Add Money) passing the credential block.
*   **On-Device Ledger Update:** UPI Switch responds with `RespPay` containing an Authentication Response Cryptogram (ARPC). The app passes the ARPC into the CL, which validates the payload and updates the local on-device balance.

> **Note:** If the user also opts for AutoPay auto-replenishment during setup, Purpose Code `71` is passed instead.

---

## 2. Subsequent Top-Up (Add Money) Flow

### Product View & Business Rules
*   **Initiation:** The customer selects "Add Money" from the UPI Lite dashboard. If the stored balance drops below ₹200, the app proactively displays a top-up prompt.
*   **Limits:** Minimum top-up amount is ₹1. The app strictly validates that $\text{Current Balance} + \text{Top-Up Amount} \le \text{₹2,000}$.
*   **Authentication:** The app invokes the CL overlay for UPI PIN authorization. Funds are strictly debited from the specific bank account linked during initial activation (no multi-bank selector).
*   **Notification:** The on-device balance updates instantly, accompanied by a real-time SMS confirmation from the issuing bank.

---

## 3. Payment Flow (Online & Offline)

### Product View & Pre-Transaction Rules
*   **Initiation:** Customer scans a QR code, selects a contact, or triggers an Intent checkout.
*   **Validation Rules:** 
    *   Transaction amount is $\le$ ₹200.
    *   Sufficient balance exists in the on-device UPI Lite wallet.
*   **Fallback:** If the amount exceeds ₹200 or Lite balance is insufficient, the app automatically falls back to standard 2FA UPI requiring a PIN.
*   **1-Click Execution:** The customer taps "Pay". No UPI PIN is required. The app enforces local device security (biometric, pattern, or passcode) prior to payment.
*   **Consolidated Statement:** To avoid SMS clutter, issuing banks send a single consolidated daily SMS summary detailing total UPI Lite transactions for that day instead of per-transaction SMS alerts.

---

## 4. Transfer Out Flow (Partial Withdrawal)

### Product View & Mechanics
*   **Concept:** Allows users to withdraw a portion of their stored UPI Lite balance back into their primary bank account at any time without closing/disabling the UPI Lite account.
*   **Processing:** Strictly an online credit flow. Because money is returning to the customer's own linked account, no UPI PIN is required.
*   **Technical Execution:** Utilizes the payment execution infrastructure with Purpose Code `46` (CREDIT transaction type).

---

## 5. Disablement (De-registration) Flow

### Product View & Lifecycle Rules
*   **Initiation:** The user selects "Disable UPI Lite" in settings. Apps must mandate that the user disables/deregisters UPI Lite prior to uninstalling or unlinking their main bank account from the UPI app.
*   **Fund Refund:** All residual funds in the Lite wallet are immediately credited back to the parent bank account without requiring a UPI PIN.
*   **Technical API (`ReqPay`):**
    *   **With Balance:** App triggers a single `ReqPay` API with Purpose Code `43` and transaction type CREDIT. This single API call clears the on-device CL balance, notifies the NPCI engine, and credits the bank account.
    *   **Zero Balance:** A de-registration notification is sent to unbind the LRN from the device.

---

## 6. Background Sync & Recovery Flows

To prevent discrepancies between the local on-device wallet and network ledgers caused by timeouts or app reinstalls, the app must enforce strict background synchronization rules.

### Sync Triggers & Guardrails
*   **Timeout / Dropout:** Occurs when a Top-Up or Payment succeeds at the bank/Auth Engine, but network loss prevents the ARPC from reaching the phone.
*   **Cooling Off Period:** The app must wait 3 minutes after a transaction timeout before firing a sync request.
*   **Attempt Cap:** Max 3 sync attempts per day for any specific stuck transaction.
*   **Fallback Protocol:** If 3 sync attempts fail, the app flags the transaction as un-synced and falls back to processing transactions via standard 2FA UPI.
*   **Transaction Blocking:** The app must block any new UPI Lite transactions until background sync completes and the missing ARPC cryptogram is successfully written to the Common Library.

---

## 7. Edge Cases: Device Change or Loss

| Scenario | Impact & Required Action |
| :--- | :--- |
| **Scenario A: Device Upgrade / Phone Switch** | **Step 1 (Old Phone):** Customer must manually trigger the Disablement Flow to transfer remaining funds back to their bank.<br>**Step 2 (New Phone):** Install the UPI App. Old LITE balances cannot be restored directly from local storage.<br>**Step 3 (Fresh Setup):** Customer performs a brand new registration generating a new LRN and keypair. |
| **Scenario B: Lost or Damaged Device** | Because the old device cannot be accessed to extract the CL state, balance recovery is handled directly by the Issuing Bank's customer support/reconciliation team. No Payer PSP API calls are involved. |