import streamlit as st
import requests
import json

st.set_page_config(page_title="VerdictForge - Judgment Summarizer", page_icon="⚖️")
st.title("⚖️ VerdictForge")
st.subheader("AI-Powered Indian Legal Judgment Summarizer")

# Sidebar info
st.sidebar.title("Navigation")
st.sidebar.info("This tool summarizes Indian legal judgments into professional and simplified formats.")

# Input field for judgment text
judgment_text = st.text_area("📜 Paste a legal judgment below:", height=300, placeholder="Enter full judgment text here...")

# API Key and endpoint
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
API_URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

# Prompt template
SYSTEM_PROMPT = (
    "You are a senior legal associate in an Indian law firm. "
    "Your job is to read a full legal judgment and output a detailed legal summary followed by a simplified explanation in plain English. "
    "Ensure your summary is relevant, captures the legal issue, judgment, reasoning, and applicable principles."
)

# Generate summary
if st.button("⚡ Generate Summary"):
    if not judgment_text.strip():
        st.warning("Please paste a legal judgment to generate a summary.")
    else:
        with st.spinner("Analyzing judgment and generating summary..."):
            try:
                payload = {
                    "model": "mistralai/mistral-7b-instruct:free",
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": judgment_text}
                    ]
                }
                response = requests.post(API_URL, headers=HEADERS, data=json.dumps(payload))
                response.raise_for_status()
                result = response.json()

                ai_reply = result['choices'][0]['message']['content']

                st.success("✅ Summary generated successfully:")
                st.markdown(ai_reply)

            except requests.exceptions.RequestException as e:
                st.error("❌ API request failed. Please check your internet or OpenRouter key.")
                st.exception(e)

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by Parthiv | [GitHub](https://github.com/parthivofficial)")
