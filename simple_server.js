const express = require('express');
const multer = require('multer');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = 5002;

app.use(cors({ origin: '*' }));
app.use(express.json());

const upload = multer({ 
  storage: multer.memoryStorage(),
  limits: { fileSize: 10 * 1024 * 1024 }
});

let genAI = null;
try {
  const { GoogleGenerativeAI } = require('@google/generative-ai');
  genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
  console.log('Gemini AI initialized');
} catch (error) {
  console.log('Gemini AI not available:', error.message);
}

app.post('/api/analyze', upload.single('image'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No image uploaded' });
    }

    if (!genAI) {
      return res.status(500).json({ error: 'AI analysis service unavailable' });
    }

    const model = genAI.getGenerativeModel({ model: 'gemini-pro' });
    
    const prompt = `Analyze this image. If it's NOT a chest X-ray, respond: {"isValidXray": false, "error": "Please upload a valid chest X-ray image"}

If it IS a chest X-ray, provide analysis in JSON:
{
  "isValidXray": true,
  "confidence": 85,
  "analysis": "detailed medical analysis",
  "findings": [{"condition": "condition", "description": "details", "severity": "low/medium/high", "confidence": 80}],
  "recommendations": [{"title": "title", "description": "recommendation", "priority": "low/medium/high"}],
  "disclaimer": "This is for educational purposes only. Consult healthcare professionals."
}`;

    const result = await model.generateContent([
      prompt,
      {
        inlineData: {
          data: req.file.buffer.toString('base64'),
          mimeType: req.file.mimetype
        }
      }
    ]);
    
    const text = result.response.text();
    console.log('Gemini response:', text);
    
    const jsonMatch = text.match(/\{[\s\S]*\}/);
    if (jsonMatch) {
      const analysis = JSON.parse(jsonMatch[0]);
      res.json(analysis);
    } else {
      res.status(500).json({ error: 'Invalid AI response format' });
    }
    
  } catch (error) {
    console.error('Analysis error:', error);
    res.status(500).json({ error: `Analysis failed: ${error.message}` });
  }
});

app.get('/api/health', (req, res) => {
  res.json({ status: 'healthy', gemini: !!genAI });
});

app.listen(PORT, () => {
  console.log(`✅ Server running on port ${PORT}`);
  console.log(`🔑 Gemini API: ${process.env.GEMINI_API_KEY ? 'Configured' : 'Missing'}`);
});