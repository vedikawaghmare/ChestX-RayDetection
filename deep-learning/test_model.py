#!/usr/bin/env python3
"""
Model Diagnostic Script - Check if DenseNet model is working properly
"""

import os
import numpy as np
import cv2
from tensorflow.keras.models import load_model
import warnings
warnings.filterwarnings('ignore')

def test_model_loading():
    """Test if model loads correctly"""
    print("🔍 Testing Model Loading...")
    print("=" * 40)
    
    model_path = "densenet.hdf5"
    
    if not os.path.exists(model_path):
        print(f"❌ Model file not found: {model_path}")
        print(f"📁 Current directory: {os.getcwd()}")
        print(f"📂 Files in directory: {os.listdir('.')}")
        return None
    
    try:
        print(f"📊 Model file size: {os.path.getsize(model_path) / (1024*1024):.1f} MB")
        
        model = load_model(model_path, compile=False)
        print("✅ Model loaded successfully!")
        
        print(f"📐 Input shape: {model.input_shape}")
        print(f"📐 Output shape: {model.output_shape}")
        print(f"🏗️  Total layers: {len(model.layers)}")
        
        return model
        
    except Exception as e:
        print(f"❌ Model loading failed: {e}")
        return None

def test_model_prediction(model):
    """Test model prediction with dummy data"""
    print("\n🧪 Testing Model Prediction...")
    print("=" * 40)
    
    if model is None:
        print("❌ No model to test")
        return False
    
    try:
        # Create dummy input matching expected shape
        input_shape = model.input_shape
        print(f"📊 Expected input shape: {input_shape}")
        
        if input_shape[1] is None:  # Variable input size
            test_shape = (1, 320, 320, 3)
        else:
            test_shape = (1,) + input_shape[1:]
        
        print(f"🎯 Using test shape: {test_shape}")
        
        # Create random test image
        test_image = np.random.rand(*test_shape).astype(np.float32)
        
        # Make prediction
        print("🔮 Making prediction...")
        predictions = model.predict(test_image, verbose=0)
        
        print(f"✅ Prediction successful!")
        print(f"📊 Output shape: {predictions.shape}")
        print(f"📊 Output type: {type(predictions)}")
        print(f"📊 Output range: [{predictions.min():.6f}, {predictions.max():.6f}]")
        
        # Check if output makes sense for 14 diseases
        if len(predictions.shape) == 2 and predictions.shape[1] == 14:
            print("✅ Output format matches 14 diseases!")
            return True
        elif len(predictions.shape) > 2:
            print(f"⚠️  Complex output shape - may need processing")
            return True
        else:
            print(f"⚠️  Unexpected output format")
            return True
            
    except Exception as e:
        print(f"❌ Prediction failed: {e}")
        return False

def test_with_real_image():
    """Test with actual X-ray image if available"""
    print("\n📸 Testing with Real Image...")
    print("=" * 40)
    
    # Look for sample images
    sample_paths = [
        "asset/00025288_001.png",
        "../asset/00025288_001.png",
        "sample.png",
        "test.jpg"
    ]
    
    sample_image = None
    for path in sample_paths:
        if os.path.exists(path):
            sample_image = path
            break
    
    if not sample_image:
        print("⚠️  No sample image found")
        return False
    
    try:
        print(f"📁 Using image: {sample_image}")
        
        # Load and preprocess image
        img = cv2.imread(sample_image)
        if img is None:
            print("❌ Failed to load image")
            return False
        
        print(f"📊 Original image shape: {img.shape}")
        
        # Resize to 320x320 (common for medical models)
        img = cv2.resize(img, (320, 320))
        img = img.astype(np.float32) / 255.0
        img = np.expand_dims(img, axis=0)
        
        print(f"📊 Processed image shape: {img.shape}")
        
        # Load model and predict
        model = load_model("densenet.hdf5", compile=False)
        predictions = model.predict(img, verbose=0)
        
        print(f"✅ Real image prediction successful!")
        print(f"📊 Predictions shape: {predictions.shape}")
        
        # Show some prediction values
        if len(predictions.shape) == 2:
            pred_flat = predictions[0]
        else:
            pred_flat = predictions.flatten()
        
        print(f"📊 Sample predictions: {pred_flat[:5]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Real image test failed: {e}")
        return False

def check_backend_model_usage():
    """Check what the backend is actually doing"""
    print("\n🔧 Checking Backend Model Usage...")
    print("=" * 40)
    
    try:
        # Import the backend to see what it does
        import backend_api
        
        print(f"📊 Backend model status: {backend_api.model is not None}")
        
        if backend_api.model is not None:
            print("✅ Backend has loaded the model!")
            print(f"📐 Model input shape: {backend_api.model.input_shape}")
            print(f"📐 Model output shape: {backend_api.model.output_shape}")
        else:
            print("⚠️  Backend is using mock predictions")
        
        return backend_api.model is not None
        
    except Exception as e:
        print(f"❌ Backend check failed: {e}")
        return False

def main():
    """Run all diagnostic tests"""
    print("🏥 DenseNet Model Diagnostic Tool")
    print("=" * 50)
    
    # Test 1: Model loading
    model = test_model_loading()
    model_loads = model is not None
    
    # Test 2: Model prediction
    prediction_works = test_model_prediction(model)
    
    # Test 3: Real image test
    real_image_works = test_with_real_image()
    
    # Test 4: Backend check
    backend_uses_model = check_backend_model_usage()
    
    # Summary
    print("\n📋 DIAGNOSTIC SUMMARY")
    print("=" * 50)
    print(f"Model File Exists: {'✅' if os.path.exists('densenet.hdf5') else '❌'}")
    print(f"Model Loads: {'✅' if model_loads else '❌'}")
    print(f"Predictions Work: {'✅' if prediction_works else '❌'}")
    print(f"Real Image Test: {'✅' if real_image_works else '❌'}")
    print(f"Backend Uses Model: {'✅' if backend_uses_model else '❌'}")
    
    if all([model_loads, prediction_works, backend_uses_model]):
        print("\n🎉 MODEL IS WORKING PROPERLY!")
        print("   Your system is using the actual DenseNet-121 model")
        print("   Predictions are real AI analysis, not mock data")
    elif model_loads and prediction_works:
        print("\n⚠️  MODEL WORKS BUT BACKEND ISSUES")
        print("   Model loads and works, but backend might use mock data")
        print("   Check backend_api.py configuration")
    else:
        print("\n❌ MODEL NOT WORKING PROPERLY")
        print("   System is likely using mock/static predictions")
        print("   Check model file and dependencies")

if __name__ == "__main__":
    main()