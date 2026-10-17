import streamlit as st
from anthropic import Anthropic
from parser_engine import sanitize_spreadsheet

st.set_page_config(page_title="Claude Parser App", layout="centered")

st.title("📊 Claude Ingestion Engine")
st.write("Upload your spreadsheet to verify row parsing and quantities across Mac, Windows, and iOS.")

# Sidebar for API Key
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Enter Anthropic API Key", type="password")

uploaded_file = st.file_uploader("Choose an Excel or CSV file", type=["xlsx", "csv"])

if uploaded_file is not None:
    file_type = uploaded_file.name.split(".")[-1]
    
    try:
        sanitized_data = sanitize_spreadsheet(uploaded_file, file_type)
        st.success(f"Sanitization layer processed {len(sanitized_data)} rows successfully!")
        
        with st.expander("Preview Cleaned Payload"):
            st.json(sanitized_data)
            
        # Button to trigger Claude
        if st.button("🚀 Send to Claude for AI Parsing"):
            if not api_key:
                st.warning("Please enter your Anthropic API Key in the sidebar.")
            else:
                with st.spinner("Claude is evaluating edge cases..."):
                    client = Anthropic(api_key=api_key)
                    
                    # Instruct Claude exactly how to handle the data
                    system_prompt = (
                        "You are a strict data validation engine. Analyze the raw row data. "
                        "Match quantities accurately. Output your answer strictly as a valid JSON array."
                    )
                    
                    message = client.messages.create(
                        model="claude-3-5-sonnet-latest",
                        max_tokens=4000,
                        system=system_prompt,
                        messages=[{"role": "user", "content": str(sanitized_data)}]
                    )
                    
                    st.subheader("🎯 Claude Validation Output")
                    st.code(message.content[0].text, language="json")
                    
    except Exception as e:
        st.error(f"Error: {e}")
