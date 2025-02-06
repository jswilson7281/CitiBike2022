import streamlit as st
import pandas as pd 
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static 
from keplergl import KeplerGl
from datetime import datetime as dt 

st.set_page_config(page_title = 'Divvy Bikes Strategy Dashboard', layout='wide')
st.title("Divvy Bikes Strategy Dashboard")
st.markdown("The dashboard will help with the expansion problems Divvy currently faces")

####################### Import data #########################################

df = pd.read_csv('final_df.csv', index_col = 0)
top20 = df.nlargest(n=20,columns='bike_rides_daily')

# ########################### DEFINE THE CHARTS ############################


## Bar chart 

fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value'], marker = {'color' : top20['value'], 'colorscale' : 'Blues'}))
fig.update_layout(
    title = 'Top 20 Most Popular Bike Stations in NYC',
    xaxis_title = 'Start Stations', 
    yaxis_title = 'Sum of Trips', 
    width = 900, height = 600
)
st.plotly_chart(fig, use_container_width = True)

## line chart 

fig_2 = make_subplots(specs = [[{'secondary_y': True}]])

fig_2.add_trace(
go.Scatter(x = df['date'], y = df['bike_rides_daily'], name = 'Daily bike rides', marker={'color': df['bike_rides_daily'], 'color': 'blue'}), secondary_y = False
)

fig_2.add_trace(
go.Scatter(x = df['date'], y = df['avgTemp'], name = 'Daily temperature', marker={'color': df['avgTemp'], 'color': 'red'}), secondary_y = True)


fig_2.update_layout(
    title = 'Top 20 most popular bike stations in NYC', 
    xaxis_title = 'Start stations',
    yaxis_title = 'Sum of trips',
    height = 800
)

st.plotly_chart(fig_2, use_container_width=True)

### Add the map  ###

path_to_html = "keplergl.html"


with open(path_to_html, 'r') as f:
    html_data = f.read()
## Show in web page 
st.header("Aggregated Bike Trips in Chicago")
st.components.v1.html(html_data,height = 1000)


            