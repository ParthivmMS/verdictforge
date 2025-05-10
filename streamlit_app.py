import streamlit as st
import requests

st.set_page_config(page_title="VerdictForge", layout="wide")
st.title("⚖️ VerdictForge: Legal Judgment Summarizer")

OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]

# Input area
user_input = st.text_area("Paste your judgment here:", height=300)

# On button click
if st.button("Generate Summary"):
    if not user_input.strip():
        st.warning("Please paste a judgment to summarize.")
    else:
        with st.spinner("Analyzing judgment..."):

            # Prepare messages
            messages = [
                {"role": "system", "content": "You are a top-tier legal assistant who summarizes Indian case law judgments clearly."},
                {"role": "user", "content": f"Summarize the following legal judgment in two parts:\n\n1. Legal Summary (professional tone)\n2. Simplified Summary (for general understanding)\n\nJudgment:\n{user_input}"}
            ]

            headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            }

            data = {
                "model": "mistralai/mixtral-8x7b",  # ✅ Correct model name
                "messages": messages
            }

            try:
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=data,
                    timeout=60
                )
                response.raise_for_status()
                result = response.json()
                summary = result["choices"][0]["message"]["content"]
                st.success("Summary generated successfully!")
                st.write(summary)

            except requests.exceptions.RequestException as e:
                st.error("❌ API request failed. Please check your internet or OpenRouter key.")
                st.exception(e)
