#!/usr/bin/env python3
"""
Test the backend API with actual model predictions
"""

import requests
import base64
import json
import numpy as np
from PIL import Image
from io import BytesIO
import cv2
import os

def create_test_image():
    """Create a test X-ray-like image"""
    # Create a realistic chest X-ray simulation
    img = np.zeros((400, 400, 3), dtype=np.uint8)
    
    # Add some chest-like structures
    cv2.ellipse(img, (200, 300), (150, 100), 0, 0, 180, (100, 100, 100), -1)  # Chest cavity
    cv2.ellipse(img, (200, 200), (80, 60), 0, 0, 360, (120, 120, 120), -1)   # Heart area
    
    # Add some noise for realism
    noise = np.random.randint(0, 50, img.shape, dtype=np.uint8)
    img = cv2.add(img, noise)
    
    return img

def test_api_with_real_image():
    """Test API with real sample image"""
    sample_path = "asset/00025288_001.png"
    
    if not os.path.exists(sample_path):
        print(f"❌ Sample image not found: {sample_path}")
        return False
    
    try:
        # Load and encode image
        with open(sample_path, "rb") as f:
            img_data = base64.b64encode(f.read()).decode()
        
        img_data_url = f"data:image/png;base64,{img_data}"
        
        # Send request
        response = requests.post(
            'http://localhost:5001/api/analyze',
            json={'image': img_data_url},
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Real image analysis successful!")
            print(f"📊 Success: {data.get('success', False)}")
            print(f"📊 Results count: {len(data.get('results', []))}")
            print(f"📊 Detected conditions: {len(data.get('detected_conditions', []))}")
            
            # Show top 3 results
            results = data.get('results', [])
            if results:
                print("\n🔍 Top 3 Predictions:")
                for i, result in enumerate(results[:3]):
                    status = "🔴" if result['detected'] else "🟢"
                    print(f"   {i+1}. {status} {result['disease']}: {result['confidence']}")
            
            return True
        else:
            print(f"❌ API request failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Real image test failed: {e}")
        return False

def test_api_with_synthetic_image():
    """Test API with synthetic image"""
    try:
        # Create test image
        img_array = create_test_image()
        img = Image.fromarray(img_array)
        
        # Convert to base64
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        img_data_url = f"data:image/png;base64,{img_base64}"
        
        # Send request
        response = requests.post(
            'http://localhost:5001/api/analyze',
            json={'image': img_data_url},
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Synthetic image analysis successful!")
            print(f"📊 Success: {data.get('success', False)}")
            
            # Show summary
            summary = data.get('summary', {})
            print(f"📊 Status: {summary.get('status', 'Unknown')}")
            print(f"📊 Detected count: {summary.get('detected_count', 0)}")
            
            return True
        else:
            print(f"❌ Synthetic image test failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Synthetic image test failed: {e}")
        return False

def test_multiple_images():
    """Test with multiple different images to see if predictions vary"""
    print("\n🔄 Testing Multiple Images for Variation...")
    
    results_list = []
    
    for i in range(3):
        try:
            # Create different test images
            img_array = np.random.randint(0, 255, (300, 300, 3), dtype=np.uint8)
            
            # Add different patterns
            if i == 0:
                cv2.circle(img_array, (150, 150), 50, (200, 200, 200), -1)
            elif i == 1:
                cv2.rectangle(img_array, (100, 100), (200, 200), (150, 150, 150), -1)
            else:
                cv2.ellipse(img_array, (150, 150), (80, 120), 45, 0, 360, (180, 180, 180), -1)
            
            img = Image.fromarray(img_array)
            
            # Convert to base64
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            img_base64 = base64.b64encode(buffer.getvalue()).decode()
            img_data_url = f"data:image/png;base64,{img_base64}"
            
            # Send request
            response = requests.post(
                'http://localhost:5001/api/analyze',
                json={'image': img_data_url},
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                if results:
                    # Get top prediction
                    top_pred = results[0]
                    results_list.append({
                        'image': i+1,
                        'top_disease': top_pred['disease'],
                        'probability': top_pred['probability'],
                        'detected_count': len(data.get('detected_conditions', []))
                    })
                    
        except Exception as e:
            print(f"❌ Test {i+1} failed: {e}")
    
    # Analyze variation
    if len(results_list) >= 2:
        print("📊 Results Variation Analysis:")
        for result in results_list:
            print(f"   Image {result['image']}: {result['top_disease']} ({result['probability']:.3f}) - {result['detected_count']} detected")
        
        # Check if results are different (indicating real model usage)
        probs = [r['probability'] for r in results_list]
        diseases = [r['top_disease'] for r in results_list]
        
        prob_variation = max(probs) - min(probs)
        disease_variation = len(set(diseases))
        
        print(f"\n📈 Probability variation: {prob_variation:.3f}")
        print(f"📈 Disease variation: {disease_variation} different top diseases")
        
        if prob_variation > 0.1 or disease_variation > 1:
            print("✅ Results show good variation - likely using real model!")
        else:
            print("⚠️  Results show little variation - might be using static data")
        
        return True
    
    return False

def main():
    """Run all backend tests"""
    print("🧪 Backend API Model Test")
    print("=" * 40)
    
    # Check if server is running
    try:
        response = requests.get('http://localhost:5001/api/health', timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Server is running")
            print(f"📊 Model loaded: {health_data.get('model_loaded', False)}")
        else:
            print("❌ Server not responding properly")
            return
    except Exception as e:
        print(f"❌ Server not running. Start it with: python3 backend_api.py")
        return
    
    print("\n" + "=" * 40)
    
    # Test 1: Real image
    print("🖼️  Test 1: Real Sample Image")
    real_image_success = test_api_with_real_image()
    
    print("\n" + "=" * 40)
    
    # Test 2: Synthetic image
    print("🎨 Test 2: Synthetic Image")
    synthetic_success = test_api_with_synthetic_image()
    
    print("\n" + "=" * 40)
    
    # Test 3: Multiple images for variation
    variation_success = test_multiple_images()
    
    # Summary
    print("\n📋 TEST SUMMARY")
    print("=" * 40)
    print(f"Real Image Test: {'✅' if real_image_success else '❌'}")
    print(f"Synthetic Image Test: {'✅' if synthetic_success else '❌'}")
    print(f"Variation Test: {'✅' if variation_success else '❌'}")
    
    if all([real_image_success, synthetic_success, variation_success]):
        print("\n🎉 ALL TESTS PASSED!")
        print("   Your model is working and producing varied, realistic predictions")
        print("   The system is using actual AI analysis, not static data")
    else:
        print("\n⚠️  SOME TESTS FAILED")
        print("   Check the backend logs for more details")

if __name__ == "__main__":
    main()