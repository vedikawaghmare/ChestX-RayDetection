import React, { useState } from 'react';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Header from './components/Header';
import ImageUpload from './components/ImageUpload';
import AnalysisResults from './components/AnalysisResults';
import LoadingSpinner from './components/LoadingSpinner';
import './styles/App.css';

function App() {
  const [analysisData, setAnalysisData] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [uploadedImage, setUploadedImage] = useState(null);

  const handleAnalysisComplete = (data) => {
    setAnalysisData(data);
    setIsAnalyzing(false);
  };

  const handleAnalysisStart = () => {
    setIsAnalyzing(true);
    setAnalysisData(null);
  };

  const handleImageUpload = (imageData) => {
    setUploadedImage(imageData);
  };

  return (
    <div className="App">
      <Header />
      
      <main className="main-content">
        <div className="container">
          <div className="app-grid">
            <div className="upload-section">
              <ImageUpload 
                onAnalysisStart={handleAnalysisStart}
                onAnalysisComplete={handleAnalysisComplete}
                onImageUpload={handleImageUpload}
                isAnalyzing={isAnalyzing}
              />
            </div>
            
            <div className="results-section">
              {isAnalyzing && <LoadingSpinner />}
              {analysisData && !isAnalyzing && (
                <AnalysisResults 
                  data={analysisData} 
                  uploadedImage={uploadedImage}
                />
              )}
              {!analysisData && !isAnalyzing && (
                <div className="welcome-message card">
                  <div className="welcome-content">
                    <div className="welcome-icon">🏥</div>
                    <h2>AI-Powered Chest X-Ray Analysis</h2>
                    <p>Upload a chest X-ray image to get instant AI-powered medical insights and analysis.</p>
                    <div className="features-list">
                      <div className="feature-item">
                        <span className="feature-icon">🔍</span>
                        <span>Advanced Image Validation</span>
                      </div>
                      <div className="feature-item">
                        <span className="feature-icon">🧠</span>
                        <span>AI-Powered Diagnosis</span>
                      </div>
                      <div className="feature-item">
                        <span className="feature-icon">📊</span>
                        <span>Detailed Medical Insights</span>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </main>

      <ToastContainer
        position="top-right"
        autoClose={5000}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
        theme="light"
      />
    </div>
  );
}

export default App;