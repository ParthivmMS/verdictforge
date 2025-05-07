import streamlit as st
import requests

st.set_page_config(page_title="Judgment Summarizer", layout="centered")
st.title("VerdictForge: Legal Judgment Summarizer")
st.write("Upload or paste a legal judgment and get a crisp summary with reasoning.")

# Hugging Face API info
API_URL = "https://api-inference.huggingface.co/models/sjvasquez/legal-longformer-base-4096-finetuned-legal-summarization"
headers = {"Authorization": f"Bearer {st.secrets['HF_API_KEY']}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        st.error(f"API Error {response.status_code}: {response.text}")
        return None
    return response.json()

# Input area
input_text = st.text_area("Paste the full judgment here", height=300)

# Submit button
if st.button("Generate Summary"):
    if not input_text.strip():
        st.warning("Please enter a legal judgment.")
    else:
        with st.spinner("Summarizing..."):
            output = query({"inputs": input_text})
            if output:
                try:
                    summary = output[0]['summary_text']
                    st.success("Summary:")
                    st.write(summary)
                except (KeyError, IndexError, TypeError):
                    st.error("Unexpected API response format.")

