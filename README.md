# Project Overview
In the fintech industry, system downtime isn't just a technical glitch—it is a massive loss in revenue and user trust. This project is a Predictive Observability Solution designed to move beyond reactive alerting.

By correlating Infrastructure Metrics (CPU/Memory), Real User Monitoring (RUM) data, and System Logs, this engine uses Machine Learning to identify "Lead Indicators" of system failure. It predicts when a server node will reach critical capacity before the users experience 500-level errors.

# Key Features
- Multivariate Anomaly Detection: Utilizes an Isolation Forest (Unsupervised ML) model to identify anomalous patterns across memory, CPU, and latency simultaneously.

- Predictive Infrastructure Scaling: Implements a Linear Regression forecasting model to estimate "Time-to-Failure" (TTF), allowing for proactive resource provisioning.

- Automated Root Cause Analysis (RCA): Employs Natural Language Processing (NLP) with K-Means clustering to automatically categorize thousands of log lines into actionable insights (e.g., identifying Java Heap Space leaks).

- Enterprise Dashboard: A high-performance, interactive interface built with Plotly Dash featuring dark-mode UI, real-time metrics, and predictive trend lines.


# Technical Stack
- Language: Python 3.11

- Frontend: Plotly Dash (HTML/CSS)

- Data Science: Scikit-Learn, Pandas, NumPy

- Visualization: Plotly Express & Graph Objects

- Deployment: Gunicorn / Render (Cloud)


# Project Structure

├── app.py                                     # Main Plotly Dash application & UI
├── DowntimeModel_in_Fintechs.ipnb             # Shared AI logic: ML models and data processing
├── requirements.txt                           # Project dependencies for cloud deployment
├── merged_observability_data.csv              # Synthetic industry-standard monitoring datasets
└── README.md                                  # Project documentation

