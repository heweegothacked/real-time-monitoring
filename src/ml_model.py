"""
Machine Learning Model for Predictions and Anomaly Detection
This module provides AI-powered predictions and anomaly detection capabilities.
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LinearRegression


class MonitoringAIModel:
    """
    AI model for real-time monitoring with prediction and anomaly detection.
    
    This class uses:
    - Isolation Forest for unsupervised anomaly detection
    - Linear Regression for trend prediction
    """
    
    def __init__(self, contamination=0.1, lookback_window=20):
        """
        Initialize the AI model.
        
        Args:
            contamination (float): Expected proportion of anomalies (0.0-0.5)
            lookback_window (int): Number of historical points for prediction
        """
        self.contamination = contamination
        self.lookback_window = lookback_window
        
        # Initialize anomaly detector
        self.anomaly_detector = IsolationForest(
            contamination=contamination,
            random_state=42
        )
        
        # Initialize predictors for each metric
        self.predictors = {
            'temperature': LinearRegression(),
            'humidity': LinearRegression(),
            'pressure': LinearRegression()
        }
        
        self.scaler = StandardScaler()
        self.is_fitted = False
    
    def train(self, data):
        """
        Train the model on historical data.
        
        Args:
            data (DataFrame): DataFrame with columns [temperature, humidity, pressure]
        """
        if len(data) < 2:
            raise ValueError("Need at least 2 data points to train")
        
        # Prepare features for anomaly detection
        features = data[['temperature', 'humidity', 'pressure']].values
        self.scaler.fit(features)
        scaled_features = self.scaler.transform(features)
        
        # Train anomaly detector
        self.anomaly_detector.fit(scaled_features)
        
        # Train prediction models
        X = np.arange(len(data)).reshape(-1, 1)
        for column in ['temperature', 'humidity', 'pressure']:
            y = data[column].values
            self.predictors[column].fit(X, y)
        
        self.is_fitted = True
        print("✓ Model trained successfully")
    
    def detect_anomalies(self, data):
        """
        Detect anomalies in current data.
        
        Args:
            data (DataFrame): Current data with temp, humidity, pressure
        
        Returns:
            list: Boolean list indicating anomalies (True = anomaly detected)
        """
        if not self.is_fitted:
            return [False] * len(data)
        
        features = data[['temperature', 'humidity', 'pressure']].values
        scaled_features = self.scaler.transform(features)
        predictions = self.anomaly_detector.predict(scaled_features)
        
        # Convert predictions: -1 (anomaly) -> True, 1 (normal) -> False
        return predictions == -1
    
    def predict_next(self, data, steps_ahead=5):
        """
        Predict future values for each metric.
        
        Args:
            data (DataFrame): Historical data
            steps_ahead (int): Number of steps to predict into the future
        
        Returns:
            dict: Predictions for temperature, humidity, and pressure
        """
        if not self.is_fitted or len(data) < 2:
            return None
        
        predictions = {}
        n = len(data)
        
        for metric in ['temperature', 'humidity', 'pressure']:
            # Create X values for prediction
            X_train = np.arange(n).reshape(-1, 1)
            X_future = np.arange(n, n + steps_ahead).reshape(-1, 1)
            
            # Get predictions
            future_values = self.predictors[metric].predict(X_future)
            
            # Keep predictions in reasonable ranges
            if metric == 'temperature':
                future_values = np.clip(future_values, -10, 50)
            elif metric == 'humidity':
                future_values = np.clip(future_values, 0, 100)
            else:  # pressure
                future_values = np.clip(future_values, 950, 1050)
            
            predictions[metric] = [round(v, 2) for v in future_values]
        
        return predictions
    
    def get_trend(self, data, metric='temperature'):
        """
        Calculate trend direction for a metric.
        
        Args:
            data (DataFrame): Historical data
            metric (str): Which metric to analyze
        
        Returns:
            str: 'increasing', 'decreasing', or 'stable'
        """
        if len(data) < 2:
            return 'stable'
        
        recent = data[metric].tail(10).values
        trend = np.polyfit(np.arange(len(recent)), recent, 1)[0]
        
        if trend > 0.5:
            return '📈 Increasing'
        elif trend < -0.5:
            return '📉 Decreasing'
        else:
            return '➡️ Stable'


if __name__ == "__main__":
    # Test the model
    from sensor_simulator import SensorSimulator
    
    simulator = SensorSimulator()
    data = simulator.generate_batch(num_readings=50, anomaly_probability=0.1)
    
    model = MonitoringAIModel()
    model.train(data)
    
    print("\nAnomaly detection:")
    anomalies = model.detect_anomalies(data.tail(10))
    print(f"Anomalies detected: {sum(anomalies)} out of {len(anomalies)}")
    
    print("\nNext 5 readings prediction:")
    predictions = model.predict_next(data, steps_ahead=5)
    for metric, values in predictions.items():
        print(f"{metric}: {values}")
    
    print("\nTrends:")
    for metric in ['temperature', 'humidity', 'pressure']:
        trend = model.get_trend(data, metric)
        print(f"{metric}: {trend}")
