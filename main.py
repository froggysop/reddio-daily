import requests
import os
import time
import random

proxy = ""  #http://login:pass@ip:port

proxies = {
    "http": proxy,
    "https": proxy,
} if proxy else None

MIN_DELAY = 10  # Minimum delay in seconds
MAX_DELAY = 30  # Maximum delay in seconds

def get_wallet_addresses(file_path):
    if not os.path.exists(file_path):
        print(f"{file_path} does not exist.")
        return []

    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

def daily_check_in(wallet_address):
    url = f"https://points-mainnet.reddio.com/v1/daily_checkin?wallet_address={wallet_address}"

    try:
        response = requests.get(url, proxies=proxies, timeout=5) if proxies else requests.get(url, timeout=5)
        response_data = response.json()

        if response_data['status'] == 'Error':
            if response_data['error'] == 'User not registered':
                print(f"Wallet: {wallet_address} - User not registered")
            elif response_data['error'] == 'Already checked in':
                print(f"Wallet: {wallet_address} - Already checked in")
            else:
                print(f"Wallet: {wallet_address} - Error: {response_data['error']}")
        else:
            print(f"Wallet: {wallet_address} - Check-in successful")

    except requests.exceptions.RequestException as e:
        print(f"Wallet: {wallet_address} - Request failed: {e}")


def process_wallets(file_path):
    wallet_addresses = get_wallet_addresses(file_path)

    if not wallet_addresses:
        print("No wallet addresses found.")
        return

    random.shuffle(wallet_addresses)

    for wallet_address in wallet_addresses:
        daily_check_in(wallet_address)
        delay = random.uniform(MIN_DELAY, MAX_DELAY)
        print(f"Waiting for {delay:.2f} seconds before the next request...")
        time.sleep(delay)

if __name__ == "__main__":
    process_wallets("wallets.txt")
