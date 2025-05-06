import streamlit as st
from transformers import pipeline

# Page title
st.set_page_config(page_title="Judgment Summarizer", layout="centered")
st.title("Judgment Summarizer")
st.markdown("**Summarize long legal judgments instantly using AI**")

# Input box
text_input = st.text_area("Paste the legal judgment text below:", height=300)

# Load the summarization pipeline
@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

summarizer = load_summarizer()

# Button to summarize
if st.button("Summarize"):
    if not text_input.strip():
        st.warning("Please paste some legal judgment text first.")
    else:
        with st.spinner("Summarizing..."):
            chunks = [text_input[i:i+1000] for i in range(0, len(text_input), 1000)]
            summary = ""
            for chunk in chunks:
                result = summarizer(chunk, max_length=130, min_length=30, do_sample=False)
                summary += result[0]['summary_text'] + " "
            st.success("Summary:")
            st.write(summary.strip())
