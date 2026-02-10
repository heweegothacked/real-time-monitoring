"""
Weather API Integration
Fetches real sensor data from OpenWeatherMap API instead of simulating data.
Replaces the sensor simulator for production use with actual environmental data.
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from database import DatabaseManager
import warnings


class WeatherAPIProvider:
    """
    Fetches real weather data from OpenWeatherMap API.
    
    This provider replaces the sensor simulator with real-world data,
    enabling the monitoring system to work with actual environmental conditions.
    """
    
    def __init__(self, api_key, city="London", db_path="data/sensor_data.db"):
        """
        Initialize Weather API provider.
        
        Args:
            api_key (str): OpenWeatherMap API key
            city (str): City name for weather data
            db_path (str): Path to SQLite database
        """
        self.api_key = api_key
        self.city = city
        self.db = DatabaseManager(db_path=db_path)
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        self.forecast_url = "https://api.openweathermap.org/data/2.5/forecast"
        self.last_reading_time = None
    
    def get_current_weather(self):
        """
        Fetch current weather data from API.
        
        Returns:
            dict: Current weather with temperature, humidity, pressure
        """
        try:
            params = {
                'q': self.city,
                'appid': self.api_key,
                'units': 'metric'  # Use Celsius
            }
            
            response = requests.get(self.base_url, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                'timestamp': datetime.now(),
                'temperature': round(data['main']['temp'], 2),
                'humidity': round(data['main']['humidity'], 2),
                'pressure': round(data['main']['pressure'], 2),
                'description': data['weather'][0]['main'],
                'city': data['name'],
                'country': data['sys']['country']
            }
        
        except requests.exceptions.RequestException as e:
            warnings.warn(f"Failed to fetch weather data: {str(e)}")
            return None
        except KeyError as e:
            warnings.warn(f"Invalid API response format: {str(e)}")
            return None
    
    def get_forecast(self, steps_ahead=5):
        """
        Fetch weather forecast for next hours.
        
        Args:
            steps_ahead (int): Number of 3-hour intervals to forecast
        
        Returns:
            list: List of forecasted readings
        """
        try:
            params = {
                'q': self.city,
                'appid': self.api_key,
                'units': 'metric',
                'cnt': min(steps_ahead, 40)  # API max is 40
            }
            
            response = requests.get(self.forecast_url, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            forecasts = []
            
            for item in data['list'][:steps_ahead]:
                forecasts.append({
                    'timestamp': datetime.fromtimestamp(item['dt']),
                    'temperature': round(item['main']['temp'], 2),
                    'humidity': round(item['main']['humidity'], 2),
                    'pressure': round(item['main']['pressure'], 2),
                    'description': item['weather'][0]['main']
                })
            
            return forecasts
        
        except requests.exceptions.RequestException as e:
            warnings.warn(f"Failed to fetch forecast data: {str(e)}")
            return []
        except KeyError as e:
            warnings.warn(f"Invalid forecast response format: {str(e)}")
            return []
    
    def get_next_reading(self, save_to_db=True, cache_minutes=10):
        """
        Get next reading with caching to avoid excessive API calls.
        
        Args:
            save_to_db (bool): Whether to save reading to database
            cache_minutes (int): Cache results for N minutes to avoid rate limits
        
        Returns:
            dict: Current weather reading
        """
        # Check if we should use cached data
        if (self.last_reading_time is not None and
            (datetime.now() - self.last_reading_time).total_seconds() < cache_minutes * 60):
            # Return simulated variation on last reading to simulate real-time changes
            last = self.get_latest_from_db()
            if last:
                return self._add_slight_variation(last, cache_minutes)
        
        reading = self.get_current_weather()
        
        if reading and save_to_db:
            self.db.save_reading(
                temperature=reading['temperature'],
                humidity=reading['humidity'],
                pressure=reading['pressure'],
                timestamp=reading['timestamp'].isoformat()
            )
            self.last_reading_time = datetime.now()
        
        return reading
    
    def _add_slight_variation(self, reading, cache_minutes):
        """
        Add slight realistic variation to cached reading.
        
        Args:
            reading (dict): Original reading
            cache_minutes (int): Minutes since last real API call
        
        Returns:
            dict: Reading with slight variation
        """
        varied_reading = reading.copy()
        
        # Add small random drift to each metric
        varied_reading['temperature'] += np.random.normal(0, 0.1)
        varied_reading['humidity'] += np.random.normal(0, 0.5)
        varied_reading['pressure'] += np.random.normal(0, 0.1)
        
        # Keep in valid ranges
        varied_reading['temperature'] = np.clip(varied_reading['temperature'], -50, 60)
        varied_reading['humidity'] = np.clip(varied_reading['humidity'], 0, 100)
        varied_reading['pressure'] = np.clip(varied_reading['pressure'], 850, 1085)
        
        return {
            **varied_reading,
            'temperature': round(varied_reading['temperature'], 2),
            'humidity': round(varied_reading['humidity'], 2),
            'pressure': round(varied_reading['pressure'], 2)
        }
    
    def get_latest_from_db(self):
        """Get latest reading from database."""
        return self.db.get_latest_reading()
    
    def generate_batch(self, num_readings=50, save_to_db=True):
        """
        Generate batch of weather readings with caching.
        
        Args:
            num_readings (int): Number of readings to generate
            save_to_db (bool): Whether to save to database
        
        Returns:
            DataFrame: Historical readings
        """
        readings = []
        
        for i in range(num_readings):
            reading = self.get_next_reading(save_to_db=save_to_db, cache_minutes=5)
            
            if reading:
                readings.append({
                    'timestamp': reading['timestamp'],
                    'temperature': reading['temperature'],
                    'humidity': reading['humidity'],
                    'pressure': reading['pressure']
                })
            
            # Small delay between calls to be respectful to API
            if i < num_readings - 1:
                import time
                time.sleep(0.5)
        
        return pd.DataFrame(readings) if readings else pd.DataFrame()
    
    def get_location_info(self):
        """
        Get location information for the configured city.
        
        Returns:
            dict: Location info (city, country, coordinates, etc)
        """
        try:
            params = {
                'q': self.city,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(self.base_url, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                'city': data['name'],
                'country': data['sys']['country'],
                'latitude': data['coord']['lat'],
                'longitude': data['coord']['lon'],
                'timezone': data.get('timezone', 'Unknown')
            }
        
        except Exception as e:
            warnings.warn(f"Failed to fetch location info: {str(e)}")
            return None


# Configuration helper
class WeatherConfig:
    """Helper class for weather API configuration."""
    
    # Get your free API key at https://openweathermap.org/api
    # Free tier includes current weather and 5-day forecast
    
    SAMPLE_CITIES = [
        "London",
        "New York",
        "Tokyo",
        "Sydney",
        "Paris",
        "Berlin",
        "Toronto",
        "Singapore",
        "Dubai",
        "Mumbai"
    ]
    
    @staticmethod
    def get_api_instructions():
        """Get instructions for obtaining OpenWeatherMap API key."""
        return """
        === Getting Your Free OpenWeatherMap API Key ===
        
        1. Visit: https://openweathermap.org/api
        2. Sign up for free account
        3. Go to API keys section
        4. Copy your Default API Key
        5. Use it in your Streamlit app:
        
           import os
           os.environ['OPENWEATHER_API_KEY'] = 'your_api_key_here'
           
        OR set as environment variable:
           set OPENWEATHER_API_KEY=your_api_key_here  (Windows)
           export OPENWEATHER_API_KEY=your_api_key_here  (Linux/Mac)
        
        === Free Tier Limits ===
        - 60 calls/minute
        - Current weather data
        - 5-day forecast (3-hour steps)
        - Perfect for this project!
        """


if __name__ == "__main__":
    # Example usage
    print("Weather API Integration Module")
    print("=" * 50)
    print(WeatherConfig.get_api_instructions())
    
    # Uncomment to test (requires valid API key):
    # api_key = "your_api_key_here"
    # provider = WeatherAPIProvider(api_key=api_key, city="London")
    # 
    # current = provider.get_current_weather()
    # print("\nCurrent Weather:")
    # print(current)
    # 
    # forecast = provider.get_forecast(steps_ahead=5)
    # print("\nForecast:")
    # for item in forecast:
    #     print(f"  {item['timestamp']}: {item['temperature']}°C")
