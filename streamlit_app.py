import streamlit as st
import requests
import json

st.set_page_config(page_title="VerdictForge - Judgment Summarizer", page_icon="⚖️")

# Inject SEO Meta Tags
st.markdown("""
<!-- SEO Meta Tags -->
<meta name="title" content="VerdictForge - AI Legal Judgment Summarizer">
<meta name="description" content="Summarize Indian court judgments using AI. Built for law students, legal researchers, and professionals.">
<meta name="keywords" content="AI Legal Summarizer, Indian Court Judgments, Case Summary, Law AI, Legal Tech India">
<meta name="author" content="VerdictForge by Parthiv M S">
<meta property="og:title" content="VerdictForge - Legal Judgment Summarizer" />
<meta property="og:description" content="Summarize Indian legal judgments in seconds with our AI-powered tool." />
<meta property="og:type" content="website" />
<meta property="og:url" content="https://verdictforge-uaaxxcnwqfhbk73s28gjl4.streamlit.app/" />
<meta property="og:image" content="https://verdictforge-uaaxxcnwqfhbk73s28gjl4.streamlit.app/favicon.png" />
""", unsafe_allow_html=True)

# Updated sidebar
choice = st.sidebar.radio("Navigate", [
    "Summarizer", 
    "Privacy Policy", 
    "About This Website", 
    "Blogs"
])

# ========== Summarizer ==========
if choice == "Summarizer":
    st.title("⚖️ VerdictForge")
    st.subheader("AI-Powered Indian Legal Judgment Summarizer")

    judgment_text = st.text_area("📜 Paste a legal judgment below:", height=300, placeholder="Enter full judgment text here...")

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

    if summary_text:
        st.download_button(
            label="📥 Download Summary as Text",
            data=summary_text,
            file_name="verdictforge_summary.txt",
            mime="text/plain"
        )

    st.markdown("---")
    st.markdown("Made with ❤️ by Parthiv | [GitHub](https://github.com/parthivofficial)")

# ========== Privacy Policy ==========
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

# ========== About ==========
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

# ========== Blogs ==========
elif choice == "Blogs":
    st.title("📚 Legal Insights & Blogs")
    
    st.header("1. Why Every Law Student Needs Judgment Summaries")
    st.markdown("""
    Understanding lengthy judgments is one of the biggest challenges for Indian law students.
    Our AI tool converts 10-page verdicts into 10-second insights — perfect for last-minute revisions and better comprehension.
    """)

    st.header("2. The Future of Legal Research is AI-Powered")
    st.markdown("""
    Manual legal research takes hours. With AI like VerdictForge, legal professionals can instantly summarize judgments, boosting productivity and client value.
    """)

    st.header("3. How VerdictForge is Helping Non-NLU Students Compete with Top Law Schools")
    st.markdown("""
    Students from government colleges often lack elite exposure. VerdictForge levels the playing field by giving every law student quick access to case summaries and analysis tools.
    """)

    st.markdown("---")
    st.markdown("Made with ❤️ by Parthiv | [GitHub](https://github.com/parthivofficial)")
