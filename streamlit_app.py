import streamlit as st
import requests

st.set_page_config(page_title="VerdictForge", layout="wide")
st.title("⚖️ VerdictForge: Legal Judgment Summarizer")

# Get the API key securely
api_key = st.secrets["OPENROUTER_API_KEY"]

# Input
user_input = st.text_area("Paste your legal judgment:", height=300)

# On click
if st.button("Generate Summary"):
    if not user_input.strip():
        st.warning("Please enter a legal judgment.")
    else:
        with st.spinner("Summarizing..."):
            url = "https://openrouter.ai/api/v1/chat/completions"

            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }

            data = {
                "model": "openai/gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a legal assistant AI. Provide a two-part output:\n\n1. Legal Summary: Summarize the judgment in a professional tone suitable for legal professionals.\n2. Simplified Summary: Explain the judgment in layman's terms."
                    },
                    {
                        "role": "user",
                        "content": user_input
                    }
                ]
            }

            try:
                response = requests.post(url, headers=headers, json=data)
                response.raise_for_status()
                result = response.json()

                output = result["choices"][0]["message"]["content"]
                st.success("✅ Summary generated successfully:")
                st.markdown(output)

            except requests.exceptions.RequestException as e:
                st.error("❌ API request failed. Please check your OpenRouter key or request format.")
                st.exception(e)
