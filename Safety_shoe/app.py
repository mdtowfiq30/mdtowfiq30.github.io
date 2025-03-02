import streamlit as st
import pandas as pd

# Google Sheet ID and Sheet Name
sheet_id = "1MBimD7Tx8H18DFbggiM-lu5C5RR4mTWC"
sheet_name = "Raw"

# Construct the CSV export URL
csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

# Function to load data
@st.cache_data
def load_data():
    return pd.read_csv(csv_url)

df = load_data()

# Remove Status and Comment columns
df = df.drop(columns=["Status", "Comment"], errors="ignore")

# Streamlit UI
st.set_page_config(page_title="Safety Shoe Status", page_icon="👞", layout="centered")

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
