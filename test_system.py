"""
Test Script - Verify all modules work correctly
Run this to make sure the project is set up properly.
"""

import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

print("=" * 60)
print("TESTING REAL-TIME MONITORING SYSTEM")
print("=" * 60)

try:
    print("\n1️⃣  Testing sensor simulator...")
    from sensor_simulator import SensorSimulator
    
    simulator = SensorSimulator()
    data = simulator.generate_batch(num_readings=20)
    print(f"   ✓ Generated {len(data)} sensor readings")
    print(f"   ✓ Sample reading:")
    print(f"      Temperature: {data['temperature'].iloc[-1]}°C")
    print(f"      Humidity: {data['humidity'].iloc[-1]}%")
    print(f"      Pressure: {data['pressure'].iloc[-1]} hPa")
    
except Exception as e:
    print(f"   ✗ Error: {e}")
    sys.exit(1)

try:
    print("\n2️⃣  Testing ML model...")
    from ml_model import MonitoringAIModel
    
    model = MonitoringAIModel()
    model.train(data)
    print(f"   ✓ Model trained successfully")
    
    anomalies = model.detect_anomalies(data.tail(5))
    print(f"   ✓ Anomaly detection: {sum(anomalies)} anomalies in last 5 readings")
    
    predictions = model.predict_next(data, steps_ahead=5)
    if predictions:
        print(f"   ✓ Predictions generated:")
        print(f"      Next temp: {predictions['temperature']}")
    
    trend = model.get_trend(data, 'temperature')
    print(f"   ✓ Temperature trend: {trend}")
    
except Exception as e:
    print(f"   ✗ Error: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ ALL TESTS PASSED!")
print("=" * 60)
print("\n📊 Next Step: Run the dashboard with:")
print("   streamlit run src/dashboard.py")
print("\n" + "=" * 60)
