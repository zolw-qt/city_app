from html import escape
import math
import json
from pathlib import Path
import geopandas as gpd
import pandas as pd
import folium
import streamlit as st
from shapely.geometry import MultiPoint, Point, Polygon, box
from shapely.ops import voronoi_diagram
from shapely.strtree import STRtree

from folium.plugins import FastMarkerCluster, HeatMap
from streamlit_folium import st_folium
from styles import inject_css
from streamlit_extras.stoggle import stoggle

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
    "Sprawdź rozmieszczenie punktów przystanków komunikacji miejskiej i ich zagęszczenie "
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


def _projected_geojson(geometries, properties=None) -> str:
    """Serializuje geometrie w EPSG:2180 jako GeoJSON w EPSG:4326."""
    frame = gpd.GeoDataFrame(
        properties or {},
        geometry=geometries,
        crs="EPSG:2180",
    ).to_crs("EPSG:4326")
    return frame.to_json(drop_id=True)


@st.cache_data(show_spinner=False)
def build_hexagons_geojson(projected_coords, bounds, hex_radius_m=350) -> str:
    """Agreguje punkty do heksagonów w metrycznym układzie EPSG:2180."""
    counts = {}
    root3 = 3**0.5

    def cube_round(q_float, r_float):
        x_float = q_float
        z_float = r_float
        y_float = -x_float - z_float
        x_round, y_round, z_round = round(x_float), round(y_float), round(z_float)
        x_diff = abs(x_round - x_float)
        y_diff = abs(y_round - y_float)
        z_diff = abs(z_round - z_float)
        if x_diff > y_diff and x_diff > z_diff:
            x_round = -y_round - z_round
        elif y_diff > z_diff:
            y_round = -x_round - z_round
        else:
            z_round = -x_round - y_round
        return x_round, z_round

    for x_coord, y_coord in projected_coords:
        q_float = (root3 / 3 * x_coord - y_coord / 3) / hex_radius_m
        r_float = (2 / 3 * y_coord) / hex_radius_m
        cell = cube_round(q_float, r_float)
        counts[cell] = counts.get(cell, 0) + 1

    clip_area = box(*bounds)
    geometries = []
    cell_counts = []
    for (q, r), count in counts.items():
        center_x = hex_radius_m * root3 * (q + r / 2)
        center_y = hex_radius_m * 1.5 * r
        vertices = [
            (
                center_x + hex_radius_m * math.cos(math.radians(30 + 60 * angle)),
                center_y + hex_radius_m * math.sin(math.radians(30 + 60 * angle)),
            )
            for angle in range(6)
        ]
        clipped = Polygon(vertices).intersection(clip_area)
        if not clipped.is_empty:
            geometries.append(clipped)
            cell_counts.append(count)

    return _projected_geojson(geometries, {"count": cell_counts})


@st.cache_data(show_spinner=False)
def build_voronoi_geojson(projected_sites, bounds) -> str:
    """Buduje komórki Voronoi z etykietą najbliższego punktu."""
    sites_by_coordinate = {}
    for x_coord, y_coord, name in projected_sites:
        key = (round(x_coord, 2), round(y_coord, 2))
        if key not in sites_by_coordinate:
            sites_by_coordinate[key] = {
                "coordinate": (x_coord, y_coord),
                "names": [],
            }
        if name and name not in sites_by_coordinate[key]["names"]:
            sites_by_coordinate[key]["names"].append(name)

    unique_coords = tuple(
        site["coordinate"] for site in sites_by_coordinate.values()
    )
    site_names = [
        escape(", ".join(site["names"]))
        for site in sites_by_coordinate.values()
    ]
    if len(unique_coords) < 2:
        return _projected_geojson([], {})

    map_area = box(*bounds)
    diagram = voronoi_diagram(
        MultiPoint(unique_coords),
        envelope=map_area,
        edges=False,
    )
    site_tree = STRtree([Point(coordinate) for coordinate in unique_coords])
    cells = []
    nearest_names = []
    for cell in diagram.geoms:
        clipped_cell = cell.intersection(map_area)
        if clipped_cell.is_empty:
            continue
        nearest_index = int(site_tree.nearest(clipped_cell.representative_point()))
        cells.append(clipped_cell)
        nearest_names.append(site_names[nearest_index])

    return _projected_geojson(cells, {"nearest_name": nearest_names})


def add_hexagon_layer(city_map, data, layer_name, color, count_alias):
    features = json.loads(data).get("features", [])
    max_count = max(
        (feature["properties"]["count"] for feature in features),
        default=1,
    )
    palette = ["#F1F5F9", "#CBD5E1", "#94A3B8", color]

    def style_hexagon(feature):
        count = feature["properties"]["count"]
        color_index = min(int((count / max_count) * len(palette)), len(palette) - 1)
        return {
            "color": color,
            "weight": 1,
            "fillColor": palette[color_index],
            "fillOpacity": 0.65,
        }

    folium.GeoJson(
        data,
        name=layer_name,
        style_function=style_hexagon,
        tooltip=folium.GeoJsonTooltip(
            fields=["count"],
            aliases=[count_alias],
            localize=True,
        ),
    ).add_to(city_map)


def add_voronoi_layer(city_map, data, layer_name, color, tooltip_alias):
    folium.GeoJson(
        data,
        name=layer_name,
        style_function=lambda feature: {
            "color": color,
            "weight": 1,
            "fillColor": color,
            "fillOpacity": 0.12,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=["nearest_name"],
            aliases=[tooltip_alias],
            sticky=True,
        ),
    ).add_to(city_map)


MAX_ACTIVE_LAYERS = 4
LAYER_STATE_DEFAULTS = {
    "layer_stops_points": True,
    "layer_stops_heatmap": False,
    "layer_stops_hexagons": False,
    "layer_stops_voronoi": False,
    "layer_preschools_points": False,
    "layer_preschools_heatmap": False,
    "layer_preschools_hexagons": False,
    "layer_preschools_voronoi": False,
}


def enforce_layer_limit(changed_key):
    active_layers = sum(
        bool(st.session_state.get(key, False)) for key in LAYER_STATE_DEFAULTS
    )
    if active_layers > MAX_ACTIVE_LAYERS:
        st.session_state[changed_key] = False
        st.session_state["layer_limit_notice"] = True
    else:
        st.session_state["layer_limit_notice"] = False


def layer_checkbox(label, key, disabled=False):
    return st.checkbox(
        label,
        key=key,
        disabled=disabled,
        on_change=enforce_layer_limit,
        args=(key,),
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

LAYER_STATE_DEFAULTS["layer_preschools_points"] = (
    preschools is not None and not preschools.empty
)

with st.sidebar:
    st.markdown("### Warstwy mapy")
    if preschools is None or preschools.empty:
        for key in (
            "layer_preschools_points",
            "layer_preschools_heatmap",
            "layer_preschools_hexagons",
            "layer_preschools_voronoi",
        ):
            st.session_state[key] = False
    for key, default in LAYER_STATE_DEFAULTS.items():
        st.session_state.setdefault(key, default)

    points_on = layer_checkbox("Punkty przystanków", "layer_stops_points")
    heatmap_on = layer_checkbox(
        "Zagęszczenie punktów przystanków",
        "layer_stops_heatmap",
    )
    stops_hexagons_on = layer_checkbox(
        "Heksagony punktów przystanków",
        "layer_stops_hexagons",
    )
    stops_voronoi_on = layer_checkbox(
        "Voronoi punktów przystanków",
        "layer_stops_voronoi",
    )
    preschools_on = layer_checkbox(
        "Punkty przedszkoli",
        "layer_preschools_points",
        disabled=preschools is None or preschools.empty,
    )
    preschool_heatmap_on = layer_checkbox(
        "Zagęszczenie punktów przedszkoli",
        "layer_preschools_heatmap",
        disabled=preschools is None or preschools.empty,
    )
    preschools_hexagons_on = layer_checkbox(
        "Heksagony punktów przedszkoli",
        "layer_preschools_hexagons",
        disabled=preschools is None or preschools.empty,
    )
    preschools_voronoi_on = layer_checkbox(
        "Voronoi punktów przedszkoli",
        "layer_preschools_voronoi",
        disabled=preschools is None or preschools.empty,
    )
    if st.session_state.get("layer_limit_notice"):
        st.markdown(
            """
            <style>
            .layer-limit-notice {
                color: #FFFFFF !important;
                background: rgba(255, 255, 255, 0.10);
                border-left: 4px solid #8AB4F8;
                border-radius: 0.4rem;
                padding: 0.65rem 0.8rem;
            }
            </style>
            <div class="layer-limit-notice">
                Możesz włączyć maksymalnie 4 warstwy naraz. Odznacz jedną z aktywnych warstw, aby włączyć kolejną.
            </div>
            """,
            unsafe_allow_html=True,
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

derived_maps_requested = any(
    (
        stops_hexagons_on,
        stops_voronoi_on,
        preschools_hexagons_on,
        preschools_voronoi_on,
    )
)
if derived_maps_requested:
    stops_metric = stops.to_crs("EPSG:2180")
    stops_projected_coords = tuple(
        zip(stops_metric.geometry.x.tolist(), stops_metric.geometry.y.tolist())
    )
    stops_projected_sites = tuple(
        (
            float(point.x),
            float(point.y),
            str(name).strip() if pd.notna(name) and str(name).strip() else "Przystanek komunikacji miejskiej",
        )
        for point, name in zip(
            stops_metric.geometry,
            stops[stops_name_column]
            if stops_name_column in stops.columns
            else ["Przystanek komunikacji miejskiej"] * len(stops),
        )
    )
    map_area = gpd.GeoSeries(
        [box(map_min_lon, map_min_lat, map_max_lon, map_max_lat)],
        crs="EPSG:4326",
    ).to_crs("EPSG:2180").iloc[0]
    if preschools is not None and not preschools.empty:
        preschools_metric = preschools.to_crs("EPSG:2180")
        preschools_projected_coords = tuple(
            zip(
                preschools_metric.geometry.x.tolist(),
                preschools_metric.geometry.y.tolist(),
            )
        )
        preschools_projected_sites = tuple(
            (
                float(point.x),
                float(point.y),
                str(name).strip().title()
                if pd.notna(name) and str(name).strip()
                else "Przedszkole",
            )
            for point, name in zip(
                preschools_metric.geometry,
                preschools[preschool_name_column]
                if preschool_name_column in preschools.columns
                else ["Przedszkole"] * len(preschools),
            )
        )
        all_projected_coords = stops_projected_coords + preschools_projected_coords
    else:
        preschools_projected_coords = ()
        preschools_projected_sites = ()
        all_projected_coords = stops_projected_coords

    min_x, min_y, max_x, max_y = map_area.bounds
    points_min_x = min(point[0] for point in all_projected_coords)
    points_min_y = min(point[1] for point in all_projected_coords)
    points_max_x = max(point[0] for point in all_projected_coords)
    points_max_y = max(point[1] for point in all_projected_coords)
    voronoi_bounds = (
        min(min_x, points_min_x) - 10,
        min(min_y, points_min_y) - 10,
        max(max_x, points_max_x) + 10,
        max(max_y, points_max_y) + 10,
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
                "Odległość w linii prostej",
                "",
                format_distance(nearest_preschool["distance_m"]),
            )
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
                html: '<div style="box-sizing:border-box;width:10px;height:10px;border:1px solid #34205F;border-radius:50%;background:#4B2E83;opacity:0.95;"></div>',
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
    heat_layer = folium.FeatureGroup(name="Zagęszczenie punktów przystanków", show=True)
    HeatMap(
        [[point.y, point.x] for point in stops.geometry],
        radius=18,
        blur=15,
        min_opacity=0.25,
    ).add_to(heat_layer)
    heat_layer.add_to(city_map)

if preschool_heatmap_on and preschools is not None and not preschools.empty:
    preschool_heat_layer = folium.FeatureGroup(
        name="Zagęszczenie punktów przedszkoli",
        show=True,
    )
    HeatMap(
        [[point.y, point.x] for point in preschools.geometry],
        radius=18,
        blur=15,
        min_opacity=0.25,
    ).add_to(preschool_heat_layer)
    preschool_heat_layer.add_to(city_map)

if stops_hexagons_on:
    stops_hexagons = build_hexagons_geojson(
        stops_projected_coords,
        voronoi_bounds,
    )
    add_hexagon_layer(
        city_map,
        stops_hexagons,
        "Heksagony punktów przystanków",
        "#4B2E83",
        "Liczba punktów przystanków w heksagonie:",
    )

if stops_voronoi_on:
    stops_voronoi = build_voronoi_geojson(
        stops_projected_sites,
        voronoi_bounds,
    )
    add_voronoi_layer(
        city_map,
        stops_voronoi,
        "Voronoi punktów przystanków",
        "#4B2E83",
        "Najbliższy przystanek:",
    )

if preschools_hexagons_on and preschools_projected_coords:
    preschools_hexagons = build_hexagons_geojson(
        preschools_projected_coords,
        voronoi_bounds,
    )
    add_hexagon_layer(
        city_map,
        preschools_hexagons,
        "Heksagony punktów przedszkoli",
        "#2E8B57",
        "Liczba punktów przedszkoli w heksagonie:",
    )

if preschools_voronoi_on and preschools_projected_coords:
    preschools_voronoi = build_voronoi_geojson(
        preschools_projected_sites,
        voronoi_bounds,
    )
    add_voronoi_layer(
        city_map,
        preschools_voronoi,
        "Voronoi punktów przedszkoli",
        "#2E8B57",
        "Najbliższe przedszkole:",
    )



if preschools_on and preschools is not None:
    preschool_layer = folium.FeatureGroup(
        name="Punkty przedszkoli",
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
            color="#1F6B45",
            fill=True,
            fill_color="#2E8B57",
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
            color="#4B2E83",
            weight=2,
            dash_array="6, 6",
        ).add_to(city_map)

        folium.CircleMarker(
            location=[
                nearest_stop["latitude"],
                nearest_stop["longitude"],
            ],
            radius=9,
            color="#34205F",
            fill=True,
            fill_color="#4B2E83",
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
            color="#2E8B57",
            weight=2,
            dash_array="6, 6",
        ).add_to(city_map)

        folium.CircleMarker(
            location=[
                nearest_preschool["latitude"],
                nearest_preschool["longitude"],
            ],
            radius=9,
            color="#1F6B45",
            fill=True,
            fill_color="#2E8B57",
            fill_opacity=1,
            tooltip=(
                f"Najbliższe przedszkole: "
                f"{escape(nearest_preschool['name'])} "
                f"— {format_distance(nearest_preschool['distance_m'])}"
            ),
        ).add_to(city_map)

legend = folium.Element(
    '<div style="position:fixed;bottom:28px;left:12px;z-index:9999;'
    'background:rgba(255,255,255,.96);padding:10px 13px;border:1px solid #bbb;'
    'border-radius:5px;box-shadow:0 1px 5px #999;font:14px/1.6 Arial,sans-serif;">'
    '<strong>Legenda</strong><br>'
    '<span style="display:inline-block;width:11px;height:11px;border-radius:50%;'
    'background:#4B2E83;border:1px solid #34205F;margin-right:7px;"></span>'
    'Punkty przystanków<br>'
    '<span style="display:inline-block;width:11px;height:11px;border-radius:50%;'
    'background:#2E8B57;border:1px solid #1F6B45;margin-right:7px;"></span>'
    'Punkty przedszkoli<br>'
    '<span style="display:inline-block;width:12px;height:12px;background:#94A3B8;'
    'border:1px solid #4B2E83;margin-right:7px;"></span>'
    'Heksagony: liczba punktów w komórce<br>'
    '<span style="display:inline-block;width:12px;height:12px;background:#FFFFFF;'
    'border:2px solid #4B2E83;margin-right:7px;"></span>'
    'Voronoi: obszar najbliższej lokalizacji<br>'
    '<span style="display:inline-block;width:54px;height:9px;vertical-align:middle;'
    'background:linear-gradient(to right,blue,lime,red);margin-right:7px;"></span>'
    'Heatmapy: większe zagęszczenie lokalizacji</div>'
)
city_map.get_root().html.add_child(legend)
st.markdown(
    """
    <style>
    .stop-marker-icon { background: transparent; border: 0; }
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
    f"Na mapie pokazano {len(stops):,} punktów przystanków, {len(preschools):,} punktów przedszkoli. "
    "Heatmapy pokazują skupiska lokalizacji, a nie jakość placówek ani liczbę miejsc. "
    "Dane o przystankach nie pokazują przebiegu tras ani częstotliwości kursowania."
)

stoggle(
    "Czym jest heatmapa?",
    """Heatmapa (mapa cieplna) to graficzny sposób przedstawienia danych za pomocą kolorów. 
    Cieplejszy kolor oznacza większe skupienie lokalizacji w danym obszarze, a chłodniejszy — mniejsze. Heatmapa nie pokazuje liczby miejsc w placówkach ani częstotliwości kursowania.
    Spróbuj włączyć "Zagęszczenie punktów przystanków" lub "Zagęszczenie punktów przedszkoli" w panelu bocznym.""",
)

stoggle(
    "Czym są heksagony?",
    """Heksagony dzielą mapę na równe komórki. Liczba w komórce pokazuje liczbę punktów przystanków lub punktów przedszkoli, zależnie od wybranej warstwy. Najedź na komórkę, aby sprawdzić dokładną wartość.""",
)

stoggle(
    "Czym jest diagram Voronoi?",
    """Voronoi dzieli mapę na obszary przypisane do najbliższych lokalizacji. Każdy obszar zawiera miejsca, z których najbliżej jest do wyznaczającego go punktu przystanku lub przedszkola. Podział opiera się na odległości w linii prostej. Diagram Voronoi nosi nazwę na cześć matematyka Georgija Woronogo.""",
)

stoggle(
    "Jak liczona jest odległość do najbliższych punktów?",
    """Dla uproszczenia odległość jest liczona w linii prostej. Wpisany adres jest zamieniany
    na współrzędne i liczona jest odległość od wszystkich punktów na mapie. Najmniejsza wartość to najbliższy punkt.""",
)
