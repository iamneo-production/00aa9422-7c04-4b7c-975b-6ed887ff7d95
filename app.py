import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

# from plotly import graph_objs as go
from prophet.plot import plot_plotly

from prophet.serialize import  model_from_json
import requests
import streamlit as st
from streamlit_lottie import st_lottie
from PIL import Image
import folium
from folium.plugins import Search, MarkerCluster
from streamlit_folium import folium_static
import pandas as pd
import geopandas as gpd
import smtplib

from shapely.geometry import Point


with st.container():
    st.write("---")
    st.header("Map")
    cities = {
        'city': ['Adilabad', 'Nizamabad', 'Karimnagar', 'Khammam', 'Warangal'],
        'country': ['India', 'India', 'India', 'India', 'India'],
        'population': [883305, 8537673, 3979576, 2693976, 2345678],
        'latitude': [19.6625054 , 18.6804717 , 18.4348833 , 17.2484683 , 17.9774221],
        'longitude': [78.4953182 , 78.0606503 , 79.0981286 , 80.006904 , 79.52881]
    }

    # Convert the city data to a GeoDataFrame
    geometry = [Point(xy) for xy in zip(cities['longitude'], cities['latitude'])]
    cities_gdf = gpd.GeoDataFrame(cities, geometry=geometry, crs='EPSG:4326')

    # Save the GeoDataFrame to a GeoJSON file
    cities_gdf.to_file('cities.geojson', driver='GeoJSON')



    # Load the city data
    cities = gpd.read_file("cities.geojson")

    # Create a folium map centered on the India
    m = folium.Map(location=[17.9774221, 79.52881], zoom_start=5)

    # Create a GeoJson layer for the city data
    geojson = folium.GeoJson(
        cities,
        name='City Data',
        tooltip=folium.GeoJsonTooltip(
            fields=['city', 'country', 'population'],
            aliases=['City', 'Country', 'Population'],
            localize=True
        )
    ).add_to(m)

    # Add a search bar to the map
    search = Search(
        layer=geojson,
        geom_type='Polygon',
        placeholder='Search for a city',
        collapsed=False,
        search_label='city'
    ).add_to(m)

    folium_static(m)


# ---- CONTACT ----
with st.container():
    st.write("---")
    st.header("Get In Touch With Us")
    st.write("##")

 
    def send_email(name, email, message):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("teamclAImate2023@gmail.com", "balzsvjxdmgtsuts")
        msg = f"Subject: New message from {name}\n\n{name} ({email}) sent the following message:\n\n{message}"
        server.sendmail("teamclAImate2023@gmail.com", "teamclAImate2023@gmail.com", msg)
        st.success("Thank you for contacting us.")
        
    name = st.text_input("Name")
    email = st.text_input("Email")
    message = st.text_area("Message")

    if st.button("Send"):
        send_email(name, email, message)