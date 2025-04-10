import streamlit as st
import pandas as pd
import requests
from io import BytesIO
from PIL import Image

# Title
st.title("🔍 Safety Shoe Image Viewer")

# Google Sheet link (CSV export format)
sheet_url = "https://docs.google.com/spreadsheets/d/1sgvvLhJHGjYiMRLsXmF-C6Hkwv7eSfO9rdxURlOFpMk/gviz/tq?tqx=out:csv&sheet=Raw"

# Load data
@st.cache_data
def load_data():
    return pd.read_csv(sheet_url)

df = load_data()

# Convert 'Date' to datetime
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Search box
emp_id = st.text_input("Enter Employee ID to search:")

if emp_id:
    filtered = df[df["Emp ID"].astype(str) == emp_id].sort_values(by="Date")

    if not filtered.empty:
        # Show basic info
        st.write(f"**Employee ID:** {emp_id}")
        st.write(f"**Department:** {filtered['Department'].iloc[0]}")

        # Prepare image gallery
        st.subheader("📅 Safety Shoe Images (Sorted by Date)")

        images = []
        for _, row in filtered.iterrows():
            img_link = str(row["Upload image"])
            if pd.isna(img_link) or "drive.google.com" not in img_link:
                continue  # Skip empty or invalid links

            # Extract Google Drive file ID
            if "id=" in img_link:
                image_id = img_link.split("id=")[-1].split("&")[0]
            elif "/d/" in img_link:
                image_id = img_link.split("/d/")[-1].split("/")[0]
            else:
                st.warning(f"⚠️ Unrecognized image URL format: {img_link}")
                continue

            image_url = f"https://drive.google.com/uc?id={image_id}"

            try:
                response = requests.get(image_url)
                img = Image.open(BytesIO(response.content)).convert("RGB")
                images.append((img, row["Date"].strftime("%Y-%m-%d")))
            except Exception as e:
                st.error(f"❌ Error loading image for date {row['Date']}: {e}")

        if images:
            cols = st.columns(len(images))
            for idx, (img, date) in enumerate(images):
                with cols[idx]:
                    st.image(img, caption=date, use_column_width=True)
        else:
            st.warning("No valid images found for this employee.")
    else:
        st.warning("No data found for this Employee ID.")
