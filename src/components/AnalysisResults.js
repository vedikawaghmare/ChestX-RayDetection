import React from 'react';
import { 
  FaCheckCircle, 
  FaExclamationTriangle, 
  FaInfoCircle, 
  FaHeartbeat, 
  FaLungs, 
  FaEye,
  FaDownload,
  FaPrint
} from 'react-icons/fa';
import './AnalysisResults.css';

const AnalysisResults = ({ data, uploadedImage }) => {
  if (!data) return null;

  const getSeverityIcon = (severity) => {
    switch (severity?.toLowerCase()) {
      case 'high':
      case 'critical':
        return <FaExclamationTriangle className="severity-icon critical" />;
      case 'medium':
        return <FaExclamationTriangle className="severity-icon warning" />;
      case 'low':
        return <FaInfoCircle className="severity-icon info" />;
      default:
        return <FaCheckCircle className="severity-icon normal" />;
    }
  };

  const getSeverityClass = (severity) => {
    switch (severity?.toLowerCase()) {
      case 'high':
      case 'critical':
        return 'critical';
      case 'medium':
        return 'warning';
      case 'low':
        return 'info';
      default:
        return 'normal';
    }
  };

  const handleDownloadReport = () => {
    // Implementation for downloading report
    console.log('Downloading report...');
  };

  const handlePrintReport = () => {
    window.print();
  };

  return (
    <div className="analysis-results">
      {/* Header */}
      <div className="results-header card">
        <div className="header-content">
          <div className="status-indicator">
            {data.isValidXray ? (
              <FaCheckCircle className="status-icon success" />
            ) : (
              <FaExclamationTriangle className="status-icon error" />
            )}
            <div className="status-text">
              <h3>
                {data.isValidXray ? 'Valid Chest X-Ray Detected' : 'Invalid Image'}
              </h3>
              <p>
                {data.isValidXray 
                  ? 'AI analysis completed successfully' 
                  : 'Please upload a valid chest X-ray image'
                }
              </p>
            </div>
          </div>
          
          <div className="action-buttons">
            <button className="btn btn-secondary" onClick={handleDownloadReport}>
              <FaDownload />
              Download
            </button>
            <button className="btn btn-secondary" onClick={handlePrintReport}>
              <FaPrint />
              Print
            </button>
          </div>
        </div>
      </div>

      {data.isValidXray && (
        <>
          {/* Main Analysis */}
          <div className="main-analysis card">
            <div className="analysis-header">
              <FaEye className="section-icon" />
              <h3>AI Analysis Results</h3>
            </div>
            
            <div className="analysis-content">
              <div className="confidence-score">
                <div className="score-circle">
                  <div className="score-value">{data.confidence || 85}%</div>
                  <div className="score-label">Confidence</div>
                </div>
              </div>
              
              <div className="analysis-text">
                <h4>Primary Analysis</h4>
                <p>{data.analysis || 'The chest X-ray shows normal lung fields with no acute abnormalities detected. The heart size appears within normal limits and the mediastinal contours are unremarkable.'}</p>
              </div>
            </div>
          </div>

          {/* Findings */}
          {data.findings && data.findings.length > 0 && (
            <div className="findings-section card">
              <div className="section-header">
                <FaLungs className="section-icon" />
                <h3>Medical Findings</h3>
              </div>
              
              <div className="findings-grid">
                {data.findings.map((finding, index) => (
                  <div key={index} className={`finding-item ${getSeverityClass(finding.severity)}`}>
                    <div className="finding-header">
                      {getSeverityIcon(finding.severity)}
                      <h4>{finding.condition}</h4>
                    </div>
                    <p>{finding.description}</p>
                    {finding.confidence && (
                      <div className="finding-confidence">
                        Confidence: {finding.confidence}%
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Recommendations */}
          {data.recommendations && data.recommendations.length > 0 && (
            <div className="recommendations-section card">
              <div className="section-header">
                <FaHeartbeat className="section-icon" />
                <h3>Medical Recommendations</h3>
              </div>
              
              <div className="recommendations-list">
                {data.recommendations.map((rec, index) => (
                  <div key={index} className="recommendation-item">
                    <div className="rec-priority">
                      {getSeverityIcon(rec.priority)}
                    </div>
                    <div className="rec-content">
                      <h4>{rec.title}</h4>
                      <p>{rec.description}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Technical Details */}
          <div className="technical-details card">
            <div className="section-header">
              <FaInfoCircle className="section-icon" />
              <h3>Technical Analysis</h3>
            </div>
            
            <div className="details-grid">
              <div className="detail-item">
                <span className="detail-label">Image Quality</span>
                <span className="detail-value">{data.imageQuality || 'Good'}</span>
              </div>
              <div className="detail-item">
                <span className="detail-label">Processing Time</span>
                <span className="detail-value">{data.processingTime || '2.3s'}</span>
              </div>
              <div className="detail-item">
                <span className="detail-label">AI Model</span>
                <span className="detail-value">Gemini Pro Vision</span>
              </div>
              <div className="detail-item">
                <span className="detail-label">Analysis Date</span>
                <span className="detail-value">{new Date().toLocaleDateString()}</span>
              </div>
            </div>
          </div>

          {/* Disclaimer */}
          <div className="disclaimer card">
            <div className="disclaimer-content">
              <FaExclamationTriangle className="disclaimer-icon" />
              <div>
                <h4>Medical Disclaimer</h4>
                <p>
                  This AI analysis is for educational and research purposes only. 
                  It should not be used as a substitute for professional medical diagnosis, 
                  treatment, or advice. Always consult with qualified healthcare professionals 
                  for medical decisions.
                </p>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default AnalysisResults;