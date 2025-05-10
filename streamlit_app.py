import streamlit as st
import requests

st.set_page_config(page_title="VerdictForge - Legal Judgment Summarizer")

st.title("⚖️ VerdictForge")
st.subheader("Summarize Legal Judgments using AI")

user_input = st.text_area("Paste your legal judgment here:", height=300)

if st.button("Summarize"):
    if not user_input.strip():
        st.warning("Please paste a judgment to summarize.")
    else:
        with st.spinner("Summarizing..."):
            try:
                api_key = st.secrets["OPENROUTER_API_KEY"]

                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }

                # Phase 1 Smart Prompt
                prompt = f"""
You are a legal AI trained to summarize Indian and UK court judgments for law students, interns, and early-stage professionals.

Summarize the following judgment in two clear parts:

1. ✅ **Legal Summary**: Summarize the key legal principles, holdings, and important reasoning in a professional tone. Include:
   - What legal issue the case addresses.
   - What rule or principle the court applied.
   - What decision was made.

2. 📝 **Simplified Summary**: Explain the same case in very simple English like you're talking to a law student or a curious non-lawyer. Use short sentences. Avoid legal jargon.

Here is the judgment:
\"\"\"
{user_input}
\"\"\"
"""

                data = {
                    "model": "mistral/mistral-7b-instruct",
                    "messages": [
                        {"role": "system", "content": "You are a helpful and accurate legal summarizer."},
                        {"role": "user", "content": prompt}
                    ]
                }

                response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
                response.raise_for_status()
                summary = response.json()["choices"][0]["message"]["content"]

                st.success("✅ Summary generated successfully!")
                st.markdown(summary)

            except requests.exceptions.RequestException as e:
                st.error("❌ API request failed. Please check your internet or OpenRouter key.")
                st.exception(e)
            except KeyError:
                st.error("❌ OpenRouter API key missing. Please add OPENROUTER_API_KEY to your Streamlit secrets.")
