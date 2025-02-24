import requests
import time
import json
import os
from datetime import datetime

# Function to fetch real-time price data from CoinGecko
def get_crypto_price(crypto_id):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    return data[crypto_id]['usd']

# Function to load existing data or initialize a new dictionary
def load_data(filename='crypto_data.json'):
    initial_data = {'bitcoin': [], 'ethereum': []}
    if not os.path.exists(filename):
        # If file doesn't exist, create it with initial data
        with open(filename, 'w') as f:
            json.dump(initial_data, f)
        return initial_data
    
    try:
        with open(filename, 'r') as f:
            data = f.read()
            if not data.strip():  # If file is empty
                with open(filename, 'w') as f:
                    json.dump(initial_data, f)
                return initial_data
            return json.loads(data)
    except json.JSONDecodeError:
        # If file is corrupted, reset it
        with open(filename, 'w') as f:
            json.dump(initial_data, f)
        return initial_data

# Function to save data to a file
def save_data(data, filename='crypto_data.json'):
    with open(filename, 'w') as f:
        json.dump(data, f)

# Function to collect data over a few days
def collect_data(duration_hours=72, interval_seconds=3600):
    data = load_data()
    end_time = time.time() + (duration_hours * 3600)  # Run for specified hours

    while time.time() < end_time:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        btc_price = get_crypto_price('bitcoin')
        eth_price = get_crypto_price('ethereum')

        # Append data with timestamp
        data['bitcoin'].append({'timestamp': timestamp, 'price': btc_price})
        data['ethereum'].append({'timestamp': timestamp, 'price': eth_price})

        print(f"Collected - BTC: ${btc_price}, ETH: ${eth_price} at {timestamp}")
        save_data(data)
        time.sleep(interval_seconds)  # Wait for the next interval

# Main execution
if __name__ == "__main__":
    # Collect data for 72 hours (3 days), fetching every hour
    print("Starting data collection for 3 days (1-hour intervals)...")
    collect_data(duration_hours=72, interval_seconds=3600)