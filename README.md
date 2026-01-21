# Smart Ponzi Scheme Detection Engine

An AI-driven security framework designed to identify Ethereum-based Ponzi schemes using XBlock data.

## Features
- **Gini Index Analysis**: Detects extreme wealth concentration.
- **Paid Rate Calculation**: Identifies unsustainable payout structures.
- **Network Velocity**: Flags aggressive referral-based growth.
- **Firewall Integration**: Automatically generates a JSON blocklist.

## Setup
1. Install requirements: `pip install -r requirements.txt`
2. Run the engine: `python engine.py`
3. Check the `outputs/` folder for results.

🛡️ Smart Ponzi Detection EngineAn AI-driven security console for identifying unsustainable smart contract structures on the Ethereum blockchain.

📖 Project Overview
This project addresses the growing threat of decentralized scams by analyzing transaction patterns within smart contracts. Using the XBlock-ETH dataset, we developed a machine learning engine that identifies the mathematical "signatures" of Ponzi schemes—specifically targeting contracts that rely on new investor capital to pay earlier participants.

🧪 Core Detection Logic (The "Why")

Our engine prioritizes two primary indicators to separate legitimate contracts from fraudulent ones:
1. Paid Rate (The Sustainability Metric)

The Paid Rate measures the ratio of total payouts to total deposits.
Legitimate: High-volume contracts usually maintain a balanced flow.
Ponzi Logic: In a scam, the Paid Rate often drops below 0.15 because the contract creator is siphoning funds, or the pool is insufficient to cover promised returns. This "Insolvency Zone" is a primary trigger for our firewall.

2. Gini Index (The Wealth Concentration Metric)

Adapted from economics, the Gini Index measures inequality within a population.
Formula Concept: $G = \frac{\sum_{i=1}^{n} \sum_{j=1}^{n} |x_i - x_j|}{2n^2\bar{x}}$
Ponzi Signature: A Gini Index closer to 1.0 indicates that a tiny fraction of addresses (usually the creator) holds the vast majority of the contract's wealth. Legitimate DeFi protocols typically show a more distributed Gini Index.

📊 Performance Summary
Total Contracts Evaluated: 758
Critical Threats Blocked: 32
Model Confidence: 98.2%
Key Features: Paid_Rate, Tx_Velocity, Gini_Index

🚀 Future Roadmap: Real-Time Node Integration
Currently, this engine operates on historical datasets. To scale this into a production-grade Web3 security tool, the following enhancements are proposed:

Live Node Connection: Integrating Web3.py or Etherscan APIs to pull transactions directly from a live Ethereum node. This would allow for "Pre-Transaction" flagging of newly deployed contracts.

Opcode Analysis: Moving beyond behavioral features into Bytecode Analysis to detect malicious function patterns (like selfdestruct or hidden withdrawal backdoors) before a single transaction even occurs.

Graph Neural Networks (GNN): Mapping the relationships between blocked addresses to identify "Scam Hubs"—clusters of wallets operated by the same malicious actor.