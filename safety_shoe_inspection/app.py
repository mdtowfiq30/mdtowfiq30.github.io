import streamlit as st
import pandas as pd
import requests
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="Employee Image Viewer", layout="wide")
st.title("👷 Safety Shoe Inspection Viewer")

# Google Sheet CSV export URL
sheet_url = "https://docs.google.com/spreadsheets/d/1sgvvLhJHGjYiMRLsXmF-C6Hkwv7eSfO9rdxURlOFpMk/gviz/tq?tqx=out:csv&sheet=Raw"

@st.cache_data(ttl=600)
def load_data(url):
    df = pd.read_csv(url)
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    return df

def convert_to_direct_download(url):
    if pd.isna(url):
        return None
    if "drive.google.com" in url:
        if "open?id=" in url:
            file_id = url.split("open?id=")[-1]
        elif "/file/d/" in url:
            file_id = url.split("/file/d/")[1].split("/")[0]
        else:
            return None
        return f"https://drive.google.com/uc?export=download&id={file_id}"
    return url

def display_images_by_id(df, emp_id):
    filtered = df[df['Emp ID'].astype(str) == str(emp_id)].sort_values(by="Date")

    if filtered.empty:
        st.warning("No data found for the given Employee ID.")
        return

    st.write(f"**Department:** {filtered['Department'].iloc[0]}")
    st.write(f"**Total Entries:** {len(filtered)}")

    image_columns = st.columns(min(len(filtered), 5))  # up to 5 images in a row

    image_found = False
    for i, (index, row) in enumerate(filtered.iterrows()):
        img_url = convert_to_direct_download(row['Upload image'])
        date = row['Date'].date() if not pd.isna(row['Date']) else "Unknown"

        if img_url:
            try:
                response = requests.get(img_url)
                img = Image.open(BytesIO(response.content))
                with image_columns[i % len(image_columns)]:
                    st.image(img, caption=f"{date}", use_column_width=True)
                    image_found = True
            except Exception as e:
                st.error(f"❌ Error loading image for date {date}: {e}")
        else:
            st.warning(f"⚠️ Invalid image link for date {date}.")

    if not image_found:
        st.warning("No valid images found for this employee.")

# Load data
df = load_data(sheet_url)

# User input
emp_id = st.text_input("🔍 Enter Employee ID to search:")

if emp_id:
    display_images_by_id(df, emp_id)
