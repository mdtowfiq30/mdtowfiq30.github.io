import streamlit as st
import pandas as pd
import requests
from PIL import Image
from io import BytesIO
from datetime import datetime

# ✅ First Streamlit command
st.set_page_config(page_title="Safety Violation Viewer", layout="wide")

# ✅ Custom CSS for styling
st.markdown("""
    <style>
    .title-container {
        text-align: center;
        margin-bottom: 2rem;
    }
    .search-container {
        display: flex;
        justify-content: center;
        margin-bottom: 2rem;
    }
    .search-box input {
        max-width: 300px !important;
        text-align: center;
    }
    .card {
        background-color: #f9f9f9;
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.06);
        margin: 0.5rem;
        text-align: center;
    }
    .card-title {
        font-weight: 600;
        font-size: 1.1rem;
        color: #333333;
        margin-bottom: 0.5rem;
    }
    .card-caption {
        font-size: 0.9rem;
        color: #666666;
        margin-top: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# ✅ Title
st.markdown('<div class="title-container"><h1>🚨 Safety Violation Viewer</h1></div>', unsafe_allow_html=True)

# ✅ Input field
st.markdown('<div class="search-container">', unsafe_allow_html=True)
emp_id = st.text_input("Enter Employee ID", key="search_box", label_visibility="collapsed", placeholder="e.g., 1234")
st.markdown('</div>', unsafe_allow_html=True)

# ✅ Load Google Sheet data
sheet_url = "https://docs.google.com/spreadsheets/d/14fR8BCvYm6HzOjQ8bzZ7sMNa8SPESkjO9NzVABgwZxw/gviz/tq?tqx=out:csv&sheet=Raw"
df = pd.read_csv(sheet_url)

# ✅ Convert date column to datetime
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# ✅ Search functionality
if emp_id:
    filtered_df = df[df['Emp ID'].astype(str) == emp_id]

    if not filtered_df.empty:
        # Show Name and Department
        name = filtered_df['Name'].iloc[0]
        dept = filtered_df['Department'].iloc[0]

        st.markdown(f"**👷 Name:** {name}")
        st.markdown(f"**🏢 Department:** {dept}")

        # Sort by date
        filtered_df = filtered_df.sort_values(by='Date')

        # Horizontal image cards
        st.markdown("### 📸 Safety Violation Records")
        cols = st.columns(len(filtered_df))  # Dynamically create columns

        for idx, row in enumerate(filtered_df.itertuples()):
            image_url = getattr(row, 'Upload Image')
            date_obj = getattr(row, 'Date')
            description = getattr(row, 'Description of Violation')

            # Format date
            formatted_date = date_obj.strftime("%d/%m/%Y") if pd.notnull(date_obj) else "No Date"

            try:
                # Convert shareable URL to direct download link
                if "drive.google.com" in image_url:
                    file_id = image_url.split("id=")[-1] if "id=" in image_url else image_url.split("/")[-2]
                    direct_url = f"https://drive.google.com/uc?export=download&id={file_id}"
                else:
                    direct_url = image_url

                response = requests.get(direct_url)
                img = Image.open(BytesIO(response.content))

                with cols[idx]:
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.image(img, caption=None, use_container_width=True)
                    st.markdown(f"<div class='card-title'>{formatted_date}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='card-caption'>{description}</div>", unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

            except Exception as e:
                with cols[idx]:
                    st.error(f"❌ Error loading image for date {formatted_date}: {e}")
    else:
        st.warning("No records found for this Employee ID.")
