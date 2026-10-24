from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from styles import inject_css

# Konfiguracja podstrony
st.set_page_config(
    page_title="Statystyki i Analiza Demograficzna",
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


# Wektory SVG Phosphor Icons
ICON_DEMO = '<svg class="ph-icon" width="28" height="28" viewBox="0 0 256 256"><path d="M232,208a8,8,0,0,1-8,8H32a8,8,0,0,1-8-8V48a8,8,0,0,1,16,0V192H224A8,8,0,0,1,232,208ZM96,128a8,8,0,0,1-2.34,5.66l-32,32a8,8,0,0,1-11.32-11.32L80,123.31l-26.34-26.35a8,8,0,0,1,11.32-11.32L93.66,114.34A8,8,0,0,1,96,128Zm125.66-37.66a8,8,0,0,1,0,11.32l-64,64a8,8,0,0,1-11.32,0L112,131.31l-10.34,10.35a8,8,0,0,1-11.32-11.32l16-16a8,8,0,0,1,11.32,0L160,146.69l57.66-57.65A8,8,0,0,1,221.66,90.34Z"></path></svg>'
ICON_SLIDERS = '<svg class="ph-icon" width="22" height="22" viewBox="0 0 256 256"><path d="M120,88A32,32,0,1,0,88,56,32,32,0,0,0,120,88Zm0-48A16,16,0,1,1,104,56,16,16,0,0,1,120,40ZM208,168a32,32,0,1,0-32-32A32,32,0,0,0,208,168Zm0-48a16,16,0,1,1-16,16A16,16,0,0,1,208,120ZM40,216H72a8,8,0,0,0,0-16H40a8,8,0,0,0,0,16Zm168,0a8,8,0,0,0,0-16H184a8,8,0,0,0,0,16ZM40,56H72a8,8,0,0,0,0-16H40a8,8,0,0,0,0,16ZM216,56a8,8,0,0,0,0-16H136a8,8,0,0,0,0,16ZM40,136H160a8,8,0,0,0,0-16H40a8,8,0,0,0,0,16Z"></path></svg>'
ICON_NUMBERS = '<svg class="ph-icon" width="26" height="26" viewBox="0 0 256 256"><path d="M224,200h-8V40a8,8,0,0,0-8-8H168a8,8,0,0,0-8,8V88H104a8,8,0,0,0-8,8v48H56a8,8,0,0,0-8,8v48H32a8,8,0,0,0,0,16H224a8,8,0,0,0,0-16ZM176,48h24V200H176ZM112,104h24V200H112ZM64,152H88v48H64Z"></path></svg>'
ICON_DATABASE = '<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="#000000" viewBox="0 0 256 256"><path d="M128,24C74.17,24,32,48.6,32,80v96c0,31.4,42.17,56,96,56s96-24.6,96-56V80C224,48.6,181.83,24,128,24Zm80,104c0,9.62-7.88,19.43-21.61,26.92C170.93,163.35,150.19,168,128,168s-42.93-4.65-58.39-13.08C55.88,147.43,48,137.62,48,128V111.36c17.06,15,46.23,24.64,80,24.64s62.94-9.68,80-24.64ZM69.61,53.08C85.07,44.65,105.81,40,128,40s42.93,4.65,58.39,13.08C200.12,60.57,208,70.38,208,80s-7.88,19.43-21.61,26.92C170.93,115.35,150.19,120,128,120s-42.93-4.65-58.39-13.08C55.88,99.43,48,89.62,48,80S55.88,60.57,69.61,53.08ZM186.39,202.92C170.93,211.35,150.19,216,128,216s-42.93-4.65-58.39-13.08C55.88,195.43,48,185.62,48,176V159.36c17.06,15,46.23,24.64,80,24.64s62.94-9.68,80-24.64V176C208,185.62,200.12,195.43,186.39,202.92Z"></path></svg>'
ICON_QUESTION = '<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="#000000" viewBox="0 0 256 256"><path d="M136,120v56a8,8,0,0,1-16,0V120a8,8,0,0,1,16,0Zm36.84-.8-5.6,56A8,8,0,0,0,174.4,184a7.32,7.32,0,0,0,.81,0,8,8,0,0,0,7.95-7.2l5.6-56a8,8,0,0,0-15.92-1.6Zm-89.68,0a8,8,0,0,0-15.92,1.6l5.6,56a8,8,0,0,0,8,7.2,7.32,7.32,0,0,0,.81,0,8,8,0,0,0,7.16-8.76ZM239.93,89.06,224.86,202.12A16.06,16.06,0,0,1,209,216H47a16.06,16.06,0,0,1-15.86-13.88L16.07,89.06A8,8,0,0,1,24,80H68.37L122,18.73a8,8,0,0,1,12,0L187.63,80H232a8,8,0,0,1,7.93,9.06ZM89.63,80h76.74L128,36.15ZM222.86,96H33.14L47,200H209Z"></path></svg>'
ICON_BABY = '<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="#000000" viewBox="0 0 256 256"><path d="M160,32h-8a16,16,0,0,0-16,16v56H55.2A40.07,40.07,0,0,0,16,72a8,8,0,0,0,0,16,24,24,0,0,1,24,24,80.09,80.09,0,0,0,80,80h40a80,80,0,0,0,0-160Zm63.48,72H166.81l41.86-33.49A63.73,63.73,0,0,1,223.48,104ZM160,48a63.59,63.59,0,0,1,36.69,11.61L152,95.35V48Zm0,128H120a64.09,64.09,0,0,1-63.5-56h167A64.09,64.09,0,0,1,160,176Zm-56,48a16,16,0,1,1-16-16A16,16,0,0,1,104,224Zm104,0a16,16,0,1,1-16-16A16,16,0,0,1,208,224Z"></path></svg>'
ICON_DETECTIVE = '<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="#000000" viewBox="0 0 256 256"><path d="M248,112H220.08l-47.5-65.41a16,16,0,0,0-25.31-.72l-12.85,14.9-.2.23a7.95,7.95,0,0,1-12.44,0l-.2-.23-12.85-14.9a16,16,0,0,0-25.31.72L35.92,112H8a8,8,0,0,0,0,16H248a8,8,0,0,0,0-16ZM96.34,56l.19.23,12.85,14.89a24,24,0,0,0,37.24,0l12.85-14.89c.06-.08.1-.15.17-.23l40.66,56H55.69ZM180,144a36,36,0,0,0-35.77,32H111.77a36,36,0,1,0-1.83,16h36.12A36,36,0,1,0,180,144ZM76,200a20,20,0,1,1,20-20A20,20,0,0,1,76,200Zm104,0a20,20,0,1,1,20-20A20,20,0,0,1,180,200Z"></path></svg>'
ICON_HOUSE = '<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="#000000" viewBox="0 0 256 256"><path d="M240,208H224V136l2.34,2.34A8,8,0,0,0,237.66,127L139.31,28.68a16,16,0,0,0-22.62,0L18.34,127a8,8,0,0,0,11.32,11.31L32,136v72H16a8,8,0,0,0,0,16H240a8,8,0,0,0,0-16ZM48,120l80-80,80,80v88H160V152a8,8,0,0,0-8-8H104a8,8,0,0,0-8,8v56H48Zm96,88H112V160h32Z"></path></svg>'
ICON_USERSWITCH = '<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="#000000" viewBox="0 0 256 256"><path d="M253.66,133.66l-24,24a8,8,0,0,1-11.32,0l-24-24a8,8,0,0,1,11.32-11.32L216,132.69V128A88,88,0,0,0,56.49,76.67a8,8,0,0,1-13-9.34A104,104,0,0,1,232,128v4.69l10.34-10.35a8,8,0,0,1,11.32,11.32Zm-41.18,55A104,104,0,0,1,24,128v-4.69L13.66,133.66A8,8,0,0,1,2.34,122.34l24-24a8,8,0,0,1,11.32,0l24,24a8,8,0,0,1-11.32,11.32L40,123.31V128a87.62,87.62,0,0,0,22.24,58.41A79.66,79.66,0,0,1,98.3,157.66a48,48,0,1,1,59.4,0,79.59,79.59,0,0,1,36.08,28.78,89.68,89.68,0,0,0,5.71-7.11,8,8,0,0,1,13,9.34ZM128,152a32,32,0,1,0-32-32A32,32,0,0,0,128,152Zm0,64a88.2,88.2,0,0,0,53.92-18.49,64,64,0,0,0-107.84,0A87.57,87.57,0,0,0,128,216Z"></path></svg>'


# Zestaw kolorow przypisanych do konkretnych cech
KOLORY = {
    "Ludność ogółem": "#1B3A5C",
    "Przedprodukcyjny": "#F4A261",
    "Produkcyjny": "#2E86C1",
    "Poprodukcyjny": "#8E6BBF",
    "Urodzenia": "#6BBF59",
    "Zgony": "#C8553D",
    "Przyrost naturalny": "#3FA796",
    "Saldo migracji": "#0A7E8C",
    "Migracje wewnętrzne": "#00A6A6",
    "Migracje zagraniczne": "#005F73",
    "Małżeństwa": "#E56B9B",
    "Rozwody": "#B9B005",
    "Samorządowe": "#264653",
    "Niesamorządowe": "#B08968",
}


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
    file_path = "data/Zbiorcze statystyki demograficzne dla Krakowa, od 1995 roku.csv"
    df = pd.read_csv(file_path, sep=";")

    # st.subheader("Podgląd danych")
    # st.write(df.head())

    # st.subheader("Podsumowanie danych")
    # st.write(df.describe())

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
WSZYSTKIE_GRUPY = ["Przedprodukcyjny", "Produkcyjny", "Poprodukcyjny"]
ETYKIETY_GRUP = {
    "Przedprodukcyjny": "Dzieci i młodzież (wiek przedprodukcyjny)",
    "Produkcyjny": "Osoby pracujące (wiek produkcyjny)",
    "Poprodukcyjny": "Seniorzy (wiek poprodukcyjny)",
}

with st.form("filters_form"):
    st.markdown(f"### {ICON_SLIDERS} Panel Filtrowania Danych", unsafe_allow_html=True)
    st.caption(
        "Domyślnie widzisz wszystkie dane. Zaznacz opcje poniżej, aby zawęzić analizę."
    )
    col_f1, col_f2, col_f3 = st.columns([1.3, 1, 1])

    with col_f1:
        selected_years = st.slider(
            "Zakres lat analizy:",
            min_value=min_year,
            max_value=max_year,
            value=(min_year, max_year),
            help="Dotyczy kart i wykresów demograficznych. Dane o przedszkolach "
            "są podawane za lata szkolne 2023–2026 i nie zależą od suwaka.",
        )

    with col_f2:
        selected_age_groups = st.multiselect(
            "Grupy wiekowe:",
            options=WSZYSTKIE_GRUPY,
            default=[],
            format_func=ETYKIETY_GRUP.get,
            placeholder="Wszystkie grupy",
            help="Dotyczy wykresu struktury wieku. Puste pole oznacza wszystkie grupy.",
        )

    with col_f3:
        selected_kg_types = st.multiselect(
            "Typ przedszkoli:",
            options=["Samorządowe", "Niesamorządowe"],
            default=[],
            placeholder="Wszystkie typy",
            help="Dotyczy wykresu dzieci w przedszkolach. Puste pole oznacza oba typy.",
        )

    submit_button = st.form_submit_button("Zastosuj filtry", type="primary")

# Puste pole = brak zawężenia (reszta kodu działa jak wcześniej)
if not selected_age_groups:
    selected_age_groups = WSZYSTKIE_GRUPY
kindergarten_type = selected_kg_types[0] if len(selected_kg_types) == 1 else "Wszystkie"

# Filtrowanie ramki danych po wybranym zakresie lat
df_filtered = df_raw[
    (df_raw["Rok"] >= selected_years[0]) & (df_raw["Rok"] <= selected_years[1])
].copy()
st.markdown("---")


# =========================================================
# SEKCJA Z WYŚWIETLONYM HEAD() ZBIORU DANYCH
# =========================================================
st.markdown(
    f"## {ICON_DATABASE} Podgląd danych demograficznych",
    unsafe_allow_html=True,
)
st.write(
    "Jeżeli interesuje cię zapoznanie się z surowymi danymi, to możesz je przejrzeć rozwijając poniższą opcję."
)
# df_podglad = load_demographic_data()
# st.write(df_podglad.head(7))
with st.expander("Zobacz dane", expanded=False):
    st.dataframe(df_raw, use_container_width=True)

st.markdown("---")


# st.markdown(
#     "### Podsumowanie danych - pytanie czy to chcemy i czy moze na koncu lepiej?"
# )
# st.write(df_podglad.describe())


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
# =========================================================
# KARTY KPI + SPARKLINE
# =========================================================
ZIELONY = ("#E6F6EA", "#1E7B34", "↑")
CZERWONY = ("#FDE8E8", "#B42318", "↓")
SZARY = ("#EEF0F3", "#5B6470", "→")


def fmt_int(v):
    return f"{v:,.0f}".replace(",", " ")


def fmt_signed(v):
    return f"{v:+,.0f}".replace(",", " ")


def fmt_2(v):
    return f"{v:.2f}".replace(".", ",")


def kpi_card(col, label, column, fmt_value, delta="pct", is_bar=False, help_txt=None):
    """Karta: etykieta, duża aktualna wartość, pigułka ze zmianą, sparkline."""
    with col:
        with st.container(border=True):
            fig, diff, pct, _ = create_sparkline(df_filtered, column, is_bar=is_bar)
            val = df_filtered[column].iloc[-1]

            bg, fg, arrow = ZIELONY if diff > 0 else CZERWONY if diff < 0 else SZARY
            if delta == "pct":
                delta_txt = f"{pct:+.1f}%".replace(".", ",")
            else:
                delta_txt = fmt_signed(diff)

            st.caption(label, help=help_txt)
            st.markdown(
                f'<div style="font-size:34px;font-weight:500;line-height:1.1;'
                f'margin:4px 0 10px 0;">{fmt_value(val)}</div>'
                f'<div style="margin-bottom:8px;"><span style="background:{bg};'
                f"color:{fg};padding:3px 10px;border-radius:999px;font-size:14px;"
                f'font-weight:600;">{arrow} {delta_txt}</span></div>',
                unsafe_allow_html=True,
            )
            st.plotly_chart(
                fig, use_container_width=True, config={"displayModeBar": False}
            )


st.caption("Zmiana liczona względem pierwszego roku wybranego zakresu.")
c1, c2, c3, c4 = st.columns(4)

kpi_card(c1, "Całkowita liczba ludności", "Liczba ludności ogółem", fmt_int)
kpi_card(c2, "Saldo migracji (osoby)", "Saldo migracji", fmt_signed, is_bar=True)
kpi_card(c3, "Dzieci i młodzież", "Liczba osób w wieku przedprodukcyjnym", fmt_int)
kpi_card(
    c4,
    "Indeks obciążenia",
    "Indeks_Obciążenia",
    fmt_2,
    help_txt="Liczba osób w wieku produkcyjnym przypadająca na jedną osobę w wieku poprodukcyjnym.",
)

st.markdown("---")

# =========================================================
# SEKCJA WYKRESÓW GŁÓWNYCH
# =========================================================
if len(df_filtered) < 2:
    st.info("Wybierz zakres obejmujący co najmniej dwa lata, aby zobaczyć analizę.")
    st.stop()

rok_od, rok_do = selected_years


# ---------- Funkcje pomocnicze ----------
def proc(v, znak=False):
    tekst = f"{v:+.1f}%" if znak else f"{v:.1f}%"
    return tekst.replace(".", ",")


def kierunek(a, b):
    return "wzrosła" if b > a else "spadła" if b < a else "nie zmieniła się"


def styl(fig, tytul_y=None, wysokosc=360):
    """Wspólny wygląd wszystkich wykresów."""
    fig.update_layout(
        template="plotly_white",
        height=wysokosc,
        margin=dict(l=0, r=0, t=10, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0, title_text=""),
        hovermode="x unified",
        xaxis_title=None,
        yaxis_title=tytul_y,
    )
    return fig


# Nazwy kolumn zgodne z kluczami słownika KOLORY (te same zmienne = te same kolory)
df_plot = df_filtered.rename(
    columns={
        "Liczba osób w wieku przedprodukcyjnym": "Przedprodukcyjny",
        "Liczba osób w wieku produkcyjnym": "Produkcyjny",
        "Liczba osób w wieku  poprodukcyjnym": "Poprodukcyjny",
        "Przyrost naturalny (w osobach)": "Przyrost naturalny",
        "Saldo migracji wewnętrznej": "Migracje wewnętrzne",
        "Saldo migracji zagranicznych": "Migracje zagraniczne",
    }
)

# ---------- Dane o przedszkolach ----------
DATA_DIR = Path(__file__).resolve().parents[2] / "data"
LATA_SZKOLNE = {
    "Samorządowe": ["2023-2024", "2024-2025", "2025-2026"],
    "Niesamorządowe": ["2023-2024", "2024-2025"],
}


def _wczytaj_csv(sciezka):
    for kodowanie in ("utf-8-sig", "cp1250"):
        try:
            return pd.read_csv(sciezka, sep=";", encoding=kodowanie)
        except UnicodeDecodeError:
            continue
    return pd.read_csv(sciezka, sep=";", encoding="latin-1")


@st.cache_data
def load_preschool_data():
    """Łączy pięć plików w jedną tabelę (ujednolicone nazwy kolumn)."""
    ramki = []
    for typ, lata in LATA_SZKOLNE.items():
        for rok_szk in lata:
            nazwa = (
                f"Przedszkola {typ.lower()} w roku {rok_szk} "
                "- liczba dzieci i oddziałów.csv"
            )
            sciezka = DATA_DIR / nazwa
            if not sciezka.exists():
                continue
            d = _wczytaj_csv(sciezka)
            d.columns = d.columns.str.strip()
            d = d.rename(
                columns={
                    "Liczba uczniów ogółem": "Liczba dzieci",
                    "Liczba dzieci ogółem": "Liczba dzieci",
                    "Liczba oddziałów ogółem": "Liczba oddziałów",
                }
            )
            if "Miejscowość" in d.columns:
                d = d[
                    d["Miejscowość"].astype(str).str.strip().str.casefold() == "kraków"
                ]
            d["Liczba dzieci"] = pd.to_numeric(d["Liczba dzieci"], errors="coerce")
            d["Liczba oddziałów"] = pd.to_numeric(
                d["Liczba oddziałów"], errors="coerce"
            )
            d["Typ"] = typ
            d["Rok szkolny"] = rok_szk.replace("-", "/")
            ramki.append(
                d[
                    [
                        "Typ",
                        "Rok szkolny",
                        "Numer RSPO",
                        "Liczba dzieci",
                        "Liczba oddziałów",
                    ]
                ]
            )
    return pd.concat(ramki, ignore_index=True) if ramki else pd.DataFrame()


# =========================================================
# 1. KTO SIĘ TU WPROWADZA?
# =========================================================
st.markdown(f"## {ICON_DETECTIVE} Kto się tu wprowadza?", unsafe_allow_html=True)

nat_suma = df_plot["Przyrost naturalny"].sum()
mig_suma = df_plot["Saldo migracji"].sum()

if mig_suma > 0 and mig_suma > nat_suma:
    wniosek_mig = (
        "Miasto rośnie głównie dzięki napływowi nowych mieszkańców, "
        "co zwykle zwiększa popyt na mieszkania na wynajem."
    )
elif mig_suma > 0:
    wniosek_mig = (
        "Na wzrost liczby mieszkańców wpływają zarówno narodziny, jak i napływ."
    )
else:
    wniosek_mig = (
        "W tym okresie napływ nowych mieszkańców nie przekładał się na wzrost."
    )

st.markdown(
    f"W latach **{rok_od}–{rok_do}** saldo migracji wyniosło łącznie "
    f"**{fmt_signed(mig_suma)}** osób, a przyrost naturalny **{fmt_signed(nat_suma)}**. "
    f"{wniosek_mig}"
)

col_a, col_b = st.columns(2)

with col_a:
    st.markdown("##### Skąd bierze się wzrost liczby mieszkańców?")
    fig = px.bar(
        df_plot,
        x="Rok",
        y=["Przyrost naturalny", "Saldo migracji"],
        barmode="group",
        color_discrete_map=KOLORY,
        labels={"value": "Osoby", "variable": ""},
    )
    st.plotly_chart(styl(fig, "Osoby"), use_container_width=True)

with col_b:
    st.markdown("##### Przeprowadzki z Polski i z zagranicy")
    fig = px.bar(
        df_plot,
        x="Rok",
        y=["Migracje wewnętrzne", "Migracje zagraniczne"],
        color_discrete_map=KOLORY,
        labels={"value": "Osoby", "variable": ""},
    )
    fig.add_trace(
        go.Scatter(
            x=df_plot["Rok"],
            y=df_plot["Saldo migracji"],
            mode="lines+markers",
            name="Saldo migracji",
            line=dict(color=KOLORY["Saldo migracji"], width=2.5),
        )
    )
    st.plotly_chart(styl(fig, "Osoby"), use_container_width=True)

st.caption(
    "Migracje wewnętrzne to przeprowadzki z innych miejscowości w Polsce, "
    "zagraniczne – z i za granicę."
)
braki_mig = df_plot.loc[df_plot["Saldo migracji"].isna(), "Rok"].tolist()
if braki_mig:
    st.caption(
        "Brak danych o saldzie migracji za: " + ", ".join(map(str, braki_mig)) + "."
    )

st.markdown("---")

# =========================================================
# 2. KTO TU MIESZKA?
# =========================================================
st.markdown(f"## {ICON_HOUSE} Kto tu mieszka?", unsafe_allow_html=True)

wiek_kol = ["Przedprodukcyjny", "Produkcyjny", "Poprodukcyjny"]
udzialy = df_plot[wiek_kol].div(df_plot[wiek_kol].sum(axis=1), axis=0) * 100
p0, p1 = udzialy.iloc[0], udzialy.iloc[-1]

st.markdown(
    f"Udział dzieci i młodzieży {kierunek(p0['Przedprodukcyjny'], p1['Przedprodukcyjny'])} "
    f"z **{proc(p0['Przedprodukcyjny'])}** do **{proc(p1['Przedprodukcyjny'])}**, "
    f"udział osób w wieku produkcyjnym z **{proc(p0['Produkcyjny'])}** do "
    f"**{proc(p1['Produkcyjny'])}**, a seniorów z **{proc(p0['Poprodukcyjny'])}** do "
    f"**{proc(p1['Poprodukcyjny'])}**. Poniższy wykres pozwala jasno ocenić to, czy Kraków to miasto młodych, "
    "czy raczej starzejące się."
)

grupy = [g for g in wiek_kol if g in selected_age_groups]
if grupy:
    dlugi = df_plot.melt(
        id_vars="Rok", value_vars=grupy, var_name="Grupa", value_name="Liczba osób"
    )
    fig = px.area(
        dlugi,
        x="Rok",
        y="Liczba osób",
        color="Grupa",
        groupnorm="percent",
        color_discrete_map=KOLORY,
        category_orders={"Grupa": grupy},
    )
    fig.update_yaxes(ticksuffix="%")
    st.plotly_chart(styl(fig, "Udział w ludności"), use_container_width=True)
    st.caption("Udziały liczone wśród wybranych grup wiekowych.")
else:
    st.warning("Wybierz co najmniej jedną grupę wiekową w panelu filtrów.")

st.markdown("---")

# =========================================================
# 3. RODZINY Z DZIEĆMI
# =========================================================
st.markdown(f"## {ICON_BABY} Rodziny z dziećmi", unsafe_allow_html=True)

idx_max = df_plot["Urodzenia"].idxmax()
rok_szczyt = int(df_plot.loc[idx_max, "Rok"])
urodz_szczyt = df_plot.loc[idx_max, "Urodzenia"]
urodz_koniec = df_plot["Urodzenia"].iloc[-1]
zmiana_od_szczytu = (urodz_koniec / urodz_szczyt - 1) * 100

st.markdown(
    f"Najwięcej urodzeń w wybranym okresie było w **{rok_szczyt}** "
    f"(**{fmt_int(urodz_szczyt)}**), a w **{rok_do}** – **{fmt_int(urodz_koniec)}** "
    f"({proc(zmiana_od_szczytu, znak=True)} względem szczytu). "
    "Dzieci z kolejnych roczników trafiają do przedszkoli z kilkuletnim opóźnieniem, "
    "więc to one wyznaczają zapotrzebowanie na miejsca w kolejnych latach."
)

col_c, col_d = st.columns(2)

with col_c:
    st.markdown("##### Urodzenia w Krakowie")
    fig = px.bar(
        df_plot,
        x="Rok",
        y="Urodzenia",
        color_discrete_sequence=[KOLORY["Urodzenia"]],
        labels={"Urodzenia": "Urodzenia"},
    )
    st.plotly_chart(styl(fig, "Liczba urodzeń"), use_container_width=True)

podsumowanie_przedszkoli = None
with col_d:
    st.markdown("##### Dzieci w przedszkolach")
    df_prz = load_preschool_data()
    if df_prz.empty:
        st.warning("Nie znaleziono plików z danymi o przedszkolach w folderze data/.")
    else:
        if kindergarten_type != "Wszystkie":
            df_prz = df_prz[df_prz["Typ"] == kindergarten_type]
        pods = df_prz.groupby(["Rok szkolny", "Typ"], as_index=False).agg(
            Dzieci=("Liczba dzieci", "sum"),
            Oddziały=("Liczba oddziałów", "sum"),
            Placówki=("Numer RSPO", "nunique"),
        )
        pods["Dzieci na oddział"] = (pods["Dzieci"] / pods["Oddziały"]).round(1)
        fig = px.bar(
            pods,
            x="Rok szkolny",
            y="Dzieci",
            color="Typ",
            barmode="stack" if kindergarten_type == "Wszystkie" else "group",
            color_discrete_map=KOLORY,
            text_auto=True,
            hover_data={"Placówki": True, "Dzieci na oddział": True},
        )
        fig.update_xaxes(type="category")
        st.plotly_chart(styl(fig, "Liczba dzieci"), use_container_width=True)

        ostatni = pods[pods["Rok szkolny"] == pods["Rok szkolny"].max()]
        czesci = [
            f"{r['Typ'].lower()}: {int(r['Placówki'])} placówek, "
            f"{fmt_int(r['Dzieci'])} dzieci i średnio {str(r['Dzieci na oddział']).replace('.', ',')} "
            "dziecka na oddział"
            for _, r in ostatni.iterrows()
        ]
        podsumowanie_przedszkoli = (
            f"W roku szkolnym {ostatni['Rok szkolny'].iloc[0]} – "
            + "; ".join(czesci)
            + "."
        )
        zakresy = [
            f"{typ.lower()} ({', '.join(g['Rok szkolny'])})"
            for typ, g in pods.groupby("Typ")
        ]
        st.caption(
            "Dostępne lata szkolne: "
            + "; ".join(zakresy)
            + ".  \n"
            + "Wykres <u>nie zależy</u> od suwaka lat.",
            unsafe_allow_html=True,
        )

if podsumowanie_przedszkoli:
    st.markdown(podsumowanie_przedszkoli)

st.markdown("---")

# =========================================================
# 4. JAK ZMIENIAJĄ SIĘ GOSPODARSTWA DOMOWE?
# =========================================================
st.markdown(
    f"## {ICON_USERSWITCH} Jak zmieniają się gospodarstwa domowe?",
    unsafe_allow_html=True,
)

roz_start = df_plot["Rozwody"].iloc[0] / df_plot["Małżeństwa"].iloc[0] * 100
roz_koniec = df_plot["Rozwody"].iloc[-1] / df_plot["Małżeństwa"].iloc[-1] * 100

st.markdown(
    f"Liczba rozwodów na 100 zawartych małżeństw {kierunek(roz_start, roz_koniec)} "
    f"z **{roz_start:.0f}** w {rok_od} r. do **{roz_koniec:.0f}** w {rok_do} r."
)
if roz_koniec > roz_start:
    st.caption(
        "Interpretacja: więcej rozstań i osób mieszkających samodzielnie zwykle "
        "oznacza większy popyt na mniejsze mieszkania. Zbiór nie zawiera jednak danych "
        "o gospodarstwach domowych, <u>zatem jest to raczej hipoteza, a nie czysty wynik odczytany z danych</u>.",
        unsafe_allow_html=True,
    )

fig = px.line(
    df_plot,
    x="Rok",
    y=["Małżeństwa", "Rozwody"],
    markers=True,
    color_discrete_map=KOLORY,
    labels={"value": "Liczba", "variable": ""},
)
st.plotly_chart(styl(fig, "Liczba w roku", wysokosc=320), use_container_width=True)

st.markdown("---")

# =========================================================
# 5. CO TO OZNACZA PRZY SZUKANIU MIESZKANIA?
# =========================================================
st.markdown(
    f"## {ICON_QUESTION} Co to oznacza przy szukaniu mieszkania?",
    unsafe_allow_html=True,
)

if mig_suma > 0:
    punkt_rynek = (
        "**Rynek najmu:** miasto przyciąga nowych mieszkańców, więc o dobre oferty "
        "jest konkurencja. Mimo to, warto rozważyć kilka dzielnic zamiast ograniczać się do jednej."
    )
else:
    punkt_rynek = (
        "**Rynek najmu:** w wybranym okresie napływ nowych mieszkańców był słaby, "
        "co może dawać większe pole do negocjacji. Mimo to, warto porównać wiele ofert, by podjąć najlepszą decyzję."
    )

if zmiana_od_szczytu < 0:
    punkt_rodziny = (
        "**Rodziny z dziećmi:** roczniki są dziś mniejsze niż w szczycie, więc dostęp do "
        "miejsc w przedszkolach może być łatwiejszy niż kilka lat temu. Jest to jednak średnia dla "
        "całego miasta, więc jeśli masz na oku konkretną okolicę, koniecznie ją sprawdź."
    )
else:
    punkt_rodziny = (
        "**Rodziny z dziećmi:** liczba urodzeń jest na szczycie okresu, więc miejsca "
        "w przedszkolach mogą być oblężone. Może to jednak zależeć od dzielnicy, ale mimo to zapisy warto planować z wyprzedzeniem."
    )

st.markdown(f"- {punkt_rynek}\n- {punkt_rodziny}")

st.info(
    "Dane dla całego miasta nie pokazują różnic między dzielnicami. Sprawdź przystanki "
    "i przedszkola przy konkretnej lokalizacji w zakładce **Mapa Miasta i Infrastruktura**."
)

# srednia_mig = df_plot["Saldo migracji"].mean()
# punkty = []
# if pd.notna(srednia_mig):
#     punkty.append(
#         f"**Konkurencja o mieszkania:** średnie roczne saldo migracji w latach "
#         f"{rok_od}–{rok_do} to **{fmt_signed(srednia_mig)}** osób."
#     )
# punkty.append(
#     f"**Rodziny z dziećmi:** liczba urodzeń w {rok_do} r. to {fmt_int(urodz_koniec)} "
#     f"({proc(zmiana_od_szczytu, znak=True)} względem roku {rok_szczyt})."
# )
# if podsumowanie_przedszkoli:
#     punkty.append(f"**Przedszkola:** {podsumowanie_przedszkoli}")
# st.markdown("\n".join(f"- {p}" for p in punkty))

# st.info(
#     "Sprawdź, jak wygląda dostępność przystanków i przedszkoli w wybranej okolicy: "
#     "otwórz zakładkę **Mapa Miasta i Infrastruktura** w menu bocznym."
# )
