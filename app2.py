import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from datetime import datetime as dt
from numerize.numerize import numerize
from PIL import Image

########################### Initial settings for the dashboard ####################################################


st.set_page_config(page_title = 'CitiBike Bikes Strategy Dashboard', layout='wide')
st.title("CitiBike Bikes Strategy Dashboard")
st.markdown("The dashboard will help with the expansion problems CitiBike currently faces")

# Define side bar
st.sidebar.title("Aspect Selector")
page = st.sidebar.selectbox('Select an aspect of the analysis',
  ["Intro page","Weather component and bike usage",
   "Most popular stations",
    "Interactive map with aggregated bike trips", "Recommendations"])

########################## Import data ###########################################################################################

df = pd.read_csv('final_df.csv', index_col = 0)
station_df= df.drop_duplicates(subset='start_station_name')
top20 = station_df.nlargest(n=20,columns='bike_rides_daily')

######################################### DEFINE THE PAGES #####################################################################


### Intro page

if page == "Intro page":
    st.markdown("#### This dashboard aims at providing helpful insights on the expansion problems CitiBike Bikes currently faces.")
    st.markdown("Right now, CitiBike bikes runs into a situation where customers complain about bikes not being available at certain times. This analysis will look at the potential reasons behind this. The dashboard is separated into 4 sections:")
    st.markdown("- Most popular stations")
    st.markdown("- Weather component and bike usage")
    st.markdown("- Interactive map with aggregated bike trips")
    st.markdown("- Recommendations")
    st.markdown("The dropdown menu on the left 'Aspect Selector' will take you to the different aspects of the analysis our team looked at.")

    #myImage = Image.open("Divvy_Bikes.jpg") #source: https://ride.divvybikes.com/blog/new-divvy-ebike
    #st.image(myImage)


    ### Create the dual axis line chart page ###
    
elif page == 'Weather component and bike usage':

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

    st.markdown("The coorelation between warmer weather months and rentals of bikes is obvious. When the weather is at a higher average the number of bikes rented in the city is also at a higher rate. This could lead to a shortage of available bikes during these warmer months.")

### Most popular stations page

    # Create the season variable

elif page == 'Most popular stations':
    
    # Create the filter on the side bar
    
    with st.sidebar:
        season_filter = st.multiselect(label= 'Select the season', options=df['season'].unique(),
    default=df['season'].unique())

    df1 = df.query('season == @season_filter')
    
    # Define the total rides
    total_rides = float(df1['bike_rides_daily'].count())    
    st.metric(label = 'Total Bike Rides', value= numerize(total_rides))
    
    # Bar chart

    fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['bike_rides_daily'], marker = {'color' : top20['bike_rides_daily'], 'colorscale' : 'Blues'}))
    fig.update_layout(
    title = 'Top 20 Most Popular Bike Stations in NYC',
    xaxis_title = 'Start Stations', 
    yaxis_title = 'Sum of Trips', 
    width = 900, height = 600
)
    st.plotly_chart(fig, use_container_width = True)
    st.markdown("From the bar chart it is clear that there are some start stations that are more popular than others - in the top 3 we can see 57th St./37th Ave., 54th St./37th Ave., and 62nd St./43rd Ave. There is not a big jump between the highest and lowest bars of the plot as all rentals fall between 1200 and 1400 which in the grand scheme of things is somewhat miniscule.")

elif page == 'Interactive map with aggregated bike trips': 

    ### Create the map ###

    st.write("Interactive map showing aggregated bike trips over NYC")

    path_to_html = "keplergl.html" 

    # Read file and keep in variable
    with open(path_to_html,'r') as f: 
        html_data = f.read()

    ## Show in webpage
    st.header("Aggregated Bike Trips in NYC")
    st.components.v1.html(html_data,height=1000)
    st.markdown("#### Using the filter on the left hand side of the map we can check whether the most popular start stations also appear in the most popular trips.")
    st.markdown("The most popular start stations are:")
    st.markdown("57 St/37 Ave, 54 St./37 Ave., and 62 St./43 Ave. With the aggregated bike trips filter enabled, we can see that even though 57 St./37 Ave. is a popular start stations, it doesn't account for the most commonly taken trips.")
    st.markdown("The most common routes are between W 26 St./8 Ave. to 10 Ave/W 28 St., Norfolk St./Broome St. to Henry St/Grand St. and, lastly W 20 St./10 Ave. to W 21 St./6 Ave.")
else:
    
    st.header("Conclusions and recommendations")
    #bikes = Image.open("recs_page.png")  #source: Midjourney
    #st.image(bikes)
    st.markdown("### Our analysis has shown that CitiBike should focus on the following objectives moving forward:")
    st.markdown("- Add more stations to the locations around the water line of the east part of the Island. Some possible locations would be East 57th Street in Sutton, East 10th in Alphabet City near the Dry Dock Playground, and on East 114th Street in Harlem by the Thomas Jeferson Park. All these locations are near the shorline which would be appealing for the breeze coming off the water in hot months and are also near or within popular areas of these communities.")
    st.markdown("- Make sure that during the warmer months bikes are well stoked at the most popular stations in order to meet the higher demand, counter to that supply a lower ammount of bikes in winter and late autumn to keep costs down.")