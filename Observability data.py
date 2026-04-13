import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set seed for reproducibility
np.random.seed(42)

def generate_observability_data(days=7):
    start_time = datetime.now() - timedelta(days=days)
    timestamps = [start_time + timedelta(minutes=5*i) for i in range(days * 24 * 12)]
    
    # INFRASTRUCTURE METRICS (CPU, Memory)
    infra_data = {
        "timestamp": timestamps,
        "node_id": "fintech-srv-01",
        "cpu_usage": np.random.normal(40, 5, len(timestamps)).clip(0, 100),
        "mem_usage": np.linspace(30, 85, len(timestamps)) + np.random.normal(0, 2, len(timestamps)), # Simulated Memory Leak
        "disk_io": np.random.uniform(10, 50, len(timestamps))
    }
    df_infra = pd.DataFrame(infra_data)

    # REAL USER MONITORING (RUM)
    # Higher memory usage correlates with slower response times
    rum_data = []
    for i, ts in enumerate(timestamps):
        # Base latency increases as memory leak progresses
        base_latency = 200 + (df_infra.iloc[i]['mem_usage'] * 2) 
        
        rum_data.append({
            "timestamp": ts,
            "action": random.choice(["Login", "Transfer", "CheckBalance"]),
            "response_time_ms": base_latency + np.random.normal(0, 50),
            "status_code": 200 if df_infra.iloc[i]['mem_usage'] < 80 else random.choice([200, 500]),
            "isp": random.choice(["MTN", "Airtel", "Glo"]),
            "region": "Lagos"
        })
    df_rum = pd.DataFrame(rum_data)

    #  SYSTEM LOGS (NLP Target)
    logs = []
    for i, ts in enumerate(timestamps):
        mem = df_infra.iloc[i]['mem_usage']
        if mem < 60:
            msg = "INFO: Transaction processed successfully"
        elif mem < 80:
            msg = "WARN: High memory pressure detected in JVM"
        else:
            msg = "ERROR: java.lang.OutOfMemoryError: Java heap space"
        
        logs.append({"timestamp": ts, "log_level": msg.split(":")[0], "message": msg})
    df_logs = pd.DataFrame(logs)

    return df_infra, df_rum, df_logs

# Generate and save
infra, rum, logs = generate_observability_data()
infra.to_csv("infra_metrics.csv", index=False)
rum.to_csv("rum_data.csv", index=False)
logs.to_csv("system_logs.csv", index=False)

print("Industry-standard datasets generated: infra_metrics.csv, rum_data.csv, system_logs.csv")