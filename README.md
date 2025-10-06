# 🏥 Chest X-Ray Medical Diagnosis System

Professional AI-powered chest X-ray analysis using DenseNet-121 deep learning model for detecting 14 different pathological conditions.

## 🚀 Features

- **Multi-Disease Detection**: Analyzes 14 different pathologies including Cardiomegaly, Pneumonia, Atelectasis, etc.
- **Professional UI**: Clean, responsive React interface with real-time analysis
- **DenseNet-121 Model**: State-of-the-art deep learning architecture
- **Confidence Scoring**: Probability scores and severity levels for each condition
- **Visual Results**: Interactive charts and detailed analysis reports

## 🏗️ Architecture

```
├── backend/           # Flask API server
│   ├── app.py        # Main Flask application
│   └── requirements.txt
├── frontend/         # React web application
│   ├── src/
│   │   ├── App.js    # Main React component
│   │   └── App.css   # Styling
│   └── package.json
└── deep-learning/    # ML model and notebooks
    ├── densenet.hdf5 # Trained model weights
    └── *.ipynb       # Jupyter notebooks
```

## 🔧 Setup Instructions

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start Flask server:**
   ```bash
   python app.py
   ```
   Server runs on `http://localhost:5002`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

3. **Start React development server:**
   ```bash
   npm start
   ```
   Application runs on `http://localhost:3000`

## 📊 Detected Conditions

The system can detect the following 14 pathological conditions:

1. **Atelectasis** - Lung collapse
2. **Cardiomegaly** - Enlarged heart
3. **Consolidation** - Lung tissue filling
4. **Edema** - Fluid buildup
5. **Effusion** - Fluid around lungs
6. **Emphysema** - Lung damage
7. **Fibrosis** - Lung scarring
8. **Hernia** - Organ displacement
9. **Infiltration** - Abnormal substances in lungs
10. **Mass** - Tumor/growth
11. **Nodule** - Small growth
12. **Pleural Thickening** - Lung lining thickening
13. **Pneumonia** - Lung infection
14. **Pneumothorax** - Collapsed lung

## 🎯 How to Use

1. **Upload Image**: Click the upload area and select a chest X-ray image (JPG, PNG, JPEG)
2. **Analyze**: Click "Analyze X-Ray" button to start the AI analysis
3. **View Results**: 
   - Summary status (Normal/Abnormal)
   - Detected conditions with confidence scores
   - Complete analysis report with all probabilities
   - Visual confidence bars and severity indicators

## 🔬 Model Details

- **Architecture**: DenseNet-121
- **Input Size**: 320x320 pixels
- **Training Dataset**: ChestX-ray8 (108,948 images from 32,717 patients)
- **Performance**: 
  - Cardiomegaly: 90% AUC
  - Edema: 86% AUC  
  - Mass: 82% AUC

## ⚠️ Medical Disclaimer

This AI system is designed for **educational and research purposes only**. It should not be used as a substitute for professional medical diagnosis. Always consult with qualified healthcare professionals for medical decisions and treatment.

## 🛠️ Technology Stack

**Backend:**
- Python 3.9+
- Flask (Web framework)
- TensorFlow/Keras (Deep learning)
- OpenCV (Image processing)
- NumPy (Numerical computing)

**Frontend:**
- React.js (UI framework)
- HTML5/CSS3 (Styling)
- JavaScript ES6+ (Logic)

**Model:**
- DenseNet-121 (CNN architecture)
- Pre-trained weights
- Multi-label classification

## 📈 API Endpoints

### `POST /api/analyze`
Analyze chest X-ray image
```json
{
  "image": "data:image/jpeg;base64,..."
}
```

### `GET /api/health`
Check server health and model status

## 🚀 Deployment

For production deployment:

1. **Backend**: Deploy Flask app using Gunicorn + Nginx
2. **Frontend**: Build React app (`npm run build`) and serve static files
3. **Model**: Ensure model file is accessible to backend server

## 📝 License

This project is for educational purposes. Model weights and dataset usage should comply with respective licenses.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request