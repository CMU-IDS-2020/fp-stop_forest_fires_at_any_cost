import altair as alt
import pandas as pd
import streamlit as st
import altair_viewer
from vega_datasets import data
import os
import vega
import matplotlib.pyplot as plt
import re

####DATA#####
df = pd.read_excel('Data.xlsx')
df1 = pd.read_excel('Data.xlsx',3)
df2 = pd.read_csv('significant-fires_2005-2019.csv')
df3 = pd.read_csv('Perscribed_Fires.csv')

####DATA TRANSFORMATION / DATA QUERIES#####

#returns ONE DataFrame
#DF -> count_by_cause_df => count of causes grouped by year and cause
@st.cache
def get_count_by_cause(df2):
    cause_df = df2[['Year', 'Cause', 'Acres']]
    cause_df['Year'] = cause_df['Year'].fillna(0).astype(int)
    count_by_cause_df = cause_df.groupby(['Year', 'Cause'])['Cause'].count()
    return count_by_cause_df

#returns ONE DataFrame
#DF -> acres_by_cause_df => sum of acres grouped by year and cause
@st.cache
def get_sum_by_acres(df2):
    cause_df = df2[['Year', 'Cause', 'Acres']]
    cause_df['Year'] = cause_df['Year'].fillna(0).astype(int)
    acres_by_cause_df = cause_df.groupby(['Year', 'Cause'])['Acres'].sum()
    return acres_by_cause_df

#returns ONE DataFrame
#Breaks down to cost by acre for df2
@st.cache
def get_cost_per_acre(df2):
    cost_df = df2[['Year', 'Cause', 'Acres', 'Estimated_Cost']]
    cost_df['Year'] = cost_df['Year'].fillna(0).astype(int)
    cost_df['Acres'] = cost_df['Acres'].replace(',', '', regex=True).fillna(0).astype(int)
    cost_df['Estimated_Cost'] = cost_df['Estimated_Cost'].replace(',', '', regex=True)
    cost_df['Estimated_Cost'] = cost_df['Estimated_Cost'].str.lstrip('$').fillna(0).astype(int)
    cost_df = cost_df.groupby(['Year', 'Cause']).sum()
    cost_df['Cost per Acre'] = cost_df['Estimated_Cost'] / cost_df['Acres']
    return cost_df

#returns ONE DataFrame
#Breaks down perscribed fires for df3
@st.cache
def get_perscribed_fires(df3):
    perscribed_df = df3[['Year', 'Description', 'State/Other', 'Total']]
    perscribed_df[['State/Other', 'Total']] = perscribed_df[['State/Other', 'Total']].replace(',', '', regex=True)
    perscribed_df[['State/Other', 'Total']] = perscribed_df[['State/Other', 'Total']].astype(int)
    #perscribed_df = perscribed_df.groupby('Year')
    return perscribed_df

###Alter name of causes
df1 = df1.replace({'Cause':{'L':'Lightning (L)','U':'Unknown (U)','H':'Human (H)','OT':'Other Investigation (OT)','NR':'Not Reported (NR)'}})


###Adjust Dates
df1['Start Month'] = df1['Start Date'].dt.strftime('%B')

months = ["January", "February", "March", "April", "May", "June", 
          "July", "August", "September", "October", "November", "December"]
df1['Start Month'] = pd.Categorical(df1['Start Month'], categories=months, ordered=True)
df1 = df1.sort_values('Start Month')
df1['Start Month'] = df1['Start Month'].astype(str)

####UNITED STATES MAP WITH OVERLAY#####
def wildfires_by_state_MAP(df):
    states = alt.topo_feature(data.us_10m.url, 'states')
    capitals = data.us_state_capitals.url

    # US states background
    background = alt.Chart(states).mark_geoshape(
        fill='lightgray',
        stroke='white'
    ).properties(
        title='Wild Fires by State',
        width=350,
        height=350
    ).project('albersUsa')

    # Points and text
    hover = alt.selection(type='single', on='mouseover', nearest=True,
                            fields=['lat', 'lon'])

    #state capitals
    base = alt.Chart(capitals).encode(
        longitude='lon:Q',
        latitude='lat:Q',
    )

    text = base.mark_text(dy=-5, align='right').encode(
    alt.Text('city', type='nominal'),
    opacity=alt.condition(~hover, alt.value(0), alt.value(1))
    )

    capital_points = base.mark_point().encode(
        color=alt.value('black'),
        size=alt.condition(~hover, alt.value(10), alt.value(100))
    ).add_selection(hover)

    slider2 = st.sidebar.slider('Select the year range',2005, 2019, (2005, 2019))
    

    causes = ['Select all', 'Unknown (U)', 'Human (H)', 'Lightning (L)', 'Other Investigation (OT)', 'Not Reported (NR)']

    option1 = st.sidebar.multiselect('Filter Map by Cause', ('Select all', 'Unknown (U)', 
                            'Human (H)', 'Lightning (L)', 'Other Investigation (OT)',
                            'Not Reported (NR)'), default='Select all')
    
    if 'Select all' in option1:
        option1=causes



    months1 = ["Select all", "January", "February", "March", "April", "May", "June", 
          "July", "August", "September", "October", "November", "December"]

    option2 = st.sidebar.multiselect('Filter Map by Fire start Month', months1, default='Select all')

    if 'Select all' in option2:
        option2=months1

    #option2 = st.sidebar.selectbox('Filter Map by Fire start Month', (df1['Start Date']))

    

    fire_points = alt.Chart(df1).mark_circle(
        size=20,
        color='steelblue'
        ).transform_filter(
            (alt.datum['Year'] >= slider2[0]) & (alt.datum['Year'] <= slider2[1])
        ).transform_filter(
            alt.FieldOneOfPredicate(field='Cause', oneOf=option1)
        ).transform_filter(
            alt.FieldOneOfPredicate(field='Start Month', oneOf=option2)
        ).encode(
            #size=alt.Size("Size (acres):Q", scale=alt.Scale(range=[0, 1000]), legend=None),
                    longitude='Long:Q',
                    latitude='Lat:Q',
        tooltip=['Name', 'Year', 'Acres','Estimated Cost','Cause', 'Start Date']
    )     

    brush = alt.selection(type='interval')

    chart_2 = alt.Chart(df).mark_point(
        ).transform_filter(
            (alt.datum['Year'] >= slider2[0]) & (alt.datum['Year'] <= slider2[1])
        ).encode(
                x='Year:Q',
                y='Acres:Q',
                color=alt.condition(brush, 'Cause:N', alt.value('lightgray'))
        ).add_selection(brush
        ).properties(
                width=400,
                height=200
    )
    
    chart_3 = alt.Chart(df).mark_bar(
        ).transform_filter(
            (alt.datum['Year'] >= slider2[0]) & (alt.datum['Year'] <= slider2[1])
        ).encode(
                y='Cause:N',
                color='Cause:N',
                x='Number of Fires:Q'
        ).transform_filter(brush
        ).properties(
                width=400,
                height=80
    )

    ### Checkbox for showing table (raw) data
    if st.sidebar.checkbox("Show Raw Data"):
        st.write(df1)


    map_chart = background + capital_points + fire_points + text

    map_chart | chart_2 & chart_3
 
if __name__ == "__main__":
    wildfires_by_state_MAP(df)

    






