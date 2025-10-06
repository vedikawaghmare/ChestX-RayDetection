# 🏥 Chest X-Ray Medical Diagnosis System

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.13-orange.svg)](https://tensorflow.org)
[![React](https://img.shields.io/badge/React-18+-61DAFB.svg)](https://reactjs.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **AI-Powered Medical Diagnosis System using DenseNet-121 Deep Learning for Chest X-Ray Analysis**

![System Preview](deep-learning/asset/xray-header-image.png)

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/chest-xray-diagnosis.git
cd chest-xray-diagnosis

# Navigate to main system
cd deep-learning

# Install dependencies
pip3 install -r requirements.txt

# Download model (see Model Setup section)

# Start the system
python3 run_system.py
```

**🌐 Open your browser to: `http://localhost:8080`**

## ✨ Features

### 🔬 AI-Powered Analysis
- **DenseNet-121 Architecture**: State-of-the-art deep learning model
- **14 Pathological Conditions**: Comprehensive medical analysis
- **Real-time Processing**: Instant results with confidence scores
- **Professional Accuracy**: Research-grade diagnostic capabilities

### 📊 Visual Analytics
- **Interactive Charts**: Bar, pie, radar, and distribution charts
- **Confidence Visualization**: Color-coded probability indicators
- **Severity Classification**: High/Medium/Low risk assessment
- **Trend Analysis**: Historical comparison capabilities

### 📄 Professional Reports
- **PDF Generation**: Comprehensive medical reports
- **Chart Integration**: Visual analytics embedded in reports
- **Medical Formatting**: Professional healthcare documentation
- **Download Ready**: One-click report generation

### 🎨 User Experience
- **Drag & Drop Upload**: Intuitive image selection
- **Responsive Design**: Works on all devices
- **Real-time Feedback**: Instant visual feedback
- **Professional Interface**: Medical-grade UI/UX design

## 🔍 Detected Conditions

| Condition | Description | Accuracy |
|-----------|-------------|----------|
| **Atelectasis** | Lung collapse | High |
| **Cardiomegaly** | Enlarged heart | 90% AUC |
| **Consolidation** | Lung tissue filling | High |
| **Edema** | Fluid buildup | 86% AUC |
| **Effusion** | Fluid around lungs | High |
| **Emphysema** | Lung damage | High |
| **Fibrosis** | Lung scarring | High |
| **Hernia** | Organ displacement | High |
| **Infiltration** | Abnormal substances | High |
| **Mass** | Tumor/growth detection | 82% AUC |
| **Nodule** | Small growth detection | High |
| **Pleural Thickening** | Lung lining thickening | High |
| **Pneumonia** | Lung infection | High |
| **Pneumothorax** | Collapsed lung | High |

## 🏗️ System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Interface │    │   Flask API     │    │  DenseNet-121   │
│                 │◄──►│                 │◄──►│   AI Model      │
│  • Upload UI    │    │  • Analysis     │    │                 │
│  • Results      │    │  • Charts       │    │  • 14 Conditions│
│  • Charts       │    │  • PDF Reports  │    │  • Confidence   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📦 Installation

### Prerequisites
- **Python 3.9+**
- **Node.js 14+** (for React version)
- **4GB+ RAM** (recommended)

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/chest-xray-diagnosis.git
cd chest-xray-diagnosis
```

### 2. Install Python Dependencies
```bash
cd deep-learning
pip3 install -r requirements.txt
```

### 3. Model Setup
Due to file size limitations, the AI model needs to be downloaded separately:

```bash
# Option 1: Download from releases
wget https://github.com/yourusername/chest-xray-diagnosis/releases/download/v1.0/densenet.hdf5

# Option 2: Use provided script
python3 download_model.py

# Option 3: Train your own (advanced)
# Follow instructions in notebooks/
```

### 4. Start System
```bash
# Complete system with web interface
python3 run_system.py

# Or React development version
./start_analysis.sh

# Or just API server
python3 backend_api.py
```

## 🎯 Usage

### 1. **Upload X-Ray Image**
- Drag & drop or click to select
- Supports: JPG, PNG, JPEG
- Automatic preprocessing

### 2. **AI Analysis**
- Click "Analyze X-Ray"
- Real-time processing
- Confidence scoring

### 3. **View Results**
- Summary status
- Individual condition probabilities
- Interactive visual charts
- Severity classifications

### 4. **Generate Report**
- Click "Download PDF Report"
- Professional medical formatting
- Charts and analysis included
- Ready for medical review

## 📊 Sample Results

### Analysis Interface
![Analysis Interface](deep-learning/asset/predictions.png)

### Visual Charts
- **Probability Distribution**: Bar chart of all conditions
- **Detection Summary**: Pie chart overview
- **Radar Analysis**: Multi-dimensional view
- **Confidence Distribution**: Statistical analysis

### PDF Report Features
- Patient information section
- Complete analysis results
- Visual charts integration
- Medical disclaimer
- Professional formatting

## 🔧 API Documentation

### Analyze X-Ray
```http
POST /api/analyze
Content-Type: application/json

{
  "image": "data:image/jpeg;base64,..."
}
```

### Generate Report
```http
POST /api/generate-report
Content-Type: application/json

{
  "analysis_data": {...},
  "patient_info": {...}
}
```

### Health Check
```http
GET /api/health
```

## 🧪 Testing

```bash
# Test model functionality
python3 test_model.py

# Test enhanced features
python3 test_enhanced_system.py

# Test API endpoints
python3 test_backend.py
```

## 🚀 Deployment

### Local Development
```bash
python3 run_system.py
```

### Production Deployment
```bash
# Using Gunicorn
gunicorn -w 4 -b 0.0.0.0:5001 backend_api:app

# Using Docker (coming soon)
docker-compose up
```

## 📚 Documentation

- **[Features Guide](FEATURES.md)** - Comprehensive feature list
- **[Installation Guide](docs/INSTALLATION.md)** - Detailed setup instructions
- **[API Documentation](docs/API.md)** - Complete API reference
- **[Model Information](docs/MODEL.md)** - AI model details
- **[Contributing Guide](CONTRIBUTING.md)** - Development guidelines

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup
```bash
# Fork and clone
git clone https://github.com/yourusername/chest-xray-diagnosis.git

# Create feature branch
git checkout -b feature/amazing-feature

# Make changes and test
python3 test_enhanced_system.py

# Submit pull request
```

## ⚠️ Medical Disclaimer

**IMPORTANT**: This system is designed for **educational and research purposes only**. It should **NOT** be used as a substitute for professional medical diagnosis, treatment, or advice.

- Always consult qualified healthcare professionals
- Clinical correlation is essential
- The AI model may produce false positives/negatives
- Not intended for clinical decision-making

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **ChestX-ray8 Dataset**: NIH Clinical Center
- **DenseNet Architecture**: Gao Huang et al.
- **Medical Community**: For validation and feedback
- **Open Source Libraries**: TensorFlow, React, Flask, and others

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/chest-xray-diagnosis/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/chest-xray-diagnosis/discussions)
- **Email**: your.email@example.com

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/chest-xray-diagnosis&type=Date)](https://star-history.com/#yourusername/chest-xray-diagnosis&Date)

---

<div align="center">

**Made with ❤️ for the medical AI community**

[🌟 Star this repo](https://github.com/yourusername/chest-xray-diagnosis) • [🐛 Report Bug](https://github.com/yourusername/chest-xray-diagnosis/issues) • [💡 Request Feature](https://github.com/yourusername/chest-xray-diagnosis/issues)

</div>