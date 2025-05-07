import streamlit as st
import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Streamlit UI
st.set_page_config(page_title="VerdictForge: Judgment Summarizer", page_icon="⚖️")
st.title("VerdictForge: Judgment Summarizer")
st.markdown("Upload or paste a legal judgment and get a crisp summary with reasoning.")

# Input box
judgment_input = st.text_area("Paste the full judgment here", height=300)

# Button to generate summary
if st.button("Generate Summary"):
    if not judgment_input.strip():
        st.warning("Please paste a judgment to summarize.")
    else:
        with st.spinner("Summarizing..."):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a legal assistant specialized in Indian court judgments. Summarize the judgment into a short paragraph followed by a bullet-point list of the reasoning."},
                        {"role": "user", "content": judgment_input}
                    ],
                    temperature=0.5,
                    max_tokens=800
                )

                summary = response['choices'][0]['message']['content']
                st.subheader("Summary:")
                st.write(summary)

            except Exception as e:
                st.error("Something went wrong while generating the summary.")
