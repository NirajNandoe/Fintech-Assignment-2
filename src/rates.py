# Topic tags: rates, exchange rates, stablecoin, fiat currency, API


import requests
import random
from src.config import *

# This module contains functions to fetch exchange rates and calculate the best stablecoin route for invoice payments.
# It retrieves the fiat to USD rate, stablecoin to USD rates, and determines the best stablecoin route based on fees and customer amounts through API calls.
# Furthermore, it calculates the necessary amounts in stablecoins and USD, taking into account onramp and offramp fees, as well as company fees.
# The def get_fiat_to_usd_rate function fetches the exchange rate for a given fiat currency to USD.
# I f currency is already in USD, it returns 1.0. Otherwise, it makes an API call to retrieve the exchange rate from a public currency API.
def get_fiat_to_usd_rate(currency):
    if currency.lower() == "usd":
        return 1.0
    url = f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/{currency.lower()}.json"
    try:
        resp = requests.get(url, timeout=5)
        data = resp.json()
        return data[currency.lower()]["usd"]
    except Exception:
        return None
# The def get_usd_to_stablecoin_rates function fetches the current USD price for each of the specified and supported stablecoins.
# The code calls the CoinGecko API to retrieve the exchange rates for the specified stablecoins against USD.
# The code maps the stablecoin to its USD rate and returns a dictionary with the stablecoin as the key and its USD rate as the value.
def get_usd_to_stablecoin_rates(stablecoins):
    url = "https://api.coingecko.com/api/v3/simple/price"
    ids = ",".join(stablecoins)
    params = {"ids": ids, "vs_currencies": "usd"}
    try:
        resp = requests.get(url, params=params, timeout=5)
        data = resp.json()
        return {coin: data[coin]["usd"] for coin in stablecoins if coin in data}
    except Exception:
        return {coin: None for coin in stablecoins}
# The def get_best_stablecoin_route function calculates the best stablecoin route for a given invoice amount in USD.
# The code retrieves the fiet to USD exchange rate for the customer's currency and the USD to stablecoin rates.
# For each stablecoin, it calculates the onramp and offramp rates, the amount of stablecoin needed, and the fees involved.
# It then determines the best stablecoin route based on the lowest customer amount required to pay the invoice, inlcuding the provider with the best rates.
# The function rutrns the most cost-effective route and its details with the `best` code.
# The `details` code summarizes the details for each conversion route and the `all_conversion_details` code contains detailed conversion information for each stablecoin.
def get_best_stablecoin_route(invoice_usd, customer_currency, stablecoins):
    fiat_to_usd = get_fiat_to_usd_rate(customer_currency)
    stablecoin_rates = get_usd_to_stablecoin_rates(stablecoins)
    best = None
    details = []
    all_conversion_details = {}

    for coin, usd_per_stable in stablecoin_rates.items():
        if not usd_per_stable or usd_per_stable == 0:
            continue

        onramp_rate = usd_per_stable * (1 + ONRAMP_SPREAD_PCT)
        offramp_rate = usd_per_stable * (1 - OFFRAMP_SPREAD_PCT)
        stablecoin_needed = invoice_usd / offramp_rate

        company_fee = invoice_usd * PLATFORM_FEE_PCT
        onramp_fee = stablecoin_needed * (onramp_rate - usd_per_stable)
        offramp_fee = stablecoin_needed * (usd_per_stable - offramp_rate)
        usd_needed = stablecoin_needed * onramp_rate

        if fiat_to_usd and fiat_to_usd > 0:
            customer_amount = usd_needed / fiat_to_usd
        else:
            continue

        route_str = (
            f"{coin.upper()}: {customer_amount:.2f} {customer_currency.upper()} (onramp fee: {onramp_fee:.2f} USD, "
            f"offramp fee: {offramp_fee:.2f} USD, company fee: {company_fee:.2f} USD)"
        )
        conversion_details = {
            "stablecoin": coin.upper(),
            "customer_amount": customer_amount,
            "stablecoin_needed": stablecoin_needed,
            "usd_received": invoice_usd,
            "onramp_provider": random.choice(ONRAMP_PROVIDERS),
            "offramp_provider": random.choice(OFFRAMP_PROVIDERS),
            "onramp_rate": onramp_rate,
            "offramp_rate": offramp_rate,
            "customer_currency": customer_currency,
            "usd_per_stable": usd_per_stable,
            "company_fee": company_fee,
            "onramp_fee": onramp_fee,
            "offramp_fee": offramp_fee,
            "conversion_costs": {
                "onramp": onramp_fee,
                "offramp": offramp_fee,
                "company": company_fee,
                "total_fees": onramp_fee + offramp_fee + company_fee
            }
        }
        all_conversion_details[coin] = conversion_details
        details.append(route_str)
        if (best is None) or (customer_amount < best["customer_amount"]):
            best = {
                "stablecoin": coin,
                "customer_amount": customer_amount,
                "stablecoin_needed": stablecoin_needed,
                "usd_needed": usd_needed,
                "company_fee": company_fee,
                "onramp_fee": onramp_fee,
                "offramp_fee": offramp_fee,
                "stablecoin_needed_with_fees": stablecoin_needed,
                "route_details": route_str,
                "conversion_details": conversion_details
            }
    return best, details, all_conversion_details
