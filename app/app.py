import streamlit as st
import tensorflow as tf
import os
import gdown
import numpy as np
from tensorflow.keras.preprocessing import image as keras_image
from PIL import Image

# Load your model here
def load_model():
    model_path = 'my_model.hdf5'
    if not os.path.exists(model_path):
        st.write("Downloading model...")  # User feedback
        gdown.download('https://drive.google.com/uc?id=1tfDOIcL7cVBzB8lsarOh0i6RvJG1IfQ9', model_path, quiet=False)
    return tf.keras.models.load_model(model_path)

model = load_model()

# Define categories
categories = ['Fire', 'Smoke']

# Set the title of the app
st.title("Fire & Smoke Detection App")

# Add custom HTML/CSS for styling
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    <style>
    body {
        font-family: 'Roboto', sans-serif;
        background-color: #fafafa;
        margin: 0;
        padding: 20px;
    }
    h1 {
        color: #333;
        text-align: center;
        font-size: 2.5em;
        margin-bottom: 20px;
    }
    .custom-button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
        font-size: 16px;
        transition: background-color 0.3s;
    }
    .custom-button:hover {
        background-color: #45a049;
    }
    </style>
    """, unsafe_allow_html=True)

# File uploader for image
file = st.file_uploader("Upload an image for detection", type=["jpg", "png"])

if file is not None:
    # Load the image
    image_for_testing = Image.open(file).convert("RGB")

    # Preprocess the image
    test_image = keras_image.img_to_array(image_for_testing)
    test_image = keras_image.smart_resize(test_image, (150, 150))
    test_image = test_image / 255.0
    test_image = np.expand_dims(test_image, axis=0)

    # Make predictions
    result = (model.predict(test_image) > 0.5).astype("int32")

    # Show the uploaded image
    st.image(image_for_testing, caption="Uploaded Image", use_column_width=True)

    # Show the prediction result
    prediction = categories[int(result[0][0])]
    st.write(f"This image most likely belongs to: **{prediction}**.")
