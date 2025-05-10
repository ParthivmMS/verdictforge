import streamlit as st
import requests

st.set_page_config(page_title="VerdictForge", layout="wide")
st.title("⚖️ VerdictForge: Legal Judgment Summarizer")

OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]

user_input = st.text_area("Paste your judgment here:", height=300)

if st.button("Generate Summary"):
    if not user_input.strip():
        st.warning("Please paste a judgment to summarize.")
    else:
        with st.spinner("Analyzing judgment..."):

            headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "HTTP-Referer": "https://your-username.streamlit.app",  # replace with your actual streamlit app link
                "Content-Type": "application/json"
            }

            data = {
                "model": "openrouter/mistral-7b",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a legal assistant that provides accurate summaries of Indian court judgments."
                    },
                    {
                        "role": "user",
                        "content": f"""Summarize the following Indian legal judgment in two parts:

1. Legal Summary (for lawyers/law students)
2. Simplified Summary (easy for common people)

Judgment:
{user_input}
"""
                    }
                ]
            }

            try:
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=data
                )
                response.raise_for_status()
                result = response.json()
                summary = result["choices"][0]["message"]["content"]
                st.success("Summary generated successfully!")
                st.markdown(summary)

            except requests.exceptions.RequestException as e:
                st.error("❌ API request failed. Please check your internet or OpenRouter key.")
                st.exception(e)
