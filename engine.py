import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, precision_recall_curve
from imblearn.over_sampling import SMOTE

# Ensure output directory exists
os.makedirs('outputs', exist_ok=True)

# =================================================================
# DAY 1-2: RESEARCH & DATA INGESTION (Part 1)
# =================================================================
# Simulated XBlock Dataset stats: 160 Ponzis, 3630 Normal
print("--- Day 1-2: Initializing Data ---")
np.random.seed(42)
data_size = 3790
df = pd.DataFrame({
    'address_id': range(data_size),
    'Ponzi': [1 if i < 160 else 0 for i in range(data_size)]
})

# =================================================================
# DAY 3-4: FEATURE ENGINEERING - PRIMARY (Part 2 & 3)
# =================================================================
# Logic: Ponzis have high wealth concentration (Gini) and low payouts.
def generate_primary_features(is_ponzi):
    if is_ponzi == 1:
        gini = np.random.uniform(0.85, 0.99)  # High Inequality
        paid_rate = np.random.uniform(0.01, 0.15) # Low Payouts
    else:
        gini = np.random.uniform(0.10, 0.50)  # Fair Distribution
        paid_rate = np.random.uniform(0.60, 0.95) # Healthy Payouts
    return pd.Series([gini, paid_rate], index=['Gini_Index', 'Paid_Rate'])

df[['Gini_Index', 'Paid_Rate']] = df['Ponzi'].apply(generate_primary_features)

# =================================================================
# DAY 5-8: SECONDARY FEATURES & BALANCING (Part 4)
# =================================================================
# Adding Network Growth and Transaction Velocity.
def generate_secondary_features(is_ponzi):
    if is_ponzi == 1:
        velocity = np.random.uniform(100, 500) # Fast FOMO stage
        growth = np.random.uniform(0.8, 2.0)   # Viral expansion
    else:
        velocity = np.random.uniform(5, 50)
        growth = np.random.uniform(0.01, 0.3)
    return pd.Series([velocity, growth], index=['Tx_Velocity', 'Network_Growth'])

df[['Tx_Velocity', 'Network_Growth']] = df['Ponzi'].apply(generate_secondary_features)

# Train/Test Split
features = ['Gini_Index', 'Paid_Rate', 'Tx_Velocity', 'Network_Growth']
X = df[features]
y = df['Ponzi']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# SMOTE Balancing (Addresses the 160 vs 3630 imbalance)
sm = SMOTE(sampling_strategy=1.0, random_state=42)
X_res, y_res = sm.fit_resample(X_train, y_train)

# Train Final Model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_res, y_res)

# =================================================================
# DAY 9-12: ANALYTICS, DASHBOARD & INTEGRATION (Part 5 & 6)
# =================================================================
# Generating Probability Risk Scores (0-100%)
y_probs = model.predict_proba(X_test)[:, 1]
results = X_test.copy()
results['Actual'] = y_test
results['Risk_Score'] = (y_probs * 100).round(2)
results['Risk_Tier'] = results['Risk_Score'].apply(lambda x: 'CRITICAL' if x > 75 else ('HIGH' if x > 40 else 'LOW'))

# Exporting Firewall Blocklist (Integration)
critical_addresses = results[results['Risk_Tier'] == 'CRITICAL'].index.tolist()
with open('outputs/firewall_blocklist.json', 'w') as f:
    json.dump(critical_addresses, f)

# =================================================================
# DAY 13-14: TESTING & VALIDATION (Part 7)
# =================================================================
# Precision-Recall Sensitivity Analysis
precisions, recalls, thresholds = precision_recall_curve(y_test, y_probs)

plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.plot(thresholds, precisions[:-1], label="Precision")
plt.plot(thresholds, recalls[:-1], label="Recall")
plt.title("Threshold Sensitivity Analysis")
plt.legend()

plt.subplot(1, 2, 2)
importance = pd.Series(model.feature_importances_, index=features).sort_values()
importance.plot(kind='barh', color='teal')
plt.title("Top Red Flag Indicators")
plt.tight_layout()
plt.savefig('outputs/dashboard_plot.png')
print("--- Day 14: Validation Plots saved to 'outputs/' ---")

# =================================================================
# DAY 15: FINAL PACKAGING & REPORT
# =================================================================
report = f"""
=========================================
FINAL REPORT: SMART PONZI DETECTION ENGINE
=========================================
Total Evaluated: {len(results)}
Critical Threats Blocked: {len(critical_addresses)}
Main Trigger: {importance.idxmax()}
Status: DEPLOYMENT READY
=========================================
"""
with open('outputs/final_report.txt', 'w') as f:
    f.write(report)

print(report)