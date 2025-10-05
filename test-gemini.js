const { GoogleGenerativeAI } = require('@google/generative-ai');
require('dotenv').config();

async function testGeminiConnection() {
  try {
    console.log('🧪 Testing Gemini AI connection...');
    
    if (!process.env.GEMINI_API_KEY) {
      throw new Error('GEMINI_API_KEY not found in environment variables');
    }
    
    const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
    const model = genAI.getGenerativeModel({ model: "gemini-2.0-flash-exp" });
    
    const prompt = "Hello! Can you confirm that you're working properly? Please respond with a simple 'Yes, I'm working!' message.";
    
    console.log('📡 Sending test request to Gemini...');
    const result = await model.generateContent(prompt);
    const response = await result.response;
    const text = response.text();
    
    console.log('✅ Gemini AI Response:', text);
    console.log('🎉 Connection successful!');
    
  } catch (error) {
    console.error('❌ Gemini AI connection failed:', error.message);
    
    if (error.message.includes('API_KEY')) {
      console.log('💡 Make sure your GEMINI_API_KEY is correctly set in the .env file');
    }
  }
}

testGeminiConnection();