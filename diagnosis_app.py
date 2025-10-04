from flask import Flask, render_template, request, jsonify
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import base64
import os

app = Flask(__name__)

class ChestXrayDiagnosis:
    def __init__(self):
        self.model = None
        self.class_names = [
            'Atelectasis', 'Cardiomegaly', 'Effusion', 'Infiltration',
            'Mass', 'Nodule', 'Pneumonia', 'Pneumothorax',
            'Consolidation', 'Edema', 'Emphysema', 'Fibrosis',
            'Pleural_Thickening', 'Hernia', 'No Finding'
        ]
        self.load_model()
    
    def load_model(self):
        """Load pre-trained model or create a simple CNN"""
        try:
            # Try to load existing model
            self.model = tf.keras.models.load_model('chest_xray_model.h5')
        except:
            # Create a simple CNN model for demonstration
            self.model = self.create_simple_model()
    
    def create_simple_model(self):
        """Create a simple CNN model"""
        model = tf.keras.Sequential([
            tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 1)),
            tf.keras.layers.MaxPooling2D(2, 2),
            tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
            tf.keras.layers.MaxPooling2D(2, 2),
            tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
            tf.keras.layers.MaxPooling2D(2, 2),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dropout(0.5),
            tf.keras.layers.Dense(512, activation='relu'),
            tf.keras.layers.Dense(len(self.class_names), activation='sigmoid')
        ])
        
        model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        return model
    
    def preprocess_image(self, image):
        """Preprocess uploaded image"""
        # Convert to grayscale
        if image.mode != 'L':
            image = image.convert('L')
        
        # Resize to model input size
        image = image.resize((224, 224))
        
        # Convert to numpy array and normalize
        img_array = np.array(image) / 255.0
        img_array = np.expand_dims(img_array, axis=-1)  # Add channel dimension
        img_array = np.expand_dims(img_array, axis=0)   # Add batch dimension
        
        return img_array
    
    def predict(self, image):
        """Make prediction on chest X-ray image"""
        processed_image = self.preprocess_image(image)
        
        # Make prediction
        predictions = self.model.predict(processed_image)[0]
        
        # Create results with confidence scores
        results = []
        for i, class_name in enumerate(self.class_names):
            confidence = float(predictions[i])
            results.append({
                'condition': class_name,
                'confidence': round(confidence * 100, 2),
                'probability': round(confidence, 4)
            })
        
        # Sort by confidence
        results.sort(key=lambda x: x['confidence'], reverse=True)
        return results

# Initialize diagnosis system
diagnosis_system = ChestXrayDiagnosis()

@app.route('/')
def index():
    return render_template('diagnosis.html')

@app.route('/diagnose', methods=['POST'])
def diagnose():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'})
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No image selected'})
    
    try:
        # Read and process image
        image = Image.open(file.stream)
        
        # Make prediction
        results = diagnosis_system.predict(image)
        
        # Convert image to base64 for display
        img_buffer = io.BytesIO()
        if image.mode != 'RGB':
            image = image.convert('RGB')
        image.save(img_buffer, format='JPEG')
        img_str = base64.b64encode(img_buffer.getvalue()).decode()
        
        return jsonify({
            'success': True,
            'predictions': results,
            'image': img_str
        })
        
    except Exception as e:
        return jsonify({'error': f'Error processing image: {str(e)}'})

@app.route('/model_info')
def model_info():
    return jsonify({
        'model_loaded': diagnosis_system.model is not None,
        'classes': diagnosis_system.class_names,
        'total_classes': len(diagnosis_system.class_names)
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)