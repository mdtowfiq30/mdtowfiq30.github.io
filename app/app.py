import streamlit as st
import tensorflow as tf
import os
import gdown
import numpy as np
from tensorflow.keras.preprocessing import image as keras_image
from PIL import Image
import matplotlib.pyplot as plt

# Define the categories for your classification
categories = ['Fire', 'Smoke']

@st.cache_resource  # Efficient caching for loading models
def load_model():
    model_path = 'my_model.hdf5'
    
    # Check if the model already exists locally
    if not os.path.exists(model_path):
        st.write("Downloading model...")  # User feedback
        # Download the model from Google Drive
        gdown.download('https://drive.google.com/uc?id=1AWTM0CbzWqt_pNJKnW2L9SVOauxln3PT', model_path, quiet=False)
    
    # Load the model
    model = tf.keras.models.load_model(model_path)
    return model

# Load the model with a spinner
with st.spinner('Loading model...'):
    model = load_model()

# Custom styling for a more professional look
st.markdown(
    """
    <style>
    .main-title {
        font-size: 36px;
        color: #2E86C1;
        text-align: center;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .upload-section {
        text-align: center;
        margin-top: 20px;
        font-size: 18px;
    }
    .result-box {
        font-size: 24px;
        font-weight: bold;
        color: #1ABC9C;
        text-align: center;
        margin-top: 30px;
    }
    </style>
    """, unsafe_allow_html=True
)

# App title in the center
st.markdown('<div class="main-title">Fire or Smoke Classification</div>', unsafe_allow_html=True)

# File uploader section on the main page
st.markdown('<div class="upload-section">Upload an image (jpg or png) to classify:</div>', unsafe_allow_html=True)
file = st.file_uploader("", type=["jpg", "png"])

# Check if the user uploaded a file
if file is None:
    st.text("Please upload an image file.")
else:
    # Load the image
    image_for_testing = Image.open(file).convert("RGB")

    # Preprocess the image for prediction
    test_image = keras_image.img_to_array(image_for_testing)
    test_image = keras_image.smart_resize(test_image, (150, 150))  # Resize the image
    test_image = test_image / 255.0  # Normalize the image
    test_image = np.expand_dims(test_image, axis=0)  # Expand dimensions for the model

    # Make predictions
    result = (model.predict(test_image) > 0.5).astype("int32")

    # Display prediction result in a professional styled box
    prediction = categories[int(result[0][0])]
    st.markdown(f'<div class="result-box">This image most likely belongs to: **{prediction}**.</div>', unsafe_allow_html=True)

    # Display the uploaded image with the prediction as the title using matplotlib
    plt.imshow(image_for_testing)
    plt.title(f"Predicted: {prediction}")
    plt.axis('off')  # Hide axes
    st.pyplot(plt)
