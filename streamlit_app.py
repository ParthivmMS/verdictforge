import streamlit as st
import requests

# Streamlit UI
st.set_page_config(page_title="VerdictForge - Legal Judgment Summarizer", layout="centered")
st.title("⚖️ VerdictForge - Legal Judgment Summarizer")
st.markdown("Paste a legal judgment below to get a clear, student-friendly summary.")

# Input
judgment = st.text_area("📄 Paste the Full Judgment", height=300)

# When user clicks the button
if st.button("🧠 Generate Summary"):
    if not judgment.strip():
        st.warning("Please paste a judgment before summarizing.")
    else:
        with st.spinner("Summarizing..."):
            try:
                # Load key from Streamlit secrets
                api_key = st.secrets["openrouter_key"]

                # Send request to OpenRouter
                url = "https://openrouter.ai/api/v1/chat/completions"
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": "mistralai/mistral-7b-instruct",
                    "messages": [
                        {"role": "system", "content": "You are a legal assistant. Summarize court judgments in a short, clear, student-friendly format."},
                        {"role": "user", "content": judgment}
                    ]
                }

                response = requests.post(url, headers=headers, json=payload)
                result = response.json()

                # Extract and display summary
                summary = result["choices"][0]["message"]["content"]
                st.success("✅ Summary:")
                st.write(summary)

            except Exception as e:
                st.error(f"❌ Something went wrong: {str(e)}")
