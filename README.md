# Chest X-Ray Frequent Itemset Mining

A Flask web application that applies the Apriori algorithm to find frequent itemsets and association rules in chest X-ray findings data.

## Features

- **Apriori Algorithm**: Finds frequent itemsets in chest X-ray findings
- **Association Rules**: Generates rules with support, confidence, and lift metrics
- **Interactive GUI**: Bootstrap-based web interface
- **Parameter Control**: Adjustable support and confidence thresholds
- **Real-time Analysis**: Upload CSV and get instant results

## Dataset

Use the NIH Chest X-rays dataset from Kaggle:
- URL: https://www.kaggle.com/datasets/nih-chest-xrays/data
- File: `Data_Entry_2017.csv`

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open browser to `http://localhost:5000`

## Usage

1. **Upload Data**: Upload the `Data_Entry_2017.csv` file
2. **Set Parameters**: 
   - Minimum Support (0.001-1.0)
   - Association Rule Metric (confidence/lift/support)
   - Minimum Threshold (0.1-1.0)
3. **Run Analysis**: Click "Run Analysis" to find frequent itemsets and rules
4. **View Results**: See frequent itemsets and association rules in tables

## Algorithm Details

- **Apriori Algorithm**: Finds frequent itemsets based on minimum support
- **Association Rules**: Generates rules from frequent itemsets using confidence, lift, or support metrics
- **Data Processing**: Splits multiple findings per image into transaction format

## Example Findings

The application will identify patterns like:
- Frequent co-occurring conditions in chest X-rays
- Association rules between different pathological findings
- Support and confidence metrics for medical insights