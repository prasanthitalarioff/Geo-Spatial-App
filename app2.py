import streamlit as st
import requests
import pandas as pd
from streamlit_folium import folium_static
import folium

# Fetch earthquake data from the USGS API
url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson"
response = requests.get(url)
data = response.json()
print(response)

# Extract relevant information from the GeoJSON data
earthquake_data = []
for feature in data['features']:
    properties = feature['properties']
    geometry = feature['geometry']
    coordinates = geometry['coordinates']
    magnitude = properties['mag']
    place = properties['place']
    time = pd.to_datetime(properties['time'], unit='ms')
    earthquake_data.append({
        'Magnitude': magnitude,
        'Location': place,
        'Time': time,
        'Coordinates': (coordinates[1], coordinates[0])  # Folium uses (latitude, longitude)
    })

# Create a DataFrame
df_earthquakes = pd.DataFrame(earthquake_data)

# Streamlit app
st.title("Earthquake Data Explorer")

# Create a Folium map
m = folium.Map(location=[0, 0], zoom_start=2, width='100%', height='100%')

# Display earthquake markers on the map
for index, row in df_earthquakes.iterrows():
    folium.Marker(location=row['Coordinates'],
                  popup=f"Magnitude: {row['Magnitude']}<br> Location: {row['Location']}<br> Date_Time: {row['Time']}"
                  ).add_to(m)

# Display the map in Streamlit
folium_static(m)
