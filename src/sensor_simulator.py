"""
Sensor Data Simulator
This module simulates real-time sensor data for temperature, humidity, and pressure.
In a real application, this would connect to actual sensors.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta


class SensorSimulator:
    """
    Simulates realistic sensor data with trends and anomalies.
    
    This class generates time-series data that mimics real sensor readings
    for temperature, humidity, and pressure measurements.
    """
    
    def __init__(self, random_seed=42):
        """
        Initialize the sensor simulator.
        
        Args:
            random_seed (int): Seed for reproducible random data
        """
        np.random.seed(random_seed)
        self.temperature = 20.0  # Celsius
        self.humidity = 50.0     # Percentage
        self.pressure = 1013.0   # hPa (hectopascals)
    
    def get_next_reading(self, anomaly_probability=0.05):
        """
        Get the next sensor reading with realistic variations.
        
        Args:
            anomaly_probability (float): Probability of an anomaly (0.0-1.0)
        
        Returns:
            dict: Dictionary with temperature, humidity, pressure, and timestamp
        """
        # Small random walk to simulate natural sensor variations
        self.temperature += np.random.normal(0, 0.5)  # Drift ±0.5°C
        self.humidity += np.random.normal(0, 2)       # Drift ±2%
        self.pressure += np.random.normal(0, 0.3)     # Drift ±0.3 hPa
        
        # Keep values in realistic ranges
        self.temperature = np.clip(self.temperature, -10, 50)
        self.humidity = np.clip(self.humidity, 0, 100)
        self.pressure = np.clip(self.pressure, 950, 1050)
        
        # Randomly introduce anomalies (sensor malfunctions, extreme conditions)
        if np.random.random() < anomaly_probability:
            if np.random.random() < 0.5:
                self.temperature += np.random.uniform(5, 15)  # Spike
            else:
                self.humidity += np.random.uniform(20, 40)    # Spike
        
        return {
            'timestamp': datetime.now(),
            'temperature': round(self.temperature, 2),
            'humidity': round(self.humidity, 2),
            'pressure': round(self.pressure, 2)
        }
    
    def generate_batch(self, num_readings=100, anomaly_probability=0.05):
        """
        Generate a batch of sensor readings.
        
        Args:
            num_readings (int): Number of readings to generate
            anomaly_probability (float): Probability of anomalies
        
        Returns:
            DataFrame: Pandas DataFrame with all readings
        """
        readings = []
        for _ in range(num_readings):
            readings.append(self.get_next_reading(anomaly_probability))
        
        return pd.DataFrame(readings)


if __name__ == "__main__":
    # Test the sensor simulator
    simulator = SensorSimulator()
    data = simulator.generate_batch(num_readings=10)
    print("Sample sensor data:")
    print(data)
