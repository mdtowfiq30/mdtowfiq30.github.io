import streamlit as st
import pandas as pd
import requests
from PIL import Image
from io import BytesIO

# --- Title ---
st.title("🔍 Safety Violation ")

# --- Load Data ---
sheet_url = "https://docs.google.com/spreadsheets/d/14fR8BCvYm6HzOjQ8bzZ7sMNa8SPESkjO9NzVABgwZxw/gviz/tq?tqx=out:csv&sheet=Raw"
df = pd.read_csv(sheet_url)

# --- Clean Data ---
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df = df.dropna(subset=['Emp ID', 'Date', 'Upload Image'])

# --- Sidebar ---
emp_id = st.text_input("Enter Employee ID to view safety violations:")

if emp_id:
    filtered_df = df[df['Emp ID'].astype(str) == emp_id]

    if not filtered_df.empty:
        name = filtered_df['Name'].iloc[0]
        dept = filtered_df['Department'].iloc[0]

        st.markdown(f"### 👤 {name}  \n🏢 Department: {dept}")

        sorted_df = filtered_df.sort_values('Date')

        st.markdown("### 📸 Violation Images")

        # Horizontal layout for images
        for _, row in sorted_df.iterrows():
            img_url = row['Upload Image']
            date = row['Date'].strftime('%Y-%m-%d')
            caption = row['Description of Violation']

            # Convert to direct download link
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

                with st.container():
                    st.image(img, caption=f"📅 {date} — {caption}", use_container_width=True)
            except Exception as e:
                st.error(f"❌ Error loading image for {date}: {e}")
    else:
        st.warning("No data found for this Employee ID.")
