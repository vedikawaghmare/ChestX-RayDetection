import React from 'react';
import { FaBrain, FaXRay, FaSearch } from 'react-icons/fa';
import './LoadingSpinner.css';

const LoadingSpinner = () => {
  return (
    <div className="loading-spinner card">
      <div className="spinner-content">
        <div className="spinner-animation">
          <div className="spinner-circle">
            <FaBrain className="spinner-icon brain" />
          </div>
          <div className="pulse-rings">
            <div className="pulse-ring"></div>
            <div className="pulse-ring"></div>
            <div className="pulse-ring"></div>
          </div>
        </div>
        
        <div className="loading-text">
          <h3>Analyzing X-Ray Image</h3>
          <p>Our AI is examining your chest X-ray for medical insights...</p>
        </div>
        
        <div className="loading-steps">
          <div className="step active">
            <FaXRay className="step-icon" />
            <span>Validating X-Ray Image</span>
          </div>
          <div className="step active">
            <FaSearch className="step-icon" />
            <span>Extracting Features</span>
          </div>
          <div className="step processing">
            <FaBrain className="step-icon" />
            <span>AI Analysis in Progress</span>
          </div>
        </div>
        
        <div className="progress-bar">
          <div className="progress-fill"></div>
        </div>
      </div>
    </div>
  );
};

export default LoadingSpinner;