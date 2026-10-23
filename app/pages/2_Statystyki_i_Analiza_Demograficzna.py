import pandas as pd
import plotly.express as px
import streamlit as st

# Konfiguracja podstrony
st.set_page_config(
    page_title="Statystyki i Analiza Demograficzna",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Style CSS paska bocznego oraz przycisku zwijania
st.markdown(
    """
<style>
    [data-testid="stSidebar"] {
        background-color: #303b51;
    }
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
    [data-testid="stSidebarNav"] a {
        display: flex !important;
        align-items: center !important;
        white-space: nowrap !important;
        overflow: visible !important;
    }
    [data-testid="stSidebarNav"] a span {
        color: #e2e8f0 !important;
        font-weight: normal !important;
        font-size: 16px !important;
        display: inline-block !important;
        white-space: nowrap !important;
        overflow: visible !important;
    }
    [data-testid="stSidebarNav"] a[aria-current="page"] {
        background-color: #242c3d !important;
        border-radius: 8px !important;
    }
    [data-testid="stSidebarNav"] a[aria-current="page"] span {
        font-weight: bold !important;
        color: #ffffff !important;
    }
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
    [data-testid="stSidebarNav"] a[href$="Strona_G%C5%82%C3%B3wna"] span::before,
    [data-testid="stSidebarNav"] a[href$="Strona_Glowna"] span::before,
    [data-testid="stSidebarNav"] ul li:nth-child(1) a span::before {
        mask: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256"><path d="M240,208H224V96a16,16,0,0,0-16-16H160V40a16,16,0,0,0-16-16H40A16,16,0,0,0,24,40V208H16a8,8,0,0,0,0,16H240a8,8,0,0,0,0-16ZM40,40h96V208H40ZM160,96h48V208H160ZM64,72A8,8,0,0,1,72,64h32a8,8,0,0,1,0,16H72A8,8,0,0,1,64,72Zm0,40a8,8,0,0,1,8-8h32a8,8,0,0,1,0,16H72A8,8,0,0,1,64,112Zm0,40a8,8,0,0,1,8-8h32a8,8,0,0,1,0,16H72A8,8,0,0,1,64,152Zm112-16a8,8,0,0,1,8-8h16a8,8,0,0,1,0,16H184A8,8,0,0,1,176,136Zm0,40a8,8,0,0,1,8-8h16a8,8,0,0,1,0,16H184A8,8,0,0,1,176,176Z"/></svg>') no-repeat center / contain !important;
        -webkit-mask: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256"><path d="M240,208H224V96a16,16,0,0,0-16-16H160V40a16,16,0,0,0-16-16H40A16,16,0,0,0,24,40V208H16a8,8,0,0,0,0,16H240a8,8,0,0,0,0-16ZM40,40h96V208H40ZM160,96h48V208H160ZM64,72A8,8,0,0,1,72,64h32a8,8,0,0,1,0,16H72A8,8,0,0,1,64,72Zm0,40a8,8,0,0,1,8-8h32a8,8,0,0,1,0,16H72A8,8,0,0,1,64,112Zm0,40a8,8,0,0,1,8-8h32a8,8,0,0,1,0,16H72A8,8,0,0,1,64,152Zm112-16a8,8,0,0,1,8-8h16a8,8,0,0,1,0,16H184A8,8,0,0,1,176,136Zm0,40a8,8,0,0,1,8-8h16a8,8,0,0,1,0,16H184A8,8,0,0,1,176,176Z"/></svg>') no-repeat center / contain !important;
    }
    [data-testid="stSidebarNav"] a[href*="Mapa"] span::before {
        mask: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256"><path d="M228.92,49.69a8,8,0,0,0-6.86-1.45L160.93,63.52,99.07,38.78a8,8,0,0,0-5.99,0L31.08,63.28A8,8,0,0,0,26,70.72V206.72a8,8,0,0,0,11.08,7.43l61-24.4,61.86,24.74a8.13,8.13,0,0,0,3,0.59,8,8,0,0,0,3-0.59l61-24.4A8,8,0,0,0,230,182.66V46.66A8,8,0,0,0,228.92,49.69ZM96,53.8,160,79.4V202.2L96,176.6ZM42,75.36l42-16.8V180.64l-42,16.8Zm172,105.28-42,16.8V75.36l42-16.8Z"/></svg>') no-repeat center / contain !important;
        -webkit-mask: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256"><path d="M228.92,49.69a8,8,0,0,0-6.86-1.45L160.93,63.52,99.07,38.78a8,8,0,0,0-5.99,0L31.08,63.28A8,8,0,0,0,26,70.72V206.72a8,8,0,0,0,11.08,7.43l61-24.4,61.86,24.74a8.13,8.13,0,0,0,3,0.59,8,8,0,0,0,3-0.59l61-24.4A8,8,0,0,0,230,182.66V46.66A8,8,0,0,0,228.92,49.69ZM96,53.8,160,79.4V202.2L96,176.6ZM42,75.36l42-16.8V180.64l-42,16.8Zm172,105.28-42,16.8V75.36l42-16.8Z"/></svg>') no-repeat center / contain !important;
    }
    [data-testid="stSidebarNav"] a[href*="Demograficzna"] span::before,
    [data-testid="stSidebarNav"] a[href*="Statystyki"] span::before {
        mask: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256"><path d="M232,208a8,8,0,0,1-8,8H32a8,8,0,0,1-8-8V48a8,8,0,0,1,16,0V192H224A8,8,0,0,1,232,208ZM96,128a8,8,0,0,1-2.34,5.66l-32,32a8,8,0,0,1-11.32-11.32L80,123.31l-26.34-26.35a8,8,0,0,1,11.32-11.32L93.66,114.34A8,8,0,0,1,96,128Zm125.66-37.66a8,8,0,0,1,0,11.32l-64,64a8,8,0,0,1-11.32,0L112,131.31l-10.34,10.35a8,8,0,0,1-11.32-11.32l16-16a8,8,0,0,1,11.32,0L160,146.69l57.66-57.65A8,8,0,0,1,221.66,90.34Z"/></svg>') no-repeat center / contain !important;
        -webkit-mask: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256"><path d="M232,208a8,8,0,0,1-8,8H32a8,8,0,0,1-8-8V48a8,8,0,0,1,16,0V192H224A8,8,0,0,1,232,208ZM96,128a8,8,0,0,1-2.34,5.66l-32,32a8,8,0,0,1-11.32-11.32L80,123.31l-26.34-26.35a8,8,0,0,1-11.32-11.32L93.66,114.34A8,8,0,0,1,96,128Zm125.66-37.66a8,8,0,0,1,0,11.32l-64,64a8,8,0,0,1-11.32,0L112,131.31l-10.34,10.35a8,8,0,0,1-11.32-11.32l16-16a8,8,0,0,1,11.32,0L160,146.69l57.66-57.65A8,8,0,0,1,221.66,90.34Z"/></svg>') no-repeat center / contain !important;
    }
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

# Wektory SVG Phosphor Icons
ICON_DEMO = '<svg class="ph-icon" width="28" height="28" viewBox="0 0 256 256"><path d="M232,208a8,8,0,0,1-8,8H32a8,8,0,0,1-8-8V48a8,8,0,0,1,16,0V192H224A8,8,0,0,1,232,208ZM96,128a8,8,0,0,1-2.34,5.66l-32,32a8,8,0,0,1-11.32-11.32L80,123.31l-26.34-26.35a8,8,0,0,1,11.32-11.32L93.66,114.34A8,8,0,0,1,96,128Zm125.66-37.66a8,8,0,0,1,0,11.32l-64,64a8,8,0,0,1-11.32,0L112,131.31l-10.34,10.35a8,8,0,0,1-11.32-11.32l16-16a8,8,0,0,1,11.32,0L160,146.69l57.66-57.65A8,8,0,0,1,221.66,90.34Z"></path></svg>'
ICON_SLIDERS = '<svg class="ph-icon" width="22" height="22" viewBox="0 0 256 256"><path d="M120,88A32,32,0,1,0,88,56,32,32,0,0,0,120,88Zm0-48A16,16,0,1,1,104,56,16,16,0,0,1,120,40ZM208,168a32,32,0,1,0-32-32A32,32,0,0,0,208,168Zm0-48a16,16,0,1,1-16,16A16,16,0,0,1,208,120ZM40,216H72a8,8,0,0,0,0-16H40a8,8,0,0,0,0,16Zm168,0a8,8,0,0,0,0-16H184a8,8,0,0,0,0,16ZM40,56H72a8,8,0,0,0,0-16H40a8,8,0,0,0,0,16ZM216,56a8,8,0,0,0,0-16H136a8,8,0,0,0,0,16ZM40,136H160a8,8,0,0,0,0-16H40a8,8,0,0,0,0,16Z"></path></svg>'
ICON_NUMBERS = '<svg class="ph-icon" width="26" height="26" viewBox="0 0 256 256"><path d="M224,200h-8V40a8,8,0,0,0-8-8H168a8,8,0,0,0-8,8V88H104a8,8,0,0,0-8,8v48H56a8,8,0,0,0-8,8v48H32a8,8,0,0,0,0,16H224a8,8,0,0,0,0-16ZM176,48h24V200H176ZM112,104h24V200H112ZM64,152H88v48H64Z"></path></svg>'

st.markdown(
    f"<h1>{ICON_DEMO} Statystyki i Analiza Demograficzna</h1>", unsafe_allow_html=True
)
st.caption(
    "Interaktywna analiza zmian liczby mieszkańców oraz struktury edukacyjnej w Krakowie."
)

st.markdown("---")


# =========================================================
# WCZYTANIE PRAWDZIWYCH DANYCH DEMOGRAFICZNYCH
# =========================================================
@st.cache_data
def load_demographic_data():
    file_path = (
        "../data/Zbiorcze statystyki demograficzne dla Krakowa, od 1995 roku.csv"
    )
    df = pd.read_csv(file_path, sep=";")

    # Oczyszczenie nazw kolumn
    df.columns = df.columns.str.strip()

    # Obliczenie wskaźnika obciążenia demograficznego: Pracujący / Poprodukcyjny
    df["Indeks_Obciążenia"] = (
        df["Liczba osób w wieku produkcyjnym"]
        / df["Liczba osób w wieku  poprodukcyjnym"]
    )

    return df


df_raw = load_demographic_data()

min_year = int(df_raw["Rok"].min())
max_year = int(df_raw["Rok"].max())

# =========================================================
# FORMULARZ FILTRÓW NA STRONIE GŁÓWNEJ
# =========================================================
with st.form("filters_form"):
    st.markdown(f"### {ICON_SLIDERS} Panel Filtrowania Danych", unsafe_allow_html=True)
    col_f1, col_f2, col_f3 = st.columns(3)

    with col_f1:
        selected_years = st.slider(
            "Zakres lat analizy:",
            min_value=min_year,
            max_value=max_year,
            value=(1998, 1999),  # Domyślnie ustawione na 1998-1999
        )

    with col_f2:
        selected_age_groups = st.multiselect(
            "Grupy wiekowe:",
            options=["Przedprodukcyjny", "Produkcyjny", "Poprodukcyjny"],
            default=["Przedprodukcyjny", "Produkcyjny", "Poprodukcyjny"],
        )

    with col_f3:
        kindergarten_type = st.selectbox(
            "Typ przedszkoli:", options=["Wszystkie", "Samorządowe", "Niesamorządowe"]
        )

    submit_button = st.form_submit_button(label="Zastosuj filtry")

# Filtrowanie ramki danych po wybranym zakresie lat
df_filtered = df_raw[
    (df_raw["Rok"] >= selected_years[0]) & (df_raw["Rok"] <= selected_years[1])
].copy()


# =========================================================
# FUNKCJA GENERUJĄCA MINIWYKRESY (SPARK LINES)
# =========================================================
def create_sparkline(df, y_col, is_bar=False, reverse_color=False):
    start_val = df[y_col].iloc[0]
    end_val = df[y_col].iloc[-1]
    is_growth = end_val >= start_val

    if reverse_color:
        color = "#ef4444" if is_growth else "#10b981"
    else:
        color = "#10b981" if is_growth else "#ef4444"

    if is_bar:
        fig = px.bar(df, x="Rok", y=y_col)
        fig.update_traces(marker_color=color)
    else:
        fig = px.line(df, x="Rok", y=y_col, render_mode="svg")
        fig.update_traces(line_color=color, line_width=2.5)

    fig.update_layout(
        margin=dict(l=0, r=0, t=5, b=5),
        height=60,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    diff = end_val - start_val
    pct = ((end_val - start_val) / abs(start_val if start_val != 0 else 1)) * 100
    return fig, diff, pct, color


# =========================================================
# NAGŁÓWEK I OPIS WPROWADZAJĄCY NAD KARTAMI SPARK LINES
# =========================================================
st.markdown(f"## {ICON_NUMBERS} Kraków w liczbach", unsafe_allow_html=True)

st.markdown(
    f"""
Ten panel prezentuje najważniejsze metryki demograficzne oraz trend ich zmian w Krakowie na przestrzeni wybranych lat. 
Służy do szybkiej oceny dynamiki wzrostu populacji, ruchów migracyjnych, liczby osób w wieku przedprodukcyjnym oraz obciążenia struktury wiekowej.
<br>
**Analizowany okres:** {selected_years[0]} – {selected_years[1]}
""",
    unsafe_allow_html=True,
)

st.markdown("<br>", unsafe_allow_html=True)

# =========================================================
# 4 KARTY SPARKLINE (Z PRAWDZIWYMI DANYMI)
# =========================================================
c1, c2, c3, c4 = st.columns(4)

# 1. Całkowita Liczba Mieszkańców
with c1:
    with st.container(border=True):
        fig1, diff1, pct1, col1_color = create_sparkline(
            df_filtered, "Liczba ludności ogółem"
        )
        val1 = df_filtered["Liczba ludności ogółem"].iloc[-1]
        st.caption("Całkowita liczba ludności")

        # Połączenie obu wartości w jeden blok HTML z precyzyjnym marginesem
        diff_formatted = f"{diff1:+,.0f}".replace(",", " ")

        st.markdown(
            f"""
            <div style="margin-top: 5px; margin-bottom: 5px;">
                <div style="color: {col1_color}; font-weight: bold; font-size: 38px; line-height: 1;">
                    {pct1:+.1f}%
                </div>
                <div style="color: #475569; font-size: 15px; font-weight: 500; margin-top: 4px;">
                    {diff_formatted}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.plotly_chart(
            fig1, use_container_width=True, config={"displayModeBar": False}
        )

# 2. Saldo Migracji
with c2:
    with st.container(border=True):
        fig2, diff2, pct2, col2_color = create_sparkline(
            df_filtered, "Saldo migracji", is_bar=True
        )
        val2 = df_filtered["Saldo migracji"].iloc[-1]
        st.caption("Saldo migracji")
        # Połączenie obu wartości w jeden blok HTML z precyzyjnym marginesem
        diff_formatted = f"{diff2:+,.0f}".replace(",", " ")

        st.markdown(
            f"""
            <div style="margin-top: 5px; margin-bottom: 5px;">
                <div style="color: {col2_color}; font-weight: bold; font-size: 38px; line-height: 1;">
                    {pct2:+.1f}%
                </div>
                <div style="color: #475569; font-size: 15px; font-weight: 500; margin-top: 4px;">
                    {diff_formatted}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.plotly_chart(
            fig2, use_container_width=True, config={"displayModeBar": False}
        )

# 3. Dzieci w wieku przedprodukcyjnym
with c3:
    with st.container(border=True):
        fig3, diff3, pct3, col3_color = create_sparkline(
            df_filtered, "Liczba osób w wieku przedprodukcyjnym"
        )
        val3 = df_filtered["Liczba osób w wieku przedprodukcyjnym"].iloc[-1]
        st.caption("Dzieci i młodzież")
        # Połączenie obu wartości w jeden blok HTML z precyzyjnym marginesem
        diff_formatted = f"{diff3:+,.0f}".replace(",", " ")

        st.markdown(
            f"""
            <div style="margin-top: 5px; margin-bottom: 5px;">
                <div style="color: {col3_color}; font-weight: bold; font-size: 38px; line-height: 1;">
                    {pct3:+.1f}%
                </div>
                <div style="color: #475569; font-size: 15px; font-weight: 500; margin-top: 4px;">
                    {diff_formatted}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.plotly_chart(
            fig3, use_container_width=True, config={"displayModeBar": False}
        )

# 4. Indeks Obciążenia Demograficznego (Pracujący / Poprodukcyjny)
with c4:
    with st.container(border=True):
        fig4, diff4, pct4, col4_color = create_sparkline(
            df_filtered, "Indeks_Obciążenia"
        )
        val4 = df_filtered["Indeks_Obciążenia"].iloc[-1]
        st.caption("Indeks obciążenia (pracujący/seniora)")
        # Połączenie obu wartości w jeden blok HTML z precyzyjnym marginesem
        diff_formatted = f"{diff4:+,.2f}".replace(",", " ")

        st.markdown(
            f"""
            <div style="margin-top: 5px; margin-bottom: 5px;">
                <div style="color: {col4_color}; font-weight: bold; font-size: 38px; line-height: 1;">
                    {pct4:+.1f}%
                </div>
                <div style="color: #475569; font-size: 15px; font-weight: 500; margin-top: 4px;">
                    {diff_formatted}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.plotly_chart(
            fig4, use_container_width=True, config={"displayModeBar": False}
        )

st.markdown("---")

# =========================================================
# SEKCJA WYKRESÓW GŁÓWNYCH
# =========================================================
col_g1, col_g2 = st.columns(2)

with col_g1:
    st.markdown("### Trend Ludności Ogółem")
    fig_main1 = px.line(
        df_filtered,
        x="Rok",
        y="Liczba ludności ogółem",
        markers=True,
        template="plotly_white",
        color_discrete_sequence=["#303b51"],
    )
    st.plotly_chart(fig_main1, use_container_width=True)

with col_g2:
    st.markdown("### Przyrost Naturalny vs Saldo Migracji")
    fig_main2 = px.bar(
        df_filtered,
        x="Rok",
        y=["Przyrost naturalny (w osobach)", "Saldo migracji"],
        barmode="group",
        template="plotly_white",
        color_discrete_sequence=["#303b51", "#465676"],
    )
    st.plotly_chart(fig_main2, use_container_width=True)
