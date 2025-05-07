
import streamlit as st

st.set_page_config(page_title="VerdictForge", page_icon="⚖️", layout="centered")

st.title("VerdictForge: Legal Draft Generator")
st.markdown("Enter details to generate legal drafts.")

case_name = st.text_input("Case Name")
judge_name = st.text_input("Judge Name")
summary = st.text_area("Enter Judgment Summary")

if st.button("Generate Draft"):
    if case_name and judge_name and summary:
        draft = f"""
IN THE HON'BLE COURT OF LAW

Case: {case_name}

BEFORE: Hon'ble Justice {judge_name}

JUDGMENT SUMMARY:
{summary}

This judgment is passed under the authority of the court based on the facts and evidence presented.

DATED: ___________

(Signed)
Hon'ble Justice {judge_name}
"""
        st.markdown("### Generated Legal Draft:")
        st.code(draft, language='markdown')
    else:
        st.warning("Please fill in all the fields before generating the draft.")

from dotenv import load_dotenv
import os

load_dotenv()  # Load .env file

hf_token = os.getenv("HUGGINGFACE_TOKEN")
