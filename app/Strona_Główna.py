import streamlit as st

# Konfiguracja strony
st.set_page_config(
    page_title="Open Data App - Kraków", layout="wide", initial_sidebar_state="expanded"
)

# Stylizacja paska bocznego oraz wstawienie ikony SVG (ph-buildings) przed nawigacją
st.markdown(
    """
<style>
    /* 1. Ciemne tło paska bocznego */
    [data-testid="stSidebar"] {
        background-color: #303b51;
    }

    /* 2. Przycisk zwijania/rozwijania paska (strzałka) - przezroczyste tło i jasnoszary kolor */
    [data-testid="stSidebarCollapseButton"] button,
    [data-testid="collapsedControl"] button {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        color: #e2e8f0 !important;
    }

    [data-testid="stSidebarCollapseButton"] button svg,
    [data-testid="collapsedControl"] button svg {
        fill: #e2e8f0 !important;
        color: #e2e8f0 !important;
    }

    [data-testid="stSidebarCollapseButton"] button:hover,
    [data-testid="collapsedControl"] button:hover {
        background-color: #465676 !important;
        border-radius: 8px !important;
    }

    /* 3. Nawigacja w panelu bocznym - zapobieganie ścinaniu i zawijaniu napisów */
    [data-testid="stSidebarNav"] a {
        display: flex !important;
        align-items: center !important;
        white-space: nowrap !important;
        overflow: visible !important;
    }

    /* Tekst w nawigacji */
    [data-testid="stSidebarNav"] a span {
        color: #e2e8f0 !important;
        font-weight: normal !important;
        font-size: 16px !important;
        display: inline-block !important;
        white-space: nowrap !important;
        overflow: visible !important;
    }

    /* Aktywna strona: szare tło i pogrubiony napis */
    [data-testid="stSidebarNav"] a[aria-current="page"] {
        background-color: #242c3d !important;
        border-radius: 8px !important;
    }
    
    [data-testid="stSidebarNav"] a[aria-current="page"] span {
        font-weight: bold !important;
        color: #ffffff !important;
    }

    /* Efekty hover dla nawigacji */
    [data-testid="stSidebarNav"] a[aria-current="page"]:hover {
        background-color: #242c3d !important;
    }

    [data-testid="stSidebarNav"] a:not([aria-current="page"]):hover {
        background-color: #465676 !important;
        border-radius: 8px !important;
    }

    /* 4. Ikony SVG przed tekstem w nawigacji */
    [data-testid="stSidebarNav"] ul li a span::before {
        content: "";
        display: inline-block !important;
        width: 20px !important;
        height: 20px !important;
        margin-right: 10px !important;
        vertical-align: -3px !important;
        flex-shrink: 0 !important;
        background-color: currentColor !important;
    }

    /* Strona Główna -> Ikona Budynków */
    [data-testid="stSidebarNav"] a[href$="Strona_G%C5%82%C3%B3wna"] span::before,
    [data-testid="stSidebarNav"] a[href$="Strona_Glowna"] span::before,
    [data-testid="stSidebarNav"] ul li:nth-child(1) a span::before {
        mask: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256"><path d="M240,208H224V96a16,16,0,0,0-16-16H160V40a16,16,0,0,0-16-16H40A16,16,0,0,0,24,40V208H16a8,8,0,0,0,0,16H240a8,8,0,0,0,0-16ZM40,40h96V208H40ZM160,96h48V208H160ZM64,72A8,8,0,0,1,72,64h32a8,8,0,0,1,0,16H72A8,8,0,0,1,64,72Zm0,40a8,8,0,0,1,8-8h32a8,8,0,0,1,0,16H72A8,8,0,0,1,64,112Zm0,40a8,8,0,0,1,8-8h32a8,8,0,0,1,0,16H72A8,8,0,0,1,64,152Zm112-16a8,8,0,0,1,8-8h16a8,8,0,0,1,0,16H184A8,8,0,0,1,176,136Zm0,40a8,8,0,0,1,8-8h16a8,8,0,0,1,0,16H184A8,8,0,0,1,176,176Z"/></svg>') no-repeat center / contain !important;
        -webkit-mask: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256"><path d="M240,208H224V96a16,16,0,0,0-16-16H160V40a16,16,0,0,0-16-16H40A16,16,0,0,0,24,40V208H16a8,8,0,0,0,0,16H240a8,8,0,0,0,0-16ZM40,40h96V208H40ZM160,96h48V208H160ZM64,72A8,8,0,0,1,72,64h32a8,8,0,0,1,0,16H72A8,8,0,0,1,64,72Zm0,40a8,8,0,0,1,8-8h32a8,8,0,0,1,0,16H72A8,8,0,0,1,64,112Zm0,40a8,8,0,0,1,8-8h32a8,8,0,0,1,0,16H72A8,8,0,0,1,64,152Zm112-16a8,8,0,0,1,8-8h16a8,8,0,0,1,0,16H184A8,8,0,0,1,176,136Zm0,40a8,8,0,0,1,8-8h16a8,8,0,0,1,0,16H184A8,8,0,0,1,176,176Z"/></svg>') no-repeat center / contain !important;
    }

    /* Mapa Miasta -> Ikona Mapy */
    [data-testid="stSidebarNav"] a[href*="Mapa"] span::before {
        mask: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256"><path d="M228.92,49.69a8,8,0,0,0-6.86-1.45L160.93,63.52,99.07,38.78a8,8,0,0,0-5.99,0L31.08,63.28A8,8,0,0,0,26,70.72V206.72a8,8,0,0,0,11.08,7.43l61-24.4,61.86,24.74a8.13,8.13,0,0,0,3,0.59,8,8,0,0,0,3-0.59l61-24.4A8,8,0,0,0,230,182.66V46.66A8,8,0,0,0,228.92,49.69ZM96,53.8,160,79.4V202.2L96,176.6ZM42,75.36l42-16.8V180.64l-42,16.8Zm172,105.28-42,16.8V75.36l42-16.8Z"/></svg>') no-repeat center / contain !important;
        -webkit-mask: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256"><path d="M228.92,49.69a8,8,0,0,0-6.86-1.45L160.93,63.52,99.07,38.78a8,8,0,0,0-5.99,0L31.08,63.28A8,8,0,0,0,26,70.72V206.72a8,8,0,0,0,11.08,7.43l61-24.4,61.86,24.74a8.13,8.13,0,0,0,3,0.59,8,8,0,0,0,3-0.59l61-24.4A8,8,0,0,0,230,182.66V46.66A8,8,0,0,0,228.92,49.69ZM96,53.8,160,79.4V202.2L96,176.6ZM42,75.36l42-16.8V180.64l-42,16.8Zm172,105.28-42,16.8V75.36l42-16.8Z"/></svg>') no-repeat center / contain !important;
    }

    /* Statystyki i Analiza Demograficzna -> Ikona Wykresu */
    [data-testid="stSidebarNav"] a[href*="Demograficzna"] span::before,
    [data-testid="stSidebarNav"] a[href*="Statystyki"] span::before {
        mask: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256"><path d="M232,208a8,8,0,0,1-8,8H32a8,8,0,0,1-8-8V48a8,8,0,0,1,16,0V192H224A8,8,0,0,1,232,208ZM96,128a8,8,0,0,1-2.34,5.66l-32,32a8,8,0,0,1-11.32-11.32L80,123.31l-26.34-26.35a8,8,0,0,1,11.32-11.32L93.66,114.34A8,8,0,0,1,96,128Zm125.66-37.66a8,8,0,0,1,0,11.32l-64,64a8,8,0,0,1-11.32,0L112,131.31l-10.34,10.35a8,8,0,0,1-11.32-11.32l16-16a8,8,0,0,1,11.32,0L160,146.69l57.66-57.65A8,8,0,0,1,221.66,90.34Z"/></svg>') no-repeat center / contain !important;
        -webkit-mask: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256"><path d="M232,208a8,8,0,0,1-8,8H32a8,8,0,0,1-8-8V48a8,8,0,0,1,16,0V192H224A8,8,0,0,1,232,208ZM96,128a8,8,0,0,1-2.34,5.66l-32,32a8,8,0,0,1-11.32-11.32L80,123.31l-26.34-26.35a8,8,0,0,1,11.32-11.32L93.66,114.34A8,8,0,0,1,96,128Zm125.66-37.66a8,8,0,0,1,0,11.32l-64,64a8,8,0,0,1-11.32,0L112,131.31l-10.34,10.35a8,8,0,0,1-11.32-11.32l16-16a8,8,0,0,1,11.32,0L160,146.69l57.66-57.65A8,8,0,0,1,221.66,90.34Z"/></svg>') no-repeat center / contain !important;
    }

    /* Style dla ikon w treści strony */
    .ph-icon {
        display: inline-block;
        vertical-align: -4px;
        margin-right: 8px;
        fill: currentColor;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Definicje wektorów SVG dla ikon z Phosphor Icons
ICON_BUILDINGS = '<svg class="ph-icon" width="32" height="32" viewBox="0 0 256 256"><path d="M240,208H224V96a16,16,0,0,0-16-16H160V40a16,16,0,0,0-16-16H40A16,16,0,0,0,24,40V208H16a8,8,0,0,0,0,16H240a8,8,0,0,0,0-16ZM40,40h96V208H40ZM160,96h48V208H160ZM64,72A8,8,0,0,1,72,64h32a8,8,0,0,1,0,16H72A8,8,0,0,1,64,72Zm0,40a8,8,0,0,1,8-8h32a8,8,0,0,1,0,16H72A8,8,0,0,1,64,112Zm0,40a8,8,0,0,1,8-8h32a8,8,0,0,1,0,16H72A8,8,0,0,1,64,152Zm112-16a8,8,0,0,1,8-8h16a8,8,0,0,1,0,16H184A8,8,0,0,1,176,136Zm0,40a8,8,0,0,1,8-8h16a8,8,0,0,1,0,16H184A8,8,0,0,1,176,176Z"></path></svg>'
ICON_TARGET = '<svg class="ph-icon" width="24" height="24" viewBox="0 0 256 256"><path d="M128,24A104,104,0,1,0,232,128,104.11,104.11,0,0,0,128,24Zm0,192a88,88,0,1,1,88-88A88.1,88.1,0,0,1,128,216Zm48-88a48,48,0,1,1-48-48A48.05,48.05,0,0,1,176,128Zm-16,0a32,32,0,1,0-32,32A32,32,0,0,0,160,128Z"></path></svg>'
ICON_MODULES = '<svg class="ph-icon" width="24" height="24" viewBox="0 0 256 256"><path d="M104,40H48A16,16,0,0,0,32,56v56a16,16,0,0,0,16,16h56a16,16,0,0,0,16-16V56A16,16,0,0,0,104,40Zm0,72H48V56h56v56Zm104-72H152a16,16,0,0,0-16,16v56a16,16,0,0,0,16,16h56a16,16,0,0,0,16-16V56A16,16,0,0,0,208,40Zm0,72H152V56h56v56ZM104,144H48a16,16,0,0,0-16,16v56a16,16,0,0,0,16,16h56a16,16,0,0,0,16-16V160A16,16,0,0,0,104,144Zm0,72H48V160h56v56Zm104-72H152a16,16,0,0,0-16,16v56a16,16,0,0,0,16,16h56a16,16,0,0,0,16-16V160A16,16,0,0,0,208,144Zm0,72H152V160h56v56Z"></path></svg>'
ICON_MAP = '<svg class="ph-icon" width="22" height="22" viewBox="0 0 256 256"><path d="M228.92,49.69a8,8,0,0,0-6.86-1.45L160.93,63.52,99.07,38.78a8,8,0,0,0-5.99,0L31.08,63.28A8,8,0,0,0,26,70.72V206.72a8,8,0,0,0,11.08,7.43l61-24.4,61.86,24.74a8.13,8.13,0,0,0,3,0.59,8,8,0,0,0,3-0.59l61-24.4A8,8,0,0,0,230,182.66V46.66A8,8,0,0,0,228.92,49.69ZM96,53.8,160,79.4V202.2L96,176.6ZM42,75.36l42-16.8V180.64l-42,16.8Zm172,105.28-42,16.8V75.36l42-16.8Z"></path></svg>'
ICON_DEMO = '<svg class="ph-icon" width="22" height="22" viewBox="0 0 256 256"><path d="M232,208a8,8,0,0,1-8,8H32a8,8,0,0,1-8-8V48a8,8,0,0,1,16,0V192H224A8,8,0,0,1,232,208ZM96,128a8,8,0,0,1-2.34,5.66l-32,32a8,8,0,0,1-11.32-11.32L80,123.31l-26.34-26.35a8,8,0,0,1,11.32-11.32L93.66,114.34A8,8,0,0,1,96,128Zm125.66-37.66a8,8,0,0,1,0,11.32l-64,64a8,8,0,0,1-11.32,0L112,131.31l-10.34,10.35a8,8,0,0,1-11.32-11.32l16-16a8,8,0,0,1,11.32,0L160,146.69l57.66-57.65A8,8,0,0,1,221.66,90.34Z"></path></svg>'

# Nagłówek główny
st.markdown(f"<h1>{ICON_BUILDINGS} Kraków Open Data App</h1>", unsafe_allow_html=True)
st.caption(
    "Prototyp interaktywnej platformy analitycznej wykorzystującej otwarte dane miejskie Krakowa."
)

st.markdown("---")

# Sekcja opisu
col_desc, col_info = st.columns([2, 1])

with col_desc:
    st.markdown(f"### {ICON_TARGET} Cel i Wizja Projektu", unsafe_allow_html=True)
    st.write("""
    Aplikacja powstała w ramach inicjatywy **Kraków Open Data App**. Jej celem jest ułatwienie osobom 
    szukającym mieszkania na wynajem, a szczególnie młodym osobom i rodzinom, oceny jakości życia i dostępności 
    infrastruktury miejskiej w poszczególnych rejonach Krakowa.
    """)

with col_info:
    st.info("""
    **Wykorzystane otwarte dane z portalu Miejskiego:**

    * [Rejestr przystanków komunikacji miejskiej](https://otwartedane.um.krakow.pl/zbiory-danych/przystanki-komunikacji-miejskiej-w-krakowie)
    * [Baza samorządowych i niesamorządowych przedszkoli](https://otwartedane.um.krakow.pl/zbiory-danych/przedszkola-w-krakowie-liczba-dzieci)
    * [Statystyki demograficzne miasta od 1995 r.](https://otwartedane.um.krakow.pl/zbiory-danych/zbiorcze-statystyki-demograficzne-dla-krakowa-od-1995-roku)
    """)

st.markdown("---")

# Sekcja nawigacji po modułach
st.markdown(f"### {ICON_MODULES} Dostępne Moduły Aplikacji", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.markdown(
            f"### {ICON_MAP} Mapa Miasta i Infrastruktura", unsafe_allow_html=True
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
        )
        st.write("Szczegółowa analiza danych demograficznych mieszkańców Krakowa.")
        st.markdown(
            "*Przejdź do zakładki **Statystyki i Analiza Demograficzna** w panelu bocznym.*"
        )
