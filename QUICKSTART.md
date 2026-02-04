# Quick Start Guide

## For Beginners - Follow These Steps

### Step 1: Install Python Packages
```bash
pip install -r requirements.txt
```

### Step 2: Run the Dashboard
```bash
streamlit run src/dashboard.py
```

### Step 3: In the Dashboard
1. Click **"🔄 Initialize System"** (left sidebar)
2. Click **"➕ Add New Reading"** to add new data
3. Explore the tabs: Live Data → AI Predictions → Anomaly Detection → Analysis

### Step 4: Customize (Optional)
- Adjust sliders in the sidebar to change behavior
- Modify Python files in the `src/` folder to add new features

## File Guide

| File | Purpose |
|------|---------|
| `sensor_simulator.py` | Creates fake sensor readings |
| `ml_model.py` | AI model for predictions & anomaly detection |
| `dashboard.py` | Web interface (Streamlit) |

## Common Questions

**Q: What are anomalies?**
A: Unusual readings that don't match normal sensor behavior (e.g., sudden temperature spike).

**Q: How does prediction work?**
A: The AI learns from past data and extends that pattern into the future.

**Q: Can I use real sensors?**
A: Yes! Replace the simulated data with real sensor readings from IoT devices.

**Q: Is this good for my resume?**
A: Absolutely! This demonstrates full-stack skills: data processing, ML, and web development.

---

Need help? Check README.md for detailed documentation.
