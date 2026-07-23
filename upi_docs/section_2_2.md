Flash UPI provides merchants with the functionality to accept UPI payments within the merchant's app without any redirection to PSPs like Google Pay, PhonePe, etc. This will increase the payment success rate for merchants.

### Customer Flow

**Returning customer who registered earlier:**
1. The customer lands on the merchant’s checkout page and selects Flash UPI.
2. Customer enters UPI PIN to complete the payment.

**The customer has an existing VPA with the partner bank:**
1. The customer lands on the merchant’s checkout page and selects ‘Add Bank Account’.
2. The customer selects the sim and gives permission to send text messages. This triggers device binding.
3. Customer’s bank account details are fetched and linked to the VPA.
4. Customer enters UPI PIN to complete the payment.

**The customer doesn't have an existing VPA with the partner bank but has used UPI via some other bank/PSP:**
1. The customer lands on the merchant’s checkout page and selects ‘Add Bank Account’.
2. The customer selects the sim and gives permission to send text messages. This triggers device binding.
3. Customer selects a bank from the available banks - All accounts with that bank are fetched.
4. We create a new VPA with `mobilenumber@axis` and link accounts which have a UPI PIN already set.
5. The customer enters UPI PIN to complete the payment.

**The customer never used UPI:**
1. The customer lands on the merchant’s checkout page and selects ‘Add Bank Account’.
2. The customer selects the sim and gives permission to send text messages. This triggers device binding.
3. Customer selects a bank from the available banks - All accounts with that bank are fetched.
4. The customer is prompted to provide their debit card details and enter an OTP to complete the setup.
5. The customer enters UPI PIN to complete the payment.

### Benefits

* **Faster and Smooth Customer Experience**
* **Higher Success Rates (by 4-5%):** With lesser opportunities for customers to drop off in the payment experience.
* **Complete In-App Flow:** With no redirections, you gain much better control over the user journey.
* **Eliminates Third-Party Dependencies:** Transactions do not need to be routed via external UPI applications, which reduces timeout issues significantly and gives you more visibility on payment failures.
