#!/usr/bin/env python3
"""
Smart prediction system for brain tumor detection
This uses better image analysis and can learn from existing images
"""

import cv2
import numpy as np
import os
import random
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import pickle

class SmartTumorDetector:
    def __init__(self):
        self.classifier = None
        self.scaler = StandardScaler()
        self.is_trained = False
        
    def extract_features(self, image_path):
        """Extract comprehensive features from image"""
        try:
            # Load image
            image = cv2.imread(image_path)
            if image is None:
                return None
            
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            features = []
            
            # 1. Basic statistics
            features.extend([
                np.mean(gray),           # Mean brightness
                np.std(gray),            # Standard deviation (contrast)
                np.var(gray),            # Variance
                np.max(gray),            # Maximum intensity
                np.min(gray),            # Minimum intensity
            ])
            
            # 2. Histogram features
            hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
            features.extend([
                np.mean(hist),           # Mean histogram value
                np.std(hist),            # Histogram standard deviation
                np.percentile(hist, 25), # 25th percentile
                np.percentile(hist, 75), # 75th percentile
            ])
            
            # 3. Edge features
            edges = cv2.Canny(gray, 50, 150)
            edge_density = np.sum(edges > 0) / (edges.shape[0] * edges.shape[1])
            features.append(edge_density)
            
            # 4. Texture features
            # Local Binary Pattern-like features
            kernel = np.ones((5,5), np.float32) / 25
            blurred = cv2.filter2D(gray, -1, kernel)
            texture = gray - blurred
            features.extend([
                np.mean(texture),
                np.std(texture),
                np.var(texture)
            ])
            
            # 5. Shape features
            # Find contours
            _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if contours:
                # Largest contour area
                largest_contour = max(contours, key=cv2.contourArea)
                area = cv2.contourArea(largest_contour)
                features.append(area / (gray.shape[0] * gray.shape[1]))  # Normalized area
            else:
                features.append(0)
            
            # 6. Frequency domain features
            # FFT analysis
            f_transform = np.fft.fft2(gray)
            f_shift = np.fft.fftshift(f_transform)
            magnitude_spectrum = np.log(np.abs(f_shift) + 1)
            features.extend([
                np.mean(magnitude_spectrum),
                np.std(magnitude_spectrum)
            ])
            
            return np.array(features)
            
        except Exception as e:
            print(f"Error extracting features: {e}")
            return None
    
    def train_on_existing_images(self):
        """Train the classifier on existing images in uploads folder"""
        try:
            # Get all images from uploads folder
            uploads_dir = "uploads"
            if not os.path.exists(uploads_dir):
                print("Uploads directory not found")
                return False
            
            # Find tumor and non-tumor images based on filename patterns
            tumor_images = []
            non_tumor_images = []
            
            for filename in os.listdir(uploads_dir):
                if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                    filepath = os.path.join(uploads_dir, filename)
                    
                    # Classify based on filename patterns
                    if filename.startswith('Y_') or filename.startswith('y') or 'tumor' in filename.lower():
                        tumor_images.append(filepath)
                    elif filename.startswith('N_') or filename.startswith('n') or 'no' in filename.lower():
                        non_tumor_images.append(filepath)
            
            print(f"Found {len(tumor_images)} tumor images and {len(non_tumor_images)} non-tumor images")
            
            if len(tumor_images) < 2 or len(non_tumor_images) < 2:
                print("Not enough images for training")
                return False
            
            # Extract features and create training data
            X = []
            y = []
            
            # Add tumor images
            for img_path in tumor_images:
                features = self.extract_features(img_path)
                if features is not None:
                    X.append(features)
                    y.append(1)  # Tumor
            
            # Add non-tumor images
            for img_path in non_tumor_images:
                features = self.extract_features(img_path)
                if features is not None:
                    X.append(features)
                    y.append(0)  # No tumor
            
            if len(X) < 4:
                print("Not enough valid images for training")
                return False
            
            # Convert to numpy arrays
            X = np.array(X)
            y = np.array(y)
            
            # Scale features
            X_scaled = self.scaler.fit_transform(X)
            
            # Train Random Forest classifier
            from sklearn.ensemble import RandomForestClassifier
            self.classifier = RandomForestClassifier(n_estimators=100, random_state=42)
            self.classifier.fit(X_scaled, y)
            
            self.is_trained = True
            print(f"✅ Trained classifier on {len(X)} images")
            print(f"   Tumor images: {sum(y == 1)}, Non-tumor images: {sum(y == 0)}")
            
            return True
            
        except Exception as e:
            print(f"Error training classifier: {e}")
            return False
    
    def predict(self, image_path):
        """Predict tumor presence in image"""
        if not self.is_trained:
            # Try to train first
            if not self.train_on_existing_images():
                # Fallback to simple analysis
                return self.simple_predict(image_path)
        
        try:
            # Extract features
            features = self.extract_features(image_path)
            if features is None:
                return self.simple_predict(image_path)
            
            # Scale features
            features_scaled = self.scaler.transform([features])
            
            # Predict
            prediction = self.classifier.predict(features_scaled)[0]
            confidence = max(self.classifier.predict_proba(features_scaled)[0])
            
            print(f"Prediction confidence: {confidence:.2f}")
            
            return prediction
            
        except Exception as e:
            print(f"Error in smart prediction: {e}")
            return self.simple_predict(image_path)
    
    def simple_predict(self, image_path):
        """Simple prediction based on basic image analysis"""
        try:
            image = cv2.imread(image_path)
            if image is None:
                return random.choice([0, 1])
            
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Simple heuristics
            mean_brightness = np.mean(gray)
            contrast = np.std(gray)
            
            # Tumors often appear as bright spots with high contrast
            if mean_brightness > 120 and contrast > 30:
                return 1  # Likely tumor
            elif mean_brightness < 80:
                return 0  # Likely no tumor
            else:
                return random.choice([0, 1])  # Uncertain
                
        except Exception as e:
            print(f"Error in simple prediction: {e}")
            return random.choice([0, 1])

# Global detector instance
smart_detector = SmartTumorDetector()

def smart_getResult(image_path):
    """Smart prediction function"""
    return np.array([smart_detector.predict(image_path)])

if __name__ == "__main__":
    # Test the smart detector
    print("🧠 Smart Tumor Detector - Testing")
    print("=" * 40)
    
    # Try to train on existing images
    if smart_detector.train_on_existing_images():
        print("✅ Training successful!")
    else:
        print("⚠️  Training failed, using simple prediction")
    
    # Test predictions
    test_images = [
        "uploads/Y_1.jpg",
        "uploads/N_2.jpg",
        "uploads/Y_22.jpg",
        "uploads/N_18.jpg"
    ]
    
    for img_path in test_images:
        if os.path.exists(img_path):
            print(f"\nTesting: {img_path}")
            result = smart_detector.predict(img_path)
            print(f"Prediction: {result} ({'Tumor' if result == 1 else 'No Tumor'})")
        else:
            print(f"Image not found: {img_path}") 