import streamlit as st
import streamlit.components.v1 as components
import requests
import json
import os

# --- Page Setup ---
st.set_page_config(
    page_title="VerdictForge – Legal Judgment Summarizer",
    page_icon="favicon.jpg",  # fallback
    layout="wide"
)

# Inject static SEO HTML file (Google will read it)
try:
    components.html(open("static/index.html", "r").read(), height=0)
except Exception as e:
    st.warning("Could not inject SEO metadata.")
    st.exception(e)

# --- Force Favicon + Title using DOM JavaScript ---
components.html("""
<script>
  // Set Title
  document.title = "VerdictForge – Indian Legal Judgment Summarizer";

  // Replace favicon dynamically with the raw GitHub asset
  const link = document.createElement('link');
  link.rel = 'icon';
  link.type = 'image/png';
  link.href = 'https://github.com/ParthivmMS/verdictforge/raw/main/favicon.jpg';
  document.head.appendChild(link);
</script>
""", height=0)

# --- SEO Meta Tags ---
st.markdown("""
<!-- SEO Meta Tags -->
<meta name="title" content="VerdictForge – AI Legal Judgment Summarizer">
<meta name="description" content="VerdictForge summarizes Indian court judgments into legal + plain English formats. Built for law students and lawyers in India.">
<meta name="keywords" content="AI Legal Summarizer, Indian Court Judgments, Case Summary, Law AI, Legal Tech India">
<meta name="author" content="VerdictForge by Parthiv M S">
<meta property="og:title" content="VerdictForge – Legal Judgment Summarizer" />
<meta property="og:description" content="Summarize Indian legal judgments in seconds with our AI-powered tool." />
<meta property="og:type" content="website" />
<meta property="og:url" content="https://verdictforge.in/" />
<meta property="og:image" content="https://github.com/ParthivmMS/verdictforge/raw/main/favicon.jpg" />
""", unsafe_allow_html=True)

# --- Google AdSense Script ---
st.markdown("""
<!-- Google AdSense -->
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1762689473102041"
     crossorigin="anonymous"></script>
""", unsafe_allow_html=True)

# --- Sidebar Menu ---
menu = st.sidebar.radio("Navigate", ["Summarizer", "Privacy Policy", "About This Website", "Blog"])

# --- Summarizer Section ---
if menu == "Summarizer":
    # Logo image (raw)
    st.markdown(
        """
        <div style='text-align: center; margin-bottom: 1rem;'>
          <img src='https://github.com/ParthivmMS/verdictforge/raw/main/favicon.jpg' width='150' />
        </div>
        """,
        unsafe_allow_html=True
    )

    # Slogan
    st.markdown(
        "<h3 style='text-align: center; color: gray; margin-top: -1rem;'>Simplify. Summarize. Succeed.</h3>",
        unsafe_allow_html=True
    )

    # Title and subtitle
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
    st.markdown("Made with ❤ by Parthiv | [GitHub](https://github.com/parthivofficial)")

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
    st.markdown("Made with ❤ by Parthiv | [GitHub](https://github.com/parthivofficial)")

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
    st.markdown("Made with ❤ by Parthiv | [GitHub](https://github.com/parthivofficial)")

# --- Blog Section ---
# --- Blog Section ---
elif menu == "Blog":
    st.title("📚 Blog")

    blog_option = st.selectbox("Choose a blog to read:", [
        "Blog 1: Why I Built an AI Legal Summarizer as a Law Student in India",
        "Blog 2: The Invisible Burden of Reading Legal Judgments",
        "Blog 3: How AI Can Help Law Students From Non-NLU Colleges",
        "Blog 4: Top 5 Legal Research Tools Every Indian Law Student Should Use in 2025"
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
        # (Continue rest of Blog 1…)

    elif blog_option == "Blog 2: The Invisible Burden of Reading Legal Judgments":
        st.header("The Invisible Burden of Reading Indian Judgments — And How AI Can Help")
        st.markdown("*Law students spend hours struggling through dense court decisions. Learn how VerdictForge removes that pain with fast, AI-powered legal summaries.*")
        # (Continue Blog 2…)

    elif blog_option == "Blog 3: How AI Can Help Law Students From Non-NLU Colleges":
        st.header("How AI Can Empower Law Students from Non-NLU Colleges in India")
        st.markdown("*Not from an NLU? No problem. Discover how VerdictForge helps students from government and private law colleges compete through smart legal tech.*")
        # (Continue Blog 3…)

    elif blog_option == "Blog 4: Top 5 Legal Research Tools Every Indian Law Student Should Use in 2025":
        st.header("Top 5 Legal Research Tools Every Indian Law Student Should Use in 2025")
        st.markdown("*Supercharge your legal studies with these must-use tools — especially if you’re in a government or private law college.*")

        st.markdown("### 1️⃣ SCC Online – Your Judgment Goldmine")
        st.markdown("""
        If you're serious about case law, you can’t avoid SCC Online. It's the gold standard for accessing Supreme Court and High Court judgments, along with citations.
        
        - Use it for: Researching landmark cases, citations, legal doctrines  
        - Tip: Use the “Case Note” section to get quick summaries.
        """)

        st.markdown("### 2️⃣ Manupatra – India's All-Round Legal Research Engine")
        st.markdown("""
        Manupatra is like a one-stop shop for case law, statutes, notifications, and legal commentary.

        - Use it for: Advanced case filtering, case maps, tracking precedents  
        - Tip: Use the ‘Referencer’ feature to quickly understand important legal concepts.
        """)

        st.markdown("### 3️⃣ Indian Kanoon – Free, Fast, Functional")
        st.markdown("""
        On a budget? Indian Kanoon gives you access to judgments, acts, and rules for free.

        - Use it for: Quick case lookup, bare act reading  
        - Tip: Use double quotes around search terms for better accuracy (“Article 21”).
        """)

        st.markdown("### 4️⃣ ChatGPT / VerdictForge – AI for Legal Summarization")
        st.markdown("""
        For quick comprehension of long judgments, AI tools like **VerdictForge** (or ChatGPT with legal prompts) save tons of time.

        - Use it for: Summarizing long cases, preparing for class discussions, exam prep  
        - Tip: Always read the judgment yourself after getting the summary.
        """)

        st.markdown("### 5️⃣ LiveLaw & Bar & Bench – Legal News You Need")
        st.markdown("""
        Legal research isn’t just about old cases. Stay updated with current legal developments using LiveLaw and Bar & Bench.

        - Use it for: Learning ongoing constitutional issues, legal controversies, court reporting  
        - Tip: Follow their Twitter handles for real-time updates.
        """)

        st.markdown("### ⚖️ Final Word")
        st.markdown("""
        You don’t need to master all five tools — but using just two or three of them regularly will level you up.

        Law is 50% reading and 50% understanding. These tools help you do both faster and smarter.

        Keep learning, co-founder.
        """)

    st.markdown("---")
    st.markdown("Made with ❤ by Parthiv | [GitHub](https://github.com/ParthivmMS)")
        # … rest of your blog content …

    st.markdown("---")
    st.markdown("Made with ❤ by Parthiv | [GitHub](https://github.com/ParthivmMS)")
