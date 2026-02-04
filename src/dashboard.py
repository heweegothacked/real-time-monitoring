"""
Real-Time Monitoring Dashboard
A Streamlit-based dashboard for visualizing sensor data and AI predictions.
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import sys

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from sensor_simulator import SensorSimulator
from ml_model import MonitoringAIModel


# Page configuration
st.set_page_config(
    page_title="Real-Time Monitoring System",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .anomaly {
        background-color: #ffcccc;
        padding: 10px;
        border-radius: 5px;
        color: #cc0000;
    }
    .normal {
        background-color: #ccffcc;
        padding: 10px;
        border-radius: 5px;
        color: #00cc00;
    }
    </style>
""", unsafe_allow_html=True)


# Initialize session state
if 'simulator' not in st.session_state:
    st.session_state.simulator = SensorSimulator(random_seed=42)
    st.session_state.data = pd.DataFrame()
    st.session_state.model = MonitoringAIModel()

if 'num_readings' not in st.session_state:
    st.session_state.num_readings = 0


def main():
    st.title("📊 Real-Time Monitoring System with AI Predictions")
    st.markdown("---")
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Data collection settings
        st.subheader("Data Collection")
        num_initial_readings = st.slider(
            "Initial readings to generate:",
            min_value=10,
            max_value=200,
            value=50,
            step=10,
            help="Number of historical readings for model training"
        )
        
        anomaly_prob = st.slider(
            "Anomaly probability:",
            min_value=0.0,
            max_value=0.5,
            value=0.05,
            step=0.05,
            help="Probability of sensor anomalies occurring"
        )
        
        # Model settings
        st.subheader("Model Settings")
        contamination = st.slider(
            "Anomaly contamination rate:",
            min_value=0.01,
            max_value=0.3,
            value=0.1,
            step=0.05,
            help="Expected proportion of anomalies in data"
        )
        
        prediction_steps = st.slider(
            "Prediction steps ahead:",
            min_value=1,
            max_value=20,
            value=5,
            step=1,
            help="How many time steps to predict into the future"
        )
        
        # Action buttons
        st.subheader("Actions")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 Initialize System"):
                st.session_state.simulator = SensorSimulator(random_seed=42)
                st.session_state.data = st.session_state.simulator.generate_batch(
                    num_readings=num_initial_readings,
                    anomaly_probability=anomaly_prob
                )
                st.session_state.model = MonitoringAIModel(contamination=contamination)
                st.session_state.model.train(st.session_state.data)
                st.session_state.num_readings = len(st.session_state.data)
                st.success("✓ System initialized!")
                st.rerun()
        
        with col2:
            if st.button("➕ Add New Reading"):
                if len(st.session_state.data) > 0:
                    new_reading = st.session_state.simulator.get_next_reading(anomaly_prob)
                    new_df = pd.DataFrame([new_reading])
                    st.session_state.data = pd.concat(
                        [st.session_state.data, new_df],
                        ignore_index=True
                    )
                    st.session_state.num_readings += 1
                    st.info("✓ New reading added!")
                    st.rerun()
                else:
                    st.warning("Initialize system first!")
    
    # Main content area
    if len(st.session_state.data) == 0:
        st.info("👈 Click 'Initialize System' in the sidebar to start")
        return
    
    # Display current status
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "Total Readings",
            st.session_state.num_readings,
            delta=None
        )
    with col2:
        st.metric(
            "System Status",
            "🟢 Active"
        )
    with col3:
        st.metric(
            "Last Update",
            st.session_state.data['timestamp'].iloc[-1].strftime("%H:%M:%S")
        )
    
    st.markdown("---")
    
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Live Data",
        "🤖 AI Predictions",
        "⚠️ Anomaly Detection",
        "📊 Analysis"
    ])
    
    # Tab 1: Live Data Visualization
    with tab1:
        st.subheader("Current Sensor Readings")
        
        # Current metrics
        current = st.session_state.data.iloc[-1]
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>🌡️ Temperature</h3>
                <h2>{current['temperature']}°C</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>💧 Humidity</h3>
                <h2>{current['humidity']}%</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3>🔘 Pressure</h3>
                <h2>{current['pressure']} hPa</h2>
            </div>
            """, unsafe_allow_html=True)
        
        # Time series plot
        st.subheader("Time Series Data")
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=st.session_state.data['timestamp'],
            y=st.session_state.data['temperature'],
            mode='lines+markers',
            name='Temperature (°C)',
            line=dict(color='red', width=2),
            marker=dict(size=4)
        ))
        
        fig.add_trace(go.Scatter(
            x=st.session_state.data['timestamp'],
            y=st.session_state.data['humidity'],
            mode='lines+markers',
            name='Humidity (%)',
            line=dict(color='blue', width=2),
            marker=dict(size=4),
            yaxis='y2'
        ))
        
        fig.add_trace(go.Scatter(
            x=st.session_state.data['timestamp'],
            y=st.session_state.data['pressure'],
            mode='lines+markers',
            name='Pressure (hPa)',
            line=dict(color='green', width=2),
            marker=dict(size=4),
            yaxis='y3'
        ))
        
        fig.update_layout(
            title="Sensor Data Over Time",
            xaxis_title="Time",
            yaxis_title="Temperature (°C)",
            yaxis2=dict(title="Humidity (%)", overlaying="y", side="right"),
            yaxis3=dict(title="Pressure (hPa)", overlaying="y", side="right", anchor="free", x=1.15),
            height=500,
            hovermode='x unified',
            legend=dict(x=0, y=1)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Tab 2: AI Predictions
    with tab2:
        st.subheader("🤖 AI-Powered Predictions")
        
        predictions = st.session_state.model.predict_next(
            st.session_state.data,
            steps_ahead=prediction_steps
        )
        
        if predictions:
            # Create prediction visualization
            future_times = [
                st.session_state.data['timestamp'].iloc[-1] + timedelta(hours=i)
                for i in range(1, prediction_steps + 1)
            ]
            
            col1, col2 = st.columns(2)
            
            # Temperature prediction
            with col1:
                fig_temp = go.Figure()
                
                # Historical data
                fig_temp.add_trace(go.Scatter(
                    x=st.session_state.data['timestamp'].tail(20),
                    y=st.session_state.data['temperature'].tail(20),
                    mode='lines+markers',
                    name='Historical',
                    line=dict(color='red', width=2)
                ))
                
                # Prediction
                fig_temp.add_trace(go.Scatter(
                    x=future_times,
                    y=predictions['temperature'],
                    mode='lines+markers',
                    name='Prediction',
                    line=dict(color='red', width=2, dash='dash'),
                    marker=dict(size=8)
                ))
                
                fig_temp.update_layout(
                    title="Temperature Prediction",
                    xaxis_title="Time",
                    yaxis_title="Temperature (°C)",
                    height=400,
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig_temp, use_container_width=True)
            
            # Humidity prediction
            with col2:
                fig_hum = go.Figure()
                
                fig_hum.add_trace(go.Scatter(
                    x=st.session_state.data['timestamp'].tail(20),
                    y=st.session_state.data['humidity'].tail(20),
                    mode='lines+markers',
                    name='Historical',
                    line=dict(color='blue', width=2)
                ))
                
                fig_hum.add_trace(go.Scatter(
                    x=future_times,
                    y=predictions['humidity'],
                    mode='lines+markers',
                    name='Prediction',
                    line=dict(color='blue', width=2, dash='dash'),
                    marker=dict(size=8)
                ))
                
                fig_hum.update_layout(
                    title="Humidity Prediction",
                    xaxis_title="Time",
                    yaxis_title="Humidity (%)",
                    height=400,
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig_hum, use_container_width=True)
            
            # Pressure prediction
            fig_pres = go.Figure()
            
            fig_pres.add_trace(go.Scatter(
                x=st.session_state.data['timestamp'].tail(20),
                y=st.session_state.data['pressure'].tail(20),
                mode='lines+markers',
                name='Historical',
                line=dict(color='green', width=2)
            ))
            
            fig_pres.add_trace(go.Scatter(
                x=future_times,
                y=predictions['pressure'],
                mode='lines+markers',
                name='Prediction',
                line=dict(color='green', width=2, dash='dash'),
                marker=dict(size=8)
            ))
            
            fig_pres.update_layout(
                title="Pressure Prediction",
                xaxis_title="Time",
                yaxis_title="Pressure (hPa)",
                height=400,
                hovermode='x unified'
            )
            
            st.plotly_chart(fig_pres, use_container_width=True)
    
    # Tab 3: Anomaly Detection
    with tab3:
        st.subheader("⚠️ Anomaly Detection Analysis")
        
        anomalies = st.session_state.model.detect_anomalies(st.session_state.data)
        num_anomalies = sum(anomalies)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Anomalies", num_anomalies)
        with col2:
            st.metric("Anomaly Rate", f"{(num_anomalies/len(st.session_state.data)*100):.1f}%")
        with col3:
            st.metric("Normal Readings", len(st.session_state.data) - num_anomalies)
        
        # Anomaly timeline
        st.subheader("Anomaly Timeline")
        
        data_with_anomalies = st.session_state.data.copy()
        data_with_anomalies['is_anomaly'] = anomalies
        
        fig = go.Figure()
        
        # Normal points
        normal_data = data_with_anomalies[~data_with_anomalies['is_anomaly']]
        fig.add_trace(go.Scatter(
            x=normal_data['timestamp'],
            y=normal_data['temperature'],
            mode='markers',
            name='Normal',
            marker=dict(color='green', size=8)
        ))
        
        # Anomaly points
        anomaly_data = data_with_anomalies[data_with_anomalies['is_anomaly']]
        if len(anomaly_data) > 0:
            fig.add_trace(go.Scatter(
                x=anomaly_data['timestamp'],
                y=anomaly_data['temperature'],
                mode='markers',
                name='Anomaly',
                marker=dict(color='red', size=12, symbol='star')
            ))
        
        fig.update_layout(
            title="Anomalies Detected in Temperature",
            xaxis_title="Time",
            yaxis_title="Temperature (°C)",
            height=400,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Anomaly details
        if num_anomalies > 0:
            st.subheader("Recent Anomalies")
            anomaly_records = data_with_anomalies[data_with_anomalies['is_anomaly']].tail(10)
            st.dataframe(anomaly_records, use_container_width=True)
    
    # Tab 4: Trend Analysis
    with tab4:
        st.subheader("📊 Trend Analysis")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            trend = st.session_state.model.get_trend(st.session_state.data, 'temperature')
            st.markdown(f"**Temperature Trend**\n{trend}")
        
        with col2:
            trend = st.session_state.model.get_trend(st.session_state.data, 'humidity')
            st.markdown(f"**Humidity Trend**\n{trend}")
        
        with col3:
            trend = st.session_state.model.get_trend(st.session_state.data, 'pressure')
            st.markdown(f"**Pressure Trend**\n{trend}")
        
        # Statistics
        st.subheader("Statistical Summary")
        
        stats_df = st.session_state.data[['temperature', 'humidity', 'pressure']].describe()
        st.dataframe(stats_df, use_container_width=True)
        
        # Distribution plots
        col1, col2, col3 = st.columns(3)
        
        with col1:
            fig = px.histogram(
                st.session_state.data,
                x='temperature',
                nbins=20,
                title='Temperature Distribution'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.histogram(
                st.session_state.data,
                x='humidity',
                nbins=20,
                title='Humidity Distribution'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col3:
            fig = px.histogram(
                st.session_state.data,
                x='pressure',
                nbins=20,
                title='Pressure Distribution'
            )
            st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()
