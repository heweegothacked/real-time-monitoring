# Project Architecture & Design

## System Overview

```
┌─────────────────────────────────────────────────────┐
│         REAL-TIME MONITORING SYSTEM                 │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌──────────────────┐                               │
│  │  Sensor Data     │                               │
│  │  Simulator       │                               │
│  └────────┬─────────┘                               │
│           │                                          │
│           ▼                                          │
│  ┌──────────────────┐     ┌──────────────────┐      │
│  │   ML Model       │────▶│   Predictions    │      │
│  │  - Anomaly       │     │  - Temperature   │      │
│  │    Detection     │     │  - Humidity      │      │
│  │  - Prediction    │     │  - Pressure      │      │
│  └──────────────────┘     └──────────────────┘      │
│           │                                          │
│           ▼                                          │
│  ┌──────────────────────────────────────────┐       │
│  │   Streamlit Dashboard                    │       │
│  │   - Live Data                            │       │
│  │   - Predictions                          │       │
│  │   - Anomalies                            │       │
│  │   - Analytics                            │       │
│  └──────────────────────────────────────────┘       │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Data Generation Phase
- `SensorSimulator` creates realistic sensor readings
- Adds natural drift and random anomalies
- Returns data in Pandas DataFrame format

### 2. Model Training Phase
- `MonitoringAIModel` receives historical data
- Normalizes features using StandardScaler
- Trains Isolation Forest for anomaly detection
- Trains Linear Regression models for predictions

### 3. Real-Time Processing Phase
- New readings are added continuously
- Model makes predictions for next 5-20 steps
- Detects anomalies in current data
- Calculates trends

### 4. Visualization Phase
- Streamlit dashboard displays everything
- Users can interact with sidebar controls
- Multiple views: Data, Predictions, Anomalies, Analytics

## Key Components Explained

### SensorSimulator (sensor_simulator.py)

**Purpose**: Generate realistic sensor data

**Methods**:
- `__init__()`: Initialize with random seed for reproducibility
- `get_next_reading()`: Generate one sensor reading
- `generate_batch()`: Generate multiple readings at once

**Key Features**:
- Natural drift using random walk
- Occasional anomalies (sensor spikes)
- Realistic value ranges (temp: -10 to 50°C, etc.)

### MonitoringAIModel (ml_model.py)

**Purpose**: Machine learning for predictions and anomaly detection

**Methods**:
- `train()`: Learn patterns from historical data
- `detect_anomalies()`: Flag unusual readings
- `predict_next()`: Forecast future values
- `get_trend()`: Determine if metric is increasing/decreasing

**Algorithms**:
1. **Isolation Forest** - Detects anomalies without labeled data
2. **Linear Regression** - Predicts future values based on trends

### Dashboard (dashboard.py)

**Purpose**: Interactive web interface for monitoring

**Features**:
- Real-time metric displays
- Interactive graphs (Plotly)
- Sidebar configuration
- Four main tabs for different views

## Technologies Used

| Component | Technology | Why? |
|-----------|-----------|------|
| Backend | Python | Fast, great for ML |
| Data Handling | Pandas | Easy data manipulation |
| Machine Learning | Scikit-learn | Simple, powerful ML algorithms |
| Visualization | Plotly | Interactive, professional charts |
| Dashboard | Streamlit | Quick web app development, no JS needed |

## Machine Learning Explained

### Anomaly Detection (Isolation Forest)

**What it does**: Finds unusual sensor readings

**How it works**:
1. Randomly select features and split values
2. Isolate each data point through binary trees
3. Points that are isolated quickly = anomalies
4. Points that take longer to isolate = normal

**Example**:
- Temperature usually 20°C ± 2°C
- Sudden reading of 35°C = Isolated quickly = Anomaly

### Prediction (Linear Regression)

**What it does**: Predicts future sensor values

**How it works**:
1. Fits a straight line to historical data: y = mx + b
2. Uses this line to predict beyond the last data point
3. Extends the trend into the future

**Example**:
- Temperature increased from 20°C to 22°C to 24°C (trend = +2°C/step)
- Predicts next values: 26°C, 28°C, 30°C, etc.

## Performance Considerations

### Scalability
- Current setup handles ~1000 readings efficiently
- For production: Consider time-series databases (InfluxDB)
- For more data: Batch processing and data archival

### Model Accuracy
- Linear Regression: Works well for simple trends
- For complex patterns: Consider LSTM or Prophet models
- Anomaly detection accuracy: ~85% with default settings

## Error Handling

The system handles:
- Empty data (won't crash)
- Insufficient data for training (graceful degradation)
- Out-of-range values (clipping to realistic limits)
- Invalid configuration (sensible defaults)

## Security Considerations

For production deployment:
- Validate all user inputs
- Use environment variables for sensitive settings
- Implement user authentication
- Add rate limiting
- Encrypt sensitive data

## Testing

Run the test script to verify everything:
```bash
python test_system.py
```

This checks:
1. Sensor simulator functionality
2. ML model training
3. Anomaly detection
4. Prediction generation
5. Trend calculation

## Customization Points

### Easy to Modify:
- Number of sensors/metrics
- Prediction algorithm
- Anomaly threshold
- Dashboard colors and layout

### Medium Difficulty:
- Data storage (add database)
- Real sensor integration
- Advanced ML models

### Advanced:
- Cloud deployment
- Real-time data streaming (Kafka)
- Distributed ML training

## Next Steps for Enhancement

1. **Real Sensors**: Connect to actual IoT devices
2. **Database**: Store data in PostgreSQL/MongoDB
3. **Alerts**: Email/SMS notifications for anomalies
4. **Advanced ML**: LSTM networks for better predictions
5. **Cloud Deploy**: Host on AWS/Heroku/Railway
6. **Mobile App**: Create mobile interface
7. **Comparison**: Multiple anomaly detection algorithms
8. **Optimization**: Hyperparameter tuning

---

This architecture is designed to be **simple enough for learning** while being **powerful enough for real applications**.
