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

# Apply Custom CSS Styling for responsiveness
st.markdown(
    """
    <style>
    /* Title Styling */
    h1 {
        text-align: center;
        color: #2c3e50;
        font-size: 2rem;
    }
    
    /* Subtitle Styling */
    h3 {
        text-align: center;
        color: #2c3e50;
        font-size: 1.5rem;
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
    }

    /* Make the title responsive */
    @media screen and (max-width: 768px) {
        h1 {
            font-size: 1.5rem; /* Reduced font size for smaller screens */
        }
        h3 {
            font-size: 1.2rem;
        }
        .stTextInput > div > div > input {
            font-size: 16px;
        }
    }
    
    /* Ensure table uses full width */
    .stDataFrame {
        width: 100% !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# Title
st.markdown("<h1>👞 Safety Shoe Status Checker</h1>", unsafe_allow_html=True)

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
            # Display results with centered title
            st.markdown("<h3>Employee Safety Shoe Information</h3>", unsafe_allow_html=True)

            # Display the table without horizontal scroll and adjust width to container size
            st.dataframe(filtered_df.style.set_properties(**{'text-align': 'center'}), height=400, use_container_width=True)
        else:
            st.error("❌ Employee ID not found! Please check and try again.")
    else:
        st.warning("⚠️ Please enter an Employee ID before submitting.")
