import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import numpy as np

# Load data
df = pd.read_csv('merged_observability_data.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'])

st.set_page_config(page_title="SmartSpend AI-Ops", layout="wide")
st.title("SmartSpend: AI-Powered Fintech Observability")

# TOP LEVEL METRIC CARDS
col1, col2, col3, col4 = st.columns(4)
health_score = 100 - (len(df[df['status_code'] == 500]) / len(df) * 100)

col1.metric("System Health", f"{health_score:.1f}%", "-2% vs yesterday")
col2.metric("Total Anomalies (AI)", len(df[df['anomaly_signal'] == -1]))
col3.metric("Avg Latency", f"{df['response_time_ms'].mean():.0f}ms")
col4.metric("Risk Level", "HIGH", delta_color="inverse")

# PREDICTIVE INFRASTRUCTURE SCALING
st.subheader("Predictive Resource Scaling (Memory Forecast)")

# Simple Linear Regression to predict the future
recent = df.tail(200).copy()
recent['index_time'] = np.arange(len(recent))
X = recent[['index_time']]
y = recent['mem_usage']
model = LinearRegression().fit(X, y)

# Predict next 100 intervals (approx 8 hours)
future_indices = np.arange(len(recent), len(recent) + 100).reshape(-1, 1)
predictions = model.predict(future_indices)
future_times = [recent['timestamp'].iloc[-1] + pd.Timedelta(minutes=5*i) for i in range(1, 101)]

# Plotting the trend
fig_forecast = go.Figure()
fig_forecast.add_trace(go.Scatter(x=recent['timestamp'], y=recent['mem_usage'], name="Current Usage"))
fig_forecast.add_trace(go.Scatter(x=future_times, y=predictions, name="AI Forecast", line=dict(dash='dash', color='red')))
fig_forecast.add_hline(y=90, line_dash="dot", line_color="orange", annotation_text="Critical Scaling Threshold")

st.plotly_chart(fig_forecast, use_container_width=True)

# LOG ANALYSIS & ANOMALIES
st.subheader("🔍 Automated Incident & Log Correlation")
left_col, right_col = st.columns(2)

with left_col:
    st.write("AI-Detected Anomaly Events")
    # Cleaned up table without the confusing index numbers
    anomalies = df[df['anomaly_signal'] == -1].tail(10)
    st.dataframe(anomalies[['timestamp', 'response_time_ms', 'status_code']], use_container_width=True, hide_index=True)

with right_col:
    st.write("Response Time Distribution")
    fig_dist = px.histogram(df, x="response_time_ms", color="status_code", nbins=30)
    st.plotly_chart(fig_dist, use_container_width=True)

# DEPLOYMENT CTA
if predictions[-1] > 90:
    st.error(f"PROACTIVE ALERT: Infrastructure exhaustion predicted by {future_times[-1].strftime('%H:%M')}. Provisioning of new node recommended.")