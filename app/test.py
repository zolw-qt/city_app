import streamlit as st
from pathlib import Path
import pandas as pd
import geopandas as gpd

import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

DATA_DIR = Path("../data")

st.set_page_config(
    page_title="Miasto w danych",
    layout="wide"
)

st.title("Miasto w danych")
st.write(
    "Interaktywna mapa rozmieszczenia przystanków "
    "komunikacji miejskiej"
)


@st.cache_data
def load_points(path):
    df = pd.read_csv(path)

    df["x"] = pd.to_numeric(df["x"], errors="coerce")
    df["y"] = pd.to_numeric(df["y"], errors="coerce")
    df = df.dropna(subset=["x", "y"]).copy()

    # Źródłowy układ współrzędnych
    gdf = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df["x"], df["y"]),
        crs="EPSG:3857"
    )

    # Układ wymagany przez Folium
    return gdf.to_crs("EPSG:4326")


stops = load_points(f"{DATA_DIR}/Przystanki_Komunikacji_Miejskiej_w_Krakowie.csv")


all_lat = pd.concat([
    stops.geometry.y,
])
all_lon = pd.concat([
    stops.geometry.x,
])



center = [all_lat.mean(), all_lon.mean()]

stops_on = st.sidebar.checkbox(
    "Heatmapa przystanków", value=True
)


m = folium.Map(
    location=center,
    zoom_start=12,
    tiles="OpenStreetMap"
)

# --- PUNKTY PRZYSTANKÓW ---
stop_points = folium.FeatureGroup(
    name="Punkty przystanków",
    show=True
)

for _, row in stops.iterrows():
    point = row.geometry

    if point is None or point.is_empty:
        continue

    name = row.get('Nazwa przystanku z numerem')
    type = str(row.get('Rodzaj przystanku')).upper()

    info = (
            f"Przystanek: {name}\n"
            f"Rodzaj przystanku: {type}"
        )

    folium.CircleMarker(
        location=[point.y, point.x],
        radius=4,
        color="blue",
        fill=True,
        fill_color="blue",
        fill_opacity=0.85,
        weight=1,
        tooltip=folium.Tooltip(
            info.replace("\n", "<br>"),
            sticky=False)

    ).add_to(stop_points)

    

stop_points.add_to(m)

stop_layer = folium.FeatureGroup(
    name="Przystanki",
    show=stops_on
)

HeatMap(
    [
        [point.y, point.x]
        for point in stops.geometry
        if point is not None and not point.is_empty
    ],
    radius=18,
    blur=15
).add_to(stop_layer)

stop_layer.add_to(m)

# # Warstwa przedszkoli
# preschool_layer = folium.FeatureGroup(
#     name="Przedszkola",
#     show=preschools_on
# )

# HeatMap(
#     [
#         [point.y, point.x]
#         for point in preschools.geometry
#         if point is not None and not point.is_empty
#     ],
#     radius=20,
#     blur=15
# ).add_to(preschool_layer)

# preschool_layer.add_to(m)

# Przełączniki warstw dostępne również na mapie
folium.LayerControl(collapsed=False).add_to(m)

# Wyświetlenie mapy bezpośrednio w Streamlit
st_folium(
    m,
    use_container_width=True,
    height=650,
    key="city_map"
)
