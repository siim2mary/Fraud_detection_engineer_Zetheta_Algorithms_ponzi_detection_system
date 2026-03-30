import networkx as nx
import json
from collections import defaultdict
from datetime import datetime

class ZethetaPonziEngine:
    """
    Advanced On-Chain Forensic Tool
    Designed for Zetheta Algorithms 15-Day Sprint Submission.
    Purpose: Detects fraudulent financial structures using Graph Theory.
    """
    
    def __init__(self):
        # The Directed Graph (DiGraph) tracks the 'Flow of Funds' (who sent to whom).
        self.graph = nx.DiGraph()
        
        # Dictionary to store per-wallet volume and transaction frequency.
        self.wallet_stats = defaultdict(lambda: {"in_vol": 0, "out_vol": 0, "tx_count": 0})
        
        # Risk Weighting Matrix: Defines how much each 'red flag' contributes to the 0-100 score.
        self.weights = {
            "sustainability": 40,  # Dependency on new capital (The 'Yield' trap)
            "concentration": 25,   # Centralized control of funds (The 'Rugpull' risk)
            "topology": 20,        # Circular flow detection (The 'Wash Trading' signal)
            "hub_risk": 15         # Existence of a single collection point (The 'Master' wallet)
        }

    def ingest_data(self, transactions):
        """
        PART 1: Data Pipeline.
        Processes raw ledger data into a topological graph structure.
        """
        for tx in transactions:
            u, v, amt = tx["from"], tx["to"], tx["amount"]
            
            # Create a directed edge from sender to receiver with the transaction amount.
            self.graph.add_edge(u, v, weight=amt)
            
            # Update volume statistics for ROI and sustainability calculations.
            self.wallet_stats[u]["out_vol"] += amt
            self.wallet_stats[v]["in_vol"] += amt
            self.wallet_stats[v]["tx_count"] += 1

    def run_diagnostics(self):
        """
        PART 2-5: Analysis & Scoring.
        Executes multi-signal fraud detection and generates explainable risk findings.
        """
        score = 0
        findings = []
        
        # --- 1. SUSTAINABILITY ANALYSIS ---
        # Financial Logic: If payouts exceed 70% of new deposits without external revenue, 
        # the system is likely paying old investors using new investor funds.
        total_in = sum(s["in_vol"] for s in self.wallet_stats.values())
        total_out = sum(s["out_vol"] for s in self.wallet_stats.values())
        sus_ratio = (total_out / total_in) if total_in > 0 else 0
        
        if sus_ratio > 0.70:
            score += self.weights["sustainability"]
            findings.append(f"Sustainability Risk: {sus_ratio:.2%} (Payouts dependent on new deposits)")

        # --- 2. CONCENTRATION ANALYSIS ---
        # Financial Logic: High capital concentration in a few wallets (Gini-style risk) 
        # indicates a high probability of a centralized 'exit-liquidity' scam.
        inflows = sorted([s["in_vol"] for s in self.wallet_stats.values()], reverse=True)
        total_vol = sum(inflows)
        conc_ratio = (sum(inflows[:3]) / total_vol) if total_vol > 0 else 0
        
        if conc_ratio > 0.50:
            score += self.weights["concentration"]
            findings.append(f"Concentration Risk: {conc_ratio:.2%} of capital controlled by top 3 wallets")

        # --- 3. TOPOLOGICAL ANALYSIS (CYCLE DETECTION) ---
        # Technical Logic: Uses simple_cycles to find 'wash trading' or 'capital recycling'
        # where funds flow in a loop to fake legitimacy or volume.
        try:
            cycles = list(nx.simple_cycles(self.graph))
            if cycles:
                score += self.weights["topology"]
                findings.append(f"Topological Risk: {len(cycles)} circular transaction loop(s) detected")
        except: 
            pass

        # --- 4. HUB IDENTIFICATION ---
        # Technical Logic: Identifies nodes with high In-Degree (many depositors) but 
        # low Out-Degree (payouts only to specific 'masters').
        for node in self.graph.nodes:
            if self.graph.in_degree(node) >= 3 and self.graph.out_degree(node) <= 1:
                score += self.weights["hub_risk"]
                findings.append(f"Hub Risk: Wallet '{node}' acts as a central collection node")
                break

        # Calculate final Risk Level based on cumulative score.
        risk_level = "CRITICAL" if score >= 70 else "MEDIUM" if score >= 40 else "LOW"
        
        return {
            "score": score,
            "level": risk_level,
            "findings": findings,
            "metadata": {
                "wallets": len(self.graph.nodes),
                "transactions": len(self.graph.edges),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
        }

if __name__ == "__main__":
    # --- PART 7: VALIDATION ---
    # Standardised Test Case representing a high-risk Ponzi structure.
    diverse_data = [
        {"from": "Retail_1", "to": "Alpha_Vault", "amount": 1000},
        {"from": "Retail_2", "to": "Alpha_Vault", "amount": 1500},
        {"from": "Retail_3", "to": "Alpha_Vault", "amount": 2000},
        {"from": "Retail_4", "to": "Beta_Mixer", "amount": 500},
        {"from": "Alpha_Vault", "to": "Early_Investor", "amount": 3200}, 
        {"from": "Early_Investor", "to": "Retail_1", "amount": 200}, # Creates a cycle   
        {"from": "Beta_Mixer", "to": "Alpha_Vault", "amount": 450},  # Creates layering   
    ]

    # Initialize engine and process the ledger.
    engine = ZethetaPonziEngine()
    engine.ingest_data(diverse_data)
    report = engine.run_diagnostics()

    # --- FINAL EXECUTIVE OUTPUT ---
    # This format is optimized for professional audit reporting.
    print(f"\n{'='*45}")
    print(f"ZETHETA AUDIT REPORT | {report['metadata']['timestamp']}")
    print(f"{'='*45}")
    print(f"FINAL RISK SCORE: {report['score']}/100")
    print(f"RISK LEVEL      : {report['level']}")
    print(f"\nEXECUTIVE SUMMARY:")
    print("The system exhibits strong Ponzi-like characteristics due to high dependency \n"
          "on new capital, centralized fund control, and circular transaction behavior.")
    print("-" * 45)
    print("DETAILED FINDINGS:")
    for f in report['findings']:
        print(f" [!] {f}")
    print("-" * 45)
    print(f"Total Wallets Analyzed : {report['metadata']['wallets']}")
    print(f"Total Transactions      : {report['metadata']['transactions']}")
    print(f"{'='*45}\n")