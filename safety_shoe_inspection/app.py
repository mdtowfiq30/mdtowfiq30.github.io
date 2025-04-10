import streamlit as st
import pandas as pd
import requests
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="Employee Image Viewer", layout="wide")
st.title("👷 Safety Shoe Inspection Viewer")

# Google Sheet CSV export URL
sheet_url = "https://docs.google.com/spreadsheets/d/1sgvvLhJHGjYiMRLsXmF-C6Hkwv7eSfO9rdxURlOFpMk/gviz/tq?tqx=out:csv&sheet=Raw"

# Custom Styling
st.markdown("""
    <style>
        /* Title styling */
        h1 {
            color: #2980b9;
            text-align: center;
            font-family: 'Arial', sans-serif;
            font-size: 3em;
            font-weight: bold;
        }

        /* Input styling */
        .stTextInput input {
            font-size: 18px;
            padding: 10px;
            border-radius: 8px;
            border: 2px solid #3498db;
        }

        /* Button styling */
        .stButton button {
            font-size: 18px;
            padding: 10px 20px;
            background-color: #3498db;
            color: white;
            border-radius: 8px;
            border: none;
            cursor: pointer;
            transition: 0.3s;
        }
        .stButton button:hover {
            background-color: #2980b9;
        }

        /* Image container styling */
        .image-container {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            justify-items: center;
            margin-top: 20px;
        }

        /* Image hover effect */
        .image-container img {
            border-radius: 15px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s;
        }

        .image-container img:hover {
            transform: scale(1.05);
        }

        /* Warning and Error message styling */
        .stWarning, .stError {
            font-size: 18px;
            color: #e74c3c;
        }

        /* Description Styling */
        .description {
            font-size: 16px;
            color: #2c3e50;
            text-align: center;
        }

    </style>
""", unsafe_allow_html=True)

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

    st.markdown("<h3 class='description'>Images sorted by Date</h3>", unsafe_allow_html=True)

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
                    st.image(img, caption=f"{date}", use_container_width=True)
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
