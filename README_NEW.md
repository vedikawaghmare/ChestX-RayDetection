# Professional Chest X-Ray AI Analyzer

A modern, professional React-based application for chest X-ray analysis using Google's Gemini AI. Features a sleek UI with drag-and-drop functionality, real-time analysis, and comprehensive medical insights.

## 🚀 Features

### Core Functionality
- **AI-Powered Analysis**: Uses Google Gemini Pro Vision for accurate chest X-ray analysis
- **Image Validation**: Automatically validates if uploaded images are chest X-rays
- **Professional UI**: Modern, responsive design with glassmorphism effects
- **Real-time Processing**: Live progress indicators and smooth animations
- **Medical Insights**: Detailed findings, recommendations, and confidence scores

### Technical Features
- **React 18**: Modern React with hooks and functional components
- **Drag & Drop**: Intuitive file upload with react-dropzone
- **Responsive Design**: Mobile-first approach with CSS Grid and Flexbox
- **Error Handling**: Comprehensive error handling and user feedback
- **API Integration**: RESTful API with proper validation and security
- **File Processing**: Image optimization with Sharp.js

## 🛠️ Technology Stack

### Frontend
- **React 18** - Modern UI framework
- **React Icons** - Professional icon library
- **React Dropzone** - File upload functionality
- **Framer Motion** - Smooth animations
- **React Toastify** - User notifications
- **Axios** - HTTP client

### Backend
- **Node.js & Express** - Server framework
- **Multer** - File upload handling
- **Sharp** - Image processing
- **Google Generative AI** - Gemini AI integration
- **CORS** - Cross-origin resource sharing

## 📦 Installation

### Prerequisites
- Node.js 16+ and npm
- Google Gemini API key

### Setup Steps

1. **Clone and Navigate**
   ```bash
   cd "/Users/darshanpatil/Documents/Mern Stack/chest x-ray/ChestX-RayDetection"
   ```

2. **Install Dependencies**
   ```bash
   npm install
   ```

3. **Environment Configuration**
   ```bash
   cp .env.example .env
   ```
   Update `.env` with your Gemini API key:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

4. **Start Development Servers**
   
   Terminal 1 (Backend):
   ```bash
   npm run server
   ```
   
   Terminal 2 (Frontend):
   ```bash
   npm start
   ```

5. **Access Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000

## 🎯 Usage

### For Users
1. **Upload Image**: Drag and drop or click to select a chest X-ray image
2. **Automatic Validation**: AI validates if the image is a chest X-ray
3. **Get Analysis**: Receive detailed medical insights and recommendations
4. **Review Results**: View findings, confidence scores, and technical details

### For Developers
- **API Endpoint**: `POST /api/analyze` with multipart/form-data
- **Response Format**: JSON with analysis results, findings, and recommendations
- **Error Handling**: Comprehensive error responses with appropriate HTTP status codes

## 📊 API Documentation

### Analyze Image
```http
POST /api/analyze
Content-Type: multipart/form-data

Body: image file (max 10MB, JPG/PNG/WEBP)
```

**Response:**
```json
{
  "isValidXray": true,
  "confidence": 85,
  "analysis": "Detailed medical analysis...",
  "imageQuality": "good",
  "findings": [
    {
      "condition": "Normal chest",
      "description": "No acute abnormalities detected",
      "severity": "low",
      "confidence": 90
    }
  ],
  "recommendations": [
    {
      "title": "Follow-up",
      "description": "Regular monitoring recommended",
      "priority": "low"
    }
  ],
  "processingTime": "2.3s"
}
```

## 🔒 Security & Privacy

- **File Validation**: Strict file type and size validation
- **Temporary Storage**: Uploaded files are automatically deleted after processing
- **API Rate Limiting**: Built-in protection against abuse
- **CORS Configuration**: Proper cross-origin resource sharing setup
- **Medical Disclaimer**: Clear disclaimers about AI limitations

## 🎨 UI/UX Features

- **Glassmorphism Design**: Modern translucent card effects
- **Smooth Animations**: Framer Motion powered transitions
- **Loading States**: Engaging progress indicators
- **Responsive Layout**: Mobile-first responsive design
- **Professional Icons**: React Icons for consistent iconography
- **Toast Notifications**: User-friendly feedback system

## 📱 Mobile Responsiveness

- Fully responsive design for all screen sizes
- Touch-friendly interface elements
- Optimized image preview for mobile devices
- Collapsible sections for better mobile UX

## 🚨 Medical Disclaimer

This application is for educational and research purposes only. It should not be used as a substitute for professional medical diagnosis, treatment, or advice. Always consult with qualified healthcare professionals for medical decisions.

## 🔧 Development

### Project Structure
```
src/
├── components/          # React components
│   ├── Header.js       # Application header
│   ├── ImageUpload.js  # File upload component
│   ├── LoadingSpinner.js # Loading animation
│   └── AnalysisResults.js # Results display
├── services/           # API services
│   └── api.js         # API client
├── styles/            # CSS files
└── App.js            # Main application

server/
├── server.js         # Express server
└── uploads/          # Temporary file storage
```

### Available Scripts
- `npm start` - Start React development server
- `npm run server` - Start Express backend server
- `npm run build` - Build production React app
- `npm test` - Run tests

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Check the GitHub issues
- Review the API documentation
- Ensure your Gemini API key is properly configured
- Verify all dependencies are installed correctly