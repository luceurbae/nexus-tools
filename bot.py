import requests
import json
import time
import random
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box


console = Console()


SESSION_PUBLIC_KEY = "020eaa00716dddf9bb0dd0d8c7335b250bf5bbdd31c820d16525892fa0e4df28a3"


def read_email_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            email = file.read().strip()
            if email:
                return email
            else:
                console.print("[red]File email.txt is empty.[/red]")
                return None
    except FileNotFoundError:
        console.print("[red]File email.txt not found.[/red]")
        return None


def start_email_verification(email):
    url = "https://app.dynamicauth.com/api/v0/sdk/adc09cea-6194-4667-8be8-931cc28dacd2/emailVerifications/create"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Mobile Safari/537.36"
    }
    data = {"email": email}
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 201:
            console.print("[green]Email verification sent successfully. Check your email for OTP.[/green]")
            return response.json()
        else:
            console.print(f"[red]Failed to send email verification: {response.status_code} - {response.text}[/red]")
            return None
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Error during request: {e}[/red]")
        return None


def complete_email_verification(verification_uuid, verification_token, session_public_key):
    url = "https://app.dynamicauth.com/api/v0/sdk/adc09cea-6194-4667-8be8-931cc28dacd2/emailVerifications/signin"
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "origin": "https://app.nexus.xyz",
        "priority": "u=1, i",
        "referer": "https://app.nexus.xyz/",
        "sec-ch-ua": "\"Chromium\";v=\"134\", \"Not:A-Brand\";v=\"24\", \"Opera GX\";v=\"119\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Mobile Safari/537.36",
        "x-dyn-api-version": "API/0.0.688",
        "x-dyn-device-fingerprint": "df6a4cb87917e665020eee06567426a4",
        "x-dyn-is-global-wallet-popup": "false",
        "x-dyn-request-id": "P9908aC7BDJUnMdUWkSeoK2wq8bA2lMOQvwEN4174QwIK5OPG8",
        "x-dyn-session-public-key": "03b144ed9eae1620a608bfa6bdfe17a3c3ebcaf8769003771895cba30b4f31517d",
        "x-dyn-version": "WalletKit/4.20.9"
    }
    data = {
        "verificationUUID": verification_uuid,
        "verificationToken": verification_token,
        "sessionPublicKey": session_public_key
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            with open("account.json", "w") as file:
                json.dump(response.json(), file, indent=4)
            console.print("[green]Verification completed. Response saved to account.json.[/green]")
            return response.json()
        else:
            console.print(f"[red]Failed to complete verification: {response.status_code} - {response.text}[/red]")
            return None
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Error during request: {e}[/red]")
        return None


def read_jwt_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            jwt = data.get('jwt')
            if jwt:
                return jwt
            else:
                console.print("[red]JWT token not found in file.[/red]")
                return None
    except FileNotFoundError:
        console.print(f"[red]File {file_path} not found.[/red]")
        return None
    except json.JSONDecodeError:
        console.print("[red]Failed to decode JSON file.[/red]")
        return None


def claim_points(token):
    url = "https://beta.orchestrator.nexus.xyz/v3/points/claim"
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "authorization": f"Bearer {token}",
        "content-length": "0",
        "content-type": "application/octet-stream",
        "origin": "https://app.nexus.xyz",
        "priority": "u=1, i",
        "referer": "https://app.nexus.xyz/",
        "sec-ch-ua": "\"Chromium\";v=\"134\", \"Not:A-Brand\";v=\"24\", \"Opera GX\";v=\"119\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Mobile Safari/537.36"
    }
    try:
        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            if response.text.strip():
                console.print("[green]Points successfully claimed.[/green]")
                return response.json()
            else:
                console.print("[green]Points successfully claimed, but response is empty.[/green]")
                return None
        else:
            console.print(f"[red]Failed to claim points: {response.status_code} - {response.text}[/red]")
            return None
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Error during request: {e}[/red]")
        return None


def check_balance():
    account_file = "account.json"
    try:
        with open(account_file, 'r') as file:
            data = json.load(file)
            wallet_address = data["user"]["verifiedCredentials"][0]["address"]
            if not wallet_address:
                console.print("[red]Wallet address not found in file.[/red]")
                return
    except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
        console.print(f"[red]Error reading account.json: {e}[/red]")
        return

    url = "https://nexus-testnet.g.alchemy.com/public"
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "origin": "https://app.nexus.xyz",
        "priority": "u=1, i",
        "referer": "https://app.nexus.xyz/",
        "sec-ch-ua": "\"Chromium\";v=\"134\", \"Not:A-Brand\";v=\"24\", \"Opera GX\";v=\"119\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Mobile Safari/537.36"
    }
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getBalance",
        "params": [wallet_address, "latest"],
        "id": 1
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            balance_hex = response.json().get("result")
            if balance_hex:
                balance_wei = int(balance_hex, 16)
                balance_eth = balance_wei / 10**18
                console.print(f"[green]Wallet balance: {balance_eth:.4f} ETH[/green]")
            else:
                console.print("[red]Failed to retrieve balance.[/red]")
        else:
            console.print(f"[red]Failed to check balance: {response.status_code} - {response.text}[/red]")
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Error during request: {e}[/red]")


def perform_email_verification():
    email_file = "email.txt"
    email = read_email_from_file(email_file)
    if email is None:
        return
    console.print(f"[cyan]Email: {email}[/cyan]")
    verification_data = start_email_verification(email)
    if verification_data is None or "verificationUUID" not in verification_data:
        console.print("[red]Failed to start email verification.[/red]")
        return
    verification_uuid = verification_data["verificationUUID"]
    console.print("[yellow]Please check your email for the OTP.[/yellow]")
    verification_token = input("Enter the OTP received: ").strip()
    complete_email_verification(verification_uuid, verification_token, SESSION_PUBLIC_KEY)

def auto_claim_points(token, min_delay, max_delay):
    if min_delay > max_delay:
        console.print("[red]Minimum delay cannot be greater than maximum delay.[/red]")
        return
    try:
        while True:
            console.print(f"\n[blue][{datetime.now().strftime('%H:%M:%S')}] Claiming points...[/blue]")
            claim_points(token)
            delay = random.randint(min_delay, max_delay)
            console.print(f"[yellow]Waiting {delay} seconds before next claim...[/yellow]")
            time.sleep(delay)
    except KeyboardInterrupt:
        console.print("[red]\nAuto claim stopped by user.[/red]")


def main_menu():
    while True:
        console.print(Panel("[bold blue]=== Nexus Auto Bot by zaluce ===[/bold blue]", box=box.ROUNDED))
        table = Table(show_header=False, box=box.SIMPLE)
        table.add_column("No", style="cyan", justify="center")
        table.add_column("Feature", style="green")
        table.add_row("1", "Email Verification")
        table.add_row("2", "Claim Points (Auto Looping)")
        table.add_row("3", "Check Balance")
        table.add_row("4", "Exit")
        console.print(table)
        choice = input("Select feature (1-4): ").strip()

        if choice == '1':
            perform_email_verification()
        elif choice == '2':
            account_file = "account.json"
            token = read_jwt_from_file(account_file)
            if token:
                try:
                    min_delay = int(input("Enter minimum delay (seconds): ").strip())
                    max_delay = int(input("Enter maximum delay (seconds): ").strip())
                    auto_claim_points(token, min_delay, max_delay)
                except ValueError:
                    console.print("[red]Delay input must be a number.[/red]")
            else:
                console.print("[red]Cannot proceed due to missing token.[/red]")
        elif choice == '3':
            check_balance()
        elif choice == '4':
            console.print("[yellow]Exiting program.[/yellow]")
            break
        else:
            console.print("[red]Invalid choice. Please select 1-4.[/red]")


if __name__ == "__main__":
    console.print(f"[cyan]Current time: {datetime.now().strftime('%I:%M %p %d-%m-%Y')}[/cyan]")
    main_menu()
