import streamlit as st
import requests
import os

st.set_page_config(page_title="⚖️ VerdictForge - Legal Judgment Summarizer")

# UI
st.title("⚖️ VerdictForge")
st.markdown("Paste a court judgment below to get a **precise 2–3 line summary**.")

# Input box
text = st.text_area("📄 Paste the judgment here", height=300)

# OpenRouter API Key (stored securely in secrets)
API_KEY = st.secrets["OPENROUTER_API_KEY"]

# Define Mistral API endpoint
url = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def get_summary(text):
    payload = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a legal summarization assistant. Summarize Indian court judgments in **2–3 concise lines**, "
                    "highlighting only the final legal conclusion, outcome, or direction by the court. Do not repeat sentences. "
                    "Make it sharp and legally relevant."
                )
            },
            {
                "role": "user",
                "content": f"Summarize the following legal judgment:\n\n{text.strip()}"
            }
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

# Button to generate summary
if st.button("🧠 Generate Summary"):
    if not text.strip():
        st.warning("Please paste a judgment.")
    else:
        with st.spinner("Summarizing... please wait."):
            try:
                summary = get_summary(text)
                st.success("✅ Summary:")
                st.write(summary)
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
