# PROJECT REQUIREMENTS

## Installation

```bash
pip install -r requirements.txt
```

## Dependencies

### Core Data Science Stack
- **streamlit==1.28.1** - Interactive web dashboard framework
- **pandas==2.1.3** - Data manipulation and analysis
- **numpy==1.26.2** - Numerical computing and arrays
- **plotly==5.18.0** - Interactive data visualization

### Machine Learning
- **scikit-learn==1.3.2** - Machine learning algorithms and tools

## What Each Package Does

### Streamlit
```python
import streamlit as st
# Turns Python scripts into interactive web apps
# No web development experience needed
```
- Creates the web dashboard UI
- Handles user interactions
- Renders metrics and charts
- No JavaScript required

### Pandas
```python
import pandas as pd
# Data manipulation with tables (DataFrames)
df = pd.DataFrame({'column': [1, 2, 3]})
```
- Stores sensor readings
- Manages time-series data
- Data filtering and analysis
- CSV/JSON import/export

### NumPy
```python
import numpy as np
# Fast numerical computing
array = np.array([1, 2, 3])
```
- Generates random numbers
- Array operations
- Mathematical functions
- Used internally by other libraries

### Scikit-learn
```python
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LinearRegression
```
- **IsolationForest**: Anomaly detection
- **LinearRegression**: Trend prediction
- Preprocessing (scaling features)
- Well-documented, beginner-friendly

### Plotly
```python
import plotly.graph_objects as go
# Interactive charts and graphs
fig = go.Figure()
fig.add_trace(...)
```
- Interactive line charts
- Hover information
- Zooming and panning
- Professional visualizations

## Version Information

All versions are:
- **Stable**: Tested and reliable
- **Compatible**: Work well together
- **Recent**: Latest features included
- **Backward Compatible**: Work with Python 3.8+

## Python Version Requirement

**Python 3.8 or higher** required

Check your version:
```bash
python --version
```

## Virtual Environment (Recommended)

Create isolated environment:

```bash
# Create
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

## Optional: Development Dependencies

For advanced development:
```bash
pip install jupyter  # Interactive notebooks
pip install pytest   # Testing framework
pip install black    # Code formatter
```

## Troubleshooting Installation

### Issue: "pip not found"
- Ensure Python is in PATH
- Try: `python -m pip install -r requirements.txt`

### Issue: "Permission denied"
- Use virtual environment (recommended)
- Or: `pip install --user -r requirements.txt`

### Issue: "Version conflict"
- Delete venv folder and recreate
- Or: `pip install --upgrade -r requirements.txt`

### Issue: Slow installation
- Check internet connection
- Try: `pip install --cache-dir ~/.cache -r requirements.txt`

## Verification

Verify installation worked:

```bash
# Run test script
python test_system.py

# Or manually test:
python -c "import streamlit, pandas, numpy, sklearn, plotly; print('✓ All packages installed')"
```

## Updates

To update all packages:
```bash
pip install --upgrade -r requirements.txt
```

To freeze current versions:
```bash
pip freeze > requirements-frozen.txt
```

## Additional Resources

- [Streamlit Docs](https://docs.streamlit.io/)
- [Pandas Docs](https://pandas.pydata.org/docs/)
- [NumPy Docs](https://numpy.org/doc/)
- [Scikit-learn Docs](https://scikit-learn.org/)
- [Plotly Docs](https://plotly.com/python/)

---

All packages are open-source and free to use!
