from diagrams import Diagram, Cluster, Edge
from diagrams.programming.language import Python
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.analytics import Spark
from diagrams.generic.network import Firewall
from diagrams.generic.device import Tablet

with Diagram("Smart Ponzi Detection Framework", show=False, direction="LR", filename="ponzi_arch_map"):
    
    # Layer A: Data Ingestion
    with Cluster("Layer A: Data Ingestion"):
        blockchain_data = [
            PostgreSQL("On-Chain Data\n(TX/Events)"),
            PostgreSQL("Event Logs\n(In/Outflow)")
        ]

    # Layer B: Analytical Engines
    with Cluster("Layer B: Analytical Engines"):
        with Cluster("Processing Logic"):
            logic_engine = Python("Detection Engine")
            
        sustainability = Spark("Sustainability Engine\n(Rs Ratio)")
        concentration = Spark("Concentration Engine\n(Gini Coeff)")
        logic_auditor = Spark("Logic Auditor\n(Referral Signs)")

    # Layer C: Scoring & Alerting
    with Cluster("Layer C: Scoring"):
        risk_score = Tablet("Risk Score (0-100)")
        early_warning = Firewall("Early Warning\n(Runway Alerts)")

    # Define Data Flow
    blockchain_data >> Edge(label="Raw Logs") >> logic_engine
    logic_engine >> [sustainability, concentration, logic_auditor]
    [sustainability, concentration, logic_auditor] >> risk_score
    risk_score >> early_warning