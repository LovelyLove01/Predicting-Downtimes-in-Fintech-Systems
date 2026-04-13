import dash
from dash import dcc, html, dash_table, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import IsolationForest

# --- 1. DATA & AI ENGINE ---
def load_and_process_data():
    df = pd.read_csv('merged_observability_data.csv')
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Run Isolation Forest Anomaly Detection
    features = ['mem_usage', 'cpu_usage', 'response_time_ms']
    model = IsolationForest(contamination=0.05, random_state=42)
    df['anomaly_signal'] = model.fit_predict(df[features])
    
    return df

df = load_and_process_data()

# --- 2. INITIALIZE DASH APP ---
app = dash.Dash(__name__)
app.title = "Nathan Claire AI-Ops"

# --- 3. APP LAYOUT ---
app.layout = html.Div(style={'backgroundColor': '#111111', 'color': 'white', 'fontFamily': 'sans-serif', 'padding': '20px'}, children=[
    
    html.H1("🚀 Nathan Claire Africa: AI-Ops Dash", style={'textAlign': 'center', 'color': '#00D4FF'}),
    html.Hr(style={'borderColor': '#333'}),

    # TOP ROW: Metric Cards
    html.Div([
        html.Div([
            html.H4("System Health"),
            html.H2("94.2%", style={'color': '#00FF00'})
        ], style={'width': '30%', 'display': 'inline-block', 'textAlign': 'center', 'border': '1px solid #333', 'borderRadius': '10px'}),
        
        html.Div([
            html.H4("Total Anomalies"),
            html.H2(len(df[df['anomaly_signal'] == -1]), style={'color': '#FF8C00'})
        ], style={'width': '30%', 'display': 'inline-block', 'textAlign': 'center', 'border': '1px solid #333', 'borderRadius': '10px', 'marginLeft': '4%'}),
        
        html.Div([
            html.H4("Avg Latency"),
            html.H2(f"{df['response_time_ms'].mean():.0f}ms", style={'color': '#00D4FF'})
        ], style={'width': '30%', 'display': 'inline-block', 'textAlign': 'center', 'border': '1px solid #333', 'borderRadius': '10px', 'marginLeft': '4%'}),
    ], style={'padding': '20px'}),

    # MIDDLE ROW: Predictive Forecasting Graph
    html.Div([
        html.H3("📈 Predictive Infrastructure Scaling (Memory Forecast)"),
        dcc.Graph(id='predictive-scaling-graph')
    ], style={'padding': '20px', 'backgroundColor': '#1A1A1A', 'borderRadius': '15px'}),

    # BOTTOM ROW: Anomaly Table and Distribution
    html.Div([
        html.Div([
            html.H3("🔍 Critical Anomaly Log"),
            dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in ['timestamp', 'response_time_ms', 'status_code']],
                data=df[df['anomaly_signal'] == -1].tail(10).to_dict('records'),
                style_header={'backgroundColor': '#333', 'color': 'white', 'fontWeight': 'bold'},
                style_data={'backgroundColor': '#222', 'color': 'white', 'border': '1px solid #444'},
                page_size=10
            )
        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            html.H3("📊 Latency Distribution"),
            dcc.Graph(id='latency-dist')
        ], style={'width': '48%', 'display': 'inline-block', 'float': 'right'})
    ], style={'padding': '20px'})
])

# --- 4. CALLBACKS FOR INTERACTIVITY ---
@app.callback(
    [Output('predictive-scaling-graph', 'figure'),
     Output('latency-dist', 'figure')],
    [Input('predictive-scaling-graph', 'id')] # Triggered on load
)
def update_dashboard(_):
    # --- Part A: Predictive Scaling Math ---
    recent = df.tail(200).copy()
    recent['time_idx'] = np.arange(len(recent))
    
    reg_model = LinearRegression().fit(recent[['time_idx']], recent['mem_usage'])
    
    # Forecast next 100 intervals
    future_idx = np.arange(len(recent), len(recent) + 100).reshape(-1, 1)
    preds = reg_model.predict(future_idx)
    future_ts = [recent['timestamp'].iloc[-1] + pd.Timedelta(minutes=5*i) for i in range(1, 101)]
    
    # Build Forecast Figure
    fig_forecast = go.Figure()
    fig_forecast.add_trace(go.Scatter(x=recent['timestamp'], y=recent['mem_usage'], name="Actual Memory"))
    fig_forecast.add_trace(go.Scatter(x=future_ts, y=preds, name="AI Forecast", line=dict(dash='dash', color='red')))
    fig_forecast.add_hline(y=90, line_dash="dot", line_color="orange", annotation_text="Critical Threshold")
    fig_forecast.update_layout(template="plotly_dark", margin=dict(l=20, r=20, t=40, b=20))

    # --- Part B: Latency Distribution ---
    fig_dist = px.histogram(df, x="response_time_ms", color="status_code", template="plotly_dark", nbins=30)
    fig_dist.update_layout(margin=dict(l=20, r=20, t=40, b=20))

    return fig_forecast, fig_dist

# --- 5. RUN SERVER ---
if __name__ == '__main__':
    app.run(debug=True)