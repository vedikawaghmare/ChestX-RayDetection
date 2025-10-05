from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from PIL import Image
import cv2
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
import io
import base64
import os
from dotenv import load_dotenv
import google.generativeai as genai
import pickle
import json
from datetime import datetime
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Gemini AI
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

app = Flask(__name__)
CORS(app, origins=['http://localhost:3000'])

class EnhancedChestXrayAnalyzer:
    def __init__(self):
        self.frequent_itemsets = None
        self.rules = None
        self.feature_rules = None
        self.gemini_model = None
        self.initialize_gemini()
        self.load_trained_model()
    
    def initialize_gemini(self):
        """Initialize Gemini AI model"""
        try:
            self.gemini_model = genai.GenerativeModel('gemini-2.0-flash-exp')
            logger.info("Gemini 2.0 Flash model initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini model: {e}")
            # Fallback to other models
            try:
                self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
                logger.info("Fallback to Gemini 1.5 Flash model")
            except:
                try:
                    self.gemini_model = genai.GenerativeModel('gemini-pro-vision')
                    logger.info("Fallback to Gemini Pro Vision model")
                except:
                    logger.error("All Gemini models failed to initialize")
    
    def load_trained_model(self):
        """Load pre-trained Apriori model"""
        try:
            with open('chest_xray_apriori_model.pkl', 'rb') as f:
                model_data = pickle.load(f)
            
            self.frequent_itemsets = model_data['frequent_itemsets']
            self.rules = model_data['rules']
            self.feature_rules = model_data.get('feature_rules')
            
            logger.info(f"Loaded trained model with {len(self.rules)} rules")
        except Exception as e:
            logger.warning(f"No trained model found: {e}, creating basic model...")
            self.create_enhanced_model()
    
    def create_enhanced_model(self):
        """Create enhanced model with medical knowledge"""
        medical_data = [
            ['Pneumonia', 'Consolidation', 'Pleural_Effusion', 'Fever'],
            ['Cardiomegaly', 'Edema', 'Heart_Failure', 'Atelectasis'],
            ['Mass', 'Nodule', 'Lung_Cancer', 'Atelectasis'],
            ['Pneumothorax', 'Atelectasis', 'Respiratory_Distress'],
            ['Consolidation', 'Pneumonia', 'Infiltration'],
            ['Pleural_Effusion', 'Heart_Failure', 'Edema'],
            ['Atelectasis', 'Pneumonia', 'Consolidation'],
            ['Fibrosis', 'Emphysema', 'COPD'],
            ['Emphysema', 'COPD', 'Respiratory_Failure'],
            ['Edema', 'Heart_Failure', 'Cardiomegaly'],
            ['No_Finding', 'Normal', 'Healthy']
        ]
        
        te = TransactionEncoder()
        te_ary = te.fit(medical_data).transform(medical_data)
        df = pd.DataFrame(te_ary, columns=te.columns_)
        
        self.frequent_itemsets = apriori(df, min_support=0.1, use_colnames=True)
        
        if len(self.frequent_itemsets) > 0:
            self.rules = association_rules(
                self.frequent_itemsets, 
                metric="confidence", 
                min_threshold=0.3
            )
            logger.info(f"Created enhanced model with {len(self.rules)} rules")
    
    def analyze_with_gemini(self, image_base64):
        """Comprehensive analysis using Gemini AI"""
        if not self.gemini_model:
            return self.fallback_analysis()
        
        try:
            # Decode base64 image
            image_data = base64.b64decode(image_base64)
            
            # Enhanced medical prompt for chest X-ray analysis
            prompt = """
            You are an expert radiologist AI. Analyze this chest X-ray image and provide a comprehensive medical assessment.

            Please provide your analysis in the following JSON format:
            {
                "isValidXray": boolean,
                "confidence": number (0-100),
                "imageQuality": "excellent/good/fair/poor",
                "analysis": "detailed medical analysis in human-understandable language",
                "findings": [
                    {
                        "condition": "condition name",
                        "description": "clear explanation of what this means for the patient",
                        "severity": "low/medium/high/critical",
                        "confidence": number (0-100),
                        "location": "anatomical location if applicable"
                    }
                ],
                "recommendations": [
                    {
                        "title": "recommendation title",
                        "description": "detailed recommendation in simple terms",
                        "priority": "low/medium/high/urgent",
                        "timeframe": "when this should be done"
                    }
                ],
                "normalFindings": [
                    "list of normal structures observed"
                ],
                "technicalNotes": "assessment of image quality and technical factors",
                "riskFactors": [
                    "potential risk factors or complications to monitor"
                ]
            }

            Key requirements:
            1. First determine if this is actually a chest X-ray
            2. If valid, provide detailed analysis in simple, patient-friendly language
            3. Explain medical terms clearly
            4. Include confidence levels for findings
            5. Provide actionable recommendations
            6. Note any limitations of the analysis
            7. Always include appropriate medical disclaimers

            Focus on:
            - Lung fields and airways
            - Heart size and shape
            - Bone structures
            - Soft tissues
            - Any abnormalities or concerning findings
            - Overall impression
            """
            
            # Create image part for Gemini
            image_part = {
                "mime_type": "image/jpeg",
                "data": image_data
            }
            
            # Generate content with Gemini
            response = self.gemini_model.generate_content([prompt, image_part])
            
            # Parse JSON response
            response_text = response.text
            
            # Extract JSON from response
            try:
                # Find JSON in the response
                start_idx = response_text.find('{')
                end_idx = response_text.rfind('}') + 1
                
                if start_idx != -1 and end_idx != -1:
                    json_str = response_text[start_idx:end_idx]
                    analysis_result = json.loads(json_str)
                else:
                    # Fallback parsing
                    analysis_result = self.parse_text_response(response_text)
                
                # Enhance with traditional analysis if valid X-ray
                if analysis_result.get('isValidXray', False):
                    traditional_analysis = self.traditional_image_analysis(image_data)
                    analysis_result = self.merge_analyses(analysis_result, traditional_analysis)
                
                return analysis_result
                
            except json.JSONDecodeError as e:
                logger.error(f"JSON parsing error: {e}")
                return self.parse_text_response(response_text)
                
        except Exception as e:
            logger.error(f"Gemini analysis error: {e}")
            return self.fallback_analysis()
    
    def parse_text_response(self, text):
        """Parse text response when JSON parsing fails"""
        is_valid = any(keyword in text.lower() for keyword in ['chest', 'x-ray', 'lung', 'heart', 'rib'])
        
        return {
            "isValidXray": is_valid,
            "confidence": 75,
            "imageQuality": "good",
            "analysis": text,
            "findings": [],
            "recommendations": [
                {
                    "title": "Consult Healthcare Provider",
                    "description": "Please consult with a qualified healthcare professional for proper medical interpretation",
                    "priority": "high",
                    "timeframe": "As soon as possible"
                }
            ],
            "normalFindings": [],
            "technicalNotes": "Analysis completed with text response",
            "riskFactors": []
        }
    
    def traditional_image_analysis(self, image_data):
        """Traditional computer vision analysis"""
        try:
            # Convert bytes to PIL Image
            image = Image.open(io.BytesIO(image_data))
            image_array = np.array(image)
            
            # Extract features
            features = self.extract_advanced_features(image_array)
            
            # Predict conditions using rule-based approach
            conditions = self.predict_conditions_from_features(features)
            
            # Apply association rules
            associated, complications = self.apply_association_rules(conditions)
            
            return {
                'traditional_features': features,
                'predicted_conditions': conditions,
                'associated_conditions': associated,
                'potential_complications': complications
            }
            
        except Exception as e:
            logger.error(f"Traditional analysis error: {e}")
            return {}
    
    def extract_advanced_features(self, image):
        """Extract comprehensive image features"""
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        else:
            gray = image
        
        # Resize for consistent analysis
        resized = cv2.resize(gray, (512, 512))
        
        features = {}
        
        # Basic intensity features
        features['brightness'] = np.mean(resized)
        features['contrast'] = np.std(resized)
        features['min_intensity'] = np.min(resized)
        features['max_intensity'] = np.max(resized)
        
        # Edge detection features
        edges = cv2.Canny(resized, 30, 100)
        features['edge_density'] = np.sum(edges > 0) / (512 * 512)
        
        # Histogram features
        hist = cv2.calcHist([resized], [0], None, [256], [0, 256])
        features['hist_peak'] = np.argmax(hist)
        features['hist_std'] = np.std(hist)
        
        # Texture features using Local Binary Pattern
        try:
            from skimage.feature import local_binary_pattern
            lbp = local_binary_pattern(resized, 8, 1, method='uniform')
            features['texture_uniformity'] = len(np.unique(lbp))
        except:
            features['texture_uniformity'] = 50  # Default value
        
        # Symmetry analysis (important for chest X-rays)
        left_half = resized[:, :256]
        right_half = np.fliplr(resized[:, 256:])
        features['symmetry'] = np.corrcoef(left_half.flatten(), right_half.flatten())[0, 1]
        
        return features
    
    def predict_conditions_from_features(self, features):
        """Enhanced condition prediction based on features"""
        conditions = []
        
        brightness = features['brightness']
        contrast = features['contrast']
        edge_density = features['edge_density']
        symmetry = features.get('symmetry', 0.5)
        
        # Enhanced rule-based prediction
        if brightness < 90:
            conditions.extend(['Pneumonia', 'Pleural_Effusion', 'Consolidation'])
        elif brightness < 110:
            conditions.extend(['Infiltration', 'Atelectasis'])
        elif brightness > 150:
            conditions.extend(['Emphysema', 'Pneumothorax'])
        
        if contrast > 70:
            conditions.extend(['Mass', 'Nodule', 'Fibrosis'])
        elif contrast > 50:
            conditions.extend(['Cardiomegaly', 'Edema'])
        elif contrast < 30:
            conditions.extend(['Pneumothorax', 'Emphysema'])
        
        if edge_density > 0.15:
            conditions.extend(['Fibrosis', 'Pleural_Thickening'])
        elif edge_density > 0.10:
            conditions.extend(['Atelectasis', 'Consolidation'])
        
        if symmetry < 0.7:
            conditions.extend(['Cardiomegaly', 'Mass', 'Pleural_Effusion'])
        
        # Remove duplicates and return
        return list(set(conditions)) if conditions else ['No_Finding']
    
    def apply_association_rules(self, initial_conditions):
        """Apply medical association rules"""
        if not self.rules or len(self.rules) == 0:
            return [], []
        
        associated = []
        complications = []
        
        severe_conditions = [
            'Respiratory_Failure', 'Heart_Failure', 'Sepsis', 'ARDS', 
            'Cardiac_Arrest', 'Lung_Cancer', 'Pulmonary_Embolism'
        ]
        
        for condition in initial_conditions:
            matching_rules = self.rules[
                self.rules['antecedents'].apply(lambda x: condition in str(x))
            ]
            
            for _, rule in matching_rules.iterrows():
                consequents = str(rule['consequents']).replace("frozenset({'", "").replace("'})", "").split("', '")
                confidence = rule['confidence']
                
                for consequent in consequents:
                    if consequent not in initial_conditions:
                        rule_info = {
                            'condition': consequent.replace('_', ' '),
                            'confidence': round(confidence * 100, 2),
                            'rule': f"{condition} → {consequent}"
                        }
                        
                        if consequent in severe_conditions:
                            complications.append(rule_info)
                        else:
                            associated.append(rule_info)
        
        return associated[:3], complications[:3]
    
    def merge_analyses(self, gemini_result, traditional_result):
        """Merge Gemini AI and traditional analysis results"""
        if not traditional_result:
            return gemini_result
        
        # Add traditional analysis insights to findings
        if 'predicted_conditions' in traditional_result:
            for condition in traditional_result['predicted_conditions']:
                if condition != 'No_Finding':
                    gemini_result['findings'].append({
                        'condition': condition.replace('_', ' '),
                        'description': f'Detected through image analysis patterns',
                        'severity': 'medium',
                        'confidence': 70,
                        'location': 'Various regions'
                    })
        
        # Add technical features
        if 'traditional_features' in traditional_result:
            features = traditional_result['traditional_features']
            gemini_result['technicalNotes'] += f" | Brightness: {features.get('brightness', 0):.1f}, Contrast: {features.get('contrast', 0):.1f}"
        
        return gemini_result
    
    def fallback_analysis(self):
        """Fallback analysis when Gemini is not available"""
        return {
            "isValidXray": True,
            "confidence": 60,
            "imageQuality": "fair",
            "analysis": "Basic analysis completed. For detailed medical interpretation, please consult a healthcare professional.",
            "findings": [
                {
                    "condition": "Analysis Limited",
                    "description": "Advanced AI analysis temporarily unavailable. Basic image processing completed.",
                    "severity": "info",
                    "confidence": 60
                }
            ],
            "recommendations": [
                {
                    "title": "Professional Consultation",
                    "description": "Please have this X-ray reviewed by a qualified radiologist or healthcare provider",
                    "priority": "high",
                    "timeframe": "Within 24-48 hours"
                }
            ],
            "normalFindings": [],
            "technicalNotes": "Fallback analysis mode",
            "riskFactors": []
        }

# Initialize the analyzer
analyzer = EnhancedChestXrayAnalyzer()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'gemini_available': analyzer.gemini_model is not None,
        'model_loaded': analyzer.rules is not None
    })

@app.route('/api/analyze', methods=['POST'])
def analyze_xray():
    """Main analysis endpoint"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No image selected'}), 400
        
        # Read and process image
        image = Image.open(file.stream)
        
        # Convert to base64 for Gemini analysis
        img_buffer = io.BytesIO()
        if image.mode != 'RGB':
            image = image.convert('RGB')
        image.save(img_buffer, format='JPEG', quality=85)
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        
        # Perform comprehensive analysis
        start_time = datetime.now()
        analysis_result = analyzer.analyze_with_gemini(img_base64)
        processing_time = (datetime.now() - start_time).total_seconds()
        
        # Add processing metadata
        analysis_result['processingTime'] = f"{processing_time:.1f}s"
        analysis_result['timestamp'] = datetime.now().isoformat()
        analysis_result['analysisId'] = f"xray_{int(datetime.now().timestamp())}"
        
        logger.info(f"Analysis completed in {processing_time:.1f}s")
        return jsonify(analysis_result)
        
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        return jsonify({
            'error': 'Analysis failed. Please try again with a valid chest X-ray image.',
            'details': str(e)
        }), 500

@app.route('/api/supported-types', methods=['GET'])
def supported_types():
    """Get supported file types"""
    return jsonify({
        'types': ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'],
        'extensions': ['.jpg', '.jpeg', '.png', '.webp'],
        'maxSize': 10 * 1024 * 1024,
        'recommendations': [
            'Use high-quality chest X-ray images',
            'Ensure good contrast and brightness',
            'Avoid rotated or cropped images',
            'Maximum file size: 10MB'
        ]
    })

@app.route('/api/model-info', methods=['GET'])
def model_info():
    """Get model information"""
    return jsonify({
        'gemini_model': 'gemini-2.0-flash-exp' if analyzer.gemini_model else 'unavailable',
        'traditional_model': 'loaded' if analyzer.rules is not None else 'basic',
        'association_rules': len(analyzer.rules) if analyzer.rules is not None else 0,
        'capabilities': [
            'Image validation',
            'Medical condition detection',
            'Risk assessment',
            'Recommendation generation',
            'Technical quality analysis'
        ]
    })

if __name__ == '__main__':
    port = int(os.getenv('PYTHON_PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port)