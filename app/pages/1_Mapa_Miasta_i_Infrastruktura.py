import streamlit as st

st.set_page_config(
    page_title="Mapa Miasta i Infrastruktura",
    layout="wide",
    initial_sidebar_state="expanded",
)

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

ICON_MAP = '<svg class="ph-icon" width="28" height="28" viewBox="0 0 256 256"><path d="M228.92,49.69a8,8,0,0,0-6.86-1.45L160.93,63.52,99.07,38.78a8,8,0,0,0-5.99,0L31.08,63.28A8,8,0,0,0,26,70.72V206.72a8,8,0,0,0,11.08,7.43l61-24.4,61.86,24.74a8.13,8.13,0,0,0,3,0.59,8,8,0,0,0,3-0.59l61-24.4A8,8,0,0,0,230,182.66V46.66A8,8,0,0,0,228.92,49.69ZM96,53.8,160,79.4V202.2L96,176.6ZM42,75.36l42-16.8V180.64l-42,16.8Zm172,105.28-42,16.8V75.36l42-16.8Z"></path></svg>'

st.markdown(f"<h1>{ICON_MAP} Mapa Miasta i Infrastruktura</h1>", unsafe_allow_html=True)
st.info("Moduł mapy miejskiej i heatmap przedszkoli oraz przystanków w budowie pozdro")
