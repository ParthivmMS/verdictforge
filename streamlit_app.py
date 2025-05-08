import streamlit as st
import requests

# API details
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {
    "Authorization": f"Bearer {st.secrets['HF_API_KEY']}"
}

# Function to call the Hugging Face API
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        st.error(f"Error {response.status_code}: {response.text}")
        return None
    return response.json()

# Streamlit App UI
st.title("VerdictForge - Legal Judgment Summarizer")
st.markdown("Paste a legal judgment below to generate a short, clear summary.")

# User Input
input_text = st.text_area("Paste the full judgment here")

if st.button("Generate Summary"):
    if input_text.strip() == "":
        st.warning("Please paste a judgment first.")
    else:
        # Limit the text to around 2000 characters for better performance
        trimmed_input = input_text[:2000]
        # Better prompt
        prompt = f"Summarize this legal judgment in 3-4 lines, focusing on key facts, legal issues, and the final decision:\n\n{trimmed_input}"
        
        with st.spinner("Generating summary, please wait..."):
            result = query({"inputs": prompt})
        
        if result:
            try:
                summary = result[0]["summary_text"]
                st.success("Summary Generated:")
                st.write(summary)
            except Exception as e:
                st.error("Unexpected response format. Please try again.")
