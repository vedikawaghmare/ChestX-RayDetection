#!/usr/bin/env python3
"""
Chest X-Ray Medical Diagnosis System
Simplified version to run the deep learning model for disease detection
"""

import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.densenet import preprocess_input
import warnings
warnings.filterwarnings('ignore')

# Disease labels
LABELS = [
    'Atelectasis', 'Cardiomegaly', 'Consolidation', 'Edema', 'Effusion',
    'Emphysema', 'Fibrosis', 'Hernia', 'Infiltration', 'Mass',
    'Nodule', 'Pleural_Thickening', 'Pneumonia', 'Pneumothorax'
]

class ChestXRayDiagnosis:
    def __init__(self, model_path='densenet.hdf5'):
        """Initialize the diagnosis system"""
        print("Loading DenseNet-121 model...")
        try:
            self.model = load_model(model_path, compile=False)
            print("✅ Model loaded successfully!")
            print(f"📊 Model input shape: {self.model.input_shape}")
            print(f"📊 Model output shape: {self.model.output_shape}")
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            return
        
        self.labels = LABELS
        
    def preprocess_image(self, image_path, target_size=(320, 320)):
        """Preprocess X-ray image for model input"""
        try:
            # Read image
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError(f"Could not load image from {image_path}")
            
            # Convert BGR to RGB
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Resize to target size
            img = cv2.resize(img, target_size)
            
            # Convert to float32 and normalize
            img = img.astype(np.float32)
            
            # Add batch dimension
            img = np.expand_dims(img, axis=0)
            
            # Apply DenseNet preprocessing (expects values in [0, 255])
            img = preprocess_input(img)
            
            return img
            
        except Exception as e:
            print(f"❌ Error preprocessing image: {e}")
            return None
    
    def predict_diseases(self, image_path, threshold=0.5):
        """Predict diseases from chest X-ray"""
        print(f"\n🔍 Analyzing X-ray: {os.path.basename(image_path)}")
        
        # Preprocess image
        processed_img = self.preprocess_image(image_path)
        if processed_img is None:
            return None
        
        # Make prediction
        try:
            predictions = self.model.predict(processed_img, verbose=0)
            
            # Handle different output shapes
            if len(predictions.shape) > 1:
                predictions = predictions[0]  # Remove batch dimension
            
            # Ensure we have the right number of predictions
            if len(predictions) != len(self.labels):
                print(f"⚠️  Model output shape mismatch: got {len(predictions)}, expected {len(self.labels)}")
                # Take first 14 predictions if more, pad with zeros if less
                if len(predictions) > len(self.labels):
                    predictions = predictions[:len(self.labels)]
                else:
                    predictions = np.pad(predictions, (0, len(self.labels) - len(predictions)))
            
            # Create results
            results = []
            for i, (label, prob) in enumerate(zip(self.labels, predictions)):
                results.append({
                    'disease': label,
                    'probability': float(prob),
                    'detected': prob > threshold
                })
            
            return results
            
        except Exception as e:
            print(f"❌ Error during prediction: {e}")
            return None
    
    def display_results(self, results, image_path):
        """Display diagnosis results"""
        if results is None:
            return
        
        print("\n" + "="*60)
        print("🏥 CHEST X-RAY DIAGNOSIS RESULTS")
        print("="*60)
        
        # Sort by probability (highest first)
        results_sorted = sorted(results, key=lambda x: x['probability'], reverse=True)
        
        # Show detected diseases
        detected = [r for r in results_sorted if r['detected']]
        if detected:
            print("\n🚨 DETECTED CONDITIONS:")
            for result in detected:
                print(f"   • {result['disease']}: {result['probability']:.1%} confidence")
        else:
            print("\n✅ NO SIGNIFICANT ABNORMALITIES DETECTED")
        
        # Show top 5 probabilities
        print(f"\n📊 TOP 5 PROBABILITIES:")
        for i, result in enumerate(results_sorted[:5]):
            status = "🔴" if result['detected'] else "🟢"
            print(f"   {i+1}. {status} {result['disease']}: {result['probability']:.1%}")
        
        # Display image
        try:
            img = cv2.imread(image_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            plt.figure(figsize=(10, 8))
            plt.imshow(img, cmap='gray')
            plt.title(f"Chest X-Ray Analysis: {os.path.basename(image_path)}")
            plt.axis('off')
            
            # Add results text
            detected_text = ", ".join([r['disease'] for r in detected]) if detected else "No abnormalities"
            plt.figtext(0.5, 0.02, f"Detected: {detected_text}", ha='center', fontsize=10)
            
            plt.tight_layout()
            plt.show()
            
        except Exception as e:
            print(f"⚠️  Could not display image: {e}")

def main():
    """Main function to run the diagnosis system"""
    print("🏥 Chest X-Ray Medical Diagnosis System")
    print("=" * 50)
    
    # Initialize diagnosis system
    diagnosis = ChestXRayDiagnosis()
    
    # Check if model loaded successfully
    if not hasattr(diagnosis, 'model'):
        return
    
    # Use sample image from assets
    sample_image = "asset/00025288_001.png"
    
    if os.path.exists(sample_image):
        print(f"\n📸 Using sample X-ray: {sample_image}")
        results = diagnosis.predict_diseases(sample_image)
        diagnosis.display_results(results, sample_image)
    else:
        print(f"\n⚠️  Sample image not found: {sample_image}")
        print("Please provide a chest X-ray image path:")
        
        # Interactive mode
        while True:
            image_path = input("\nEnter X-ray image path (or 'quit' to exit): ").strip()
            
            if image_path.lower() == 'quit':
                break
                
            if os.path.exists(image_path):
                results = diagnosis.predict_diseases(image_path)
                diagnosis.display_results(results, image_path)
            else:
                print(f"❌ File not found: {image_path}")
    
    print("\n✨ Analysis complete!")

if __name__ == "__main__":
    main()