import streamlit as st
import pandas as pd
import gdown
from PIL import Image
import requests
from io import BytesIO

# Set Page Config
st.set_page_config(page_title="Safety Shoe Image Viewer", page_icon="👞", layout="centered")

# Load Data from Google Drive
url = "https://docs.google.com/spreadsheets/d/1sgvvLhJHGjYiMRLsXmF-C6Hkwv7eSfO9rdxURlOFpMk/export?format=xlsx"
output = "safety_shoe.xlsx"
gdown.download(url, output, quiet=False)

# Read Excel file
df = pd.read_excel(output, sheet_name="Raw")

# Apply Custom CSS Styling for responsiveness
st.markdown(
    """
    <style>
    /* Title Styling */
    h1 {
        text-align: center;
        color: #2c3e50;
        font-size: 2rem;
        font-weight: bold;
    }
    
    /* Subtitle Styling */
    h3 {
        text-align: center;
        color: #2c3e50;
        font-size: 1.5rem;
    }

    /* Styling for image gallery */
    .image-gallery {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: 20px;
        justify-items: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title
st.markdown("<h1>👞 Safety Shoe Image Viewer by Date</h1>", unsafe_allow_html=True)

# Date Selection
st.write("### Filter by Date:")
start_date = st.date_input("Start Date", df['Date'].min())
end_date = st.date_input("End Date", df['Date'].max())

# Filter Data by Date Range
filtered_df = df[(df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))]

# If data is available after filtering
if not filtered_df.empty:
    st.write(f"### Showing Images from {start_date} to {end_date}")

    # Create a grid layout for displaying images
    st.markdown("<h3>Safety Shoe Images</h3>", unsafe_allow_html=True)

    # Loop through the filtered data to show images
    for index, row in filtered_df.iterrows():
        img_url = row['Upload image']  # Assuming 'Upload image' has the image URL
        try:
            response = requests.get(img_url)
            img = Image.open(BytesIO(response.content))
            st.image(img, caption=f"Employee ID: {row['EMP ID']} | Department: {row['Department']} | Status: {row['Current Status']}", use_column_width=True)
        except Exception as e:
            st.error(f"❌ Error loading image: {e}")
else:
    st.warning("⚠️ No data found for the selected date range.")
