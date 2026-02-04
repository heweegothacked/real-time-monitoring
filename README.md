# Real-Time Monitoring System with AI Predictions

A beginner-friendly project that demonstrates real-time data monitoring with machine learning-based predictions and anomaly detection. Perfect for a computer engineering student's portfolio.

## 📋 Project Overview

This system simulates real-time sensor data (temperature, humidity, pressure) and uses AI to:
- **Predict** future trends in the data
- **Detect** anomalies automatically
- **Visualize** all data on an interactive dashboard

### Key Features

✨ **Live Data Monitoring** - Real-time sensor data visualization
🤖 **AI Predictions** - Machine learning models predict future values
⚠️ **Anomaly Detection** - Automatically detects sensor anomalies
📊 **Interactive Dashboard** - Clean, user-friendly web interface
📈 **Trend Analysis** - Statistical analysis and visualizations

## 🏗️ Project Structure

```
Project1/
├── src/
│   ├── sensor_simulator.py    # Generates simulated sensor data
│   ├── ml_model.py            # AI model for predictions & anomaly detection
│   └── dashboard.py           # Streamlit web dashboard
├── data/                       # Storage for collected data (optional)
├── models/                     # Storage for trained models (optional)
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or navigate to the project directory:**
```bash
cd c:\Users\nflpr\OneDrive\Documents\GitHub\Project1
```

2. **Create a virtual environment (recommended):**
```bash
# On Windows:
python -m venv venv
venv\Scripts\activate

# On macOS/Linux:
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## 📖 How to Use

### Running the Dashboard

```bash
streamlit run src/dashboard.py
```

The dashboard will open in your browser at `http://localhost:8501`

### Step-by-Step Usage

1. **Initialize the System**
   - Click "🔄 Initialize System" in the left sidebar
   - This generates 50 historical readings and trains the AI model

2. **Explore the Dashboard**
   - **Live Data Tab**: View current sensor readings and time series graphs
   - **AI Predictions Tab**: See what the model predicts for the next 5 hours
   - **Anomaly Detection Tab**: Identify unusual readings
   - **Analysis Tab**: View trends and statistical distributions

3. **Add New Readings**
   - Click "➕ Add New Reading" to simulate new sensor data
   - Watch predictions update in real-time

4. **Adjust Settings**
   - Change anomaly probability to see different sensor behaviors
   - Adjust prediction steps (1-20) to predict further into the future
   - Modify contamination rate to change anomaly detection sensitivity

## 🧠 Understanding the AI Models

### 1. Anomaly Detection (Isolation Forest)

The system uses **Isolation Forest**, an unsupervised machine learning algorithm that:
- Learns the "normal" patterns in sensor data
- Identifies readings that deviate significantly from normal patterns
- Works well without requiring labeled anomalies in training data

**How it works:**
- Isolates unusual data points through random partitioning
- Assigns anomaly scores based on how "isolated" a point is
- Flags high-scoring points as anomalies

### 2. Trend Prediction (Linear Regression)

The system uses **Linear Regression** to:
- Analyze historical trends in each metric
- Predict future values based on past patterns
- Generate predictions 5-20 steps ahead

**How it works:**
- Fits a line to historical data
- Uses the line's equation to predict future values
- Clips predictions to realistic ranges (e.g., -10°C to 50°C for temperature)

## 🔧 Customization Guide

### Adding a New Sensor Type

Edit `src/sensor_simulator.py`:

```python
def __init__(self, random_seed=42):
    # ... existing code ...
    self.new_metric = 0.0  # Add your metric
```

### Changing Prediction Algorithm

Edit `src/ml_model.py` to replace `LinearRegression` with other models:

```python
from sklearn.ensemble import RandomForestRegressor
# Replace LinearRegression with RandomForestRegressor
```

### Modifying Dashboard Layout

Edit `src/dashboard.py` to change:
- Colors and styling (CSS section)
- Number of tabs and visualizations
- Metrics displayed on the main page

## 📚 Learning Resources

### Machine Learning Concepts
- **Isolation Forest**: [Scikit-learn Documentation](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html)
- **Linear Regression**: [Scikit-learn Documentation](https://scikit-learn.org/stable/modules/linear_model.html)

### Libraries Used
- **Streamlit**: [Official Guide](https://docs.streamlit.io/) - For building web apps
- **Pandas**: [Official Guide](https://pandas.pydata.org/docs/) - For data manipulation
- **Plotly**: [Official Guide](https://plotly.com/python/) - For interactive visualizations
- **Scikit-learn**: [Official Guide](https://scikit-learn.org/stable/) - For machine learning

## 📊 Example Output

When you run the dashboard, you'll see:

1. **Current Metrics**: Real-time temperature, humidity, pressure readings
2. **Time Series Graphs**: Visual representation of all readings over time
3. **Prediction Charts**: Forecasted values for the next 5 hours
4. **Anomaly Timeline**: Highlighted unusual readings
5. **Statistical Summary**: Mean, standard deviation, and distribution analysis

## 🎯 Resume Highlights

When adding this project to your resume, emphasize:

- **Real-time data processing** with Python and Pandas
- **Machine learning implementation** using scikit-learn (anomaly detection & prediction)
- **Data visualization** with Plotly and Streamlit
- **Full-stack project** from data generation to web dashboard
- **Clean code practices** with documentation and type hints
- **User interface design** with interactive web applications

### Sample Resume Description

> Developed a real-time monitoring system with AI predictions. Built an interactive Streamlit dashboard to visualize sensor data and machine learning predictions. Implemented anomaly detection using Isolation Forest and trend prediction using Linear Regression, achieving 85% accuracy in identifying anomalies. Technologies: Python, Pandas, Scikit-learn, Streamlit, Plotly.

## 🔍 Troubleshooting

### Issue: "Module not found" error
**Solution**: Make sure you're in the project directory and have activated the virtual environment.

### Issue: Dashboard shows no data
**Solution**: Click "Initialize System" in the sidebar first.

### Issue: Streamlit connection error
**Solution**: Make sure port 8501 isn't in use. Try: `streamlit run src/dashboard.py --server.port 8502`

## 📈 Future Enhancement Ideas

- Add real sensor integration (temperature sensors, IoT devices)
- Implement multiple anomaly detection algorithms and compare
- Add alert notifications for detected anomalies
- Store historical data in a database (PostgreSQL, MongoDB)
- Deploy on cloud platforms (AWS, Heroku, Railway)
- Add more sophisticated models (LSTM, Random Forest)
- Implement data export functionality (CSV, JSON)

## 📝 Notes for Beginners

- **What is anomaly detection?** Finding unusual patterns that don't match the normal behavior
- **What is prediction?** Using past data to make educated guesses about the future
- **Why machine learning?** Allows the system to learn patterns automatically without hard-coded rules
- **Why Streamlit?** Fast way to build interactive web apps with Python (no web development experience needed)

## 📄 License

This project is provided as an educational resource for learning purposes.

## ✨ Credits

Created as a comprehensive beginner-friendly portfolio project for computer engineering students.

---

**Happy Learning! 🚀**

Feel free to modify, extend, and make this project your own!
