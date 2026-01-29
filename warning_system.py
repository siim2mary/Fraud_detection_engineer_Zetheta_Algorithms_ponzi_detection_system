def check_early_warnings(current_score, previous_score, treasury_delta):
    """
    Part 5: Early Warning System
    Checks if the rate of change indicates an imminent collapse.
    """
    alerts = []
    
    # 1. Momentum Warning (Sudden risk spike)
    score_change = current_score - previous_score
    if score_change > 15:
        alerts.append("🚨 RAPID RISK ESCALATION: Momentum shift detected.")
        
    # 2. Liquidity Warning (Sudden drain)
    if treasury_delta < -0.15: # 15% drop in treasury in one cycle
        alerts.append("⚠️ LIQUIDITY DRAIN: Large capital outflow detected.")
        
    # 3. Final Warning (The 'Point of No Return')
    if current_score > 90:
        alerts.append("💀 DEATH SPIRAL: Insolvency is mathematically certain.")
        
    return alerts