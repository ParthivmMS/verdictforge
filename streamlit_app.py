import streamlit as st
import requests
import json

st.title("⚖️ VerdictForge - Legal Judgment Summarizer")
st.markdown("Paste a court judgment to get an AI-generated summary and a simplified version.")

OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]

# Text input
judgment = st.text_area("📄 Paste Judgment", height=300)

if st.button("🧠 Generate Summary"):
    if not judgment.strip():
        st.warning("Please paste a judgment.")
    else:
        with st.spinner("Summarizing..."):
            try:
                # Step 1: Main Summary
                prompt_summary = (
                    f"Summarize the following legal judgment in a short, clear paragraph:\n\n{judgment}"
                )
                headers = {
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json"
                }
                payload_summary = {
                    "model": "mistralai/mistral-7b-instruct",
                    "messages": [{"role": "user", "content": prompt_summary}],
                }

                res1 = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, data=json.dumps(payload_summary))
                summary_text = res1.json()["choices"][0]["message"]["content"].strip()

                st.success("✅ Legal Summary:")
                st.write(summary_text)

                # Step 2: Simplified Summary
                prompt_simplified = (
                    f"Rewrite this legal summary in a shorter and simpler way that a first-year law student can easily understand:\n\n{summary_text}"
                )
                payload_simplify = {
                    "model": "mistralai/mistral-7b-instruct",
                    "messages": [{"role": "user", "content": prompt_simplified}],
                }

                res2 = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, data=json.dumps(payload_simplify))
                simplified_text = res2.json()["choices"][0]["message"]["content"].strip()

                st.info("📝 Simplified Summary:")
                st.write(simplified_text)

            except Exception as e:
                st.error(f"❌ Something went wrong: {e}")
