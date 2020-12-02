import altair as alt
import pandas as pd
import streamlit as st
import altair_viewer
from vega_datasets import data
import os
import vega
import matplotlib.pyplot as plt

df = pd.read_excel('Data.xlsx')
df1 = pd.read_excel('Data.xlsx',3)

####BRUSH####
brush = alt.selection(type='interval', encodings=['x'])

####Date Slider####
def display_date_slider(df):
    min_date = min(df["Year"]).to_pydatetime()
    max_date = max(df["Year"]).to_pydatetime()
    return st.slider("Select Date Range", min_date, max_date, (min_date, max_date))

####Title####
def display_title_and_info():
    st.title("Stop Forest Fires at any COST")
   



####SECTION NUMBER 1
###Brief Summary####
####Video timelapse#####


###     TAYLOR and JOSH (Mostly TAYLOR)


####SECTION NUMBER 2
###Brief summary/instructions on how to interact
###Couple of illustrations for Federal_Suppression_Cost####


###      ARPIT and SAMMY



####SECTION NUMBER 3
###Brief summary/instructions on how to interact
###Couple of illustrations for Wildfires_by_state####

###     SAMMY

#######################################
####UNITED STATES MAP WITH OVERLAY#####
#######################################
slider2 = st.slider('Select the year range',2005, 2019, (2005, 2019))

states = alt.topo_feature(data.us_10m.url, feature='states')


# US states background
background = alt.Chart(states).mark_geoshape(
    fill='lightgray',
    stroke='white'
).properties(
    width=800,
    height=500
).project('albersUsa')

# airport positions on background
points = alt.Chart(df1).mark_circle(
    size=10,
    color='steelblue'
).encode(
    size=alt.Size("Size (acres):Q", scale=alt.Scale(range=[0, 1000]), legend=None),
    longitude='Long:Q',
    latitude='Lat:Q',
    tooltip=['Name', 'Year', 'Size (acres)','Estimated Cost','Cause*']
)#.add_selection(
  #  select_year
#).transform_filter(
 #   select_year
#)





####SECTION NUMBER 4
###Brief summary/instructions on how to interact
###Couple of illustrations for the Predictor Model####


###     TAYLOR and JOSH (Mostly TAYLOR)



if __name__ == "__main__":
    display_title_and_info()
    
