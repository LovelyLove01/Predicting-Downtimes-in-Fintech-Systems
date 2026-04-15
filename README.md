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


# Method
1. Ingestion: The system ingests telemetry data similar to exports from Dynatrace, Edge or Datadog etc.

2. Inference: The Isolation Forest assigns an anomaly score to each data point.

3. Forecasting: The Linear Regression model analyzes the memory trend to project the critical 90% threshold.

4. Clustering: Logs are vectorized via TF-IDF and clustered to point to the specific error type (e.g., Cluster 2 = OutOfMemory)


# Installation & Setup
To run this project locally:

1. Clone the repository:
   
git clone (https://github.com/LovelyLove01/Predicting-Downtimes-in-Fintech-Systems.git)

2. Install dependencies:

pip install -r requirements.txt

3. Run the dashboard:
python app.py
Access at http://127.0.0.1:8050/


# Future Roadmap
1. Real-time API Integration: Direct hooks into APMs like Edge, Dynatrace etc

2. Auto-scaling Webhooks: Automated triggers to spin up AWS/Azure nodes based on AI forecasts.

3. Deep Learning (LSTM): Implementing Long Short-Term Memory networks for more complex, non-linear seasonality forecasting.

Contact: Love Adegbenro – LinkedIn Profile: www.linkedin.com/in/love-adegbenro

Company Context: Developed for portfolio alignment with observability standards.



