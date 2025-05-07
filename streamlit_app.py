import streamlit as st
import requests

# Hugging Face API setup
API_URL = "https://api-inference.huggingface.co/models/nsi319/legal-led-base-16384"
headers = {"Authorization": f"Bearer {st.secrets['HF_API_KEY']}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Streamlit UI
st.set_page_config(page_title="VerdictForge: Judgment Summarizer", layout="centered")

st.title("⚖️ VerdictForge: Judgment Summarizer")
st.subheader("Upload or paste a legal judgment and get a crisp summary with reasoning.")

input_text = st.text_area("Paste the full judgment here")

if st.button("Generate Summary"):
    if input_text.strip() != "":
        with st.spinner("Summarizing judgment..."):
            response = query({"inputs": input_text})

            try:
                summary = response[0]["summary_text"]
                st.success("Generated Summary:")
                st.write(summary)
            except Exception as e:
                st.error("Something went wrong while generating the summary.")
                st.code(str(response))
    else:
        st.warning("Please paste a judgment to summarize.")
