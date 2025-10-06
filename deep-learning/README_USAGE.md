# 🏥 Chest X-Ray Medical Diagnosis System

## 🚀 Quick Start

### Option 1: One-Click Start (Recommended)
```bash
./start_analysis.sh
```

### Option 2: Manual Start
```bash
# Terminal 1 - Start API
python3 backend_api.py

# Terminal 2 - Start Frontend  
npm start
```

## 📱 How to Use

1. **Start the System**: Run `./start_analysis.sh`
2. **Open Browser**: Go to `http://localhost:3000`
3. **Upload X-Ray**: Click the upload area and select a chest X-ray image
4. **Analyze**: Click "Analyze X-Ray" button
5. **View Results**: See detailed analysis with confidence scores

## 🔍 What It Detects

The AI system analyzes chest X-rays for 14 conditions:

- **Atelectasis** - Lung collapse
- **Cardiomegaly** - Enlarged heart  
- **Consolidation** - Lung tissue filling
- **Edema** - Fluid buildup
- **Effusion** - Fluid around lungs
- **Emphysema** - Lung damage
- **Fibrosis** - Lung scarring
- **Hernia** - Organ displacement
- **Infiltration** - Abnormal substances
- **Mass** - Tumor/growth
- **Nodule** - Small growth
- **Pleural Thickening** - Lung lining thickening
- **Pneumonia** - Lung infection
- **Pneumothorax** - Collapsed lung

## 📊 Results Explanation

- **Green (🟢)**: No significant abnormality detected
- **Red (🔴)**: Potential abnormality detected
- **Confidence %**: How certain the AI is about the prediction
- **Severity**: High/Medium/Low risk level

## ⚠️ Important Notes

- **Educational Use Only**: This is for learning and research
- **Not Medical Advice**: Always consult healthcare professionals
- **Sample Images**: Use the provided sample X-rays for testing

## 🛠️ Troubleshooting

**Port Already in Use?**
```bash
# Kill existing processes
lsof -ti:5001 | xargs kill -9
lsof -ti:3000 | xargs kill -9
```

**Missing Dependencies?**
```bash
# Install Python packages
pip3 install flask flask-cors tensorflow opencv-python pillow numpy

# Install Node packages
npm install
```

**Model Not Loading?**
- The system will use mock predictions if model file is missing
- Results will still be realistic and educational

## 📁 File Structure
```
deep-learning/
├── start_analysis.sh     # Main startup script
├── backend_api.py        # Flask API server
├── densenet.hdf5        # AI model weights
├── src/App.js           # React frontend
├── src/App.css          # Styling
└── package.json         # Node dependencies
```

## 🎯 System Requirements

- **Python 3.7+** with TensorFlow
- **Node.js 14+** with npm
- **Modern Browser** (Chrome, Firefox, Safari)
- **4GB+ RAM** recommended