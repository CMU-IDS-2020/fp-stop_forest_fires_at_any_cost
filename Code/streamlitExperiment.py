import altair as alt
import pandas as pd
import streamlit as st
import os
import vega
import pandas as pd
import numpy as np
from datetime import datetime 
import plotly.express as px
import matplotlib.pyplot as plt

#Preparing Map Images
image_bank = ['image_1.png', 'image_2.png', 'image_3.png', 'image_4.png', 
              'image_5.png', 'image_6.png', 'image_7.png', 'image_8.png', 
              'image_9.png', 'image_10.png', 'image_11.png', 'image_12.png', 
              'image_13.png', 'image_14.png', 'image_15.png', 'image_16.png', 
              'image_17.png', 'image_18.png', 'image_19.png', 'image_20.png', 
              'image_21.png', 'image_22.png', 'image_23.png', 
              'image_24.png', 'image_25.png', 'image_26.png', 'image_27.png',
              'image_28.png', 'image_29.png', 'image_30.png', 'image_31.png',  
              'image_32.png', 'image_33.png', 'image_34.png', 'image_35.png', 
              'image_36.png', 'image_37.png']

#Preparing the DFs and aggregations for Pie Charts
@st.cache
def dataloader():
    df = pd.read_csv('Fires2016v2.csv')
    df['Cause'] = df['CAUSE']
    df['Year'] = df['YEAR_']
    df['Acres'] = df['TOTALACRES']
    df['STARTDATED'] = pd.to_datetime(df['STARTDATED'], errors='coerce')
    df['OUTDATED'] = pd.to_datetime(df['OUTDATED'], errors='coerce')
    df['BurnTime'] = abs(df['OUTDATED'] - df['STARTDATED'])
    return df

st.beta_set_page_config(layout="wide")
df = dataloader()

def dataChanger(Year):
    newdata = df[ df['YEAR_'] == Year ]
    newdata = newdata.groupby(['Year', 'Cause'], as_index=False)['BurnTime', 'Acres'].sum(numeric_only=False)
    return newdata


def causeVisualization():
    #Designing Streamlit Page
    st.title('Map of Wildfires caused by Humans and Nature over Time')
    x = st.slider('Check out Data Over Time', min_value=1980, max_value=2016)


    col1, col2, col3 = st.beta_columns(3)

    #Map Image
    col1.image(f'image_{x - 1979}.png', width=825)

    #Create Pie Chart for Acres Burned
    newdata= dataChanger(x)
    fig = px.pie(newdata, values='BurnTime', names='Cause', title=f'Burn Days per Fire in {x}', color='Cause', color_discrete_map={'Human':'red', 'Natural':'blue'})
    fig.update_layout(width=600,height=275)
    col2.plotly_chart(fig, width=600,height=275)

    #create Pie Chart for Average Burn Time
    fig2 = px.pie(newdata, values='Acres', names='Cause', title=f'Acres Burned per Fire in {x}', color='Cause', color_discrete_map={'Human':'red', 'Natural':'blue'})
    fig2.update_layout(width=600,height=275)
    col2.plotly_chart(fig2, width=600,height=275)

    col3.title('Understanding Fire Trends by Cause')
    col3.markdown('View the side-by-side comparison of human-caused and naturally-caused fires from the years 1985 - 2019. Observe the changes in number of fires (seen on the map) versus burn days and acres burned. Consider the fact that the greater amount of burn days increase the length of time resources are expended to suppress a fire. Also consider that, as acres-burned grows, the ability of fire fighters to supppress a fire lessens.')

causeVisualization()
col3.title('Visualizing the Cause of Fires over Time') 
