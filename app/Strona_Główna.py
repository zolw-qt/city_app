import streamlit as st
from styles import inject_css

from streamlit_extras.let_it_rain import *

rain(
    emoji="📈",
    font_size=54,
    falling_speed=5,
    animation_length="3s",
)

# Konfiguracja strony
st.set_page_config(
    page_title="Open Data App - Kraków", layout="wide", initial_sidebar_state="expanded"
)

# Style CSS paska bocznego oraz przycisku zwijania
st.set_page_config(
    page_title="Statystyki i Analiza Demograficzna",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_css()

# Definicje wektorów SVG dla ikon z Phosphor Icons
ICON_BUILDINGS = '<svg class="ph-icon" width="32" height="32" viewBox="0 0 256 256"><path d="M240,208H224V96a16,16,0,0,0-16-16H160V40a16,16,0,0,0-16-16H40A16,16,0,0,0,24,40V208H16a8,8,0,0,0,0,16H240a8,8,0,0,0,0-16ZM40,40h96V208H40ZM160,96h48V208H160ZM64,72A8,8,0,0,1,72,64h32a8,8,0,0,1,0,16H72A8,8,0,0,1,64,72Zm0,40a8,8,0,0,1,8-8h32a8,8,0,0,1,0,16H72A8,8,0,0,1,64,112Zm0,40a8,8,0,0,1,8-8h32a8,8,0,0,1,0,16H72A8,8,0,0,1,64,152Zm112-16a8,8,0,0,1,8-8h16a8,8,0,0,1,0,16H184A8,8,0,0,1,176,136Zm0,40a8,8,0,0,1,8-8h16a8,8,0,0,1,0,16H184A8,8,0,0,1,176,176Z"></path></svg>'
ICON_TARGET = '<svg class="ph-icon" width="24" height="24" viewBox="0 0 256 256"><path d="M128,24A104,104,0,1,0,232,128,104.11,104.11,0,0,0,128,24Zm0,192a88,88,0,1,1,88-88A88.1,88.1,0,0,1,128,216Zm48-88a48,48,0,1,1-48-48A48.05,48.05,0,0,1,176,128Zm-16,0a32,32,0,1,0-32,32A32,32,0,0,0,160,128Z"></path></svg>'
ICON_MODULES = '<svg class="ph-icon" width="24" height="24" viewBox="0 0 256 256"><path d="M104,40H48A16,16,0,0,0,32,56v56a16,16,0,0,0,16,16h56a16,16,0,0,0,16-16V56A16,16,0,0,0,104,40Zm0,72H48V56h56v56Zm104-72H152a16,16,0,0,0-16,16v56a16,16,0,0,0,16,16h56a16,16,0,0,0,16-16V56A16,16,0,0,0,208,40Zm0,72H152V56h56v56ZM104,144H48a16,16,0,0,0-16,16v56a16,16,0,0,0,16,16h56a16,16,0,0,0,16-16V160A16,16,0,0,0,104,144Zm0,72H48V160h56v56Zm104-72H152a16,16,0,0,0-16,16v56a16,16,0,0,0,16,16h56a16,16,0,0,0,16-16V160A16,16,0,0,0,208,144Zm0,72H152V160h56v56Z"></path></svg>'
ICON_MAP = '<svg class="ph-icon" width="22" height="22" viewBox="0 0 256 256"><path d="M228.92,49.69a8,8,0,0,0-6.86-1.45L160.93,63.52,99.07,38.78a8,8,0,0,0-5.99,0L31.08,63.28A8,8,0,0,0,26,70.72V206.72a8,8,0,0,0,11.08,7.43l61-24.4,61.86,24.74a8.13,8.13,0,0,0,3,0.59,8,8,0,0,0,3-0.59l61-24.4A8,8,0,0,0,230,182.66V46.66A8,8,0,0,0,228.92,49.69ZM96,53.8,160,79.4V202.2L96,176.6ZM42,75.36l42-16.8V180.64l-42,16.8Zm172,105.28-42,16.8V75.36l42-16.8Z"></path></svg>'
ICON_DEMO = '<svg class="ph-icon" width="22" height="22" viewBox="0 0 256 256"><path d="M232,208a8,8,0,0,1-8,8H32a8,8,0,0,1-8-8V48a8,8,0,0,1,16,0V192H224A8,8,0,0,1,232,208ZM96,128a8,8,0,0,1-2.34,5.66l-32,32a8,8,0,0,1-11.32-11.32L80,123.31l-26.34-26.35a8,8,0,0,1,11.32-11.32L93.66,114.34A8,8,0,0,1,96,128Zm125.66-37.66a8,8,0,0,1,0,11.32l-64,64a8,8,0,0,1-11.32,0L112,131.31l-10.34,10.35a8,8,0,0,1-11.32-11.32l16-16a8,8,0,0,1,11.32,0L160,146.69l57.66-57.65A8,8,0,0,1,221.66,90.34Z"></path></svg>'

# Nagłówek główny
st.markdown(
    f"<h1>{ICON_BUILDINGS} Kraków Open Data App</h1>",
    unsafe_allow_html=True,
    anchors=False,
)
st.caption(
    "Prototyp interaktywnej platformy analitycznej wykorzystującej otwarte dane miejskie Krakowa."
)

st.markdown("---")

# Sekcja opisu
col_desc, col_info = st.columns([2, 1])

with col_desc:
    st.markdown(
        f"### {ICON_TARGET} Cel i Wizja Projektu", unsafe_allow_html=True, anchors=False
    )
    st.write("""
    Prototyp aplikacji powstał w ramach konkursu **Kraków Open Data App**.\n
    Celem aplikacji jest zainteresowanie użytkowników otwartymi danymi i zachęcić do własnej zabawy i analizy
    oraz ułatwić porównywanie dzielnic Krakowa osobom szukającym mieszkania na wynajem, pod względem dostępności infrastruktury miejskiej.
    W przyszłości aplikacja może zostać uzupełniona o dane takie jak szkoły podstawowe, szkoły ponadpodstawowe oraz inne elmenty miasta.
    """)

    # Prototyp aplik jest ułatwienie osobom 
    # szukającym mieszkania na wynajem, a szczególnie młodym osobom i rodzinom, oceny jakości życia i dostępności 
    # infrastruktury miejskiej w poszczególnych rejonach Krakowa.

with col_info:
    st.info("""
    **Wykorzystane otwarte dane z portalu Miejskiego:**

    * [Rejestr przystanków komunikacji miejskiej](https://otwartedane.um.krakow.pl/zbiory-danych/przystanki-komunikacji-miejskiej-w-krakowie)
    * [Baza samorządowych i niesamorządowych przedszkoli](https://otwartedane.um.krakow.pl/zbiory-danych/przedszkola-w-krakowie-liczba-dzieci)
    * [Statystyki demograficzne miasta od 1995 r.](https://otwartedane.um.krakow.pl/zbiory-danych/zbiorcze-statystyki-demograficzne-dla-krakowa-od-1995-roku)
    """)

st.markdown("---")

# Sekcja nawigacji po modułach
st.markdown(
    f"### {ICON_MODULES} Dostępne Moduły Aplikacji",
    unsafe_allow_html=True,
    anchors=False,
)

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.markdown(
            f"### {ICON_MAP} Mapa Miasta i Infrastruktura",
            unsafe_allow_html=True,
            anchors=False,
        )
        st.write("Interaktywna mapa Krakowa z warstwami heatmap.")
        st.markdown(
            "*Przejdź do zakładki **Mapa Miasta i Infrastruktura** w panelu bocznym.*"
        )

with col2:
    with st.container(border=True):
        st.markdown(
            f"### {ICON_DEMO} Statystyki i Analiza Demograficzna",
            unsafe_allow_html=True,
            anchors=False,
        )
        st.write("Szczegółowa analiza danych demograficznych mieszkańców Krakowa.")
        st.markdown(
            "*Przejdź do zakładki **Statystyki i Analiza Demograficzna** w panelu bocznym.*"
        )
