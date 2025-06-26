# Topic tags: ledger
# This module provides functions to manage a simple ledger.
# the add_entry function allows adding a new entry to the ledger, and the get_ledger function retrieves the current state of the ledger.
def add_entry(ledger, entry):
    ledger.append(entry)

def get_ledger(ledger):
    return ledger
