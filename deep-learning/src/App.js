import React, { useState } from 'react';
import './App.css';

function App() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedImage(file);
      setError(null);
      
      // Create preview
      const reader = new FileReader();
      reader.onload = (e) => {
        setImagePreview(e.target.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const analyzeImage = async () => {
    if (!selectedImage) {
      setError('Please select an image first');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const reader = new FileReader();
      reader.onload = async (e) => {
        const base64Image = e.target.result;
        
        const response = await fetch('http://localhost:5001/api/analyze', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            image: base64Image
          })
        });

        const data = await response.json();
        
        if (data.success) {
          setAnalysisResult(data);
        } else {
          setError(data.error || 'Analysis failed');
        }
        setLoading(false);
      };
      reader.readAsDataURL(selectedImage);
    } catch (err) {
      setError('Failed to connect to analysis server');
      setLoading(false);
    }
  };

  const resetAnalysis = () => {
    setSelectedImage(null);
    setImagePreview(null);
    setAnalysisResult(null);
    setError(null);
  };

  return (
    <div className="App">
      <header className="app-header">
        <h1>🏥 Chest X-Ray Medical Diagnosis</h1>
        <p>AI-Powered Analysis using DenseNet-121 Deep Learning Model</p>
      </header>

      <main className="main-content">
        {/* Upload Section */}
        <div className="upload-section">
          <div className="upload-card">
            <h2>📸 Upload Chest X-Ray Image</h2>
            <div className="upload-area">
              <input
                type="file"
                accept="image/*"
                onChange={handleImageUpload}
                className="file-input"
                id="file-upload"
              />
              <label htmlFor="file-upload" className="upload-label">
                {imagePreview ? (
                  <img src={imagePreview} alt="X-ray preview" className="image-preview" />
                ) : (
                  <div className="upload-placeholder">
                    <span className="upload-icon">📁</span>
                    <p>Click to select chest X-ray image</p>
                    <small>Supports: JPG, PNG, JPEG</small>
                  </div>
                )}
              </label>
            </div>
            
            <div className="action-buttons">
              <button 
                onClick={analyzeImage} 
                disabled={!selectedImage || loading}
                className="analyze-btn"
              >
                {loading ? '🔄 Analyzing...' : '🔍 Analyze X-Ray'}
              </button>
              
              {(selectedImage || analysisResult) && (
                <button onClick={resetAnalysis} className="reset-btn">
                  🔄 Reset
                </button>
              )}
            </div>

            {error && (
              <div className="error-message">
                ❌ {error}
              </div>
            )}
          </div>
        </div>

        {/* Results Section */}
        {analysisResult && (
          <div className="results-section">
            <div className="results-header">
              <h2>📊 Analysis Results</h2>
              <div className="summary-card">
                <div className="summary-status">
                  <span className={`status-indicator ${analysisResult.summary.detected_count > 0 ? 'abnormal' : 'normal'}`}>
                    {analysisResult.summary.status}
                  </span>
                </div>
                <div className="summary-stats">
                  <div className="stat">
                    <span className="stat-label">Conditions Checked:</span>
                    <span className="stat-value">{analysisResult.total_conditions_checked}</span>
                  </div>
                  <div className="stat">
                    <span className="stat-label">Detected:</span>
                    <span className="stat-value">{analysisResult.summary.detected_count}</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Detected Conditions */}
            {analysisResult.detected_conditions.length > 0 && (
              <div className="detected-conditions">
                <h3>🚨 Detected Conditions</h3>
                <div className="conditions-grid">
                  {analysisResult.detected_conditions.map((condition, index) => (
                    <div key={index} className="condition-card detected">
                      <div className="condition-header">
                        <h4>{condition.disease}</h4>
                        <span className={`severity-badge ${condition.severity.toLowerCase()}`}>
                          {condition.severity}
                        </span>
                      </div>
                      <div className="condition-details">
                        <div className="confidence-bar">
                          <div 
                            className="confidence-fill" 
                            style={{width: `${condition.probability * 100}%`}}
                          ></div>
                        </div>
                        <span className="confidence-text">{condition.confidence}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* All Results */}
            <div className="all-results">
              <h3>📋 Complete Analysis Report</h3>
              <div className="results-table">
                <div className="table-header">
                  <span>Condition</span>
                  <span>Probability</span>
                  <span>Confidence</span>
                  <span>Status</span>
                </div>
                {analysisResult.results.map((result, index) => (
                  <div key={index} className={`table-row ${result.detected ? 'positive' : 'negative'}`}>
                    <span className="condition-name">{result.disease}</span>
                    <span className="probability">
                      <div className="probability-bar">
                        <div 
                          className="probability-fill" 
                          style={{width: `${result.probability * 100}%`}}
                        ></div>
                      </div>
                    </span>
                    <span className="confidence">{result.confidence}</span>
                    <span className={`status ${result.detected ? 'detected' : 'clear'}`}>
                      {result.detected ? '🔴 Detected' : '🟢 Clear'}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* Disclaimer */}
            <div className="disclaimer">
              <h4>⚠️ Medical Disclaimer</h4>
              <p>
                This AI analysis is for educational and research purposes only. 
                It should not be used as a substitute for professional medical diagnosis. 
                Always consult with qualified healthcare professionals for medical decisions.
              </p>
            </div>
          </div>
        )}
      </main>

      <footer className="app-footer">
        <p>Powered by DenseNet-121 Deep Learning Model | ChestX-ray8 Dataset</p>
      </footer>
    </div>
  );
}

export default App;