import streamlit as st
import requests
import json
import os

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

# --- Google AdSense ---
st.markdown("""
<!-- Google AdSense -->
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1762689473102041"
     crossorigin="anonymous"></script>
""", unsafe_allow_html=True)

# --- Sidebar Menu ---
menu = st.sidebar.radio("Navigate", ["Summarizer", "Privacy Policy", "About This Website", "Blog"])

# --- Summarizer Section ---
if menu == "Summarizer":
    st.title("⚖️ VerdictForge")
    st.subheader("AI-Powered Indian Legal Judgment Summarizer")

    judgment_text = st.text_area("📜 Paste a legal judgment below:", height=300, placeholder="Enter full judgment text here...")

    OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

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
    st.title("📚 Blog")

    blog_option = st.selectbox("Choose a blog to read:", [
        "Blog 1: Why I Built an AI Legal Summarizer as a Law Student in India",
        "Blog 2: The Invisible Burden of Reading Legal Judgments",
        "Blog 3: How AI Can Help Law Students From Non-NLU Colleges"
    ])

    if blog_option == "Blog 1: Why I Built an AI Legal Summarizer as a Law Student in India":
        st.header("Why I Built VerdictForge — An AI Legal Summarizer for Indian Law Students")
        st.markdown("*VerdictForge simplifies Indian court judgments using AI-powered legal and plain English summaries. Built by a first-year law student for students and researchers across India.*")
        st.markdown("### 🧠 The Problem: Judgment Fatigue in Indian Law Colleges")
        st.markdown("""
        In my first year at a government law college, I struggled with what many students silently face — **judgment fatigue**.  
        Long, complex court decisions with confusing legal jargon. Hours spent reading just to understand one case.

        As a law student from a non-NLU college, I didn’t have seniors to guide me or law firm mentors to help. But I had one edge — curiosity.
        """)

        st.markdown("### ⚙️ The Idea: Can AI Help Us Understand Judgments Faster?")
        st.markdown("""
        I asked myself: *What if an AI tool could explain judgments like a senior advocate — clearly, briefly, and usefully?*

        That’s how **VerdictForge** was born.

        Even without a tech background, I built it using:
        - **Streamlit** for UI
        - **Mistral-7B via OpenRouter** for summarization

        VerdictForge:
        - Breaks down court decisions into **crisp legal summaries**
        - Gives **plain English explanations**
        - Focuses specifically on **Indian judgments**
        """)

        st.markdown("### 🚀 Why This Matters for Law Students")
        st.markdown("""
        Most legal tech tools are built for lawyers, not students. But we need it the most.

        VerdictForge is:
        - A **study companion** for exams
        - A **research booster** for moots and internships
        - A **time-saver** for anyone reading judgments

        It's especially designed for **students from non-NLU backgrounds** — to level the playing field with AI.
        """)

        st.markdown("### 🌱 What’s Next")
        st.markdown("""
        I want to grow VerdictForge into a full legal assistant:
        - Auto-detect legal issues
        - Extract citations
        - Support regional languages

        If you’re a student, intern, or junior associate, I built this for you.

        👉 Let’s reshape legal education in India — with tech.
        """)

    elif blog_option == "Blog 2: The Invisible Burden of Reading Legal Judgments":
        st.header("The Invisible Burden of Reading Indian Judgments — And How AI Can Help")
        st.markdown("*Law students spend hours struggling through dense court decisions. Learn how VerdictForge removes that pain with fast, AI-powered legal summaries.*")
        st.markdown("### 📚 Reading vs. Understanding: The Student’s Struggle")
        st.markdown("""
        Law students and junior advocates often drown in pages of judgments.  
        We copy-paste from SCC Online, Manupatra, or court websites… then read… re-read… summarize by hand.

        It’s exhausting. We lose hours each day on something that should be simple.
        """)

        st.markdown("### ⚖️ Why the System Feels Broken")
        st.markdown("""
        Legal research should feel like gaining insight — not surviving a punishment.  
        But instead of teaching us how to understand, the system trains us to just “get through it.”

        This isn’t efficiency. It’s burnout.
        """)

        st.markdown("### 🤖 How AI Solves the Friction")
        st.markdown("""
        That’s where **VerdictForge** comes in.

        We’re not replacing lawyers — we’re removing friction. Think of VerdictForge as:
        - A personal legal intern who never gets tired
        - Someone who reads fast, summarizes crisply, and simplifies legal jargon

        With every summary, we give time back to:
        - Law students preparing for exams
        - Interns handling case research
        - Professionals managing court loads

        ⚡ This is legal productivity — built for India.
        """)

    elif blog_option == "Blog 3: How AI Can Help Law Students From Non-NLU Colleges":
        st.header("How AI Can Empower Law Students from Non-NLU Colleges in India")
        st.markdown("*Not from an NLU? No problem. Discover how VerdictForge helps students from government and private law colleges compete through smart legal tech.*")
        st.markdown("### 🎓 The Legal Divide in India")
        st.markdown("""
        Let’s be real — the Indian legal world is tiered.

        NLU students get better internships, more exposure, and stronger networks.  
        But what about students from government or private colleges?

        We’re often left behind. Not due to skill — but lack of access.
        """)

        st.markdown("### 💡 The Power of AI as an Equalizer")
        st.markdown("""
        I study in a government law college. I don’t have alumni power or firm connections.  
        But I discovered something powerful — **technology**.

        With tools like VerdictForge, any law student can:
        - Read judgments faster
        - Understand complex decisions in plain English
        - Save time for internships, moots, and writing

        AI doesn’t care where you study — it **levels the field**.
        """)

        st.markdown("### 🔮 Building for the Forgotten Majority")
        st.markdown("""
        VerdictForge is not just a tool. It’s a rebellion — against the idea that only elite law schools deserve support.

        My dream is to make legal tech accessible to **every Indian law student**, especially from non-NLU backgrounds.

        If we use AI smartly, we can rise based on **skill — not brand**.
        """)

    st.markdown("---")
    st.markdown("Made with ❤ by Parthiv | [GitHub](https://github.com/ParthivmMS)")
