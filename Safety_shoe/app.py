import streamlit as st
import pandas as pd
import gdown
import os

# ✅ Move set_page_config() to the first line
st.set_page_config(page_title="Safety Shoe Status", page_icon="👞", layout="centered")

# Google Drive Shareable Link
drive_link = "https://docs.google.com/spreadsheets/d/1MBimD7Tx8H18DFbggiM-lu5C5RR4mTWC/edit?usp=sharing"

# Extract File ID from the link
file_id = drive_link.split("/d/")[1].split("/")[0]

# Generate a direct download link
download_url = f"https://drive.google.com/uc?id={file_id}"

# Download the Excel file
file_path = "safety_shoes.xlsx"
gdown.download(download_url, file_path, quiet=False)

# Load the Excel file
@st.cache_data
def load_data():
    return pd.read_excel(file_path, sheet_name="Raw")

df = load_data()

# Remove Status and Comment columns
df = df.drop(columns=["Status", "Comment"], errors="ignore")

# Custom CSS
st.markdown("""
    <style>
        .title {
            font-size: 30px;
            font-weight: bold;
            color: #004466;
            text-align: center;
        }
        .search-box {
            text-align: center;
        }
        .dataframe {
            border-radius: 10px;
            overflow: hidden;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<p class="title">Safety Shoe Status Checker</p>', unsafe_allow_html=True)

# Search box
st.markdown('<p class="search-box">Enter Employee ID to Check Status:</p>', unsafe_allow_html=True)
employee_id = st.text_input("Employee ID", "")

# Filter and display result
if employee_id:
    filtered_data = df[df["ID"].astype(str) == employee_id]
    if not filtered_data.empty:
        st.dataframe(filtered_data.style.set_properties(**{'background-color': '#f5f5f5', 
                                                           'border': '1px solid #ddd', 
                                                           'border-radius': '5px'}))
    else:
        st.warning("No record found. Please check the Employee ID.")

# Cleanup: Remove the file after loading
if os.path.exists(file_path):
    os.remove(file_path)
