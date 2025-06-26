# Topic tags: PDF, invoice, FPDF

from fpdf import FPDF
from src.config import COMPANY_NAME, COMPANY_ADDRESS, COMPANY_EMAIL, COMPANY_VAT

# This module contains utility functions for generating PDF invoices.
# The code uses the 'fpdf' library to create a PDF document that includes the invoice details. It also adds the company logo to the PDF if available.
# the pdf.image code attempts to load a logo image from the current directory. If the image is not found, it will simply skip adding the logo.
# The "Arial" font is used for the text, with different styles (bold, regular) applied as needed.
# The 0,10 parameters in the pdf.cell method specify the width and height of the cells, while the ln=True parameter indicates that a new line should be started after each cell.
def generate_invoice_pdf(invoice, conversion_details, filename, recipient_type="business"):
    pdf = FPDF()
    pdf.add_page()
    try:
        pdf.image("logo.png", x=10, y=8, w=33)
    except Exception:
        pass
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "INVOICE", 0, 1, "C")
    pdf.ln(5)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"{COMPANY_NAME}", ln=True)
    pdf.cell(0, 10, f"{COMPANY_ADDRESS}", ln=True)
    pdf.cell(0, 10, f"{COMPANY_EMAIL}", ln=True)
    pdf.cell(0, 10, f"VAT: {COMPANY_VAT}", ln=True)
    pdf.ln(10)
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, f"Invoice No: {invoice['invoice_number']}", ln=True)
    pdf.cell(0, 10, f"Date: {invoice['date']}", ln=True)
    pdf.cell(0, 10, f"Due Date: {invoice['due_date']}", ln=True)
    pdf.cell(0, 10, f"Payment Terms: {invoice['payment_terms']}", ln=True)
    pdf.cell(0, 10, f"Status: {invoice['status']}", ln=True)
    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Billed To:", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, f"{invoice['customer']}", ln=True)
    pdf.cell(0, 10, f"{invoice['customer_address']}", ln=True)
    pdf.cell(0, 10, f"{invoice['customer_email']}", ln=True)
    pdf.cell(0, 10, f"VAT: {invoice['customer_vat']}", ln=True)
    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Line Items:", ln=True)
    pdf.set_font("Arial", size=10)
    for item in invoice["line_items"]:
        pdf.cell(0, 8, f"{item['description']}: {item['amount']} {invoice['currency']}", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Totals:", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, f"Subtotal: {invoice['subtotal']} {invoice['currency']}", ln=True)
    pdf.cell(0, 10, f"VAT ({invoice['vat_rate']}%): {invoice['vat_amount']} {invoice['currency']}", ln=True)
    pdf.cell(0, 10, f"Total: {invoice['total']} {invoice['currency']}", ln=True)
    pdf.ln(10)
    if recipient_type == "business" and conversion_details:
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Conversion Details:", ln=True)
        pdf.set_font("Arial", size=10)
        details = [
            f"Stablecoin: {conversion_details.get('stablecoin', 'N/A')}",
            f"On-Ramp Provider: {conversion_details.get('onramp_provider', 'N/A')}",
            f"Off-Ramp Provider: {conversion_details.get('offramp_provider', 'N/A')}",
            f"Conversion Rate: 1 {conversion_details.get('customer_currency', '')} = {1/conversion_details.get('onramp_rate', 1):.6f} {conversion_details.get('stablecoin', '')}",
            f"Fees: ${conversion_details.get('conversion_costs', {}).get('total_fees', 0):.2f}"
        ]
        for detail in details:
            pdf.cell(0, 8, detail, ln=True)
    pdf.output(filename)
