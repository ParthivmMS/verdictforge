import streamlit as st
import requests
import json

st.set_page_config(page_title="VerdictForge - Judgment Summarizer", page_icon="⚖️")

# Sidebar navigation
choice = st.sidebar.radio("Navigate", ["Summarizer", "Privacy Policy", "About This Website"])

if choice == "Summarizer":
    # === Your original code, unmodified, except indented under this block ===
    st.title("⚖️ VerdictForge")
    st.subheader("AI-Powered Indian Legal Judgment Summarizer")

    # Replace previous sidebar.info with menu, so no sidebar.info here
    judgment_text = st.text_area(
        "📜 Paste a legal judgment below:", 
        height=300, 
        placeholder="Enter full judgment text here..."
    )

    OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
    API_URL = "https://openrouter.ai/api/v1/chat/completions"
    HEADERS = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    SYSTEM_PROMPT = (
        "You are a senior legal associate in an Indian law firm. "
        "Your job is to read a full legal judgment and output a detailed legal summary followed by a simplified explanation in plain English. "
        "Ensure your summary is relevant, captures the legal issue, judgment, reasoning, and applicable principles."
    )

    summary_text = None

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
                    summary_text = ai_reply

                    st.success("✅ Summary generated successfully:")
                    st.markdown(ai_reply)

                except requests.exceptions.RequestException as e:
                    st.error("❌ API request failed. Please check your internet or OpenRouter key.")
                    st.exception(e)

    # Download button appears once summary_text is set
    if summary_text:
        st.download_button(
            label="📥 Download Summary as Text",
            data=summary_text,
            file_name="verdictforge_summary.txt",
            mime="text/plain"
        )

    # Footer (still on this page)
    st.markdown("---")
    st.markdown("Made with ❤️ by Parthiv | [GitHub](https://github.com/parthivofficial)")

elif choice == "Privacy Policy":
    st.title("Privacy Policy")
    st.markdown("""
    **Effective Date:** May 11, 2025

    This website does not store any personal data or uploaded judgments.
    All processing is done temporarily and securely via OpenRouter AI.
    We respect your privacy and do not share or sell your data to third parties.
    """)
    st.markdown("---")
    st.markdown("Made with ❤️ by Parthiv | [GitHub](https://github.com/parthivofficial)")

elif choice == "About This Website":
    st.title("About This Website")
    st.markdown("""
    **VerdictForge** is an AI-powered legal judgment summarization tool designed 
    to help law students, professionals, and researchers quickly understand long 
    court decisions.

    Built using the Mistral-7B model via OpenRouter, VerdictForge aims to:
    - Save time during legal research  
    - Improve comprehension of lengthy judgments  
    - Assist law students from non-NLU backgrounds  

    Developed with passion by a law student exploring the intersection of law and AI.
    """)
    st.markdown("---")
    st.markdown("Made with ❤️ by Parthiv | [GitHub](https://github.com/parthivofficial)")
