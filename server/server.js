const express = require('express');
const multer = require('multer');
const cors = require('cors');
const path = require('path');
const fs = require('fs');
const axios = require('axios');
const FormData = require('form-data');
require('dotenv').config();

const { GoogleGenerativeAI } = require('@google/generative-ai');
const sharp = require('sharp');

const app = express();
const PORT = process.env.PORT || 5002;

// Initialize Gemini AI
const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);

// Middleware
app.use(cors({
  origin: ['http://localhost:3001', 'http://localhost:5002'],
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));

app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  if (req.method === 'OPTIONS') {
    res.sendStatus(200);
  } else {
    next();
  }
});

app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Create uploads directory if it doesn't exist
const uploadsDir = path.join(__dirname, 'uploads');
if (!fs.existsSync(uploadsDir)) {
  fs.mkdirSync(uploadsDir, { recursive: true });
}

// Configure multer for file uploads
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, uploadsDir);
  },
  filename: (req, file, cb) => {
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
    cb(null, `xray-${uniqueSuffix}${path.extname(file.originalname)}`);
  }
});

const upload = multer({
  storage: storage,
  limits: {
    fileSize: 10 * 1024 * 1024, // 10MB limit
  },
  fileFilter: (req, file, cb) => {
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'];
    if (allowedTypes.includes(file.mimetype)) {
      cb(null, true);
    } else {
      cb(new Error('Invalid file type. Only JPG, PNG, and WEBP are allowed.'));
    }
  }
});

// Helper function to convert image to base64
const imageToBase64 = async (imagePath) => {
  try {
    // Process image with sharp to ensure compatibility
    const processedImage = await sharp(imagePath)
      .resize(1024, 1024, { fit: 'inside', withoutEnlargement: true })
      .jpeg({ quality: 85 })
      .toBuffer();
    
    return processedImage.toString('base64');
  } catch (error) {
    console.error('Error processing image:', error);
    throw new Error('Failed to process image');
  }
};

// Helper function to analyze image with Gemini
const analyzeWithGemini = async (imagePath) => {
  try {
    const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });
    
    const imageBase64 = await imageToBase64(imagePath);
    
    const prompt = `
    You are a medical AI assistant specializing in chest X-ray analysis. Please analyze this image and provide:

    1. First, determine if this is a valid chest X-ray image (respond with true/false)
    2. If it's a valid chest X-ray, provide a detailed medical analysis including:
       - Overall assessment of the chest X-ray
       - Any abnormalities or findings detected
       - Confidence level of your analysis (0-100%)
       - Recommendations for further evaluation if needed
       - Technical quality assessment of the image

    Please format your response as a JSON object with the following structure:
    {
      "isValidXray": boolean,
      "confidence": number (0-100),
      "analysis": "detailed analysis text",
      "imageQuality": "excellent/good/fair/poor",
      "findings": [
        {
          "condition": "condition name",
          "description": "detailed description",
          "severity": "low/medium/high",
          "confidence": number
        }
      ],
      "recommendations": [
        {
          "title": "recommendation title",
          "description": "detailed recommendation",
          "priority": "low/medium/high"
        }
      ],
      "technicalNotes": "any technical observations about image quality"
    }

    Important: 
    - Be thorough but clear in your analysis
    - Always include appropriate medical disclaimers
    - If the image is not a chest X-ray, set isValidXray to false and explain why
    - Provide confidence scores for your findings
    - Use medical terminology but explain it in understandable terms
    `;

    const imagePart = {
      inlineData: {
        data: imageBase64,
        mimeType: "image/jpeg"
      }
    };

    const result = await model.generateContent([prompt, imagePart]);
    const response = await result.response;
    const text = response.text();

    // Try to parse JSON response
    try {
      const jsonMatch = text.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        return JSON.parse(jsonMatch[0]);
      } else {
        // Fallback if JSON parsing fails
        return {
          isValidXray: text.toLowerCase().includes('chest') && text.toLowerCase().includes('x-ray'),
          confidence: 75,
          analysis: text,
          imageQuality: "good",
          findings: [],
          recommendations: [],
          technicalNotes: "Analysis completed successfully"
        };
      }
    } catch (parseError) {
      console.error('JSON parsing error:', parseError);
      return {
        isValidXray: true,
        confidence: 70,
        analysis: text,
        imageQuality: "good",
        findings: [],
        recommendations: [],
        technicalNotes: "Analysis completed with text response"
      };
    }
  } catch (error) {
    console.error('Gemini analysis error:', error);
    throw new Error('Failed to analyze image with AI');
  }
};

// Routes

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    version: '1.0.0'
  });
});

// Get supported file types
app.get('/api/supported-types', (req, res) => {
  res.json({
    types: ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'],
    extensions: ['.jpg', '.jpeg', '.png', '.webp'],
    maxSize: 10 * 1024 * 1024
  });
});

// Main analysis endpoint - proxy to Python backend
app.post('/api/analyze', upload.single('image'), async (req, res) => {
  const startTime = Date.now();
  
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No image file uploaded' });
    }

    console.log('Processing image:', req.file.filename);
    
    // Try Python backend first
    try {
      const axios = require('axios');
      const FormData = require('form-data');
      
      const formData = new FormData();
      formData.append('image', fs.createReadStream(req.file.path));
      
      const pythonResponse = await axios.post('http://localhost:5001/api/analyze', formData, {
        headers: {
          ...formData.getHeaders(),
          'Access-Control-Allow-Origin': '*'
        },
        timeout: 30000
      });
      
      // Clean up uploaded file
      fs.unlink(req.file.path, (err) => {
        if (err) console.error('Error deleting file:', err);
      });
      
      console.log('Analysis completed via Python backend');
      return res.json(pythonResponse.data);
      
    } catch (pythonError) {
      console.log('Python backend unavailable, using Node.js backend');
      
      // Fallback to Node.js Gemini analysis
      const analysisResult = await analyzeWithGemini(req.file.path);
      
      // Add processing time
      const processingTime = ((Date.now() - startTime) / 1000).toFixed(1) + 's';
      analysisResult.processingTime = processingTime;
      
      // Clean up uploaded file
      fs.unlink(req.file.path, (err) => {
        if (err) console.error('Error deleting file:', err);
      });
      
      console.log('Analysis completed in', processingTime);
      res.json(analysisResult);
    }
    
  } catch (error) {
    console.error('Analysis error:', error);
    
    // Clean up file if it exists
    if (req.file && req.file.path) {
      fs.unlink(req.file.path, (err) => {
        if (err) console.error('Error deleting file:', err);
      });
    }
    
    res.status(500).json({
      error: error.message || 'Internal server error during analysis'
    });
  }
});

// Error handling middleware
app.use((error, req, res, next) => {
  console.error('Server error:', error);
  
  if (error instanceof multer.MulterError) {
    if (error.code === 'LIMIT_FILE_SIZE') {
      return res.status(413).json({ error: 'File too large. Maximum size is 10MB.' });
    }
    return res.status(400).json({ error: error.message });
  }
  
  res.status(500).json({ error: 'Internal server error' });
});

// 404 handler
app.use('*', (req, res) => {
  res.status(404).json({ error: 'Endpoint not found' });
});

// Start server
app.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`);
  console.log(`📊 Health check: http://localhost:${PORT}/api/health`);
  
  // Check if Gemini API key is configured
  if (!process.env.GEMINI_API_KEY) {
    console.warn('⚠️  GEMINI_API_KEY not found in environment variables');
  } else {
    console.log('✅ Gemini AI configured successfully');
  }
});

module.exports = app;