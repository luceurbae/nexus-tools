# Nexus Bot

The **Nexus Bot** is a Python script designed to automate interactions with the Nexus platform. It provides features for email verification, automatic point claiming, and wallet balance checking. The bot uses the `rich` library to offer a visually appealing terminal interface with colored text, tables, and panels for an enhanced user experience.

## Features

### 1. Email Verification
### 2. Claim Points (Auto Looping)
### 3. Check Balance

## Prerequisites
- **Register nexus here: https://app.nexus.xyz**

## Installation

### Step 1: Clone the Repository
Clone the repository to your local machine:
```bash
git clone https://github.com/luceurbae/nexus-tools.git
cd nexus-tools
```

### Step 2: Install Dependencies
The repository includes a requirements.txt file listing the required libraries (requests and rich). Install them using
```bash
pip install -r requirements.txt #or use python3 install -r requirements.txt for linux/mac
```
### Step 3: Prepare email.txt 
Create a file named email.txt in the repository directory.
Add a single valid email address (e.g., user@example.com) without trailing spaces or newlines.
Example:
```
user@example.com
```

### Usage
### Step 1: Run the Script From the repository directory, run:
```bash
python bot.py
```
Step 2: Select a Feature The script will display a menu:
```
Current time: 02:20 PM 06-07-2025
╭─────────────── Feature Menu ───────────────╮
│                                            │
│    No    Feature                           │
│    1     Email Verification                │
│    2     Claim Points (Auto Looping)       │
│    3     Check Balance                     │
│    4     Exit                              │
│                                            │
╰────────────────────────────────────────────╯
Select feature (1-4):
```
Enter the number corresponding to the desired feature.

### Feature Usage Examples
### Email Verification (Option 1) Select 1.
Check your email for the OTP (including spam/junk folder).
Enter the OTP when prompted.
Example output:
```
Email: user@example.com
Email verification sent successfully. Check your email for OTP.
Please check your email for the OTP.
Enter the OTP received: 123456
Verification completed. Response saved to account.json.
```
### Claim Points (Option 2) Select 2.
Enter minimum and maximum delays (e.g., 200 and 300 seconds).
The bot will claim points automatically with random delays.
Stop with Ctrl+C.
Example output:
```
Enter minimum delay (seconds): 200
Enter maximum delay (seconds): 300
[14:20:00] Claiming points...
Points successfully claimed.
Waiting 245 seconds before next claim...
```
### Check Balance (Option 3) Select 3.
Example output:
```
Wallet balance: 1.2345 NEX
```
### Exit (Option 4)Select 4 to terminate the program.

### Buy me a coffee 🍵
Address:
- ETH: 0xadc855ccdd9e7da48755bc507cefe65103b7d025
- SOL: 52E7popE1gdqnTAsVTLJLBSVWdawZtCUHRLwowfvtcD
