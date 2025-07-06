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
                console.print("[red]File email.txt kosong.[/red]")
                return None
    except FileNotFoundError:
        console.print("[red]File email.txt tidak ditemukan.[/red]")
        return None


def start_email_verification(email):
    url = "https://app.dynamicauth.com/api/v0/sdk/adc09cea-6194-4667-8be8-931cc28dacd2/emailVerifications/create"
    headers = {"Content-Type": "application/json"}
    data = {"email": email}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        console.print("[green]Verifikasi email berhasil dikirim. Silakan periksa email Anda untuk OTP.[/green]")
        return response.json()
    else:
        console.print(f"[red]Gagal mengirim verifikasi email: {response.status_code} - {response.text}[/red]")
        return None


def complete_email_verification(verification_uuid, verification_token, session_public_key):
    url = "https://app.dynamicauth.com/api/v0/sdk/adc09cea-6194-4667-8be8-931cc28dacd2/emailVerifications/signin"
    headers = {"Content-Type": "application/json"}
    data = {
        "verificationUUID": verification_uuid,
        "verificationToken": verification_token,
        "sessionPublicKey": session_public_key
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        with open("account.json", "w") as file:
            json.dump(response.json(), file, indent=4)
        console.print("[green]Verifikasi selesai. Respons disimpan ke account.json[/green]")
        return response.json()
    else:
        console.print(f"[red]Gagal menyelesaikan verifikasi: {response.status_code} - {response.text}[/red]")
        return None


def read_jwt_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            jwt = data.get('jwt')
            if jwt:
                return jwt
            else:
                console.print("[red]Token JWT tidak ditemukan dalam file.[/red]")
                return None
    except FileNotFoundError:
        console.print(f"[red]File {file_path} tidak ditemukan.[/red]")
        return None


def claim_points(token):
    url = "https://beta.orchestrator.nexus.xyz/v3/points/claim"
    headers = {"authorization": f"Bearer {token}", "Content-Type": "application/octet-stream"}
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        console.print("[green]Poin berhasil diklaim.[/green]")
        return response.json() if response.text.strip() else None
    else:
        console.print(f"[red]Gagal mengklaim poin: {response.status_code} - {response.text}[/red]")
        return None


def check_balance():
    account_file = "account.json"
    try:
        with open(account_file, 'r') as file:
            data = json.load(file)
            wallet_address = data["user"]["verifiedCredentials"][0]["address"]
    except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
        console.print(f"[red]Error membaca file account.json: {e}[/red]")
        return

    url = "https://nexus-testnet.g.alchemy.com/public"
    payload = {"jsonrpc": "2.0", "method": "eth_getBalance", "params": [wallet_address, "latest"], "id": 1}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        balance_hex = response.json().get("result")
        balance_eth = int(balance_hex, 16) / 10**18
        console.print(f"[cyan]Saldo dompet: {balance_eth:.4f} NEX[/cyan]")
    else:
        console.print(f"[red]Gagal check balance: {response.status_code} - {response.text}[/red]")


def perform_email_verification():
    email = read_email_from_file("email.txt")
    if email:
        console.print(f"[cyan]Email: {email}[/cyan]")
        verification_data = start_email_verification(email)
        if verification_data and "verificationUUID" in verification_data:
            verification_uuid = verification_data["verificationUUID"]
            verification_token = input("Masukkan OTP yang diterima: ").strip()
            complete_email_verification(verification_uuid, verification_token, SESSION_PUBLIC_KEY)


def auto_claim_points(token, min_delay, max_delay):
    if min_delay > max_delay:
        console.print("[red]Jeda minimal tidak boleh lebih besar dari jeda maksimal.[/red]")
        return
    try:
        while True:
            console.print(f"\n[blue][{datetime.now().strftime('%H:%M:%S')}] Mengklaim poin...[/blue]")
            claim_points(token)
            delay = random.randint(min_delay, max_delay)
            console.print(f"[yellow]Menunggu {delay} detik...[/yellow]")
            time.sleep(delay)
    except KeyboardInterrupt:
        console.print("[red]\nAuto claim dihentikan.[/red]")


def main_menu():
    while True:
        console.print(Panel("[bold blue]=== Nexus Auto Bot - Zaluce ===[/bold blue]", box=box.ROUNDED))
        table = Table(show_header=False, box=box.SIMPLE)
        table.add_column("No", style="cyan", justify="center")
        table.add_column("Fitur", style="cyan")
        table.add_row("1", "Login & Verif Email")
        table.add_row("2", "Klaim Poin")
        table.add_row("3", "Check Balance")
        table.add_row("4", "Keluar")
        console.print(table)
        choice = input("Pilih fitur (1-4): ").strip()

        if choice == '1':
            perform_email_verification()
        elif choice == '2':
            token = read_jwt_from_file("account.json")
            if token:
                try:
                    min_delay = int(input("Masukkan jeda minimal (detik): ").strip())
                    max_delay = int(input("Masukkan jeda maksimal (detik): ").strip())
                    auto_claim_points(token, min_delay, max_delay)
                except ValueError:
                    console.print("[red]Input jeda harus berupa angka.[/red]")
        elif choice == '3':
            check_balance()
        elif choice == '4':
            console.print("[yellow]Keluar dari program.[/yellow]")
            break
        else:
            console.print("[red]Pilihan tidak valid. Silakan pilih 1-4.[/red]")


if __name__ == "__main__":
    console.print(f"[cyan]Waktu saat ini: {datetime.now().strftime('%H:%M %d-%m-%Y')}[/cyan]")
    main_menu()