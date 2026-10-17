import streamlit as st

# Configure the page title
st.set_page_config(page_title="Claude Parser App", layout="centered")

# Set up simple text on the screen
st.title("📊 Claude Ingestion Engine")
st.write("Welcome! This app will help you upload and parse spreadsheets using Claude.")

# Create a file upload box
uploaded_file = st.file_uploader("Choose an Excel or CSV file", type=["xlsx", "csv"])

if uploaded_file is not None:
    st.success("File uploaded successfully! Next, we will connect our data parsing engine.")
