import streamlit as st
import pandas as pd
import gdown
from PIL import Image
import requests
from io import BytesIO

st.set_page_config(page_title="Safety Shoe Inspection", page_icon="🛠️", layout="wide")

# Download the Excel file from Google Sheets
file_url = "https://docs.google.com/spreadsheets/d/1sgvvLhJHGjYiMRLsXmF-C6Hkwv7eSfO9rdxURlOFpMk/export?format=xlsx"
output_file = "safety_data.xlsx"
gdown.download(file_url, output_file, quiet=True)

# Read Excel file
df = pd.read_excel(output_file, sheet_name="Raw")

# Clean column names just in case there are spaces or hidden characters
df.columns = df.columns.str.strip()

# Title
st.title("🛠️ Safety Shoe Inspection Viewer")
st.markdown("Search by Employee ID to see their safety shoe inspection history with images, sorted by date.")

# Input: Search by Employee ID
emp_id = st.text_input("Enter Employee ID")

if emp_id:
    filtered = df[df["Emp ID"].astype(str) == emp_id.strip()]
    
    if not filtered.empty:
        st.subheader("🧾 Employee Info")
        st.write(f"**Employee ID:** {filtered['Emp ID'].iloc[0]}")
        st.write(f"**Department:** {filtered['Department'].iloc[0]}")
        st.write(f"**Current Status:** {filtered['Current Status'].iloc[0]}")

        st.subheader("🖼️ Uploaded Images (Sorted by Date)")
        filtered = filtered.sort_values(by="Date")
        
        # Display images in horizontal layout
        images = []
        for _, row in filtered.iterrows():
            image_id = row["Upload image"].split("id=")[-1]
            image_url = f"https://drive.google.com/uc?id={image_id}"
            try:
                response = requests.get(image_url)
                img = Image.open(BytesIO(response.content))
                images.append((img, row["Date"].strftime("%Y-%m-%d")))
            except Exception as e:
                st.error(f"Error loading image for date {row['Date']}: {e}")

        # Show in horizontal columns
        cols = st.columns(len(images) if images else 1)
        for col, (img, date) in zip(cols, images):
            col.image(img, caption=date, use_column_width=True)

    else:
        st.warning("No record found for this Employee ID.")
