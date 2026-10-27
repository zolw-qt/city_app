import geopandas as gpd
import streamlit as st
from geopy.exc import GeocoderServiceError, GeocoderTimedOut
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim
from shapely.geometry import Point


@st.cache_resource
def _get_nominatim_limiter():
    geolocator = Nominatim(
        user_agent="krakow_infrastructure_app",
        timeout=10,
    )
    return RateLimiter(
        geolocator.geocode,
        min_delay_seconds=1.1,
        max_retries=0,
        swallow_exceptions=False,
    )


@st.cache_data(ttl=24 * 60 * 60, show_spinner=False)
def geocode_krakow_address(address, bounds):
    """Zamienia adres na współrzędne; wynik jest buforowany przez 24 godziny."""
    address = address.strip()
    if not address:
        return None

    min_lat, max_lat, min_lon, max_lon = bounds
    viewbox = [
        (max_lat, min_lon),  # północny zachód
        (min_lat, max_lon),  # południowy wschód
    ]

    location = _get_nominatim_limiter()(
        f"{address}, Kraków, Polska",
        exactly_one=True,
        country_codes="pl",
        language="pl",
        addressdetails=True,
        viewbox=viewbox,
        bounded=True,
    )

    if location is None:
        return None

    return {
        "latitude": float(location.latitude),
        "longitude": float(location.longitude),
        "display_name": location.address,
    }


def find_nearest(points, latitude, longitude, name_column=None, default_name="Punkt"):
    """Zwraca najbliższy punkt i odległość w metrach."""
    if points is None or points.empty:
        return None

    points_m = points.to_crs("EPSG:2180")
    address_point = gpd.GeoSeries(
        [Point(longitude, latitude)],
        crs="EPSG:4326",
    ).to_crs("EPSG:2180").iloc[0]

    distances = points_m.geometry.distance(address_point)
    nearest_index = distances.idxmin()
    nearest_row = points.loc[nearest_index]

    name = default_name
    if name_column and name_column in points.columns:
        value = nearest_row.get(name_column)
        if value is not None and str(value).strip():
            name = str(value).strip()

    return {
        "name": name,
        "latitude": float(nearest_row.geometry.y),
        "longitude": float(nearest_row.geometry.x),
        "distance_m": float(distances.loc[nearest_index]),
    }


def format_distance(distance_m):
    if distance_m < 1000:
        return f"{distance_m:.0f} m"
    return f"{distance_m / 1000:.2f} km"