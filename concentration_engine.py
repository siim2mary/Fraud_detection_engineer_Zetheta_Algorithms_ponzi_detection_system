import numpy as np
import pandas as pd

def calculate_gini(balances):
    """Calculates the Gini Coefficient for a list of wallet balances."""
    if len(balances) == 0: return 0
    sorted_balances = np.sort(balances)
    n = len(balances)
    index = np.arange(1, n + 1)
    # Gini formula: (2 * sum(i * balance) / (n * sum(balance))) - (n + 1) / n
    return (np.sum((2 * index - n - 1) * sorted_balances) / (n * np.sum(sorted_balances)))

def analyze_wallet_concentration(df):
    """
    Part 3: Wallet Flow & Concentration Analysis
    """
    # Group by wallet to see who holds the most 'Yield Received'
    wallet_stats = df.groupby('wallet_address')['yield_disbursed'].sum().reset_index()
    
    # Calculate Gini Coefficient for the current distribution
    gini_score = calculate_gini(wallet_stats['yield_disbursed'].values)
    
    # Identify 'Insider' Wallets (Wallets holding > 20% of total yield)
    total_yield = wallet_stats['yield_disbursed'].sum()
    wallet_stats['yield_share'] = wallet_stats['yield_disbursed'] / total_yield
    insiders = wallet_stats[wallet_stats['yield_share'] > 0.20]
    
    return {
        'gini_coefficient': round(gini_score, 2),
        'insider_count': len(insiders),
        'is_concentrated': gini_score > 0.80
    }