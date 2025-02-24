import pandas as pd
import numpy as np
import json

def load_data(filename='crypto_data.json'):
    with open(filename, 'r') as f:
        return json.load(f)

def analyze_data(filename='crypto_data.json'):
    data = load_data(filename)
    
    # Convert to DataFrame for easier analysis
    btc_df = pd.DataFrame(data['bitcoin'])
    eth_df = pd.DataFrame(data['ethereum'])
    
    # Ensure timestamps align and merge data
    df = pd.merge(btc_df, eth_df, on='timestamp', suffixes=('_btc', '_eth'))
    
    # Calculate correlation
    correlation = np.corrcoef(df['price_btc'], df['price_eth'])[0, 1]
    
    # Basic price comparison stats
    btc_avg = df['price_btc'].mean()
    eth_avg = df['price_eth'].mean()
    btc_change = ((df['price_btc'].iloc[-1] - df['price_btc'].iloc[0]) / df['price_btc'].iloc[0]) * 100
    eth_change = ((df['price_eth'].iloc[-1] - df['price_eth'].iloc[0]) / df['price_eth'].iloc[0]) * 100
    
    # Additional statistics
    btc_std = df['price_btc'].std()
    eth_std = df['price_eth'].std()
    btc_min = df['price_btc'].min()
    btc_max = df['price_btc'].max()
    eth_min = df['price_eth'].min()
    eth_max = df['price_eth'].max()

    # Summary
    summary = (
        f"Analysis Summary (based on {len(df)} data points):\n"
        f"\nCorrelation Analysis:\n"
        f" - BTC/ETH price correlation: {correlation:.4f}\n"
        f"\nBitcoin Statistics:\n"
        f" - Average price: ${btc_avg:.2f}\n"
        f" - Standard deviation: ${btc_std:.2f}\n"
        f" - Price range: ${btc_min:.2f} - ${btc_max:.2f}\n"
        f" - Price change: {btc_change:.2f}%\n"
        f"\nEthereum Statistics:\n"
        f" - Average price: ${eth_avg:.2f}\n"
        f" - Standard deviation: ${eth_std:.2f}\n"
        f" - Price range: ${eth_min:.2f} - ${eth_max:.2f}\n"
        f" - Price change: {eth_change:.2f}%"
    )
    print(summary)
    return summary

if __name__ == "__main__":
    print("Analyzing crypto data...")
    analyze_data()