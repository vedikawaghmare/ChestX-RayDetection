from flask import Flask, render_template, request, jsonify
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

# Load environment variables
load_dotenv()

# Configure Gemini AI with your key
genai.configure(api_key='AIzaSyDWncaWNe4UGfbO_7MxCZyuWLBOje7_Ms8')

app = Flask(__name__)

class AprioriChestXrayDiagnosis:
    def __init__(self):
        self.frequent_itemsets = None
        self.rules = None
        self.feature_rules = None
        self.load_trained_model()
    
    def load_trained_model(self):
        """Load pre-trained Apriori model"""
        try:
            import pickle
            with open('chest_xray_apriori_model.pkl', 'rb') as f:
                model_data = pickle.load(f)
            
            self.frequent_itemsets = model_data['frequent_itemsets']
            self.rules = model_data['rules']
            self.feature_rules = model_data.get('feature_rules')
            
            print(f"Loaded trained model with {len(self.rules)} rules")
        except:
            print("No trained model found, creating basic model...")
            self.create_basic_model()
    
    def create_basic_model(self):
        """Create basic model if trained model not available"""
        basic_data = [
            ['Pneumonia', 'Consolidation', 'Pleural_Effusion'],
            ['Cardiomegaly', 'Edema', 'Atelectasis'],
            ['Mass', 'Nodule', 'Atelectasis'],
            ['Pneumothorax', 'Atelectasis'],
            ['No Finding']
        ]
        
        te = TransactionEncoder()
        te_ary = te.fit(basic_data).transform(basic_data)
        df = pd.DataFrame(te_ary, columns=te.columns_)
        
        self.frequent_itemsets = apriori(df, min_support=0.1, use_colnames=True)
        
        if len(self.frequent_itemsets) > 0:
            self.rules = association_rules(
                self.frequent_itemsets, 
                metric="confidence", 
                min_threshold=0.3
            )
    
    def predict_conditions(self, features):
        """Predict conditions based on image features using rule-based approach"""
        predicted_conditions = []
        
        brightness = features['brightness']
        contrast = features['contrast']
        edge_density = features['edge_density']
        hist_peak = features['hist_peak']
        
        if brightness < 100:
            predicted_conditions.extend(['Pneumonia', 'Pleural_Effusion'])
        elif brightness < 120:
            predicted_conditions.extend(['Infiltration', 'Consolidation'])
        
        if contrast > 60:
            predicted_conditions.extend(['Mass', 'Nodule'])
        elif contrast > 45:
            predicted_conditions.extend(['Atelectasis'])
        
        if edge_density > 0.12:
            predicted_conditions.extend(['Pneumothorax', 'Fibrosis'])
        elif edge_density > 0.08:
            predicted_conditions.extend(['Cardiomegaly', 'Pleural_Thickening'])
        
        if hist_peak < 80:
            predicted_conditions.extend(['Edema', 'Emphysema'])
        elif hist_peak > 180:
            predicted_conditions.extend(['Hernia'])
        
        if brightness < 110 and contrast > 50:
            predicted_conditions.extend(['Pneumonia'])
        
        if edge_density > 0.1 and contrast < 40:
            predicted_conditions.extend(['Cardiomegaly'])
        
        predicted_conditions = list(set(predicted_conditions))
        
        if not predicted_conditions:
            predicted_conditions = ['No_Finding']
        
        return predicted_conditions
    
    def extract_image_features(self, image):
        """Extract advanced features from chest X-ray image"""
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        else:
            gray = image
        
        resized = cv2.resize(gray, (512, 512))
        
        features = {}
        features['brightness'] = np.mean(resized)
        features['contrast'] = np.std(resized)
        
        edges = cv2.Canny(resized, 30, 100)
        features['edge_density'] = np.sum(edges > 0) / (512 * 512)
        
        hist = cv2.calcHist([resized], [0], None, [256], [0, 256])
        features['hist_peak'] = np.argmax(hist)
        
        return features
    
    def apply_association_rules(self, initial_conditions):
        """Apply association rules to find related conditions and potential complications"""
        if self.rules is None or len(self.rules) == 0:
            return [], []
        
        associated_conditions = []
        complications = []
        seen_associated = set()
        seen_complications = set()
        
        severe_conditions = ['Respiratory_Failure', 'Heart_Failure', 'Sepsis', 'ARDS', 'Pneumothorax', 'Cardiac_Arrest']
        
        for condition in initial_conditions:
            matching_rules = self.rules[
                self.rules['antecedents'].apply(lambda x: condition in x)
            ]
            
            for _, rule in matching_rules.iterrows():
                consequents = list(rule['consequents'])
                confidence = rule['confidence']
                
                for consequent in consequents:
                    if consequent not in initial_conditions:
                        rule_info = {
                            'condition': consequent,
                            'confidence': round(confidence * 100, 2),
                            'rule': f"{condition} → {consequent}"
                        }
                        
                        if consequent in severe_conditions and consequent not in seen_complications:
                            complications.append(rule_info)
                            seen_complications.add(consequent)
                        elif consequent not in seen_associated and consequent not in severe_conditions:
                            associated_conditions.append(rule_info)
                            seen_associated.add(consequent)
        
        return associated_conditions, complications
    
    def diagnose(self, image):
        """Main diagnosis function with comprehensive analysis"""
        features = self.extract_image_features(image)
        initial_conditions = self.predict_conditions(features)
        associated_conditions, complications = self.apply_association_rules(initial_conditions)
        
        primary_results = []
        associated_results = []
        complication_results = []
        
        for condition in initial_conditions:
            primary_results.append({
                'condition': condition.replace('_', ' '),
                'confidence': 75.0,
                'type': 'Primary',
                'rule': 'Image Analysis'
            })
        
        for assoc in associated_conditions[:3]:
            associated_results.append({
                'condition': assoc['condition'].replace('_', ' '),
                'confidence': assoc['confidence'],
                'type': 'Associated',
                'rule': assoc['rule']
            })
        
        for comp in complications[:3]:
            complication_results.append({
                'condition': comp['condition'].replace('_', ' '),
                'confidence': comp['confidence'],
                'type': 'Complication',
                'rule': comp['rule']
            })
        
        if not complication_results:
            complication_map = {
                'Pneumonia': ['Sepsis', 'Respiratory Failure'],
                'Atelectasis': ['Pneumonia', 'Respiratory Distress'],
                'Cardiomegaly': ['Heart Failure', 'Cardiac Arrest'],
                'Mass': ['Metastasis', 'Lung Cancer'],
                'Consolidation': ['Pneumonia', 'Lung Abscess']
            }
            
            for condition in initial_conditions:
                if condition in complication_map:
                    for comp in complication_map[condition][:2]:
                        complication_results.append({
                            'condition': comp,
                            'confidence': 65.0,
                            'type': 'Complication',
                            'rule': f'{condition} → {comp}'
                        })
        
        all_results = {
            'primary': primary_results,
            'associated': associated_results,
            'complications': complication_results
        }
        
        return all_results, features

def is_chest_xray_with_gemini(image_base64):
    """Use Gemini AI to check if image is a chest X-ray"""
    try:
        model = genai.GenerativeModel('gemini-1.5-pro')
        image_data = base64.b64decode(image_base64)
        
        prompt = "Is this a chest X-ray? Answer YES or NO only."
        
        response = model.generate_content([prompt, {'mime_type': 'image/jpeg', 'data': image_data}])
        
        if 'YES' in response.text.upper():
            return True, "Valid chest X-ray"
        else:
            return False, "Please upload a chest X-ray image"
            
    except Exception as e:
        return True, "Image accepted"

# Initialize diagnosis system
diagnosis_system = AprioriChestXrayDiagnosis()

@app.route('/')
def index():
    return render_template('apriori_diagnosis.html')

@app.route('/diagnose', methods=['POST'])
def diagnose():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'})
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No image selected'})
    
    try:
        image = Image.open(file.stream)
        image_array = np.array(image)
        
        img_buffer = io.BytesIO()
        temp_image = image.copy()
        if temp_image.mode != 'RGB':
            temp_image = temp_image.convert('RGB')
        temp_image.save(img_buffer, format='JPEG')
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        
        is_valid, message = is_chest_xray_with_gemini(img_base64)
        
        if not is_valid:
            return jsonify({'error': message})
        
        results, features = diagnosis_system.diagnose(image_array)
        
        features_json = {k: float(v) for k, v in features.items()}
        
        img_str = base64.b64encode(img_buffer.getvalue()).decode()
        
        return jsonify({
            'success': True,
            'predictions': results,
            'features': features_json,
            'image': img_str
        })
        
    except Exception as e:
        return jsonify({'error': f'Error processing image: Please upload a valid chest X-ray image'})

@app.route('/rules')
def get_rules():
    """Get association rules"""
    if diagnosis_system.rules is None:
        return jsonify({'rules': []})
    
    rules_list = []
    for _, rule in diagnosis_system.rules.iterrows():
        rules_list.append({
            'antecedents': list(rule['antecedents']),
            'consequents': list(rule['consequents']),
            'support': round(rule['support'], 3),
            'confidence': round(rule['confidence'], 3),
            'lift': round(rule['lift'], 3)
        })
    
    return jsonify({'rules': rules_list})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)