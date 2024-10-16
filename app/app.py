
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
        gdown.download('https://drive.google.com/uc?id=1tfDOIcL7cVBzB8lsarOh0i6RvJG1IfQ9', model_path, quiet=False)
    
    # Load the model
    model = tf.keras.models.load_model(model_path)
    return model

# Load the model with a spinner
with st.spinner('Loading model...'):
    model = load_model()

# App title
st.title("Fire or Smoke Classification")

# File uploader for the user to upload an image
file = st.file_uploader("Please upload an image file", type=["jpg", "png"])

# Check if the user uploaded a file
if file is None:
    st.text("Please upload an image file.")
else:
    # Load the image
    image_for_testing = Image.open(file)

    # Preprocess the image for prediction
    test_image = keras_image.img_to_array(image_for_testing)
    test_image = keras_image.smart_resize(test_image, (150, 150))  # Resize the image
    test_image = test_image / 255.0  # Normalize the image
    test_image = np.expand_dims(test_image, axis=0)  # Expand dimensions for the model

    # Make predictions
    result = (model.predict(test_image) > 0.5).astype("int32")

    # Display the uploaded image
    st.image(image_for_testing, caption="Uploaded Image", use_column_width=True)

    # Display prediction result
    prediction = categories[int(result[0][0])]
    st.write(f"This image most likely belongs to: **{prediction}**.")

    # Optionally display the prediction with matplotlib
    plt.imshow(image_for_testing)
    plt.title(f"Predicted: {prediction}")
    plt.axis('off')  # Hide axes
    plt.show()
