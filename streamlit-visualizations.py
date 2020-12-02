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

brush = alt.selection(type='interval', encodings=['x'])

###Title####

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
# 'Select the year range' -> Text to display
# 2015 -> The lower bound
# 2019 -> The higher bound
# (2015, 2019) -> Default selected range

#slider = alt.binding_range(min=2005, max=2019, step=1)
#select_year = alt.selection_single(name="Year", fields=['Year'],bind=slider2, init={'Year': 2019})


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




### FIRST CHART ###
bar1 = alt.Chart(df).mark_bar().encode(
    x = alt.X('Year:O', scale=alt.Scale(zero=False),axis=alt.Axis(titleFontSize=20,labelFontSize=14)),
    y = alt.Y('Total:Q', scale=alt.Scale(zero=False), title='Total Cost ($)', axis=alt.Axis(titleFontSize=20,labelFontSize=14)),
    opacity=alt.condition(brush, alt.OpacityValue(1), alt.OpacityValue(0.7))
).add_selection(
    brush
#).properties(
#    width=800,
#    height=500
)

rule1 = alt.Chart(df).mark_rule(color='red').encode(
    y='mean(Total):Q',
    size=alt.SizeValue(3)
).transform_filter(
    brush
)
################################
### SECOND CHART ###
bar2 = alt.Chart(df).mark_bar().encode(
    x = alt.X('Year:O', scale=alt.Scale(zero=False),axis=alt.Axis(titleFontSize=20,labelFontSize=14)),
    y = alt.Y('Acres:Q', scale=alt.Scale(zero=False), title='Acres', axis=alt.Axis(titleFontSize=20,labelFontSize=14)),
    opacity=alt.condition(brush, alt.OpacityValue(1), alt.OpacityValue(0.7))
).add_selection(
    brush
#).properties(
#    width=800,
#    height=500
)

rule2 = alt.Chart(df).mark_rule(color='red').encode(
    y='mean(Acres):Q',
    size=alt.SizeValue(3)
).transform_filter(
    brush
)
################################
### THIRD CHART ###
bar3 = alt.Chart(df).mark_bar().encode(
    x = alt.X('Year:O', scale=alt.Scale(zero=False),axis=alt.Axis(titleFontSize=20,labelFontSize=14)),
    y = alt.Y('Fires:Q', scale=alt.Scale(zero=False), title='Number of Fires', axis=alt.Axis(titleFontSize=20,labelFontSize=14)),
    opacity=alt.condition(brush, alt.OpacityValue(1), alt.OpacityValue(0.7))
).add_selection(
    brush
#).properties(
#    width=800,
#    height=500
)

rule3 = alt.Chart(df).mark_rule(color='red').encode(
    y='mean(Fires):Q',
    size=alt.SizeValue(3)
).transform_filter(
    brush
)


#st.write("## Total Supression Cost of Fires per Year")
#bar1 + rule1
#st.write("## Acres Burned per Year")
#bar2 + rule2
#st.write("## Number of Fires per Year")
#bar3 + rule3
st.write("## United States Map Showing Fires per Year")
background + points
