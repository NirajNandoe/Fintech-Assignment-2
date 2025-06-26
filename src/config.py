# Topic tags: configuration, currencies, fees, company details, providers

import os
# This file contains configuration constants for the Crossover Solutions platform.
# This code block defines where the base directory, data directory, invoice files, and ledger are located. 
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
INVOICE_FILE = os.path.join(DATA_DIR, "invoices.json")
LEDGER_FILE = os.path.join(DATA_DIR, "ledger.json")

# This code block defines the supported currencies, stablecoins, platform fees, and company details.
# In a real-world application, these would be loaded and upates through the use of API calls or a database.
# The supported fiat currencies and stablecoins are defined here, along with the platform fee percentage and the onramp/offramp spread percentages.
# The defined currencies and stablecoins would be automatically set in a real-world environment. As this is a demo, they are hardcoded for simplicity, using only 7 currencies
# and 3 stablecoins.
# The platform fee, indicates the 1% fee the using company has to pay Crossover for using the platform.
# The onramp and offramp spread percentages indicate the fees charged by the onramp and offramp providers. 
# In a real-world application, these would be dynamic and updated based on market conditions.
SUPPORTED_CURRENCIES = ["USD", "EUR", "GBP", "INR", "JPY", "AUD", "CAD"]
STABLECOINS = ["usdc", "usdt", "dai"]
PLATFORM_FEE_PCT = 0.01
ONRAMP_SPREAD_PCT = 0.005
OFFRAMP_SPREAD_PCT = 0.005

# This code block defines the billing company details, including the name, address, email, and VAT number.
# These details would be used in the invoice generation and settlement processes.
# In a real-world application, these would be loaded from a configuration file or database.
COMPANY_NAME = "Crossover Solutions"
COMPANY_ADDRESS = "123 Main Street, Rotterdam, Netherlands"
COMPANY_EMAIL = "info@crossover-solutions.com"
COMPANY_VAT = "NL123456789B01"

# This code block defines the onramp and offramp providers.
# These providers would be used in the conversion process to handle the onramp and offramp conversions.
# in a real-world application, the provider with the best rates would be selected dynamically based on market conditions.
ONRAMP_PROVIDERS = ["MoonPay", "Ramp", "Transak"]
OFFRAMP_PROVIDERS = ["Circle", "Binance", "Coinbase"]
