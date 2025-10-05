import React from 'react';
import { FaXRay, FaBrain, FaShieldAlt } from 'react-icons/fa';
import './Header.css';

const Header = () => {
  return (
    <header className="header">
      <div className="container">
        <div className="header-content">
          <div className="logo">
            <FaXRay className="logo-icon" />
            <div className="logo-text">
              <h1>ChestXray AI</h1>
              <span className="tagline">Professional Medical Analysis</span>
            </div>
          </div>
          
          <div className="header-features">
            <div className="feature-badge">
              <FaBrain className="feature-icon" />
              <span>AI Powered</span>
            </div>
            <div className="feature-badge">
              <FaShieldAlt className="feature-icon" />
              <span>HIPAA Compliant</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;