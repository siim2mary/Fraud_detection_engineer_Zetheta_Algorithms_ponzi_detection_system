def calculate_red_flag_score(sustainability_ratio, gini_coef, reserve_decay):
    """
    Part 4: Red Flag Scoring Algorithm
    Inputs: 
        sustainability_ratio (float): Outflow/Inflow
        gini_coef (float): 0 to 1 measurement of concentration
        reserve_decay (float): Percentage of treasury lost per day
    """
    # Normalize components to 0-100 scale
    s_score = min(sustainability_ratio * 50, 100) # Caps at 2.0 ratio
    g_score = gini_coef * 100
    d_score = min(reserve_decay * 500, 100)       # Flags fast drains
    
    # Weighted Calculation
    final_score = (s_score * 0.45) + (g_score * 0.25) + (d_score * 0.30)
    
    # Categorization Logic
    if final_score > 85:
        category = "🚨 IMMEDIATE RISK: ACTIVE PONZI"
    elif final_score > 60:
        category = "⚠️ HIGH RISK: UNSUSTAINABLE"
    elif final_score > 30:
        category = "🟡 MODERATE RISK: MONITOR"
    else:
        category = "✅ LOW RISK"
        
    return round(final_score, 2), category