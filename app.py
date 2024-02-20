import streamlit as st
import requests
import geopandas as gpd
import pandas as pd

# Fetch earthquake data
url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson"
response = requests.get(url)
data = response.json()

# Convert to GeoDataFrame
earthquake_data = {
    'Magnitude': [feature['properties']['mag'] for feature in data['features']],
    'Location': [feature['properties']['place'] for feature in data['features']],
    'lon': [feature['geometry']['coordinates'][0] for feature in data['features']],
    'lat': [feature['geometry']['coordinates'][1] for feature in data['features']]
}
gdf = gpd.GeoDataFrame(earthquake_data, geometry=gpd.points_from_xy(earthquake_data['lon'], earthquake_data['lat']))

# Create map
st.map(gdf)

# Display earthquake information when a marker is clicked
st.write("Earthquake Information:")
selected_index = st.selectbox("Select earthquake:", options=list(range(len(gdf))))
if selected_index is not None:
    selected_earthquake = gdf.iloc[selected_index]
    st.write(f"Magnitude: {selected_earthquake['Magnitude']}")
    st.write(f"Location: {selected_earthquake['Location']}")
