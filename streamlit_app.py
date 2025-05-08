import streamlit as st
import requests

# Load the API key from secrets
API_URL = "https://api-inference.huggingface.co/models/pszemraj/led-large-book-summary"


headers = {
    "Authorization": f"Bearer {st.secrets['HF_API_KEY']}"
}

# Function to query the model
def query(payload):
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code != 200:
            st.error(f"Error {response.status_code}: {response.text}")
            return None
        return response.json()
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# Streamlit UI
st.title("VerdictForge - Legal Judgment Summarizer")
st.markdown("Upload or paste a full legal judgment below and get a crisp summary.")

input_text = st.text_area("Paste the full judgment here")

if st.button("Generate Summary"):
    if input_text.strip() == "":
        st.warning("Please paste a judgment first.")
    else:
        st.info("Generating summary, please wait...")
        result = query({"inputs": input_text})
        if result:
            try:
                summary = result[0]["summary_text"]
                st.success("Summary Generated:")
                st.write(summary)
            except (KeyError, IndexError):
                st.error("Unexpected response format from Hugging Face model.")
        else:
            st.error("No summary could be generated.")
