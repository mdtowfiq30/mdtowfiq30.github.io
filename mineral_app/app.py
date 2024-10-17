import streamlit as st
import tensorflow as tf
import os
import gdown
import numpy as np
from tensorflow.keras.utils import load_img, img_to_array
from PIL import Image
import matplotlib.pyplot as plt

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
    .note-section {
        font-size: 16px;
        color: #E74C3C;
        text-align: center;
        margin-top: 10px;
    }
    .result-box {
        font-size: 24px;
        font-weight: bold;
        color: #1ABC9C;
        text-align: center;
        margin-top: 30px;
    }
    .description-box {
        font-size: 16px;
        color: #34495E;
        text-align: center;
        margin-top: 10px;
        padding: 10px;
        border: 1px solid #D5DBDB;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True
)

# App title in the center
st.markdown('<div class="main-title">Mineral Classification</div>', unsafe_allow_html=True)

# Note to indicate supported minerals
st.markdown(
    '<div class="note-section">Note: This model can only classify the following minerals: Biotite, Bornite, Chrysocolla, Malachite, Muscovite, Quartz.</div>', 
    unsafe_allow_html=True
)

# File uploader section on the main page
st.markdown('<div class="upload-section">Upload a mineral image (jpg, png, jpeg):</div>', unsafe_allow_html=True)
file = st.file_uploader("", type=["jpg", "png", "jpeg"])

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

    # Get the prediction result and description
    mineral_name, description = Categories[classification]

    # Display the prediction result and description
    st.markdown(f'<div class="result-box">This image most likely belongs to: **{mineral_name}**.</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="description-box">{description}</div>', unsafe_allow_html=True)

    # Display the uploaded image with the prediction as the title using matplotlib
    plt.imshow(Image.open(file))
    plt.title(f"Predicted: {mineral_name}")
    plt.axis('off')  # Hide axes
    st.pyplot(plt)
