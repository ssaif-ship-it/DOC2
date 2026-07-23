Unlike traditional card networks, UPI operates on a streamlined, interoperable **4-Pillar Model**.

This architecture is orchestrated entirely by the **NPCI** through a central routing engine known as the **UPI Switch**.

### The 4 Pillars of a UPI Transaction

1. **Payer PSP (Payment Service Provider):** The consumer-facing application (e.g., GPay, PhonePe). It captures the PIN but never touches the money.
2. **Remitter Bank (Issuer Bank):** The bank where the customer holds their account. It verifies the PIN and authorizes the debit.
3. **Payee PSP (The Aggregator/Acquiring Bank):** This is the layer your Payment Aggregator operates in. It generates the payment request and normalizes the payload.
4. **Beneficiary Bank:** The bank where the merchant's account is held.

### Real-Time vs. Batch

* **Authorization is Real-Time (Milliseconds):** When a user hits "Pay," the NPCI Switch coordinates the debit/credit messaging in under 3 seconds. You fulfill the order based on this Webhook.
* **Settlement is Batched (T+1):** The physical cash has not yet moved. The actual transfer of funds happens in massive batches behind the scenes settling to your account on a T+1 cycle.
<img width="859" height="516" alt="Screenshot 2026-07-23 at 12 57 41 PM" src="https://github.com/user-attachments/assets/049ca0d5-7352-4886-b824-e8ada7839fd4" />