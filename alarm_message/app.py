import streamlit as st
import pywhatkit

st.title("Fire Alarm Alert System")

# Get user input for the alarm location and message
location = st.selectbox("Select Alarm Location", ["Section A", "Section B", "Section C"])
message = f"🔥 Fire Alert: Fire detected in {location}!"

# List of phone numbers to send the alert to
phone_numbers = ["+8801725692402"]  # Add numbers here

if st.button("Send Message"):
    for number in phone_numbers:
        pywhatkit.sendwhatmsg_instantly(number, message)
    st.success("Message sent successfully!")
