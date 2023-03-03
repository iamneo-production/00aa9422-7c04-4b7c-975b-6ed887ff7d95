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
lottie_coding = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json")


st.sidebar.header('Team cl_AI_mate')

st.sidebar.subheader('What you want to Predict?')
time_hist_color = st.sidebar.selectbox('Choose:', ('AQI', 'Heat wave')) 

# st.sidebar.subheader('Choose a city:')
# donut_theta = st.sidebar.selectbox('Select data', ('Adilabad', 'Nizamabad', 'Karimnagar', 'Khammam', 'Warangal'))

# st.sidebar.subheader('Line chart parameters')
# plot_data = st.sidebar.multiselect('Select data', ['temperature', 'humidity'], ['temperature', 'humidity'])
# plot_height = st.sidebar.slider('Specify plot height', 200, 500, 250)

st.sidebar.markdown('''
---
Created with ❤️ by Team cl_AI_mate

''')
                    


with open('Architecture.pdf', "rb") as f:
    data = f.read()
b64 = base64.b64encode(data).decode("utf-8")
pdf_display = f'<embed src="data:application/pdf;base64,{b64}" width="300" height="600" type="application/pdf">'
st.sidebar.markdown(pdf_display, unsafe_allow_html=True)


# ---- HEADER SECTION ----
with st.container():
    left_column, right_column = st.columns(2)
    with left_column:
        st.title("Team cl_AI_mate")
        st.title("Heatwave Prediction")
        st.write(
            "Telangana Tier-2 cities - Alidabad, Nizamabad, Karimnagar, Khammam and Warangal."
        )
        st.write("Learn More >")

    with right_column:
        image = Image.open('images/hw2.jpg')
        st.image(image)
       


      



def prepare(df):
   df['datetime'] = pd.to_datetime(df['datetime'])
   df.set_index('datetime', inplace=True)
   df = df.resample('d').max()
   df = df.reset_index()
   df['date'] = df['datetime'].dt.date
   df.set_index('date', inplace=True)
   T=(df['temp']*9/5)+32  
   df['temp']=T
   R=df['humidity']
   hi = -42.379 + 2.04901523*T + 10.14333127*R - 0.22475541*T*R - 6.83783*(10*-3)(T*T) - 5.481717*(10*-2)*R*R + 1.22874(10*-3)*T*T*R + 8.5282(10*-4)*T*R*R - 1.99(10**-6)*T*T*R*R
   df['heat_index'] = hi
   return df

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