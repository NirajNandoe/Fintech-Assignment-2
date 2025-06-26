# Topic tags: email, invoice, business, customer
# This module contains utility functions for sending emails related to invoices.
# This is a mock implementation for demonstration purposes.
# The reciepient's email address is determined based on the recipient type, which can be either "business" or "customer".
# The print functions simulate sending an email by printing a message to the console that the email has been sent.
# The return code indicates that the email was sent successfully.
def send_invoice_email(invoice, pdf_filename, recipient_type="business"):
    recipient = invoice["business_email"] if recipient_type == "business" else invoice["customer_email"]
    print(f"Simulated: Invoice {invoice['invoice_number']} sent to {recipient} ({recipient_type} version)")
    return True
