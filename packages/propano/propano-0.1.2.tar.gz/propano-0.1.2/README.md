# Propano
A lightweight, open-source network anomaly detection package leveraging **Facebook Prophet** for time-series modeling.  

Propano leverages Facebook Prophet to detect anomalies in time-series data. Our approach integrates domain knowledge, anomaly scoring, continuity analysis, and proximity analysis to reduce noise and false positives—helping detect meaningful anomalies rather than isolated outliers.

Few inputs a user can use to detect the anomalies.

✔ Domain Knowledge: Static cut-off lower and upper bounds for a metric. Currently, it is static, we intend to derive dynamic suggestion of this value as an insight to the users.
Data points lying beyond this range will be considered for the anomaly detection.
Ex: If a CPU usage has spike from 20% to 60% and the lower bound is set to 70%, then this spike would be ignored.

✔ Anomaly Scoring: Sigmoid based scoring(0 - 1) with scale factor can be used by the consumers to set the threshold for anomalies based on the sensitivity(Low, Medium, High sensitivity).
Low Sensitivity: Anomalous points with scores above 0.9
Medium Sensitivity: Anomalous points with scores above 0.7
High Sensitivity: Anomalous points with scores above 0.5
Custom Threshold also supported.
Anomalies detection in this step are considered for further process.

✔ Continuity Analysis:
Consumers of the library can specify the period of continuity of the anomalous behaviour.
Anomalies detection in this step are considered for further process.

✔ Proximity Analysis:
This will reduce the clutter's in the final anomalous points detected.
Start and end of the block of anomalies(range) is shown in the final output.
If the data is crossing the trend, deviation from the anomalous range values are intelligently considered as well.

**Getting Started**
```bash
pip install propano
```
OR
```bash
pip3 install propano
```
**Project Structure**
```bash
propano/
├── src/
│   ├── propano/
│   │   ├── __init__.py
│   │   ├── anomaly_detector.py   # Core anomaly detection logic
│   │   ├── cli.py                # Command-line interface (CLI)
│   │   ├── utils.py              # Helper functions (e.g., data preprocessing)
│   │   ├── visualization.py      # Functions for plotting anomalies
│   ├── tests/
│   │   ├── test_anomaly_detector.py  # Unit tests
│   │   ├── test_cli.py               # Unit tests for CLI
│   │   ├── test_utils.py
│   ├── data/
│   │   ├── raw/                  # Raw network traffic data
│   │   │   ├── sample_network_data.csv
│   │   ├── processed/             # Preprocessed data files
│   │   │   ├── cleaned_data.csv
│   ├── notebooks/
│   │   ├── anomaly_detection_demo.ipynb  # Jupyter notebook example
├── examples/
│   ├── example_usage.py          # Example script demonstrating package usage
├── docs/
│   ├── README.md                 # Project documentation
│   ├── CONTRIBUTING.md           # Guidelines for contributors
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                 # GitHub Actions CI/CD workflow
├── setup.py                      # Package setup script
├── requirements.txt              # Dependencies
├── LICENSE                       # Open-source license
├── .gitignore                    # Ignore unnecessary files
```


**Useful Commands for the Developers**

*To install the dependencies*
```
pip install -r requirements.txt
```

*To Build and Upload to PyPI*

```
python -m build
```

```
pip uninstall propano -y && pip install .
```

```
twine upload dist/*
```