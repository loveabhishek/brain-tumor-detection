#!/usr/bin/env python3
"""
Test script to verify the improved brain tumor detection system
"""

import requests
import os
import time

def test_improved_system():
    """Test the improved prediction system"""
    print("🧠 Testing Improved Brain Tumor Detection System")
    print("=" * 50)
    
    # Test 1: Check if Flask app is running
    try:
        response = requests.get("http://127.0.0.1:8080/", timeout=5)
        if response.status_code == 200:
            print("✅ Flask application is running")
        else:
            print("❌ Flask application returned status:", response.status_code)
            return
    except requests.exceptions.RequestException as e:
        print("❌ Flask application is not running")
        print("   Start it with: python app.py")
        return
    
    # Test 2: Test prediction with sample images
    print("\n📊 Testing Predictions with Sample Images")
    print("-" * 40)
    
    # Find test images
    uploads_dir = "uploads"
    test_images = []
    
    if os.path.exists(uploads_dir):
        for filename in os.listdir(uploads_dir):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                filepath = os.path.join(uploads_dir, filename)
                test_images.append((filename, filepath))
    
    if not test_images:
        print("❌ No test images found in uploads folder")
        return
    
    print(f"Found {len(test_images)} test images")
    
    # Test a few images
    for i, (filename, filepath) in enumerate(test_images[:3]):
        print(f"\n🔍 Testing {filename}...")
        
        try:
            # Prepare test data
            test_data = {
                'patient_name': 'Test Patient',
                'patient_age': '35',
                'patient_sex': 'Male'
            }
            
            # Prepare file upload
            with open(filepath, 'rb') as f:
                files = {'file': (filename, f, 'image/jpeg')}
                
                # Make prediction request
                response = requests.post(
                    "http://127.0.0.1:8080/predict",
                    data=test_data,
                    files=files,
                    timeout=30
                )
            
            if response.status_code == 200:
                result = response.json()
                prediction = result.get('prediction', 'Unknown')
                tumor_data = result.get('tumor_data')
                pdf_filename = result.get('pdf_filename')
                
                print(f"   Prediction: {prediction}")
                if tumor_data:
                    print(f"   Tumor Size: {tumor_data['size']} cm")
                    print(f"   Danger Level: {'HIGH' if tumor_data['is_dangerous'] else 'LOW'}")
                if pdf_filename:
                    print(f"   PDF Report: {pdf_filename}")
                
                # Expected result based on filename
                expected = "Yes Brain Tumor" if filename.startswith(('Y_', 'y')) else "No Brain Tumor"
                if filename.startswith(('N_', 'n')):
                    expected = "No Brain Tumor"
                
                print(f"   Expected: {expected}")
                
                if prediction == expected:
                    print("   ✅ Prediction matches expected result!")
                else:
                    print("   ⚠️  Prediction differs from expected result")
                    
            else:
                print(f"   ❌ Request failed with status: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error testing {filename}: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Testing completed!")
    print("\n📝 Next Steps:")
    print("1. Open http://127.0.0.1:8080/ in your browser")
    print("2. Upload your tumor images and test the system")
    print("3. Check the generated PDF reports in the uploads folder")

if __name__ == "__main__":
    test_improved_system() 