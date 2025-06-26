# Topic tags: invoice, payment, settlement, business, customer
import uuid

# This module provides functions to create and manage invoices.
# The def create_invoice function generates a new invoice with the provided details, including business and customer information, line items, and VAT calculations.
# The function calulcates the subtotal by summing the amounts of all line items, calculates the VAT amount based on the provided VAT rate, and computes the total amount due.
# The function generates a invoice ID using the uuid package to ensure each invoice is unique.
# The initila status of the invoice is set to "UNPAID", and it includes fields for route details and conversion details, which can be updated later when the invoice is paid.
def create_invoice(
    business, business_address, business_email, business_vat,
    customer, customer_address, customer_email, customer_vat,
    invoice_number, date, due_date, payment_terms, line_items, vat_rate, currency
):
    subtotal = sum(item["amount"] for item in line_items)
    vat_amount = subtotal * vat_rate / 100
    total = subtotal + vat_amount
    return {
        "id": str(uuid.uuid4()),
        "invoice_number": invoice_number,
        "business": business,
        "business_address": business_address,
        "business_email": business_email,
        "business_vat": business_vat,
        "customer": customer,
        "customer_address": customer_address,
        "customer_email": customer_email,
        "customer_vat": customer_vat,
        "date": str(date),
        "due_date": str(due_date),
        "payment_terms": payment_terms,
        "line_items": line_items,
        "subtotal": subtotal,
        "vat_rate": vat_rate,
        "vat_amount": vat_amount,
        "total": total,
        "currency": currency,
        "status": "UNPAID",
        "route_details": "",
        "conversion_details": {},
    }

# This module provides a function to mark an invoice as paid and generate a settlement record.
# This code simulates the payment of an invoice by updating its status to "PAID" and storing the details of the payment, 
# including the stablecoin used, amounts, fees, and conversion details.
# The invoice status ius set to "PAID", and the route details and conversion details are updated with the provided information.
# The ouput consits of a settlement dictionary that includes all relevant information about the payment, such as the invoice ID, business and customer details, 
# amounts in stablecoin, fees, and conversion details.
def pay_invoice(invoice, stablecoin, stablecoin_amount, usd_received, customer_currency, customer_amount, company_fee, onramp_fee, offramp_fee, route_details, conversion_details):
    invoice["status"] = "PAID"
    invoice["route_details"] = route_details
    invoice["conversion_details"] = conversion_details
    settlement = {
        "invoice_id": invoice["id"],
        "invoice_number": invoice["invoice_number"],
        "business": invoice["business"],
        "business_address": invoice["business_address"],
        "business_email": invoice["business_email"],
        "business_vat": invoice["business_vat"],
        "customer": invoice["customer"],
        "customer_address": invoice["customer_address"],
        "customer_email": invoice["customer_email"],
        "customer_vat": invoice["customer_vat"],
        "date": invoice["date"],
        "due_date": invoice["due_date"],
        "payment_terms": invoice["payment_terms"],
        "subtotal": invoice["subtotal"],
        "vat_rate": invoice["vat_rate"],
        "vat_amount": invoice["vat_amount"],
        "total": invoice["total"],
        "currency": invoice["currency"],
        "customer_currency": customer_currency.upper(),
        "customer_amount": customer_amount,
        "stablecoin": stablecoin.upper(),
        "amount_stablecoin": stablecoin_amount,
        "usd_received": usd_received,
        "company_fee": company_fee,
        "onramp_fee": onramp_fee,
        "offramp_fee": offramp_fee,
        "route_details": route_details,
        "conversion_details": conversion_details,
        "status": "PAID"
    }
    return settlement
