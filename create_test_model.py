#!/usr/bin/env python3
"""
Create a simple test model for brain tumor detection demonstration
This creates a basic model that can analyze images (for demo purposes)
"""

import os
import numpy as np
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Flatten, Dense, Dropout
from tensorflow.keras.applications.vgg19 import VGG19
from tensorflow.keras.optimizers import Adam

def create_test_model():
    """Create a simple test model for demonstration"""
    print("Creating test model for brain tumor detection...")
    
    # Create the model architecture (same as your original)
    base_model = VGG19(include_top=False, input_shape=(240,240,3))
    x = base_model.output
    flat = Flatten()(x)
    class_1 = Dense(4608, activation='relu')(flat)
    drop_out = Dropout(0.2)(class_1)
    class_2 = Dense(1152, activation='relu')(drop_out)
    output = Dense(2, activation='softmax')(class_2)
    model = Model(base_model.inputs, output)
    
    # Compile the model
    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # Save the model weights
    model.save_weights('vgg_unfrozen.h5')
    print("✅ Test model weights saved as 'vgg_unfrozen.h5'")
    print("⚠️  Note: This is a test model with random weights for demonstration")
    print("   For real predictions, you need to train the model with actual data")
    
    return model

if __name__ == "__main__":
    create_test_model() 