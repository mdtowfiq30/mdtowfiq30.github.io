import streamlit as st
import pandas as pd
import gdown

# Set Page Config
st.set_page_config(page_title="Safety Shoe Status", page_icon="👞", layout="centered")

# Load Data from Google Drive
url = "https://docs.google.com/spreadsheets/d/1MBimD7Tx8H18DFbggiM-lu5C5RR4mTWC/export?format=xlsx"
output = "safety_shoe_data.xlsx"
gdown.download(url, output, quiet=False)

# Read Excel file
df = pd.read_excel(output, sheet_name="Raw")

# Drop "Status" & "Comment" columns
df = df.drop(columns=["Status", "Comment"])

# Title
st.markdown("<h1 style='text-align: center; color: #2c3e50;'>👞 Safety Shoe Status Checker</h1>", unsafe_allow_html=True)

# Search Box & Submit Button
emp_id = st.text_input("🔍 Enter Employee ID:", "")

# Add some spacing
st.write("")
col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    submit = st.button("🔎 Submit")

# If Submit Button is Clicked
if submit:
    if emp_id:
        filtered_df = df[df["ID"].astype(str) == emp_id]

        # Remove empty rows if any
        filtered_df = filtered_df.dropna(how="all")

        if not filtered_df.empty:
            # Display results inside a styled container with no horizontal scroll
            st.write("### Employee Safety Shoe Information")

            # Ensure the entire table fits on the screen without truncation
            st.dataframe(filtered_df.style.set_properties(**{'text-align': 'center'}), height=400, use_container_width=True)
        else:
            st.error("❌ Employee ID not found! Please check and try again.")
    else:
        st.warning("⚠️ Please enter an Employee ID before submitting.")
