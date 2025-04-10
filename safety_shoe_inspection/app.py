import streamlit as st
import pandas as pd
import gdown
from PIL import Image
import requests
from io import BytesIO

# Set Page Config
st.set_page_config(page_title="Employee Safety Shoe Status", page_icon="👞", layout="centered")

# Load Data from Google Drive
url = "https://docs.google.com/spreadsheets/d/1sgvvLhJHGjYiMRLsXmF-C6Hkwv7eSfO9rdxURlOFpMk/export?format=xlsx"
output = "safety_shoe.xlsx"
gdown.download(url, output, quiet=False)

# Read Excel file
df = pd.read_excel(output, sheet_name="Raw")

# Convert the 'Date' column to datetime format for easier sorting
df['Date'] = pd.to_datetime(df['Date'])

# Function to get the correct image link from Google Drive
def get_google_drive_image_link(url):
    # This converts the Google Drive link to a direct image URL
    file_id = url.split('/')[-2]
    return f"https://drive.google.com/uc?export=view&id={file_id}"

# Title
st.markdown("<h1>👞 Employee Safety Shoe Images Viewer</h1>", unsafe_allow_html=True)

# Employee ID search input
emp_id = st.text_input("Enter Employee ID to search:")

if emp_id:
    # Filter the DataFrame by Employee ID
    filtered_df = df[df['Emp ID'].astype(str) == emp_id]

    if not filtered_df.empty:
        st.write(f"### Showing Data for Employee ID: {emp_id}")

        # Display the employee's info (Current Status, Department, etc.)
        st.write(f"**Department:** {filtered_df['Department'].iloc[0]}")
        st.write(f"**Current Status:** {filtered_df['Current Status'].iloc[0]}")
        
        # Sort by Date (from previous to current)
        filtered_df = filtered_df.sort_values(by='Date', ascending=True)

        # Display images horizontally
        st.markdown("<h3>Images</h3>", unsafe_allow_html=True)
        
        # Create a horizontal layout for displaying images
        cols = st.columns(len(filtered_df))

        # Loop through each image and display it in the columns
        for i, (index, row) in enumerate(filtered_df.iterrows()):
            img_url = get_google_drive_image_link(row['Upload image'])  # Get direct image URL
            try:
                response = requests.get(img_url)
                img = Image.open(BytesIO(response.content))
                cols[i].image(img, caption=f"Date: {row['Date'].date()}", use_column_width=True)
            except Exception as e:
                cols[i].error(f"❌ Error loading image: {e}")
    else:
        st.warning("No data found for the given Employee ID.")
