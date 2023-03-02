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


st.set_page_config(page_title="Team cl_AI_mate", page_icon=":tada:", layout="wide")


def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


# Use local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("style/style.css")

# ---- LOAD ASSETS ----
lottie_coding = load_lottieurl("")


st.sidebar.header('Team cl_AI_mate')

st.sidebar.subheader('What you want to Predict?')
time_hist_color = st.sidebar.selectbox('Choose:', ('AQI', 'Heat wave')) 

st.sidebar.subheader('Choose a city:')
donut_theta = st.sidebar.selectbox('Select data', ('Adilabad', 'Nizamabad', 'Karimnagar', 'Khammam', 'Warangal'))

st.sidebar.subheader('Line chart parameters')
plot_data = st.sidebar.multiselect('Select data', ['temperature', 'humidity'], ['temperature', 'humidity'])
plot_height = st.sidebar.slider('Specify plot height', 200, 500, 250)

st.sidebar.markdown('''
---
Created with ❤️ by [Team cl_AI_mate]().
''')
# ---- HEADER SECTION ----
with st.container():
    left_column, right_column = st.columns(2)
    with left_column:
        st.title("Team cl_AI_mate")
        st.title("Heatwave Prediction")
        st.write(
            "Telangana Tier-2 cities - Alidabad, Nizamabad, Karimnagar, Khammam and Warangal."
        )
        st.write("")

    with right_column:
        image = Image.open('images/hw2.jpg')
        st.image(image)
       

# ---- WHAT I DO ----
with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st.header("Our Approach")
        st.write("##")
        st.write(
            """
            The problem statemeint asks you to build a solution to predict two environmental factors in the Tier-2 cities of the Indian state of Telangana: 


            1. Heat Wave Occurrences: Heat waves are prolonged periods of excessively high temperatures, which can have severe impacts on public health and local ecosystems. The task is to develop a solution that can predict when heat waves will occur in the Tier-2 cities of Telangana, to make people aware of the future occurrence of the Heat wave. 

 

            2. Air Quality Index (AQI): AQI is a measure of the air quality in a given location. It takes into account various pollutants in the air and provides a single numerical value that represents the overall air quality. The goal is to predict the AQI in the Tier-2 cities of Telangana to help residents and local authorities make informed decisions about air quality and health. 

  
            The solution should be able to accurately predict both heat wave occurrences and AQI for the time frame January 2023 - December 2023 on a monthly basis, which can help to mitigate their impacts on public health and the environment. 
            """
        )

    with right_column:
        st_lottie(lottie_coding, height=300, key="coding")