import streamlit as st
import requests
import json

# --- Page Setup ---
st.set_page_config(page_title="VerdictForge - Judgment Summarizer", page_icon="⚖️")

# --- SEO Meta Tags ---
st.markdown("""
<!-- SEO Meta Tags -->
<meta name="title" content="VerdictForge - AI Legal Judgment Summarizer">
<meta name="description" content="Summarize Indian court judgments using AI. Built for law students, legal researchers, and professionals.">
<meta name="keywords" content="AI Legal Summarizer, Indian Court Judgments, Case Summary, Law AI, Legal Tech India">
<meta name="author" content="VerdictForge by Parthiv M S">
<meta property="og:title" content="VerdictForge - Legal Judgment Summarizer" />
<meta property="og:description" content="Summarize Indian legal judgments in seconds with our AI-powered tool." />
<meta property="og:type" content="website" />
<meta property="og:url" content="https://verdictforge.in/" />
<meta property="og:image" content="https://verdictforge.in/favicon.png" />
""", unsafe_allow_html=True)



# --- Sidebar Menu ---
menu = st.sidebar.radio("Navigate", ["Summarizer", "Privacy Policy", "About This Website", "Blog"])

# --- Summarizer Section ---
if menu == "Summarizer":
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

# --- Privacy Policy Section ---
elif menu == "Privacy Policy":
    st.title("Privacy Policy")
    st.markdown("""
    **Effective Date:** May 11, 2025

    This website does not store any personal data or uploaded judgments.
    All processing is done temporarily and securely via OpenRouter AI.
    We respect your privacy and do not share or sell your data to third parties.
    """)
    st.markdown("---")
    st.markdown("Made with ❤️ by Parthiv | [GitHub](https://github.com/parthivofficial)")

# --- About Page Section ---
elif menu == "About This Website":
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

# --- Blog Section ---
elif menu == "Blog":
    blog_choice = st.sidebar.radio("Blog Posts", [
        "Why I Built an AI Legal Summarizer",
        "How AI Can Save Hours of Legal Research"
    ])

    if blog_choice == "Why I Built an AI Legal Summarizer":
        st.title("Blog 1: Why I Built an AI Legal Summarizer as a Law Student in India")
        st.markdown("""
        In my first year at a government law college, I faced a problem that many students silently struggle with — judgment fatigue.  
        Long, dense court decisions that took hours to read. Confusing legal jargon. No one to explain it simply.

        I thought, what if I could build something that explains these judgments like a senior — clearly, briefly, and usefully?

        That’s how **VerdictForge** was born.

        With no tech background, I used AI (Mistral via OpenRouter) and Streamlit to build a tool that:
        - Breaks down judgments into simplified summaries
        - Highlights legal issues, reasoning, and decisions
        - Provides both legal and plain English explanations

        This isn’t just a summarizer. It’s a study companion, a research accelerator, and a time-saver.

        My vision is to grow VerdictForge into a full legal AI assistant — helping students, lawyers, and law firms across India.

        If you're reading this, you're part of that journey. Let’s reshape legal education together.

        ---
        Made with ❤️ by Parthiv | [GitHub](https://github.com/parthivofficial)
        """)

    elif blog_choice == "How AI Can Save Hours of Legal Research":
        st.title("Blog 2: How AI Can Save Hours of Legal Research for Law Students and Lawyers")
        st.markdown("""
        **“Sir, it took me 6 hours to go through the entire judgment. I couldn’t even finish my notes.”**

        If you’re a law student or junior associate in India, this probably sounds familiar. Long judgments. Tough English. Dozens of citations. And deadlines always lurking.

        In traditional legal research, it takes **hours** to skim through dense court rulings, extract key points, and rewrite them in a presentable format. Worse, this time crunch leads to **incomplete understanding**, rushed briefs, and **burnout**.

        ### What If You Could Do This in Minutes?

        That’s exactly what VerdictForge was built for.

        VerdictForge is an AI-powered legal judgment summarizer that does the heavy lifting for you. Instead of reading every page manually, you paste the judgment—and **get an instant summary** with the:

        - Case facts  
        - Legal issues  
        - Reasoning  
        - Final decision  
        - Easy-to-understand takeaway

        This means:
        - Law students save hours of note-taking during exams.
        - Advocates can prep for arguments faster.
        - Law firms boost research efficiency.

        ### A Real-Life Use Case:

        A student from a government law college preparing for his intern presentation pasted a 5-page SC judgment into VerdictForge. The tool gave him a **clear, concise** 3-paragraph summary in under 10 seconds.

        He impressed his senior advocate—and understood the case better.

        ### Why This Matters

        In the AI age, time is your biggest asset. Legal research doesn't need to feel like punishment. Whether you’re preparing for moot court, working on a case brief, or revising for exams, VerdictForge is your **24x7 legal assistant**.

        ### Final Thought

        Smart students don’t work harder—they use smarter tools.

        If you're still manually breaking down judgments, you’re wasting precious time. Try VerdictForge today and **let AI do the heavy lifting**—so you can focus on learning, arguing, and winning.

        ---
        Made with ❤️ by Parthiv | [GitHub](https://github.com/parthivofficial)
        """)
