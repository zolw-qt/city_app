import streamlit as st
from styles import inject_css

st.set_page_config(
    page_title="Mapa Miasta i Infrastruktura",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Style CSS paska bocznego oraz przycisku zwijania
st.set_page_config(
    page_title="Statystyki i Analiza Demograficzna",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_css()

ICON_MAP = '<svg class="ph-icon" width="28" height="28" viewBox="0 0 256 256"><path d="M228.92,49.69a8,8,0,0,0-6.86-1.45L160.93,63.52,99.07,38.78a8,8,0,0,0-5.99,0L31.08,63.28A8,8,0,0,0,26,70.72V206.72a8,8,0,0,0,11.08,7.43l61-24.4,61.86,24.74a8.13,8.13,0,0,0,3,0.59,8,8,0,0,0,3-0.59l61-24.4A8,8,0,0,0,230,182.66V46.66A8,8,0,0,0,228.92,49.69ZM96,53.8,160,79.4V202.2L96,176.6ZM42,75.36l42-16.8V180.64l-42,16.8Zm172,105.28-42,16.8V75.36l42-16.8Z"></path></svg>'

st.markdown(f"<h1>{ICON_MAP} Mapa Miasta i Infrastruktura</h1>", unsafe_allow_html=True)
st.info("Moduł mapy miejskiej i heatmap przedszkoli oraz przystanków w budowie pozdro")
