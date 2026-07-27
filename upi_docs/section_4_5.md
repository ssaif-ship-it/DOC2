## 4.5 UPI Lite & Prepaid Wallets (PPI)

This section provides comprehensive integration and operational specifications for two key alternative low-value/wallet-based payment solutions on the UPI network: UPI Lite (an on-device wallet for instant, PIN-less small-value payments) and Prepaid Payment Instruments (PPI Wallets on UPI) (interoperable third-party digital wallets processing payments across standard merchant UPI QR codes and Intent checkouts).

---

### PART A: UPI LITE (On-Device PIN-Less Wallet)

UPI Lite is an on-device wallet solution designed by NPCI to process low-value transactions seamlessly without cluttering bank passbooks or stressing core banking systems (CBS). By storing balance directly within the secure Common Library (CL) on the customer's phone, UPI Lite enables 1-click PIN-less payments for amounts up to ₹200.

#### 1. Enablement & Initial Top-Up Flow

**Product View & User Journey**
*   **Discovery & Opt-In:** The customer sees an activation prompt/banner on the app's home screen and taps "Set-up now".
*   **Bank Selection & Consent:** The app displays linked bank accounts eligible for UPI Lite. The customer selects an account, reviews features, and agrees to the Terms & Conditions.
*   **Top-Up Amount:** The customer enters an initial top-up amount (recommended presets: ₹500, ₹1,000, ₹2,000).
*   **Authentication:** The customer enters their UPI PIN via the NPCI Common Library (CL) overlay screen.
*   **Confirmation:** Upon success, a "Money added Successfully!" screen displays the updated balance (up to ₹2,000), and an SMS notification is triggered by the PSP.

**Mandatory Business & Security Validations**
*   **Device Integrity:** The app must verify that the device is not rooted or jailbroken. Activation is strictly blocked on compromised devices.
*   **Single Active Wallet Limit:** The Common Library can only hold balance for one UPI Lite account at a time.
*   **Maximum Stored Value:** The initial top-up cannot exceed the maximum stored value limit of ₹2,000.
*   **Issuer Eligibility:** The app must filter and present only issuing banks that are live on the UPI Lite network.

**Technical Architecture & API Sequence**
*   **Phase 1 - Eligibility Query:** Payer PSP calls RespListAccPvd to check if the selected issuing bank account supports UPI Lite.
*   **Phase 1 - Keypair Generation:** Upon user consent, the app invokes the device Common Library (CL) to generate a cryptographic key pair. The CL returns the Public Key to the app.
*   **Phase 1 - Registration Call:** The Payer PSP initiates a ReqListKeys call (with type="GetLite") to the UPI network, passing the Public Key to the NPCI Auth Engine.
*   **Phase 1 - LRN Allocation:** The NPCI Auth Engine stores the Public Key, registers the device, and returns RespListKeys containing a unique LITE Reference Number (LRN) for the user's Lite account.
*   **Phase 2 - Cryptogram Generation:** The app captures the top-up amount and UPI PIN. The CL constructs a secure credential block containing the UPI PIN and an Authentication Request Cryptogram (ARQC).
*   **Phase 2 - Top-up Execution (ReqPay):** Payer PSP executes ReqPay with Purpose Code 41 (Enablement + Add Money) passing the credential block. *(Note: If the user also opts for AutoPay auto-replenishment during setup, Purpose Code 71 is passed instead).*
*   **Phase 2 - On-Device Ledger Update:** UPI Switch responds with RespPay containing an Authentication Response Cryptogram (ARPC). The app passes the ARPC into the CL, which validates the payload and updates the local on-device balance.

#### 2. Subsequent Top-Up (Add Money) Flow

*   **Initiation:** The customer selects "Add Money" from the UPI Lite dashboard. If the stored balance drops below ₹200, the app proactively displays a top-up prompt.
*   **Limits:** Minimum top-up amount is ₹1. The app strictly validates that Current Balance + Top-Up Amount ≤ ₹2,000.
*   **Authentication:** The app invokes the CL overlay for UPI PIN authorization. Funds are strictly debited from the specific bank account linked during initial activation (no multi-bank selector).
*   **Notification:** The on-device balance updates instantly, accompanied by a real-time SMS confirmation from the issuing bank.

#### 3. Payment Flow (Online & Offline)

*   **Initiation:** Customer scans a QR code, selects a contact, or triggers an Intent checkout.
*   **Validation Rules:** Transaction amount is ≤ ₹200, and sufficient balance exists in the on-device UPI Lite wallet.
*   **Fallback:** If the amount exceeds ₹200 or Lite balance is insufficient, the app automatically falls back to standard 2FA UPI requiring a PIN.
*   **1-Click Execution:** The customer taps "Pay". No UPI PIN is required. The app enforces local device security (biometric, pattern, or passcode) prior to payment.
*   **Consolidated Statement:** To avoid SMS clutter, issuing banks send a single consolidated daily SMS summary detailing total UPI Lite transactions for that day instead of per-transaction SMS alerts.

#### 4. Transfer Out Flow (Partial Withdrawal)

*   **Concept:** Allows users to withdraw a portion of their stored UPI Lite balance back into their primary bank account at any time without closing/disabling the UPI Lite account.
*   **Processing:** Strictly an online credit flow. Because money is returning to the customer's own linked account, no UPI PIN is required.
*   **Technical Execution:** Utilizes the payment execution infrastructure with Purpose Code 46 (CREDIT transaction type).

#### 5. Disablement (De-registration) Flow

*   **Initiation:** The user selects "Disable UPI Lite" in settings. Apps must mandate that the user disables/deregisters UPI Lite prior to uninstalling or unlinking their main bank account from the UPI app.
*   **Fund Refund:** All residual funds in the Lite wallet are immediately credited back to the parent bank account without requiring a UPI PIN.
*   **Technical API (ReqPay) With Balance:** App triggers a single ReqPay API with Purpose Code 43 and transaction type CREDIT. This single API call clears the on-device CL balance, notifies the NPCI engine, and credits the bank account.
*   **Technical API (ReqPay) Zero Balance:** A de-registration notification is sent to unbind the LRN from the device.

#### 6. Background Sync & Recovery Flows

To prevent discrepancies between the local on-device wallet and network ledgers caused by timeouts or app reinstalls, the app must enforce strict background synchronization rules.

*   **Timeout / Dropout:** Occurs when a Top-Up or Payment succeeds at the bank/Auth Engine, but network loss prevents the ARPC from reaching the phone.
*   **Cooling Off Period:** The app must wait 3 minutes after a transaction timeout before firing a sync request.
*   **Attempt Cap:** Max 3 sync attempts per day for any specific stuck transaction.
*   **Fallback Protocol:** If 3 sync attempts fail, the app flags the transaction as un-synced and falls back to processing transactions via standard 2FA UPI.
*   **Transaction Blocking:** The app must block any new UPI Lite transactions until background sync completes and the missing ARPC cryptogram is successfully written to the Common Library.

#### 7. Edge Cases: Device Change or Loss

| Scenario | Impact & Required Action |
| :--- | :--- |
| **Scenario A: Device Upgrade / Phone Switch** | **Step 1 (Old Phone):** Customer must manually trigger the Disablement Flow to transfer remaining funds back to their bank. <br> **Step 2 (New Phone):** Install the UPI App. Old LITE balances cannot be restored directly from local storage. <br> **Step 3 (Fresh Setup):** Customer performs a brand new registration generating a new LRN and keypair. |
| **Scenario B: Lost or Damaged Device** | Because the old device cannot be accessed to extract the CL state, balance recovery is handled directly by the Issuing Bank's customer support/reconciliation team. No Payer PSP API calls are involved. |

---

### PART B: PREPAID PAYMENT INSTRUMENTS (PPI Wallets on UPI)

Prepaid Payment Instruments (PPIs)—such as Paytm Wallet, Mobikwik, Amazon Pay, and PhonePe Wallet—are fully integrated into the UPI ecosystem under NPCI's interoperability directives. This enables users to utilize their pre-funded wallet balances to pay at any merchant accepting UPI, without requiring the merchant to explicitly onboard with each individual wallet provider.

#### 1. Interoperability Architecture & User Onboarding

**Regulatory & KYC Prerequisites**
*   **Full-KYC Mandate:** RBI and NPCI mandate that only Full-KYC PPI accounts can be linked to the UPI network for interoperable payments. Small-value/Min-KYC wallets are strictly excluded from cross-network UPI transactions.
*   **Device & SIM Binding:** Just like bank-backed UPI handles, linking a PPI wallet to a UPI PSP app requires strict device binding and mobile number verification against the registered wallet phone number.

**User Linking Flow**
*   **Selection:** The customer selects "Add Wallet / Prepaid Account" inside their UPI PSP App (e.g., Paytm, Mobikwik, BHIM).
*   **Account Fetching:** The PSP queries the PPI Issuer via NPCI directory services using the user's bound mobile number.
*   **VPA Mapping:** Upon successful verification, a unique virtual payment handle is associated with the wallet (e.g., user@paytm or user@mobikwik).
*   **Authentication Setup:** The customer sets or verifies their wallet authorization credentials (wallet passcode, biometric lock, or 2FA PIN depending on issuer setup).

#### 2. Wallet Top-Up (Loading) Rules & Restrictions

To maintain financial system stability and prevent regulatory arbitrage, wallet loading via UPI is strictly regulated:

*   **MCC Tagging:** All wallet top-up transactions are classified under MCC 6540 (POI Funding Transactions / Wallet Load).
*   **RuPay Credit Cards Blocked:** NPCI strictly prohibits loading PPI wallets using RuPay Credit Cards on UPI to prevent un-authorized cash extraction or credit-to-cash laundering.
*   **Pre-Sanctioned Credit Lines Blocked:** Credit lines cannot be used to load wallets.
*   **Permitted Sources:** Wallet loads under MCC 6540 can only be funded via Savings Accounts, Current Accounts, or Overdraft Accounts.
*   **Initiation Flow Restrictions:** Wallet top-ups under MCC 6540 are strictly restricted to Payer-Initiated Intent flows. Dynamic QR and Collect requests are systematically blocked by the NPCI switch for wallet loading.

#### 3. Interoperable P2M Transaction Journey

When a customer pays a merchant using their linked PPI Wallet balance:

*   **Checkout Initiation:** The customer scans any interoperable merchant UPI QR code (BharatQR / Dynamic QR) or clicks a UPI Intent link on a merchant app/website.
*   **Instrument Selection:** On the payment screen, the customer selects their PPI Wallet as the preferred funding source instead of their savings bank account.
*   **Balance Validation:** The Payer PSP verifies that the wallet has sufficient stored balance for the order.
*   **Authorization:** Depending on the wallet issuer configuration, transactions ≤ ₹2,000 are executed via 1-click biometric/app passcode authentication or wallet PIN. Transactions > ₹2,000 are validated via two-factor authorization required by the issuer.
*   **Real-time Settlement Signal:** The PPI Issuer debits the wallet ledger, and NPCI routes the success authorization message to Cashfree / Acquiring Bank.

#### 4. Interchange Fee Structure & Merchant Economics

Unlike standard savings account UPI transactions (which carry 0% MDR for merchants), PPI interoperable P2M transactions incur an Interchange Fee paid by the acquiring entity/merchant to the wallet issuer to cover credit, fraud, and infrastructure costs.

**NPCI Interchange Fee Slabs for PPI Merchant Transactions**

| Transaction Type / Industry Category | MCC Scope | Transaction Ceiling | Interchange Fee |
| :--- | :--- | :--- | :--- |
| Standard Retail & E-Commerce | 5411, 5311, 5651, etc. | ≤ ₹2,000 | 0.0% (Free) |
| Standard Retail & E-Commerce | Standard Merchant MCCs | > ₹2,000 | 1.1% |
| Fuel Stations | 5541, 5542 | Any Amount | 0.5% |
| Utilities & Telecom | 4900, 4814 | Any Amount | 0.7% |
| Educational Services | 8211, 8220, 8299 | Any Amount | 0.7% |
| Agriculture & Mutual Funds | 0742, 6211 (select) | Any Amount | 0.7% |

**Key Merchant Rules for PPI Acceptance**
*   **Interoperable Acceptance by Default:** Merchants enabled for dynamic UPI checkouts natively accept wallet-funded payments without extra integration.
*   **No Consumer Surcharging:** Merchants are strictly prohibited from charging an extra convenience fee or surcharge to customers who choose to checkout using PPI wallets.
*   **P2P & P2PM Blocked:** Interoperable PPI wallet transactions are restricted to verified commercial merchants (P2M). Peer-to-Peer (P2P) and unverified small merchant (P2PM) transfers via PPI are blocked on the network switch.

#### 5. Refunds & Post-Transaction Lifecycle

*   **Automated Source Refunds:** When a merchant issues a refund for a PPI-funded transaction, Cashfree and NPCI route the refund strictly back to the originating wallet ID.
*   **UDIR Framework Integration:** All PPI wallet dispute resolutions, failed transaction reversals, and pending status checks are fully integrated into NPCI's Unified Dispute and Issue Resolution (UDIR) system.
*   **Wallet Credit Limits:** If a refund causes the customer's monthly wallet holding limit to be exceeded, the PPI issuer holds the refund in a pending staging ledger and notifies the user to upgrade or clear balance per RBI guidelines.