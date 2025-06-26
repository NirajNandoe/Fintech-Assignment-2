# Topic tags: conversion, stablecoin, onramp, offramp, rates, fees

import random
from src.config import ONRAMP_PROVIDERS, OFFRAMP_PROVIDERS

# This module contains utility functions for handling conversions and generating summaries.
# The function creates a detailed summary of the conversion process, including the stablecoin used, onramp and offramp providers, rates, fees, and customer amounts.
# This summary is used to display the detailed conversion information in the user interface for each invoice that has been created. 
def get_conversion_summary(conversion_details):
    """Generate detailed conversion summary for UI display"""
    return {
        "stablecoin": conversion_details.get("stablecoin", "N/A"),
        "onramp_provider": conversion_details.get("onramp_provider", random.choice(ONRAMP_PROVIDERS)),
        "offramp_provider": conversion_details.get("offramp_provider", random.choice(OFFRAMP_PROVIDERS)),
        "onramp_rate": conversion_details.get("onramp_rate", 0),
        "offramp_rate": conversion_details.get("offramp_rate", 0),
        "onramp_fee": conversion_details.get("onramp_fee", 0),
        "offramp_fee": conversion_details.get("offramp_fee", 0),
        "company_fee": conversion_details.get("company_fee", 0),
        "customer_amount": conversion_details.get("customer_amount", 0),
        "customer_currency": conversion_details.get("customer_currency", "USD")
    }
