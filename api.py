# Topic tags: API, FastAPI, invoices, ledger, smart contracts

from fastapi import FastAPI
from src.config import INVOICE_FILE, LEDGER_FILE
from src.storage import load_json
# This code creates a FastAPI web application that provides API endpoitns to retrieve invoices, ledger entries, and smart contracts.
# This API allows for ERP & accounting integrations and allows for external reporting. 
# The API endpoints are designed to be simple and easy to use, allowing for quick access to the data stored in the invoices and ledger files.
app = FastAPI()

@app.get("/api/invoices")
def get_invoices():
    return load_json(INVOICE_FILE)

@app.get("/api/ledger")
def get_ledger():
    return load_json(LEDGER_FILE)

@app.get("/api/smart-contracts")
def get_smart_contracts():
    ledger = load_json(LEDGER_FILE)
    return [entry for entry in ledger if "conversion_details" in entry]
