#!/usr/bin/env python3
"""
Simple Chest X-Ray Diagnosis Demo
"""

import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import load_model
import warnings
warnings.filterwarnings('ignore')

# Disease labels
LABELS = [
    'Atelectasis', 'Cardiomegaly', 'Consolidation', 'Edema', 'Effusion',
    'Emphysema', 'Fibrosis', 'Hernia', 'Infiltration', 'Mass',
    'Nodule', 'Pleural_Thickening', 'Pneumonia', 'Pneumothorax'
]

def load_and_inspect_model():
    """Load model and inspect its architecture"""
    try:
        print("🔍 Loading and inspecting model...")
        model = load_model('densenet.hdf5', compile=False)
        
        print(f"✅ Model loaded successfully!")
        print(f"📊 Input shape: {model.input_shape}")
        print(f"📊 Output shape: {model.output_shape}")
        print(f"📊 Number of layers: {len(model.layers)}")
        
        # Print model summary
        print("\n🏗️  Model Architecture:")
        model.summary()
        
        return model
        
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return None

def preprocess_image_simple(image_path, target_size=(224, 224)):
    """Simple image preprocessing"""
    try:
        # Read and preprocess image
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Could not load image: {image_path}")
        
        # Convert BGR to RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Resize
        img = cv2.resize(img, target_size)
        
        # Normalize to [0,1]
        img = img.astype(np.float32) / 255.0
        
        # Add batch dimension
        img = np.expand_dims(img, axis=0)
        
        return img
        
    except Exception as e:
        print(f"❌ Error preprocessing: {e}")
        return None

def demo_prediction():
    """Demo the prediction system"""
    print("🏥 Chest X-Ray Diagnosis Demo")
    print("=" * 40)
    
    # Load model
    model = load_and_inspect_model()
    if model is None:
        return
    
    # Check for sample image
    sample_image = "asset/00025288_001.png"
    
    if not os.path.exists(sample_image):
        print(f"❌ Sample image not found: {sample_image}")
        return
    
    print(f"\n📸 Processing sample X-ray: {sample_image}")
    
    # Preprocess image
    processed_img = preprocess_image_simple(sample_image)
    if processed_img is None:
        return
    
    try:
        # Make prediction
        print("🔮 Making prediction...")
        predictions = model.predict(processed_img, verbose=0)
        
        print(f"📊 Raw prediction shape: {predictions.shape}")
        print(f"📊 Raw predictions: {predictions}")
        
        # Handle different output formats
        if len(predictions.shape) > 2:
            # If output is multi-dimensional, flatten or take mean
            predictions = np.mean(predictions, axis=(1, 2)) if len(predictions.shape) == 4 else predictions.flatten()
        
        if len(predictions.shape) == 2:
            predictions = predictions[0]  # Remove batch dimension
        
        print(f"📊 Processed predictions shape: {predictions.shape}")
        print(f"📊 Number of outputs: {len(predictions)}")
        
        # Display results
        print("\n🏥 DIAGNOSIS RESULTS:")
        print("=" * 30)
        
        # If we have 14 outputs, map to diseases
        if len(predictions) == 14:
            for i, (label, prob) in enumerate(zip(LABELS, predictions)):
                status = "🔴" if prob > 0.5 else "🟢"
                print(f"{status} {label}: {prob:.3f}")
        else:
            # Just show raw predictions
            print(f"Raw model outputs ({len(predictions)} values):")
            for i, pred in enumerate(predictions):
                print(f"  Output {i}: {pred:.6f}")
        
        # Display the image
        display_image(sample_image)
        
    except Exception as e:
        print(f"❌ Error during prediction: {e}")
        import traceback
        traceback.print_exc()

def display_image(image_path):
    """Display the X-ray image"""
    try:
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        plt.figure(figsize=(8, 6))
        plt.imshow(img, cmap='gray')
        plt.title(f"Chest X-Ray: {os.path.basename(image_path)}")
        plt.axis('off')
        plt.tight_layout()
        plt.show()
        
    except Exception as e:
        print(f"⚠️  Could not display image: {e}")

if __name__ == "__main__":
    demo_prediction()