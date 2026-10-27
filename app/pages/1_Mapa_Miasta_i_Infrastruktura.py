from html import escape
from pathlib import Path
import geopandas as gpd
import pandas as pd
import folium
import streamlit as st

from folium.plugins import FastMarkerCluster, HeatMap
from streamlit_folium import st_folium
from styles import inject_css
from streamlit_extras.stoggle import *

from address_search import (
    find_nearest,
    format_distance,
    geocode_krakow_address,
)
from geopy.exc import GeocoderServiceError, GeocoderTimedOut


st.set_page_config(
    page_title="Mapa Miasta i Infrastruktura",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_css()

ICON_MAP = (
    '<svg class="ph-icon" width="28" height="28" viewBox="0 0 256 256" '
    'aria-hidden="true"><path d="M228.92,49.69a8,8,0,0,0-6.86-1.45L160.93,63.52,99.07,38.78a8,8,0,0,0-5.99,0L31.08,63.28A8,8,0,0,0,26,70.72V206.72a8,8,0,0,0,11.08,7.43l61-24.4,61.86,24.74a8.13,8.13,0,0,0,3,.59,8,8,0,0,0,3-.59l61-24.4A8,8,0,0,0,230,182.66V46.66A8,8,0,0,0,228.92,49.69ZM96,53.8,160,79.4V202.2L96,176.6ZM42,75.36l42-16.8V180.64l-42,16.8Zm172,105.28-42,16.8V75.36l42-16.8Z"/></svg>'
)

st.markdown(
    f"<h1>{ICON_MAP} Mapa Miasta i Infrastruktura</h1>",
    unsafe_allow_html=True,
    anchors=False,
)

st.caption(
    "Sprawdź rozmieszczenie przystanków komunikacji miejskiej i ich zagęszczenie "
    "w różnych częściach Krakowa."
)

st.markdown(
    """
    <style>
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"],
    [data-testid="stSidebar"] [data-testid="stCheckbox"] label,
    [data-testid="stSidebar"] [data-testid="stCheckbox"] label p {
        color: #FFFFFF !important;
    }

    [data-testid="stSidebar"] [data-testid="stCheckbox"] input[type="checkbox"] {
        accent-color: #2E86C1 !important;
    }

    [data-testid="stSidebar"] [data-testid="stCheckbox"] [role="checkbox"] {
        border-color: #2E86C1 !important;
    }

    [data-testid="stSidebar"] [data-testid="stCheckbox"]
    [role="checkbox"][aria-checked="true"] {
        background-color: #2E86C1 !important;
        border-color: #2E86C1 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
STOPS_FILE = DATA_DIR / "Przystanki_Komunikacji_Miejskiej_w_Krakowie.csv"
PRESCHOOLS_FILE = DATA_DIR / "przedszkola_wspolrzedne.csv"
SOURCE_CRS = "EPSG:3857"

stops_name_column = "Nazwa przystanku z numerem"
stops_type_column = "Rodzaj przystanku"
preschool_name_column = "Nazwa szkoły_placówki"

@st.cache_data(show_spinner="Wczytuję lokalizacje przystanków…")
def load_stops(path: str, modified_at: float) -> gpd.GeoDataFrame:
    """Wczytuje współrzędne przystanków i przelicza je na EPSG:4326."""
    del modified_at  # Wartość służy do odświeżenia cache po zmianie pliku.

    last_error = None
    df = None
    for encoding in ("utf-8-sig", "cp1250", "latin-1"):
        try:
            # sep=None rozpoznaje typowy separator CSV (przecinek lub średnik).
            df = pd.read_csv(path, sep=None, engine="python", encoding=encoding)
            break
        except UnicodeDecodeError as exc:
            last_error = exc

    if df is None:
        raise ValueError("Nie udało się odczytać kodowania pliku CSV.") from last_error

    df.columns = df.columns.astype(str).str.strip()
    required = {"x", "y"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(
            "W pliku przystanków brakuje wymaganych kolumn: "
            + ", ".join(sorted(missing))
            + ". Oczekiwane są kolumny x i y w układzie EPSG:3857."
        )

    df["x"] = pd.to_numeric(df["x"], errors="coerce")
    df["y"] = pd.to_numeric(df["y"], errors="coerce")
    df = df.dropna(subset=["x", "y"]).copy()
    if df.empty:
        return gpd.GeoDataFrame(df, geometry=[], crs="EPSG:4326")

    points = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df["x"], df["y"]),
        crs=SOURCE_CRS,
    ).to_crs("EPSG:4326")
    points = points[
        points.geometry.notna()
        & ~points.geometry.is_empty
        & points.geometry.is_valid
    ].copy()
    return points

@st.cache_data(show_spinner="Wczytuję lokalizacje przedszkoli…")
def load_preschools(path: str, modified_at: float) -> gpd.GeoDataFrame:
    del modified_at  # Odświeża cache po zmianie pliku.

    df = pd.read_csv(path, sep=None, engine="python", encoding="utf-8-sig")
    df.columns = df.columns.astype(str).str.strip()

    # Obsługujemy podaną literówkę oraz poprawną pisownię longitude.
    columns = {column.casefold(): column for column in df.columns}
    longitude_column = columns.get("longitiude") or columns.get("longitude")
    latitude_column = columns.get("latitude")

    if longitude_column is None or latitude_column is None:
        raise ValueError(
            "Plik przedszkoli musi zawierać kolumny "
            "'longitiude' (lub 'longitude') i 'latitude'."
        )

    df[longitude_column] = pd.to_numeric(df[longitude_column], errors="coerce")
    df[latitude_column] = pd.to_numeric(df[latitude_column], errors="coerce")
    df = df.dropna(subset=[longitude_column, latitude_column]).copy()

    # Odrzucamy wartości, które nie mogą być współrzędnymi geograficznymi.
    df = df[
        df[longitude_column].between(-180, 180)
        & df[latitude_column].between(-90, 90)
    ].copy()

    return gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(
            df[longitude_column],
            df[latitude_column],
        ),
        crs="EPSG:4326",
    )

if not STOPS_FILE.is_file():
    st.error(
        "Nie znaleziono pliku z lokalizacjami przystanków. "
        f"Oczekiwana ścieżka: `{STOPS_FILE}`."
    )
    st.stop()

try:
    stops = load_stops(str(STOPS_FILE), STOPS_FILE.stat().st_mtime)
except (OSError, pd.errors.ParserError, ValueError) as exc:
    st.error(f"Nie udało się wczytać danych przystanków: {exc}")
    st.stop()

if stops.empty:
    st.warning("Plik nie zawiera poprawnych współrzędnych przystanków.")
    st.stop()

preschools = None

if not PRESCHOOLS_FILE.is_file():
    st.warning(
        f"Nie znaleziono pliku z lokalizacjami przedszkoli: `{PRESCHOOLS_FILE}`."
    )
else:
    try:
        preschools = load_preschools(
            str(PRESCHOOLS_FILE),
            PRESCHOOLS_FILE.stat().st_mtime,
        )
        if preschools.empty:
            st.warning("Plik przedszkoli nie zawiera poprawnych współrzędnych.")
    except (OSError, pd.errors.ParserError, ValueError) as exc:
        st.error(f"Nie udało się wczytać danych przedszkoli: {exc}")

with st.sidebar:
    st.markdown("### Warstwy mapy")
    points_on = st.checkbox("Punkty przystanków", value=True)
    heatmap_on = st.checkbox("Zagęszczenie przystanków", value=False)
    preschools_on = st.checkbox(
    "Punkty przedszkoli",
    value=preschools is not None and not preschools.empty,
    disabled=preschools is None or preschools.empty,
    )


center = [float(stops.geometry.y.mean()), float(stops.geometry.x.mean())]

# Keeps the map centered
map_margin = 0.03

map_min_lat = float(stops.geometry.y.min()) - map_margin
map_max_lat = float(stops.geometry.y.max()) + map_margin
map_min_lon = float(stops.geometry.x.min()) - map_margin
map_max_lon = float(stops.geometry.x.max()) + map_margin

search_bounds = (
    map_min_lat,
    map_max_lat,
    map_min_lon,
    map_max_lon,
)

st.markdown("### Znajdź najbliższe miejsca")

with st.form("address_search_form"):
    
    st.caption("Wpisz adres bez dodatkowych słów takich jak: 'ul.'\nWyniki wyszukiwania są ograniczone do Krakowa.")

    address_query = st.text_input(
        "Adres",
        placeholder="np. Długa 1",
    )
    search_submitted = st.form_submit_button(
        "Znajdź najbliższe",
        type="primary",
    )


if search_submitted:
    st.session_state.pop("nearest_search_result", None)

    if not address_query.strip():
        st.warning("Wpisz adres.")
    else:
        try:
            geocoded = geocode_krakow_address(
                address_query,
                search_bounds,
            )
        except (GeocoderTimedOut, GeocoderServiceError):
            st.error("Nie udało się połączyć z usługą wyszukiwania adresów.")
            geocoded = None

        if geocoded is None and address_query.strip():
            st.warning(
                "Nie znaleziono adresu w obszarze Krakowa. "
                "Sprawdź pisownię lub podaj nazwę ulicy i numer."
            )
        elif geocoded is not None:
            st.session_state["nearest_search_result"] = {
                "query": address_query.strip(),
                **geocoded,
            }

search_result = st.session_state.get("nearest_search_result")

if search_result:
    nearest_stop = find_nearest(
        stops,
        search_result["latitude"],
        search_result["longitude"],
        name_column=stops_name_column,
        default_name="Przystanek komunikacji miejskiej",
    )
    nearest_preschool = find_nearest(
        preschools,
        search_result["latitude"],
        search_result["longitude"],
        name_column=preschool_name_column,
        default_name="Przedszkole",
    )

    st.caption(
        "Adres jest wysyłany do usługi Nominatim/OpenStreetMap w celu "
        "znalezienia współrzędnych. © OpenStreetMap contributors."
    )

    result_col1, result_col2 = st.columns(2)

    with result_col1:
        if nearest_stop:
            st.metric(
                "Najbliższy przystanek",
                nearest_stop["name"],
                format_distance(nearest_stop["distance_m"]),
            )
        else:
            st.info("Brak danych o przystankach.")

    with result_col2:
        if nearest_preschool:
            nearest_preschool["name"] = str(nearest_preschool["name"]).strip().title()
            st.markdown("**Najbliższe przedszkole**")
            st.markdown(
            f'<div style="font-size: 1.1rem; line-height: 1.35; '
            f'white-space: normal; overflow-wrap: anywhere;">'
            f'{escape(nearest_preschool["name"])}</div>',
            unsafe_allow_html=True,
        )
            st.metric(
            "",
            "",
            format_distance(nearest_preschool["distance_m"]),
            )
            # st.caption(
            #     f"Odległość w linii prostej: "
            #     f"{format_distance(nearest_preschool['distance_m'])}"
            #     )
        else:
            st.info("Brak danych o przedszkolach.")

city_map = folium.Map(
    location=center,
    zoom_start=12,
    min_zoom=11,
    max_bounds=True,
    min_lat=map_min_lat,
    max_lat=map_max_lat,
    min_lon=map_min_lon,
    max_lon=map_max_lon,
    tiles="OpenStreetMap",
    control_scale=True,
)

if points_on:
    # Jeden klaster zamiast budowania setek lub tysięcy obiektów Leaflet w Pythonie.
    # Tooltipy są escapowane przed przekazaniem do JavaScriptu.
    marker_data = []
    marker_columns = ["geometry"]
    if stops_name_column:
        marker_columns.append(stops_name_column)
    if stops_type_column:
        marker_columns.append(stops_type_column)

    for values in stops[marker_columns].itertuples(index=False, name=None):
        point = values[0]
        details = []
        column_index = 1
        if stops_name_column:
            value = values[column_index]
            column_index += 1
            if pd.notna(value) and str(value).strip():
                details.append(f"Przystanek: {escape(str(value).strip())}")
        if stops_type_column:
            value = values[column_index]
            if pd.notna(value) and str(value).strip():
                details.append(f"Rodzaj: {escape(str(value).strip())}")
        tooltip_text = "<br>".join(details) if details else "Przystanek komunikacji miejskiej"
        marker_data.append([point.y, point.x, tooltip_text])

    marker_callback = """
    function (row) {
        var marker = L.marker([row[0], row[1]], {
            icon: L.divIcon({
                className: 'stop-marker-icon',
                html: '<div style="box-sizing:border-box;width:10px;height:10px;border:1px solid #1B3A5C;border-radius:50%;background:#2E86C1;opacity:0.95;"></div>',
                iconSize: [12, 12],
                iconAnchor: [6, 6]
            })
        });
        marker.bindTooltip(row[2], {sticky: true});
        return marker;
    }
    """
    point_layer = folium.FeatureGroup(name="Punkty przystanków", show=True)
    FastMarkerCluster(
        data=marker_data,
        callback=marker_callback,
        name="Punkty przystanków",
        show=True,
        maxClusterRadius=35,
        disableClusteringAtZoom=14,
        spiderfyOnMaxZoom=True,
        showCoverageOnHover=False,
        zoomToBoundsOnClick=True,
    ).add_to(point_layer)
    point_layer.add_to(city_map)

if heatmap_on:
    heat_layer = folium.FeatureGroup(name="Zagęszczenie przystanków", show=True)
    HeatMap(
        [[point.y, point.x] for point in stops.geometry],
        radius=18,
        blur=15,
        min_opacity=0.25,
    ).add_to(heat_layer)
    heat_layer.add_to(city_map)



if preschools_on and preschools is not None:
    preschool_layer = folium.FeatureGroup(
        name="Przedszkola",
        show=True,
    )

    for _, row in preschools.iterrows():
        point = row.geometry
        preschool_name = row.get(preschool_name_column, "Przedszkole")

        if pd.isna(preschool_name) or not str(preschool_name).strip():
            preschool_name = "Przedszkole"
        else:
            preschool_name = str(preschool_name).strip().title()

        tooltip_html = (
            '<div style="width: 380px; max-width: 380px; '
            'white-space: normal; line-height: 1.3;">'
            f'{escape(preschool_name)}'
            '</div>'
        )

        folium.CircleMarker(
            location=[point.y, point.x],
            radius=5,
            color="#1B3A5C",
            fill=True,
            fill_color="#F4A261",
            fill_opacity=0.9,
            weight=1,
            tooltip=folium.Tooltip(tooltip_html, sticky=True),
        ).add_to(preschool_layer)

    preschool_layer.add_to(city_map)

if search_result:
    address_location = [
        search_result["latitude"],
        search_result["longitude"],
    ]

    folium.Marker(
        location=address_location,
        tooltip=f"Wyszukany adres: {search_result['query']}",
        icon=folium.Icon(color="red", icon="home", prefix="fa"),
    ).add_to(city_map)

    if nearest_stop:
        folium.PolyLine(
            [
                address_location,
                [nearest_stop["latitude"], nearest_stop["longitude"]],
            ],
            color="#2E86C1",
            weight=2,
            dash_array="6, 6",
        ).add_to(city_map)

        folium.CircleMarker(
            location=[
                nearest_stop["latitude"],
                nearest_stop["longitude"],
            ],
            radius=9,
            color="#1B3A5C",
            fill=True,
            fill_color="#2E86C1",
            fill_opacity=1,
            tooltip=(
                f"Najbliższy przystanek: {escape(nearest_stop['name'])} "
                f"— {format_distance(nearest_stop['distance_m'])}"
            ),
        ).add_to(city_map)

    if nearest_preschool:
        folium.PolyLine(
            [
                address_location,
                [
                    nearest_preschool["latitude"],
                    nearest_preschool["longitude"],
                ],
            ],
            color="#F4A261",
            weight=2,
            dash_array="6, 6",
        ).add_to(city_map)

        folium.CircleMarker(
            location=[
                nearest_preschool["latitude"],
                nearest_preschool["longitude"],
            ],
            radius=9,
            color="#1B3A5C",
            fill=True,
            fill_color="#F4A261",
            fill_opacity=1,
            tooltip=(
                f"Najbliższe przedszkole: "
                f"{escape(nearest_preschool['name'])} "
                f"— {format_distance(nearest_preschool['distance_m'])}"
            ),
        ).add_to(city_map)

folium.LayerControl(collapsed=False).add_to(city_map)
st.markdown(
    """
    <style>
    .stop-marker-icon { background: transparent; border: 0; }
    .stop-marker-dot {
        display: block; width: 10px; height: 10px;
        border: 1px solid #1B3A5C; border-radius: 50%;
        background: #2E86C1; opacity: 0.9;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
st_folium(
    city_map,
    use_container_width=True,
    height=650,
    key="city_map",
)
st.caption(
    f"Na mapie pokazano {len(stops):,} lokalizacji przystanków, {len(preschools):,} lokalizacji przedszkoli. "
    "Punkty opisują miejsca przystanków; dostępne dane nie pokazują przebiegu tras "
    "ani częstotliwości kursowania."
)

stoggle(
    "Czym jest heatmapa?",
    """Heatmapa (mapa cieplna) to graficzny sposób przedstawienia danych za pomocą kolorów. 
    Ciepłe kolory to miejsca "gorące" tam gdzie punktów jest najwięcej, a zimne kolory, takie jak niebieski i zielony to miejsca gdzie punktów jest mniej.
    Spróbuj włączyć "Zagęszczenie przystanków" na mapie, aby ją zobaczyć.""",
)

stoggle(
    "Jak liczona jest odległość do najbliższych punktów?",
    """Dla uproszczenia odległość jest liczona w linii prostej. Wpisany adres jest zamieniany
    na współrzędne i liczona jest odległość od wszystkich punktów na mapie. Najmniejsza wartość to najbliższy punkt.""",
)