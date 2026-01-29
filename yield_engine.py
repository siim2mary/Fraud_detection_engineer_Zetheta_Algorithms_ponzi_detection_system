import pandas as pd

def calculate_yield_health(df):
    """
    Part 2: Flagging Unsustainable Yields
    """
    # 1. Sustainability Ratio (Yield Paid / New Deposits)
    # Ratio > 1.0 means the contract is losing money
    df['sustainability_ratio'] = df['yield_disbursed'] / df['new_deposits']
    
    # 2. Net Treasury Flow
    df['net_flow'] = df['new_deposits'] - df['yield_disbursed']
    
    # 3. Protocol Runway (How many days of yield are left in the reserve?)
    # If runway is low and sustainability ratio is high, the collapse is near.
    df['runway_days'] = df['treasury_balance'] / df['yield_disbursed'].replace(0, 1)
    
    # 4. The Flagging Logic
    def flag_ponzi(row):
        if row['sustainability_ratio'] > 1.2 and row['runway_days'] < 7:
            return "🚨 CRITICAL: Ponzi Collapse Likely"
        if row['sustainability_ratio'] > 1.0:
            return "⚠️ WARNING: Unsustainable Yield"
        return "✅ STABLE"

    df['yield_status'] = df.apply(flag_ponzi, axis=1)
    
    return df