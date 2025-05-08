import streamlit as st
import requests

# Hugging Face Model API URL
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"

# Get token securely from Streamlit secrets
headers = {
    "Authorization": f"Bearer {st.secrets['HF_API_KEY']}"
}

# Query function
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        st.error(f"Error {response.status_code}: {response.text}")
        return None
    return response.json()

# UI
st.title("VerdictForge – Legal Judgment Summarizer")
st.markdown("Paste a legal judgment below to generate a summary.")

input_text = st.text_area("Paste the judgment here")

if st.button("Generate Summary"):
    if not input_text.strip():
        st.warning("Please paste a legal judgment first.")
    else:
        st.info("Generating summary...")
        result = query({"inputs": input_text})
        if result:
            try:
                st.success("Summary:")
                st.write(result[0]['summary_text'])
            except:
                st.error("The model returned an unexpected format.")
