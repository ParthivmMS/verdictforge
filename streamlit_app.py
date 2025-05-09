import streamlit as st
import requests

# Config
API_URL = "https://api-inference.huggingface.co/models/knkarthick/Legal-Bert-Summarizer"
headers = {"Authorization": f"Bearer {st.secrets['HF_API_KEY']}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        st.error(f"Error {response.status_code}: {response.text}")
        return None
    return response.json()

st.title("⚖️ VerdictForge - Legal Judgment Summarizer")
st.markdown("Paste a court judgment below to get a 3–4 line summary.")

input_text = st.text_area("📜 Paste full judgment", height=300)

if st.button("🧠 Generate Summary"):
    if not input_text.strip():
        st.warning("Please paste the judgment.")
    else:
        st.info("Summarizing... please wait.")
        result = query({"inputs": input_text})
        if result:
            try:
                summary = result[0]["summary_text"]
                st.success("✅ Summary:")
                st.write(summary)
            except:
                st.error("⚠️ Unexpected format from API.")

