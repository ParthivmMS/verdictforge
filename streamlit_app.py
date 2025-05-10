import streamlit as st
import requests

st.title("⚖️ VerdictForge - Legal Judgment Summarizer")
st.markdown("Paste a court judgment below. We'll generate a short summary using Mistral.")

API_KEY = st.secrets["OPENROUTER_API_KEY"]
API_URL = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def get_summary(text):
    payload = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "system", "content": "You are a legal expert who summarizes court judgments into 2–3 clear lines."},
            {"role": "user", "content": f"Summarize this legal judgment:\n\n{text}"}
        ],
        "temperature": 0.5,
        "max_tokens": 300
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        st.error(f"Error {response.status_code}: {response.text}")
        return None

judgment = st.text_area("📜 Paste your judgment here", height=300)

if st.button("🧠 Generate Summary"):
    if judgment.strip():
        st.info("Summarizing... please wait.")
        summary = get_summary(judgment)
        if summary:
            st.success("✅ Summary:")
            st.write(summary)
    else:
        st.warning("Please enter some text.")
