# Nexus Bot

The **Nexus Bot** is a Python script designed to automate interactions with the Nexus platform, including email verification, automatic point claiming, and wallet balance checking. The script uses the `rich` library to provide a visually appealing terminal interface with colored text, tables, and panels for a better user experience.

## Features
1. **Email Verification**  
   Reads an email address from `email.txt`, sends a verification request to the Nexus API, and completes the process using an OTP provided by the user. The response, including a JWT token, is saved to `account.json`.

2. **Claim Points (Auto Looping)**  
   Automatically claims points using the JWT token from `account.json`. Users can specify a minimum and maximum delay (in seconds) for random intervals between claims. The loop continues until stopped with `Ctrl+C`.

3. **Check Balance**  
   Retrieves the wallet balance in ETH from the Nexus testnet, using the wallet address stored in `account.json`.

## Prerequisites
To run the Nexus Bot, ensure you have the following:

1. **Python 3.6 or Higher**  
   Install Python from [python.org](https://www.python.org/downloads/) or your system's package manager (e.g., `apt`, `brew`).

2. **Required Python Libraries**  
   Install the `requests` and `rich` libraries using pip:
   ```bash
   pip install -r requirements.txt #or use python3 install -r requirements.txt for linux/mac
