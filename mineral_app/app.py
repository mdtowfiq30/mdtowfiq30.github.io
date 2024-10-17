from tensorflow.keras.utils import load_img, img_to_array
import numpy as np
import streamlit as st
import tensorflow as tf
import os
import gdown

# Define categories and their descriptions
Categories = {
    0: ("Biotite", "Biotite is a common phyllosilicate mineral within the mica group, commonly found in igneous and metamorphic rocks."),
    1: ("Bornite", "Bornite is an important copper ore mineral found in copper deposits. It has a brown to copper-red color on fresh surfaces."),
    2: ("Chrysocolla", "Chrysocolla is a hydrated copper phyllosilicate mineral with a cyan (blue-green) color, often associated with copper mining."),
    3: ("Malachite", "Malachite is a green copper carbonate hydroxide mineral, often found in association with copper deposits."),
    4: ("Muscovite", "Muscovite is a silicate mineral in the mica group, typically found in metamorphic rocks. It has a pale color and is highly reflective."),
    5: ("Quartz", "Quartz is one of the most common minerals in the Earth's crust. It comes in many forms, but is best known for its glass-like clarity.")
}

@st.cache_resource  # Efficient caching for loading models
def load_model():
    model_path = 'model_l2_regularization.hdf5'
    
    # Check if the model already exists locally
    if not os.path.exists(model_path):
        st.write("Downloading model...")  # User feedback
        # Download the model from Google Drive
        gdown.download('https://drive.google.com/uc?id=1UnzJgO0T__lpwlGqax7t7v2lLx35bL4N', model_path, quiet=False)
    
    # Load the model
    model = tf.keras.models.load_model(model_path)
    return model

with st.spinner('Loading model...'):
    model = load_model()

# App title
st.write("""
         # Mineral Classification
         """)

# File uploader for the user to upload an image
file = st.file_uploader("Please upload a mineral image", type=["jpg", "png", "jpeg"])

# Check if the user uploaded a file
if file is None:
    st.text("Please upload an image file.")
else:
    # Load the image
    img = load_img(file, target_size=(150, 150))

    # Display the uploaded image
    st.image(img, caption="Uploaded Image", use_column_width=True)

    # Preprocess the image for prediction
    x = img_to_array(img)
    x /= 255.0
    x = np.expand_dims(x, axis=0)
    images = np.vstack([x])
    # Predict the class of the image
    classes = model.predict(images)
    classification = np.argmax(classes)

    # Display the prediction result and description
    mineral_name, description = Categories[classification]
    st.write(f"### This image most likely belongs to: {mineral_name}")
    st.write(description)
