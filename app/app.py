import streamlit as st
import tensorflow as tf
import os
import gdown
import numpy as np
from tensorflow.keras.preprocessing import image as keras_image
from PIL import Image
import matplotlib.pyplot as plt

# Define the categories for your classification
categories = ['🔥 Fire', '💨 Smoke']

@st.cache_resource  # Efficient caching for loading models
def load_model():
    model_path = 'my_model.hdf5'
    
    # Check if the model already exists locally
    if not os.path.exists(model_path):
        st.write("Downloading model...")  # User feedback
        gdown.download('https://drive.google.com/uc?id=1tfDOIcL7cVBzB8lsarOh0i6RvJG1IfQ9', model_path, quiet=False)
    
    # Load the model
    model = tf.keras.models.load_model(model_path)
    return model

# Sidebar for file upload
st.sidebar.title("🔥 Smoke or Fire Detector")
st.sidebar.write("Upload an image to classify whether it contains fire or smoke.")

# Load the model with a spinner
with st.spinner('Loading model...'):
    model = load_model()

# File uploader in the sidebar
file = st.sidebar.file_uploader("Upload an image file", type=["jpg", "png"])

st.title("🚨 Fire or Smoke Classification")
st.write("This application helps in identifying whether the uploaded image contains **fire** or **smoke**. Upload an image and let the AI do the work!")

if file is None:
    st.write("👈 Upload an image from the sidebar to start.")
else:
    # Display uploaded image
    image_for_testing = Image.open(file).convert("RGB")
    st.image(image_for_testing, caption="Uploaded Image", use_column_width=True)
    
    # Show a progress bar while processing the image
    with st.spinner('Analyzing the image...'):
        # Preprocess the image for prediction
        test_image = keras_image.img_to_array(image_for_testing)
        test_image = keras_image.smart_resize(test_image, (150, 150))  # Resize the image
        test_image = test_image / 255.0  # Normalize the image
        test_image = np.expand_dims(test_image, axis=0)  # Expand dimensions for the model

        # Make predictions
        result = (model.predict(test_image) > 0.5).astype("int32")
    
    # Display the result with improved text formatting
    prediction = categories[int(result[0][0])]
    confidence_message = f"### Prediction: **{prediction}**"
    
    st.success(confidence_message)

    # Optionally, display the prediction with matplotlib (optional)
    plt.imshow(image_for_testing)
    plt.title(f"Predicted: {prediction}")
    plt.axis('off')  # Hide axes
    st.pyplot(plt)

# Footer
st.sidebar.markdown("""
---
*Developed with ❤️ by [Your Name]*  
Powered by TensorFlow & Streamlit
""")
