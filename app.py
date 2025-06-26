# Topic tags: Streamlit, invoices, ledger, stablecoins, smart contracts, ERP

import streamlit as st
import os
import pandas as pd
import datetime
# This is the main application file for the Crossover Solutions platform.
# It provides a user interface for creating invoices, viewing invoices and ledger entries, and simulating
# payments using stablecoins.
# The application uses Streamlit for the user interface. 
from src.config import *
from src.storage import load_json, save_json
from src.invoice import create_invoice, pay_invoice
from src.rates import get_best_stablecoin_route
from src.pdf_utils import generate_invoice_pdf
from src.email_utils import send_invoice_email
from src.smart_contract import generate_smart_contract_details

# This code initializes the Streamlit application and sets up the session state for line items.
# It checks if the session state for line items exists, and if not, initializes it with a default line item.
if 'line_items' not in st.session_state:
    st.session_state.line_items = [{'description': '', 'amount': 0.0}]

def add_line_item():
    st.session_state.line_items.append({'description': '', 'amount': 0.0})

def remove_line_item(index):
    if len(st.session_state.line_items) > 1:
        st.session_state.line_items.pop(index)

st.set_page_config(page_title="Crossover Solutions", page_icon="💸", layout="wide")
st.sidebar.image("logo.png", width=150)

os.makedirs(DATA_DIR, exist_ok=True)
invoices = load_json(INVOICE_FILE)
ledger = load_json(LEDGER_FILE)

tab1, tab2, tab3, tab4 = st.tabs(["Create Invoice", "Invoices", "Ledger", "ERP System"])
# This code creates the main tabs for the Streamlit application.
# The tab1 is used for invoice creation, with dynamic lining making it possible to add or remove lines.
# The code collects the details of the customers, creates and invoice and saves it to the JSON file.
with tab1:
    st.header("Create Invoice")
    st.button('Add Line Item', on_click=add_line_item)
    for i, item in enumerate(st.session_state.line_items):
        cols = st.columns([3, 1, 1])
        with cols[0]:
            st.session_state.line_items[i]['description'] = st.text_input(
                f'Description {i+1}', value=item['description'], key=f'desc_{i}')
        with cols[1]:
            st.session_state.line_items[i]['amount'] = st.number_input(
                f'Amount {i+1}', min_value=0.0, value=item['amount'], step=0.01, key=f'amt_{i}')
        with cols[2]:
            if st.button('Remove', key=f'remove_{i}'):
                remove_line_item(i)
                st.experimental_rerun()
    with st.form("invoice_form"):
        business = st.text_input("Business Name", value=COMPANY_NAME)
        business_address = st.text_input("Business Address", value=COMPANY_ADDRESS)
        business_email = st.text_input("Business Email", value=COMPANY_EMAIL)
        business_vat = st.text_input("Business VAT", value=COMPANY_VAT)
        customer = st.text_input("Customer Name")
        customer_address = st.text_input("Customer Address")
        customer_email = st.text_input("Customer Email")
        customer_vat = st.text_input("Customer VAT")
        invoice_number = st.text_input("Invoice Number", value=f"INV{len(invoices)+1:04d}")
        date = st.date_input("Invoice Date", value=datetime.date.today())
        due_date = st.date_input("Due Date", value=datetime.date.today() + datetime.timedelta(days=30))
        payment_terms = st.text_input("Payment Terms", value="30 days")
        vat_rate = st.number_input("VAT Rate (%)", min_value=0.0, max_value=25.0, value=21.0)
        currency = st.selectbox("Invoice Currency", SUPPORTED_CURRENCIES, index=0)
        submitted = st.form_submit_button('Create Invoice')
        if submitted:
            line_items = [
                {'description': li['description'], 'amount': li['amount']}
                for li in st.session_state.line_items
                if li['description'] or li['amount'] > 0
            ]
            if not line_items:
                st.error("Please add at least one line item.")
            else:
                inv = create_invoice(
                    business, business_address, business_email, business_vat,
                    customer, customer_address, customer_email, customer_vat,
                    invoice_number, str(date), str(due_date), payment_terms, line_items, vat_rate, currency
                )
                invoices.append(inv)
                save_json(INVOICE_FILE, invoices)
                filename = f"invoice_{inv['invoice_number']}_business.pdf"
                generate_invoice_pdf(inv, {}, filename)
                st.success("Invoice created and sent to company email!")
                st.session_state.line_items = [{'description': '', 'amount': 0.0}]
# This code creates the second tab for viewing invoices.
# The tab2 displays all created invoices.
# The tab2 allows for simulating of the payment in the currency selected by the customer.
# It then calucltes the best stablecoin route with the fetched rates and simulates the payment.
# The invoice status is updated to "PAID" and the settlement details are saved to the ledger.
# Furthermore, it provides options to download the invoice as a PDF and email it to the customer.
# The tab2 also displays the conversion details and generates a smart contract for the payment.
with tab2:
    st.header("Invoices")
    if invoices:
        for i, inv in enumerate(invoices):
            with st.expander(f"Invoice {i+1} ({inv['invoice_number']}) - {inv['status']}"):
                st.write(f"**Business:** {inv['business']}  \n**Customer:** {inv['customer']}  \n**Amount:** {inv['total']} {inv['currency']}")
                st.write(f"**Business Email:** {inv['business_email']}  \n**Customer Email:** {inv['customer_email']}")
                st.write(f"**Business Address:** {inv['business_address']}  \n**Customer Address:** {inv['customer_address']}")
                st.write(f"**Invoice Date:** {inv['date']}  \n**Due Date:** {inv['due_date']}  \n**Payment Terms:** {inv['payment_terms']}")
                st.write(f"**Line Items:**")
                for item in inv["line_items"]:
                    st.write(f"- {item['description']}: {item['amount']} {inv['currency']}")
                st.write(f"**Subtotal:** {inv['subtotal']} {inv['currency']}  \n**VAT ({inv['vat_rate']}%):** {inv['vat_amount']} {inv['currency']}  \n**Total:** {inv['total']} {inv['currency']}")
                if inv["status"] == "UNPAID":
                    customer_currency = st.selectbox(
                        f"Customer payment currency for invoice {i+1}",
                        SUPPORTED_CURRENCIES, key=f"currency_{i}"
                    )
                    if st.button(f"Simulate Payment for Invoice {i+1}"):
                        best, details, all_conversion_details = get_best_stablecoin_route(
                            invoice_usd=inv["total"],
                            customer_currency=customer_currency,
                            stablecoins=STABLECOINS
                        )
                        if not best:
                            st.error("Could not fetch live rates or no stablecoin route available.")
                            continue
                        # Simulate payment and update invoice
                        settlement = pay_invoice(
                            inv,
                            best["stablecoin"],
                            best["stablecoin_needed"],
                            inv["total"],
                            customer_currency,
                            best["customer_amount"],
                            best["company_fee"],
                            best["onramp_fee"],
                            best["offramp_fee"],
                            best["route_details"],
                            best["conversion_details"]
                        )
                        ledger.append(settlement)
                        save_json(LEDGER_FILE, ledger)
                        save_json(INVOICE_FILE, invoices)
                        st.success(
                            f"Customer pays: {best['customer_amount']:.2f} {customer_currency.upper()} "
                            f"(via {best['stablecoin'].upper()} route, incl. all provider fees). "
                            f"Company receives exactly {inv['total']:.2f} USD (company fee: {best['company_fee']:.2f} USD)."
                        )
                        st.info("Conversion options:\n" + "\n".join(details))
                else:
                    cd = inv.get("conversion_details", {})
                    st.markdown("#### Conversion Summary")
                    st.write(f"**Stablecoin Used:** {cd.get('stablecoin','')}")
                    st.write(f"**On-Ramp Provider:** {cd.get('onramp_provider','')}")
                    st.write(f"**Off-Ramp Provider:** {cd.get('offramp_provider','')}")
                    st.write(f"**On-Ramp Rate:** {cd.get('onramp_rate',0):.6f}")
                    st.write(f"**Off-Ramp Rate:** {cd.get('offramp_rate',0):.6f}")
                    st.write(f"**On-Ramp Fee:** {cd.get('onramp_fee',0):.2f} USD")
                    st.write(f"**Off-Ramp Fee:** {cd.get('offramp_fee',0):.2f} USD")
                    st.write(f"**Company Fee:** {cd.get('company_fee',0):.2f} USD")
                    st.write(f"**Total Conversion Fees:** {cd.get('conversion_costs',{}).get('total_fees',0):.2f} USD")
                    st.write(f"**Customer Paid:** {cd.get('customer_amount',0):.2f} {cd.get('customer_currency','')}")

                    st.subheader("Smart Contract Execution")
                    contract_details = generate_smart_contract_details(cd)
                    st.json(contract_details)

                    business_pdf = f"invoice_{inv['invoice_number']}_business.pdf"
                    customer_pdf = f"invoice_{inv['invoice_number']}_customer.pdf"
                    generate_invoice_pdf(inv, cd, business_pdf, "business")
                    generate_invoice_pdf(inv, cd, customer_pdf, "customer")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        with open(business_pdf, "rb") as f:
                            st.download_button(
                                label="Download Business PDF",
                                data=f,
                                file_name=business_pdf,
                                mime="application/pdf"
                            )
                    with col2:
                        with open(customer_pdf, "rb") as f:
                            st.download_button(
                                label="Download Customer PDF",
                                data=f,
                                file_name=customer_pdf,
                                mime="application/pdf"
                            )
                    with col3:
                        if st.button(f"Email to Customer", key=f"email_{i}"):
                            if send_invoice_email(inv, customer_pdf, "customer"):
                                st.success(f"Invoice sent to {inv['customer_email']}")
    else:
        st.info("No invoices yet.")
# This code creates the third tab for viewing the ledger.
# The tab3 displays all ledger entries, which include settlement details for paid invoices in a tabular format.
with tab3:
    st.header("Ledger")
    if ledger:
        st.dataframe(pd.DataFrame(ledger))
    else:
        st.info("No ledger entries yet.")
# This code creates the fourth tab for the ERP system.
# The tab4 displays the API endpoints for the ERP system and shows the invoices and ledger entries
# The tab4 allows for the download of invoices and ledger entries as CSV files.
# Lastly, it simulates an ERP system view. 
with tab4:
    st.header("ERP System")
    st.subheader("API Endpoints:")
    st.code("GET /api/invoices\nGET /api/ledger\nGET /api/smart-contracts")
    if invoices:
        st.subheader("ERP: All Invoices")
        st.dataframe(pd.DataFrame(invoices))
        st.subheader("ERP: Ledger")
        st.dataframe(pd.DataFrame(ledger))
    else:
        st.info("ERP: No invoices yet.")
