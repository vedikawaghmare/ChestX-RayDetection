import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { FaCloudUploadAlt, FaImage, FaCheckCircle, FaExclamationTriangle } from 'react-icons/fa';
import { toast } from 'react-toastify';
import { analyzeImage } from '../services/api';
import './ImageUpload.css';

const ImageUpload = ({ onAnalysisStart, onAnalysisComplete, onImageUpload, isAnalyzing }) => {
  const [uploadedFile, setUploadedFile] = useState(null);
  const [preview, setPreview] = useState(null);

  const onDrop = useCallback((acceptedFiles, rejectedFiles) => {
    if (rejectedFiles.length > 0) {
      toast.error('Please upload a valid image file (JPG, PNG, WEBP)');
      return;
    }

    const file = acceptedFiles[0];
    if (file) {
      setUploadedFile(file);
      
      // Create preview
      const reader = new FileReader();
      reader.onload = (e) => {
        setPreview(e.target.result);
        onImageUpload(e.target.result);
      };
      reader.readAsDataURL(file);
      
      toast.success('Image uploaded successfully!');
    }
  }, [onImageUpload]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.webp']
    },
    maxFiles: 1,
    maxSize: 10 * 1024 * 1024, // 10MB
  });

  const handleAnalyze = async () => {
    if (!uploadedFile) {
      toast.error('Please upload an image first');
      return;
    }

    onAnalysisStart();
    
    try {
      const result = await analyzeImage(uploadedFile);
      onAnalysisComplete(result);
      toast.success('Analysis completed successfully!');
    } catch (error) {
      console.error('Analysis error:', error);
      toast.error(error.message || 'Analysis failed. Please try again.');
      onAnalysisComplete(null);
    }
  };

  const clearImage = () => {
    setUploadedFile(null);
    setPreview(null);
    onImageUpload(null);
  };

  return (
    <div className="image-upload card">
      <div className="upload-header">
        <h2>Upload Chest X-Ray</h2>
        <p>Upload a chest X-ray image for AI-powered analysis</p>
      </div>

      <div className="upload-area">
        {!preview ? (
          <div
            {...getRootProps()}
            className={`dropzone ${isDragActive ? 'active' : ''}`}
          >
            <input {...getInputProps()} />
            <div className="dropzone-content">
              <FaCloudUploadAlt className="upload-icon" />
              <h3>
                {isDragActive ? 'Drop the image here' : 'Drag & drop an image here'}
              </h3>
              <p>or click to select a file</p>
              <div className="file-types">
                <span>Supported: JPG, PNG, WEBP</span>
                <span>Max size: 10MB</span>
              </div>
            </div>
          </div>
        ) : (
          <div className="preview-container">
            <div className="preview-header">
              <div className="file-info">
                <FaImage className="file-icon" />
                <div>
                  <span className="file-name">{uploadedFile.name}</span>
                  <span className="file-size">
                    {(uploadedFile.size / 1024 / 1024).toFixed(2)} MB
                  </span>
                </div>
              </div>
              <button 
                className="btn btn-secondary clear-btn"
                onClick={clearImage}
                disabled={isAnalyzing}
              >
                Clear
              </button>
            </div>
            
            <div className="image-preview">
              <img src={preview} alt="Uploaded X-ray" />
              <div className="image-overlay">
                <FaCheckCircle className="success-icon" />
                <span>Image Ready</span>
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="upload-actions">
        <button
          className="btn btn-primary analyze-btn"
          onClick={handleAnalyze}
          disabled={!uploadedFile || isAnalyzing}
        >
          {isAnalyzing ? (
            <>
              <div className="loading"></div>
              Analyzing...
            </>
          ) : (
            <>
              <FaCheckCircle />
              Analyze X-Ray
            </>
          )}
        </button>
        
        {uploadedFile && (
          <div className="upload-status">
            <FaCheckCircle className="status-icon success" />
            <span>Ready for analysis</span>
          </div>
        )}
      </div>

      <div className="upload-info">
        <div className="info-item">
          <FaExclamationTriangle className="info-icon" />
          <span>This tool is for educational purposes only and should not replace professional medical diagnosis.</span>
        </div>
      </div>
    </div>
  );
};

export default ImageUpload;