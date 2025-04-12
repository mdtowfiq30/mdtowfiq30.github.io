import streamlit as st
import pandas as pd
import requests
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="Safety Violation Viewer", layout="wide")
st.title("🚨 Safety Violation Viewer")

# Load data
sheet_url = "https://docs.google.com/spreadsheets/d/14fR8BCvYm6HzOjQ8bzZ7sMNa8SPESkjO9NzVABgwZxw/gviz/tq?tqx=out:csv&sheet=Raw"
df = pd.read_csv(sheet_url)

# Clean & convert date
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df = df.dropna(subset=['Emp ID', 'Date', 'Upload Image'])

# Sidebar search
emp_id = st.text_input("🔍 Enter Employee ID to view safety violations:")

if emp_id:
    filtered_df = df[df['Emp ID'].astype(str) == emp_id]

    if not filtered_df.empty:
        name = filtered_df['Name'].iloc[0]
        dept = filtered_df['Department'].iloc[0]

        st.markdown(f"### 👤 Name: `{name}`  \n🏢 Department: `{dept}`")
        st.markdown("### 🖼 Violation History")

        # Sort by date
        sorted_df = filtered_df.sort_values('Date')

        # Display in horizontal columns
        cols = st.columns(len(sorted_df))

        for col, (_, row) in zip(cols, sorted_df.iterrows()):
            img_url = row['Upload Image']
            date_str = row['Date'].strftime('%d/%m/%Y')
            caption = row['Description of Violation']

            # Convert to direct link
            if "drive.google.com" in img_url:
                if "id=" in img_url:
                    file_id = img_url.split("id=")[-1]
                elif "/file/d/" in img_url:
                    file_id = img_url.split("/file/d/")[1].split("/")[0]
                else:
                    file_id = None

                if file_id:
                    direct_url = f"https://drive.google.com/uc?export=download&id={file_id}"
                else:
                    direct_url = img_url
            else:
                direct_url = img_url

            try:
                response = requests.get(direct_url)
                img = Image.open(BytesIO(response.content))

                with col:
                    st.markdown(f"**📅 {date_str}**", unsafe_allow_html=True)
                    st.image(img, use_container_width=True)
                    st.caption(f"📝 {caption}")
            except Exception as e:
                col.error(f"❌ Error loading image: {e}")
    else:
        st.warning("No data found for this Employee ID.")
