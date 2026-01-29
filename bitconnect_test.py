import pandas as pd
import numpy as np
import random

def generate_bitconnect_data():
    """
    Simulates the 60 days leading up to the BitConnect collapse.
    Includes timestamps, deposits, yields, treasury, and wallet data.
    """
    days = 60
    # Set the range ending at the historical collapse date (Jan 16, 2018)
    dates = pd.date_range(end='2018-01-16', periods=days)
    
    # 1. Simulate Capital Inflow (New Deposits)
    # Grows steadily, then drops off as regulators issued warnings in early Jan.
    inflows = np.concatenate([
        np.linspace(10000, 55000, 40), # Hype phase
        np.linspace(55000, 40000, 10), # plateau
        np.linspace(40000, 500, 10)    # Panic phase
    ])
    
    # 2. Simulate Yield Outflow (Interest Paid)
    # Starts low but spikes as insiders pull out 'referral' bonuses before the crash.
    outflows = np.concatenate([
        np.linspace(2000, 15000, 40),  
        np.linspace(15000, 45000, 10), # Outflows begin to exceed inflows
        np.linspace(45000, 60000, 10)  # Massive drain
    ])
    
    # 3. Calculate Treasury Balance
    # Starting treasury of $200k
    treasury = [200000]
    for i in range(1, days):
        # Treasury = Previous + New Money - Money Paid Out
        current_bal = treasury[-1] + inflows[i] - outflows[i]
        treasury.append(max(0, current_bal)) # Cannot go below zero

    # 4. Generate Wallet Data (Crucial for Part 3)
    # We create a pool of 50 wallets, but assign 80% of yield to 5 'Insider' wallets.
    wallets = [f"0x{random.randint(1000, 9999)}...{random.randint(10, 99)}" for _ in range(50)]
    insider_wallets = wallets[:5]
    other_wallets = wallets[5:]
    
    data_rows = []
    for i in range(days):
        # Pick a wallet for this day's activity
        # If it's a 'Drain' day (last 20 days), insiders take more
        if i > 40:
            current_wallet = random.choice(insider_wallets)
        else:
            current_wallet = random.choice(other_wallets)
            
        data_rows.append({
            'timestamp': dates[i],
            'new_deposits': inflows[i],
            'yield_disbursed': outflows[i],
            'treasury_balance': treasury[i],
            'wallet_address': current_wallet # This fixes the KeyError
        })

    df = pd.DataFrame(data_rows)
    
    # Standardize column names (Safety measure)
    df.columns = df.columns.str.strip().str.lower()
    
    return df

if __name__ == "__main__":
    # Test run to verify columns
    test_df = generate_bitconnect_data()
    print("Success! Columns created:", test_df.columns.tolist())
    print(test_df.tail(5))