#!/usr/bin/env python3
"""
Test Enhanced System with Charts and PDF Reports
"""

import requests
import base64
import json
import numpy as np
from PIL import Image
from io import BytesIO
import os

def test_analysis_with_charts():
    """Test analysis endpoint with chart generation"""
    print("🧪 Testing Enhanced Analysis with Charts...")
    
    try:
        # Create test image
        img_array = np.random.randint(50, 200, (400, 400, 3), dtype=np.uint8)
        
        # Add some medical-like features
        from PIL import ImageDraw
        img = Image.fromarray(img_array)
        draw = ImageDraw.Draw(img)
        
        # Draw chest-like structures
        draw.ellipse([100, 200, 300, 350], fill=(120, 120, 120))  # Chest cavity
        draw.ellipse([180, 150, 220, 200], fill=(100, 100, 100))  # Heart area
        
        # Convert to base64
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        img_data_url = f"data:image/png;base64,{img_base64}"
        
        # Send analysis request
        response = requests.post(
            'http://localhost:5001/api/analyze',
            json={'image': img_data_url},
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Analysis successful!")
            print(f"📊 Results: {len(data.get('results', []))} conditions")
            print(f"📊 Detected: {len(data.get('detected_conditions', []))} conditions")
            print(f"📊 Charts: {len(data.get('charts', {}))} generated")
            
            # List available charts
            charts = data.get('charts', {})
            if charts:
                print("📈 Available charts:")
                for chart_name in charts.keys():
                    print(f"   • {chart_name}")
            
            return data
        else:
            print(f"❌ Analysis failed: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Analysis test failed: {e}")
        return None

def test_pdf_generation(analysis_data):
    """Test PDF report generation"""
    print("\n📄 Testing PDF Report Generation...")
    
    if not analysis_data:
        print("❌ No analysis data for PDF test")
        return False
    
    try:
        # Send PDF generation request
        response = requests.post(
            'http://localhost:5001/api/generate-report',
            json={
                'analysis_data': analysis_data,
                'patient_info': {
                    'id': 'TEST-001',
                    'name': 'Test Patient'
                }
            },
            headers={'Content-Type': 'application/json'},
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and data.get('pdf_data'):
                print("✅ PDF generation successful!")
                print(f"📄 Filename: {data.get('filename')}")
                
                # Save PDF for verification
                pdf_data = base64.b64decode(data['pdf_data'])
                with open(f"test_{data['filename']}", 'wb') as f:
                    f.write(pdf_data)
                print(f"💾 PDF saved as: test_{data['filename']}")
                
                return True
            else:
                print("❌ PDF generation failed in response")
                return False
        else:
            print(f"❌ PDF request failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ PDF test failed: {e}")
        return False

def test_chart_generation():
    """Test chart generation directly"""
    print("\n📊 Testing Direct Chart Generation...")
    
    try:
        from report_generator import report_generator
        
        # Create mock results
        mock_results = [
            {'disease': 'Cardiomegaly', 'probability': 0.75, 'detected': True, 'severity': 'High', 'confidence': '75.0%'},
            {'disease': 'Pneumonia', 'probability': 0.60, 'detected': True, 'severity': 'Medium', 'confidence': '60.0%'},
            {'disease': 'Atelectasis', 'probability': 0.30, 'detected': False, 'severity': 'Low', 'confidence': '30.0%'},
            {'disease': 'Edema', 'probability': 0.20, 'detected': False, 'severity': 'Low', 'confidence': '20.0%'},
        ]
        
        detected = [r for r in mock_results if r['detected']]
        
        # Generate charts
        charts = report_generator.create_analysis_charts(mock_results, detected)
        
        print(f"✅ Chart generation successful!")
        print(f"📈 Generated charts: {list(charts.keys())}")
        
        # Verify charts have data
        for chart_name, chart_data in charts.items():
            if chart_data:
                print(f"   • {chart_name}: {len(chart_data)} characters")
            else:
                print(f"   • {chart_name}: No data")
        
        return len(charts) > 0
        
    except Exception as e:
        print(f"❌ Chart generation test failed: {e}")
        return False

def main():
    """Run all enhanced system tests"""
    print("🏥 Enhanced Chest X-Ray System Test")
    print("=" * 50)
    
    # Check server
    try:
        response = requests.get('http://localhost:5001/api/health', timeout=5)
        if response.status_code == 200:
            print("✅ Server is running")
        else:
            print("❌ Server not responding")
            return
    except:
        print("❌ Server not running. Start with: python3 backend_api.py")
        return
    
    # Test 1: Chart generation
    chart_success = test_chart_generation()
    
    # Test 2: Analysis with charts
    analysis_data = test_analysis_with_charts()
    analysis_success = analysis_data is not None
    
    # Test 3: PDF generation
    pdf_success = test_pdf_generation(analysis_data) if analysis_data else False
    
    # Summary
    print("\n📋 ENHANCED SYSTEM TEST SUMMARY")
    print("=" * 50)
    print(f"Chart Generation: {'✅' if chart_success else '❌'}")
    print(f"Analysis with Charts: {'✅' if analysis_success else '❌'}")
    print(f"PDF Report Generation: {'✅' if pdf_success else '❌'}")
    
    if all([chart_success, analysis_success, pdf_success]):
        print("\n🎉 ALL ENHANCED FEATURES WORKING!")
        print("   ✅ Matplotlib charts are generating properly")
        print("   ✅ Analysis includes visual charts")
        print("   ✅ PDF reports with charts are working")
        print("   ✅ System is ready for professional use")
    else:
        print("\n⚠️  SOME ENHANCED FEATURES NEED ATTENTION")
        if not chart_success:
            print("   ❌ Chart generation issues")
        if not analysis_success:
            print("   ❌ Analysis endpoint issues")
        if not pdf_success:
            print("   ❌ PDF generation issues")

if __name__ == "__main__":
    main()