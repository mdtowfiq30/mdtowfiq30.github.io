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

# Apply Custom CSS Styling
st.markdown(
    """
    <style>
    /* Title Styling */
    .title {
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 20px;
    }
    
    /* Input Box Styling */
    .stTextInput > div > div > input {
        font-size: 18px;
        padding: 10px;
    }

    /* Submit Button */
    .stButton > button {
        font-size: 18px;
        padding: 10px 20px;
        background-color: #3498db;
        color: white;
        border-radius: 8px;
        border: none;
        cursor: pointer;
        transition: 0.3s;
    }
    .stButton > button:hover {
        background-color: #2980b9;
    }

    /* Data Display Styling */
    .data-container {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
        margin-top: 20px;
        font-size: 18px;
        width: 100%;
        text-align: left;
        overflow-x: auto;
    }

    /* Center the entire output */
    .center-output {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        flex-direction: column;
    }

    /* Adjust table display to prevent horizontal scrolling */
    .table-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: flex-start;
    }
    .table-item {
        margin-right: 20px;
        margin-bottom: 10px;
        background-color: white;
        padding: 10px;
        border-radius: 8px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        min-width: 200px;
        max-width: 250px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title
st.markdown('<p class="title">👞 Safety Shoe Status Checker</p>', unsafe_allow_html=True)

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

        if not filtered_df.empty:
            st.markdown('<div class="center-output">', unsafe_allow_html=True)
            st.markdown('<div class="data-container">', unsafe_allow_html=True)
            
            # Create a container to hold all rows horizontally
            st.markdown('<div class="table-container">', unsafe_allow_html=True)

            for index, row in filtered_df.iterrows():
                st.markdown('<div class="table-item">', unsafe_allow_html=True)
                for col in filtered_df.columns:
                    st.markdown(f"<b>{col}:</b> {row[col]}<br>", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error("❌ Employee ID not found! Please check and try again.")
    else:
        st.warning("⚠️ Please enter an Employee ID before submitting.")
