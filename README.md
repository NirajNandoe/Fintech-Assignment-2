## Author
Niraj Nandoe (700368)
700368nn@student.eur.nl

----------------------------------------------------------------------------------------------------------------------------

## Overview
Crossover Solutions is a Fintech startup that aims at automating and innovating cross-border payments for SME's using Blockchain technology.
By implementing stablecoins, smart contracts, and on- and off-ramp providers, we aim to achieve fast conversions against the lowest costs.
All while allowing customers to pay in the currencies they prefer, and companies to get paid in the currency that they prefer.
Furthermore, Crossover Solutions provides a automated invoicing system that creates invoices and automatically sends them to the customers.
The invoicing system tracks the payment status of the invoices and which payment route has been chosen.
The final data is bundled in a ledger and can be accesed through our API, allowing for compatability with ERP and accouting sytems. 

----------------------------------------------------------------------------------------------------------------------------

## Table of Contents
- Features
- Architecture
- Comparison to the business plan
- Technology
- How to Run
- Usage
- Technical Implications and Risk
- License



----------------------------------------------------------------------------------------------------------------------------

## Features
The Crossover Solution MVP platform contains the following features:
- Multi-currency payment support and invoice creation. Dynamic lines make it able to expand the invoices as desired.
- Automated payments are simulated with live rates provided to an API connection, allowing for identifaction of the best stablecoin conversion routes.
- The conversion is transaparantly broken down and insight is provided into the chosen on/off-ramp providers, stablecoin, the rate, and the total fees.
- The smart contract settlement is simulated and visible in the User Interface, simulating how the smart contract would settle in real-world applications.
- PDF invoice creation and export to customers through automated emails.
- A transparent ledger in which all invoices are saved. These invoices can be downloaded as a csv file.
- ERP compatible API endpoints for fast connection.
- Clean User Interface with multiple tabs, improving user experience.

----------------------------------------------------------------------------------------------------------------------------

## Architecture
The Crossover Solutions MVP makes use of the following architectures:
- The Backend: Python and FastAPI (FastAPI allows for ERP compatibility).
- The Frontend: Streamlit (Streamlit allows web interface of the MVP).
- Data Storage: JSON files for the invoices and the ledger.
- Modules:
    - invoice.py: Creates and manages the invoices.
    - rates.py: Fetches the live rates and applies the conversions between currencies.
    - pdf_utils.py: Generates the invoices in PDF format.
    - smart_contracts.py: Simulates the settlement of smart contracts.
    - email_utils.py: Simulates the automatic emails.
    - storage.py: Allows for data storage.
    - config.py: Defines the base characters.
- The MVP is a procedural paradigm, as the code is written as reusable functions.

----------------------------------------------------------------------------------------------------------------------------

## Comparison to the business plan
- The on- and off-ramp and DeFi pool technology is fullt automated and simulated wihtin the MVP. This process offers transparency in the chosen conversion routes.
- All blockchain and smart contract interaction, is hidden from the user, disregarding the need of technological knowledge.
- Built in API endpoints allowing for full ERP compatiblity. 

----------------------------------------------------------------------------------------------------------------------------

## Technology
- Programming language: Python 3.11+
- Framework: Streamlit, FastAPI, fpdf, pandas, requests

Python is a widely used langauge in the FinTech industry and enables for quick and high quality software creation.
Streamlit provides a fast GUI tht is webbased and can be accessed through a provided link given after running the MVP.
FastAPI allows for secure ERP compatability.

----------------------------------------------------------------------------------------------------------------------------

## How to Run
1. Clone the repository from GitHub
2. Install the dependencies
    - Using "pip install -r requirements.txt" in the temrinal all required packages will be downloaded.
3. Run the Streamlit webapp
    - this is done by typing "streamlit run app.py" in the console and pressing enter afterwards.
4. The app will automatically open in the browers, and the link to the Webapp will be provided.
5. Start the API server
    - by typing "uvicorn api:app-reload" in the console, the API can be started. 

----------------------------------------------------------------------------------------------------------------------------

## Usage
In this step it will be explained how the MVP is supposed to be used.
1. Create an invoice
    - Fill in the required details.
    - Download or email the invoice to the customer.
2. Simulate the payment
    - Choose the currency the customer will pay in.
    - See the chosen conversion path between providers, stablecoins, rates and the fees.
    - The payment is settled via a simulated smart contract, which is visible in the UI.
    - PLEASE NOTE: Simulating the payment requires pressing the simulate buttin twice.
3. After payment settlement
    - Download the PDF of the invoice.
    - Email the proof of payment to the customer.
    - View the smart contract and the used converison rout including chosen provider and total fees
    - Ability to download the transcations in a csv file from the ledger.
4. ERP connection
    - Connect to the API endpoints and view or export all invoices.

----------------------------------------------------------------------------------------------------------------------------

## Technical Implications and risk
Before application in a real-world setting, changes have to be made to the MVP. These changes will be discussed.

- Scaling 
    - Instead of JSON, a database created in SQL is necessary.
    - Real time API connection to providers has to be implemented.
    - The Streamlit webapp has to be deployed in the cloud, this can be for example, Amazon webserver, Google Cloud or Azure.

- Challenges
    - User support, and monitoring the payments.
    - Keeping the software up-to-date.

- Risks
    - Data privacy must be GDPR complied.
    - The API key needs be secure.
    - The smart contracts must be trusted and the vulnerabilities have to be mapped.

----------------------------------------------------------------------------------------------------------------------------

## License
Use is made of a MIT license.
The MIT license is an open-software license that allows anyone to modify and sell software.
