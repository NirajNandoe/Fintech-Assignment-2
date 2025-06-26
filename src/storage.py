# Topic tags: storage, JSON

import json
import os
# This module provides functions to load and save JSON data to files.
# The `load_json` function loads datas from a JSON file at the specified path, allowing for the retrieval of data such as invoices and ledger entries.
# If the file does not exist or is not valid JSON, it returns an empty list. 
# If the file exists and contains valid JSON, it returns the parsed data.
def load_json(path):
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []
# The `save_json` function saves the data as Json to a file at the specified path.
# The code opens the file and rewrites the content to JSON format with an indentation of 2 spaces for readability.
# This function is used to save data such as invoices and ledger entries to a file.
def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
