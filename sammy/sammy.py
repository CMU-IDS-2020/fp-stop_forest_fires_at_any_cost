import altair as alt
import pandas as pd
import streamlit as st
import altair_viewer
from vega_datasets import data
import os
import vega
import matplotlib.pyplot as plt
import re


@st.cache
def load():
 	df = pd.read_csv('fire_data.csv')
 	df['YEAR2'] = pd.to_datetime(df['YEAR'],format='%Y')
 	df['STARTDATED'] = pd.to_datetime(df['STARTDATED'],format='%m/%d/%y')
 	df['CONTRDATED'] = pd.to_datetime(df['CONTRDATED'],format='%m/%d/%y')
 	df['Days'] = (df['CONTRDATED'] - df['STARTDATED']).dt.days

 	return df

@st.cache
def load2():
	df = pd.read_excel('Data.xlsx',3)
	df['cost_per_acre'] = (df['Estimated Cost']/df['Acres'])
	df['Start Date'] = pd.to_datetime(df['Start Date'],format='%m/%d/%y')
	df['Contain or Last Report Date'] = pd.to_datetime(df['Contain or Last Report Date'],format='%m/%d/%y')
	df['Days'] = (df['Contain or Last Report Date'] - df['Start Date']).dt.days
	df = df[(df['Days'] > 0) & (df['cost_per_acre'] > 0)]
	df = df[(df['Cause'] == 'L') | (df['Cause'] == 'H')]
	df['Cause'].replace({'H':'Human','L':'Natural'}, inplace=True)
	return df

@st.cache
def load3():
	df = pd.read_excel('Data.xlsx')
	df['cost_per_acre'] = df['Total']/df['Acres']

	return df

df = load()
df_sig = load2()
df_main = load3()


states = alt.topo_feature(data.us_10m.url, 'states')
source = 'https://raw.githubusercontent.com/sammyhajomar/test/main/altair-dataset1.csv'
variables = ['State','acres','id']

# US states background
background = alt.Chart(states).mark_geoshape(
    fill='lightgray',
    stroke='white'
).properties(
    title='Wild Fires by State'
).project('albersUsa'
).properties(
            width=800,
            height=500
)

slider = alt.binding_range(min=1980, max=2016, step=1, name='Year')

select_year = alt.selection_single(name="SelectorName", fields=['YEAR'],
                                   bind=slider, init={'YEAR': 2000})

single = alt.selection_single(empty='all', fields=['CAUSE'])

fire_points = alt.Chart(df).mark_circle(  
	).encode(
        size=alt.Size("TOTALACRES:Q", title='Acres Burned', scale=alt.Scale(range=[0, 1000])),
        longitude='DLONGITUDE:Q',
        latitude='DLATITUDE:Q',
    	tooltip=[alt.Tooltip('YEAR',title='Year'),alt.Tooltip('TOTALACRES',title='Acres Burned', format = ",.4r"), 
    				alt.Tooltip('CAUSE',title='Cause'),alt.Tooltip('STARTDATED',title='Start Date'),alt.Tooltip('STATE',title='State')],
    	color='CAUSE'
    ).add_selection(
    	select_year
    ).transform_filter(
    	select_year
)


chart_1 = alt.Chart(df).mark_line(point=True).encode(
		alt.X('year(YEAR2):T',title='Year',scale=alt.Scale(zero=False),axis=alt.Axis(titleFontSize=14,labelFontSize=14)),
		alt.Y('sum(TOTALACRES):Q',title='Total Acres Burned', scale=alt.Scale(zero=False), axis=alt.Axis(titleFontSize=14,labelFontSize=14)),
		color='CAUSE:N',
		tooltip=[alt.Tooltip("YEAR2",title='Year'), alt.Tooltip('mean(TOTALACRES)',title='Acres Burned', format=",.4r")]
	).properties(
		width=800,
		height=300

)

chart_2 = alt.Chart(df).mark_line(point=True).encode(
		alt.X('year(YEAR2):T',title='Year',scale=alt.Scale(zero=False),axis=alt.Axis(titleFontSize=14,labelFontSize=14)),
		alt.Y('sum(Days):Q',title='Total Number of Days per Fires', scale=alt.Scale(zero=False), axis=alt.Axis(titleFontSize=14,labelFontSize=14)),
		color='CAUSE:N',
		tooltip=[alt.Tooltip("YEAR2",title='Year'), alt.Tooltip('mean(Days)',title='Days of Fire', format=".2r")]
	).properties(
		width=800,
		height=300

)

chart_3 = alt.Chart(df).mark_bar().encode(
 		alt.X('STATE',title='State', sort='-y'),
 		alt.Y('sum(TOTALACRES):Q',title='Acres Burned', axis=alt.Axis(format=',.4r')),
 		color=alt.Color('CAUSE:N'),
 		tooltip=[alt.Tooltip("CAUSE",title='Cause'), alt.Tooltip('sum(TOTALACRES)',title='Acres Burned', format=",.4r")]
 	).add_selection(
    	select_year
    ).transform_filter(
    	select_year

)


US_map = alt.Chart(states).mark_geoshape().encode(
    	color=alt.Color('acres:Q',title='Acreage Burned'),
    	tooltip=['State:N',alt.Tooltip('acres:Q',title='Total Acres Burned', format = ",.4r")]
	).transform_lookup(
   		lookup='id',
    	from_=alt.LookupData(source,'id',variables),
	).project(
    	type='albersUsa'
)


brush = alt.selection(type='interval', encodings=['x'])

bar1 = alt.Chart(df_main).mark_bar().encode(
    x = alt.X('Year:O', scale=alt.Scale(zero=False),axis=alt.Axis(titleFontSize=20,labelFontSize=14)),
    y = alt.Y('Total:Q', scale=alt.Scale(zero=False), title='Total Cost', axis=alt.Axis(titleFontSize=20,labelFontSize=14, format = "$,.6r")),
    opacity=alt.condition(brush, alt.OpacityValue(1), alt.OpacityValue(0.7)),
    tooltip=[alt.Tooltip("Total:Q",title='Total Cost', format="$,.4r"), alt.Tooltip("Year",title='Year')]
).add_selection(
    brush
)

rule1 = alt.Chart(df_main).mark_rule(color='red').encode(
    	y='mean(Total):Q',
    	size=alt.SizeValue(3)
	).transform_filter(
    	brush
)

bar2 = alt.Chart(df_main).mark_bar().encode(
    x = alt.X('Year:O', scale=alt.Scale(zero=False),axis=alt.Axis(titleFontSize=20,labelFontSize=14)),
    y = alt.Y('Acres:Q', scale=alt.Scale(zero=False), title='Acres Burned', axis=alt.Axis(titleFontSize=20,labelFontSize=14)),
    opacity=alt.condition(brush, alt.OpacityValue(1), alt.OpacityValue(0.7)),
    tooltip=[alt.Tooltip("Acres",title='Acres Burned', format=",.6r"), alt.Tooltip("Year",title='Year')]
).add_selection(
    brush
)

rule2 = alt.Chart(df_main).mark_rule(color='red').encode(
    y='mean(Acres):Q',
    size=alt.SizeValue(3)
).transform_filter(
    brush
)

bar3 = alt.Chart(df_main).mark_bar().encode(
    x = alt.X('Year:O', scale=alt.Scale(zero=False),axis=alt.Axis(titleFontSize=20,labelFontSize=14)),
    y = alt.Y('Fires:Q', scale=alt.Scale(zero=False), title='Number of Fires', axis=alt.Axis(titleFontSize=20,labelFontSize=14)),
    opacity=alt.condition(brush, alt.OpacityValue(1), alt.OpacityValue(0.7)),
    tooltip=[alt.Tooltip("Fires",title='Number of Fires', format=",.4r"),alt.Tooltip("Year",title='Year')]
).add_selection(
    brush
)

rule3 = alt.Chart(df_main).mark_rule(color='red').encode(
    y='mean(Fires):Q',
    size=alt.SizeValue(3)
).transform_filter(
    brush
)

bar4 = alt.Chart(df_main).mark_bar().encode(
    x = alt.X('Year:O', scale=alt.Scale(zero=False),axis=alt.Axis(titleFontSize=20,labelFontSize=14)),
    y = alt.Y('cost_per_acre:Q', scale=alt.Scale(zero=False), title='Cost per Acre', axis=alt.Axis(titleFontSize=20,labelFontSize=14, format = "$,.2r")),
    opacity=alt.condition(brush, alt.OpacityValue(1), alt.OpacityValue(0.7)),
    tooltip=[alt.Tooltip("cost_per_acre",title='Cost per Acre', format="$,.2r"),alt.Tooltip("Year",title='Year')]
).add_selection(
    brush
)

rule4 = alt.Chart(df_main).mark_rule(color='red').encode(
    y='mean(cost_per_acre):Q',
    size=alt.SizeValue(3)
).transform_filter(
    brush
)

slider1 = alt.binding_range(min=2006, max=2019, step=1, name='Year')

select_year1 = alt.selection_single(name="SelectorName", fields=['Year'],
                                   bind=slider1, init={'Year': 2006})

scatter = alt.Chart(df_sig).mark_circle(size=200
	).encode(
		x=alt.X('Days:Q', title='Days of Fire',scale=alt.Scale(zero=False),axis=alt.Axis(titleFontSize=20,labelFontSize=14)),
        y=alt.Y('cost_per_acre:Q', title='Cost per Acre', scale=alt.Scale(zero=False),axis=alt.Axis(titleFontSize=20,labelFontSize=14,format="$,.2r")),
        color= alt.Color('Cause:N'),
        tooltip=[alt.Tooltip('Name:N',title='Name of Fire'), alt.Tooltip('Acres:Q',title='Acres Burned'), alt.Tooltip('cost_per_acre:Q',title="Cost per Acre", format="$,.2r"),alt.Tooltip('Days:Q',title="Days of Fire")],
        size=alt.Size("Acres:Q", title='Acres Burned',scale=alt.Scale(range=[0, 1000])),
    ).properties(
        width=800,
        height=500
    ).add_selection(
    	select_year1
    ).transform_filter(
    	select_year1
)

scatter

(bar1 + rule1) & (bar2 + rule2) & (bar3 + rule3) & (bar4 + rule4)

map_chart = background + fire_points

map_chart

chart_3

chart_1

chart_2