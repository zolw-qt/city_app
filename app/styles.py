from pathlib import Path

import streamlit as st


def inject_css():
    css = (Path(__file__).parent / "styles.css").read_text(encoding="utf-8-sig")
    css = css.replace("<style>", "").replace("</style>", "")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
