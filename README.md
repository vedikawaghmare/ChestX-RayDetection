# Chest X-Ray Detection with Apriori Algorithm

A Flask web application that applies the Apriori algorithm to find frequent itemsets and association rules in chest X-ray findings data, enhanced with Gemini AI for image validation.

## Features

- **Apriori Algorithm**: Finds frequent itemsets in chest X-ray findings
- **Association Rules**: Generates rules with support, confidence, and lift metrics
- **Gemini AI Integration**: Validates uploaded images are chest X-rays
- **Interactive GUI**: Bootstrap-based web interface with drag-drop functionality
- **Real-time Diagnosis**: Upload chest X-ray images and get instant AI-powered diagnosis
- **Medical Insights**: Shows primary conditions, associations, and potential complications

## Dataset

Uses the NIH Chest X-rays dataset from Kaggle:
- URL: https://www.kaggle.com/datasets/nih-chest-xrays/data
- File: `Data_Entry_2017.csv` (112,120+ patient records)
- Trained model: `chest_xray_apriori_model.pkl`

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up Gemini AI API key in `.env` file:
```
GEMINI_API_KEY=your_api_key_here
```

3. Run the application:
```bash
python apriori_diagnosis_app.py
```

4. Open browser to `http://localhost:5003`

## Usage

1. **Upload Image**: Drag and drop or select a chest X-ray image
2. **AI Validation**: Gemini AI validates the image is a chest X-ray
3. **Get Diagnosis**: View AI-powered analysis with:
   - Primary conditions detected
   - Associated conditions from medical patterns
   - Potential complications if untreated
4. **Medical Insights**: Understand confidence levels and association rules

## Algorithm Details

- **Apriori Algorithm**: Trained on real NIH medical data to find frequent itemsets
- **Association Rules**: Generates medical insights with confidence and lift metrics
- **Image Analysis**: Extracts features like brightness, contrast, and edge density
- **Rule Application**: Maps image features to medical conditions using trained patterns

## Files Structure

- `apriori_diagnosis_app.py` - Main Flask application
- `train_apriori_model.py` - Training script for Apriori model
- `chest_xray_apriori_model.pkl` - Trained model with 4 association rules
- `Data_Entry_2017.csv` - NIH dataset with 112K+ patient records
- `templates/` - HTML templates for web interface
- `static/` - CSS and JavaScript files

## Example Medical Insights

The application identifies patterns like:
- Pneumonia → Sepsis (65% confidence)
- Cardiomegaly → Heart Failure (65% confidence)
- Atelectasis → Effusion (38% confidence)
- Mass → Lung Cancer risk assessment
