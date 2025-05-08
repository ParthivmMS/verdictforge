import streamlit as st
import requests

# Hugging Face API URL for summarization model
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"

# Header with API Key from Streamlit secrets
headers = {
    "Authorization": f"Bearer {st.secrets['HF_API_KEY']}"
}

# Function to call Hugging Face model
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        st.error(f"Error {response.status_code}: {response.text}")
        return None
    return response.json()

# Streamlit UI
st.title("VerdictForge: Legal Judgment Summarizer")
st.markdown("**Paste a full legal judgment below.** You’ll get a crisp, 3-4 line summary.")

input_text = st.text_area("Paste the legal judgment here")

if st.button("Summarize"):
    if not input_text.strip():
        st.warning("Please enter a judgment first.")
    else:
        with st.spinner("Generating summary..."):
            prompt = f"Summarize the following legal case in 3-4 lines focusing on facts, issues, and final decision:\n\n{input_text}"
            result = query({"inputs": prompt})
            if result and isinstance(result, list):
                try:
                    summary = result[0]["summary_text"]
                    st.success("Summary:")
                    st.write(summary)
                except Exception as e:
                    st.error(f"Unexpected format: {e}")
            else:
                st.error("No summary returned. The model might be overloaded or input too long.")
