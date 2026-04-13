import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np

st.set_page_config(page_title="SmartSpend AI Observability", layout="wide")
st.title("AI-Powered Observability Dashboard")

# Load our processed data
df = pd.read_csv('merged_observability_data.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'])

# SIDEBAR: NODE SELECTION
node = st.sidebar.selectbox("Select Server Node", df['node_id'].unique())
current_data = df[df['node_id'] == node]

# PREDICTIVE SCALING
st.subheader("Predictive Infrastructure Scaling")
col1, col2 = st.columns([3, 1])

# Math for Prediction: Linear Regression on Memory
X = np.array(range(len(current_data))).reshape(-1, 1)
y = current_data['mem_usage'].values
model = LinearRegression().fit(X, y)

# Predict next 24 hours (roughly 288 five-minute intervals)
future_X = np.array(range(len(current_data), len(current_data) + 288)).reshape(-1, 1)
future_preds = model.predict(future_X)

with col1:
    fig = px.line(current_data, x='timestamp', y='mem_usage', title="Memory Trend & Forecast")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.metric("Current Memory", f"{y[-1]:.2f}%")
    days_to_failure = (100 - y[-1]) / model.coef_[0] / 288 # Simplified prediction
    st.warning(f"Estimated Time to 100%: {days_to_failure:.1f} Days")

# SECTION 2: AI ANOMALY LOGS 
st.subheader("Real-Time AI Incident Analysis")
anomaly_df = current_data[current_data['anomaly_signal'] == -1].tail(10)
st.table(anomaly_df[['timestamp', 'response_time_ms', 'status_code']])