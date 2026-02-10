"""
SQLite Database Manager for Persistent Data Storage
This module handles all database operations for storing and retrieving sensor readings.
"""

import sqlite3
import pandas as pd
from datetime import datetime
from pathlib import Path


class DatabaseManager:
    """
    Manages SQLite database operations for sensor data persistence.
    
    This class handles:
    - Database initialization and schema creation
    - Saving sensor readings
    - Retrieving historical data
    - Data aggregation and statistics
    """
    
    def __init__(self, db_path="data/sensor_data.db"):
        """
        Initialize the database manager.
        
        Args:
            db_path (str): Path to SQLite database file
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_database()
    
    def init_database(self):
        """Initialize the database schema if it doesn't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create readings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL UNIQUE,
                temperature REAL NOT NULL,
                humidity REAL NOT NULL,
                pressure REAL NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create anomalies table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS anomalies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reading_id INTEGER NOT NULL,
                timestamp TEXT NOT NULL,
                anomaly_type TEXT,
                severity REAL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (reading_id) REFERENCES readings(id)
            )
        ''')
        
        # Create predictions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                metric TEXT NOT NULL,
                prediction_value REAL NOT NULL,
                steps_ahead INTEGER,
                model_type TEXT DEFAULT 'linear',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_reading(self, temperature, humidity, pressure, timestamp=None):
        """
        Save a single sensor reading to the database.
        
        Args:
            temperature (float): Temperature in Celsius
            humidity (float): Humidity percentage
            pressure (float): Pressure in hPa
            timestamp (str): ISO format timestamp (defaults to now)
        
        Returns:
            int: Reading ID if successful, None if duplicate timestamp
        """
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO readings (timestamp, temperature, humidity, pressure)
                VALUES (?, ?, ?, ?)
            ''', (timestamp, temperature, humidity, pressure))
            
            reading_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return reading_id
        
        except sqlite3.IntegrityError:
            # Duplicate timestamp
            return None
    
    def save_readings_batch(self, df):
        """
        Save multiple readings from a DataFrame.
        
        Args:
            df (DataFrame): DataFrame with columns [timestamp, temperature, humidity, pressure]
        
        Returns:
            int: Number of readings successfully saved
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        count = 0
        for _, row in df.iterrows():
            try:
                cursor.execute('''
                    INSERT INTO readings (timestamp, temperature, humidity, pressure)
                    VALUES (?, ?, ?, ?)
                ''', (
                    row['timestamp'].isoformat() if hasattr(row['timestamp'], 'isoformat') else str(row['timestamp']),
                    row['temperature'],
                    row['humidity'],
                    row['pressure']
                ))
                count += 1
            except sqlite3.IntegrityError:
                # Skip duplicate timestamps
                pass
        
        conn.commit()
        conn.close()
        return count
    
    def get_readings(self, limit=None, offset=0):
        """
        Retrieve sensor readings from the database.
        
        Args:
            limit (int): Maximum number of readings to retrieve
            offset (int): Number of readings to skip
        
        Returns:
            DataFrame: DataFrame with all readings
        """
        conn = sqlite3.connect(self.db_path)
        
        if limit is None:
            query = 'SELECT timestamp, temperature, humidity, pressure FROM readings ORDER BY timestamp DESC'
            df = pd.read_sql_query(query, conn)
        else:
            query = f'SELECT timestamp, temperature, humidity, pressure FROM readings ORDER BY timestamp DESC LIMIT {limit} OFFSET {offset}'
            df = pd.read_sql_query(query, conn)
        
        conn.close()
        
        if not df.empty:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp').reset_index(drop=True)
        
        return df
    
    def get_readings_since(self, hours=1):
        """
        Get all readings from the last N hours.
        
        Args:
            hours (int): Number of hours to look back
        
        Returns:
            DataFrame: Readings from the specified time period
        """
        conn = sqlite3.connect(self.db_path)
        
        query = '''
            SELECT timestamp, temperature, humidity, pressure 
            FROM readings 
            WHERE datetime(timestamp) >= datetime('now', ? || ' hours')
            ORDER BY timestamp
        '''
        
        df = pd.read_sql_query(query, conn, params=(-hours,))
        conn.close()
        
        if not df.empty:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        return df
    
    def get_latest_reading(self):
        """
        Get the most recent sensor reading.
        
        Returns:
            dict: Latest reading or None if no data exists
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT timestamp, temperature, humidity, pressure 
            FROM readings 
            ORDER BY timestamp DESC 
            LIMIT 1
        ''')
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'timestamp': row[0],
                'temperature': row[1],
                'humidity': row[2],
                'pressure': row[3]
            }
        return None
    
    def save_anomaly(self, reading_id, timestamp, anomaly_type='unknown', severity=1.0):
        """
        Save detected anomaly to database.
        
        Args:
            reading_id (int): ID of the reading with anomaly
            timestamp (str): Timestamp of the anomaly
            anomaly_type (str): Type of anomaly detected
            severity (float): Severity score 0-1
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO anomalies (reading_id, timestamp, anomaly_type, severity)
            VALUES (?, ?, ?, ?)
        ''', (reading_id, timestamp, anomaly_type, severity))
        
        conn.commit()
        conn.close()
    
    def get_anomalies(self, limit=100):
        """
        Get recent anomalies.
        
        Args:
            limit (int): Maximum number of anomalies to retrieve
        
        Returns:
            DataFrame: Recent anomalies
        """
        conn = sqlite3.connect(self.db_path)
        
        query = '''
            SELECT timestamp, anomaly_type, severity 
            FROM anomalies 
            ORDER BY timestamp DESC 
            LIMIT ?
        '''
        
        df = pd.read_sql_query(query, conn, params=(limit,))
        conn.close()
        
        if not df.empty:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        return df
    
    def save_prediction(self, timestamp, metric, prediction_value, steps_ahead=5, model_type='linear'):
        """
        Save model prediction to database.
        
        Args:
            timestamp (str): Timestamp of prediction
            metric (str): Metric name (temperature, humidity, pressure)
            prediction_value (float): Predicted value
            steps_ahead (int): Steps predicted ahead
            model_type (str): Type of model used (linear, lstm, etc)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO predictions (timestamp, metric, prediction_value, steps_ahead, model_type)
            VALUES (?, ?, ?, ?, ?)
        ''', (timestamp, metric, prediction_value, steps_ahead, model_type))
        
        conn.commit()
        conn.close()
    
    def get_stats(self):
        """
        Get statistics about stored data.
        
        Returns:
            dict: Statistics including count, temperature range, etc
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM readings')
        count = cursor.fetchone()[0]
        
        if count > 0:
            cursor.execute('''
                SELECT 
                    MIN(temperature) as temp_min,
                    MAX(temperature) as temp_max,
                    AVG(temperature) as temp_avg,
                    MIN(humidity) as humidity_min,
                    MAX(humidity) as humidity_max,
                    AVG(humidity) as humidity_avg
                FROM readings
            ''')
            stats_row = cursor.fetchone()
            
            cursor.execute('SELECT COUNT(*) FROM anomalies')
            anomaly_count = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                'total_readings': count,
                'anomalies_detected': anomaly_count,
                'temperature_range': (stats_row[0], stats_row[1]),
                'temperature_avg': stats_row[2],
                'humidity_range': (stats_row[3], stats_row[4]),
                'humidity_avg': stats_row[5]
            }
        
        conn.close()
        return {'total_readings': 0}
    
    def clear_old_data(self, days=30):
        """
        Delete readings older than specified days.
        
        Args:
            days (int): Number of days to keep
        
        Returns:
            int: Number of rows deleted
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM readings 
            WHERE datetime(timestamp) < datetime('now', ? || ' days')
        ''', (-days,))
        
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        return deleted_count


if __name__ == "__main__":
    # Test the database manager
    db = DatabaseManager()
    
    # Save a test reading
    reading_id = db.save_reading(temperature=22.5, humidity=55.0, pressure=1013.5)
    print(f"✓ Saved reading with ID: {reading_id}")
    
    # Retrieve readings
    readings = db.get_readings(limit=5)
    print(f"✓ Retrieved {len(readings)} readings")
    print(readings)
    
    # Get stats
    stats = db.get_stats()
    print(f"✓ Database stats: {stats}")
