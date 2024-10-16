import streamlit as st
import tensorflow as tf
import os
import gdown
import cv2
from PIL import Image, ImageOps
import numpy as np

# Define the categories for your classification
categories = ['Fire', 'Smoke']

@st.cache_resource  # Efficient caching for loading models
def load_model():
    model_path = 'my_model.hdf5'
    
    # Check if the model already exists locally
    if not os.path.exists(model_path):
        st.write("Downloading model...")  # User feedback
        # Download the model from Google Drive
        gdown.download('https://drive.google.com/uc?id=1tfDOIcL7cVBzB8lsarOh0i6RvJG1IfQ9', model_path, quiet=False)
    
    # Load the model
    model = tf.keras.models.load_model(model_path)
    return model

with st.spinner('Loading model...'):
    model = load_model()

# App title
st.write("""
         # Fire or Smoke Classification
         """
         )

# File uploader for the user to upload an image
file = st.file_uploader("Please upload a brain scan file", type=["jpg", "png"])


# Function to preprocess the image and make predictions
def import_and_predict(image_data, model):
    size = (150, 150)    
    image = ImageOps.fit(image_data, size, Image.LANCZOS)
    image = np.asarray(image) / 255.0  # Normalize the image
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    img_reshape = img[np.newaxis, ...]  # Reshape for model input
    prediction = model.predict(img_reshape)  # Make prediction
    
    return prediction

# Check if the user uploaded a file
if file is None:
    st.text("Please upload an image file")
else:
    image = Image.open(file)  # Open the uploaded image
    st.image(image, use_column_width=True)  # Display the image
    predictions = import_and_predict(image, model)  # Get predictions
    score = tf.nn.softmax(predictions[0])  # Get softmax scores
    
    # Display the predictions and confidence score
    st.write(predictions)
    st.write(score)
    st.write(
        "This image most likely belongs to **{}** with a **{:.2f}** percent confidence."
        .format(categories[np.argmax(score)], 100 * np.max(score))
    )
