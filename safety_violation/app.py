import streamlit as st
import pandas as pd
import requests
from PIL import Image
from io import BytesIO
from datetime import datetime

# Must be the first Streamlit command
st.set_page_config(page_title="Safety Violation Viewer", layout="wide")

# Google Sheet link (published CSV format)
sheet_url = "https://docs.google.com/spreadsheets/d/14fR8BCvYm6HzOjQ8bzZ7sMNa8SPESkjO9NzVABgwZxw/gviz/tq?tqx=out:csv&sheet=Raw"

# Load and clean the data
@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Emp ID', 'Date'])
    return df

df = load_data(sheet_url)

# App Title
st.markdown("<h1 style='text-align: center; color: #2E86C1;'>Safety Violation Viewer</h1>", unsafe_allow_html=True)
st.markdown("---")

# Search box
st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
emp_id_input = st.text_input("Enter Employee ID", max_chars=20, key="search_input", label_visibility="collapsed")
st.markdown("</div>", unsafe_allow_html=True)

# Filter and display results
if emp_id_input:
    filtered_df = df[df["Emp ID"].astype(str).str.strip() == emp_id_input.strip()]

    if not filtered_df.empty:
        name = filtered_df["Name"].iloc[0]
        dept = filtered_df["Department"].iloc[0]

        st.markdown(f"<h4 style='text-align: center;'>👷 Name: {name} | 🏢 Department: {dept}</h4>", unsafe_allow_html=True)
        st.markdown("---")

        # Sort by date
        filtered_df = filtered_df.sort_values("Date")

        # Display images in horizontal layout
        image_cols = st.columns(len(filtered_df))

        for col, (_, row) in zip(image_cols, filtered_df.iterrows()):
            try:
                image_url = row["Upload Image"]
                # Convert shared Google Drive URL to direct link
                if "drive.google.com" in image_url:
                    if "id=" in image_url:
                        file_id = image_url.split("id=")[-1]
                    elif "/d/" in image_url:
                        file_id = image_url.split("/d/")[1].split("/")[0]
                    else:
                        file_id = None
                    if file_id:
                        direct_url = f"https://drive.google.com/uc?export=download&id={file_id}"
                        response = requests.get(direct_url)
                        image = Image.open(BytesIO(response.content))

                        formatted_date = row['Date'].strftime('%d/%m/%Y')
                        description = row["Description of Violation"]

                        with col:
                            st.image(image, caption=description, use_container_width=True)
                            st.markdown(f"<div style='text-align: center; font-weight: bold;'>{formatted_date}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.warning(f"⚠️ Could not load image for {row['Date'].strftime('%d/%m/%Y')}")
    else:
        st.error("No data found for this Employee ID.")
