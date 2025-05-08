import streamlit as st
import requests

# API URL for FalconAI summarization model
API_URL = "https://api-inference.huggingface.co/models/falconsai/text_summarization"

# Load Hugging Face API Key from secrets
headers = {
    "Authorization": f"Bearer {st.secrets['HF_API_KEY']}"
}

# Function to call the Hugging Face summarization model
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        st.error(f"Error {response.status_code}: {response.text}")
        return None
    return response.json()

# Streamlit UI
st.title("VerdictForge - Legal Judgment Summarizer")
st.markdown("**Upload or paste a full legal judgment below and get a crisp summary.**")

input_text = st.text_area("Paste the full legal judgment here")

if st.button("Generate Summary"):
    if input_text.strip() == "":
        st.warning("Please paste a legal judgment first.")
    else:
        st.info("Generating summary. Please wait...")
        prompt = f"Summarize this legal judgment in 3-4 lines, focusing on key facts, legal issues, and the final decision:\n\n{input_text}"
        result = query({"inputs": prompt})
        if result:
            try:
                summary = result[0]["summary_text"]
                st.success("Summary Generated:")
                st.write(summary)
            except:
                st.error("Unexpected response format from Hugging Face model.")
