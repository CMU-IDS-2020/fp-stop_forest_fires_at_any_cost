import altair as alt
import pandas as pd
import streamlit as st
import altair_viewer
from vega_datasets import data
import os, vega, time, random, base64
import matplotlib.pyplot as plt
import re
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime 
import plotly.express as px
from itertools import cycle
###
from IPython.display import HTML

@st.cache
def load5():
    df5 = pd.read_csv('predict_raw.zip')
    return df5

result = load5()

def other_viz(result):
    #result = load5()
    years = list(result['YEAR_'].sort_values().unique())
    states = list(result['STATE'].sort_values().unique())
 
    firetype_df = result.groupby(['YEAR_','STATE', 'FIRETYPE']).size().reset_index(name="firetype count")
    firetype_df['Average'] = (firetype_df['firetype count'] / sum(firetype_df['firetype count']))
    firetype_df['FIRETYPE'] = firetype_df['FIRETYPE'].replace(0, 'Action Fires/Supressed Fires')
    firetype_df['FIRETYPE'] = firetype_df['FIRETYPE'].replace(1, 'Natural Out')
    firetype_df['FIRETYPE'] = firetype_df['FIRETYPE'].replace(2, 'Support Action/Assist Fire')
    firetype_df['FIRETYPE'] = firetype_df['FIRETYPE'].replace(3, 'Fire Management/Perscribed')
    firetype_df['FIRETYPE'] = firetype_df['FIRETYPE'].replace(4, 'False Alarm')
    firetype_df['FIRETYPE'] = firetype_df['FIRETYPE'].replace(5, 'Severe')

    firetype_df2 = result.groupby(['YEAR_','FIRETYPE']).size().reset_index(name="Firetype Count")
    firetype_df2['FIRETYPE'] = firetype_df2['FIRETYPE'].replace(0, 'Action Fires/Supressed Fires')
    firetype_df2['FIRETYPE'] = firetype_df2['FIRETYPE'].replace(1, 'Natural Out')
    firetype_df2['FIRETYPE'] = firetype_df2['FIRETYPE'].replace(2, 'Support Action/Assist Fire')
    firetype_df2['FIRETYPE'] = firetype_df2['FIRETYPE'].replace(3, 'Fire Management/Perscribed')
    firetype_df2['FIRETYPE'] = firetype_df2['FIRETYPE'].replace(4, 'False Alarm')
    firetype_df2['FIRETYPE'] = firetype_df2['FIRETYPE'].replace(5, 'Severe')

    year_dropdown = alt.binding_select(options=years)
    year_select = alt.selection_single(fields=['YEAR_'], bind=year_dropdown)

    state_dropdown = alt.binding_select(options=states)
    state_select = alt.selection_single(fields=['STATE'], bind=state_dropdown)

    fire_type = alt.Chart(firetype_df).mark_bar(color='firebrick').encode(
        x=alt.X('Average:Q', axis=alt.Axis(format='.0%')),
        y='FIRETYPE:N',
        #opacity=alt.condition(
        #    year_select & state_select,
        #    alt.value(1),
        #    alt.value(.1)
    ).add_selection(year_select,state_select
    ).transform_filter(year_select
    ).transform_filter(state_select
    ).properties(width = 300, height = 200, title = f''
)
    fire_total = alt.Chart(firetype_df2).mark_circle(
    opacity=0.8,
    stroke='black',
    strokeWidth=1
    ).encode(
    alt.X('YEAR_:O', axis=alt.Axis(labelAngle=360, values = [1980,1985,1990, 1995, 2000, 2005, 2010, 2016]), title = 'Year'),
    alt.Y('FIRETYPE:N', title = 'Types of Fire'),
    alt.Size('Firetype Count:Q',
        scale=alt.Scale(range=[0, 1000]),
        legend = None
    ),
    alt.Color('FIRETYPE:N', legend=None),
    alt.Tooltip(['Firetype Count:Q', 'YEAR_']),
    ).properties(width=400, height=200, title ='National Count of Fires by Type')

    fire_type | fire_total



def other_viz3(result):
    #result = load5()
    types = ['Action Fires/Supressed Fires', 
                'Natural Out', 
                'Support Action/Assist Fire', 
                'Fire Management/Perscribed', 
                'False Alarm', 'Severe']

    firetype_df2 = result.groupby(['YEAR_','FIRETYPE']).size().reset_index(name="Firetype Count")
    firetype_df2['FIRETYPE'] = firetype_df2['FIRETYPE'].replace(0, 'Action Fires/Supressed Fires')
    firetype_df2['FIRETYPE'] = firetype_df2['FIRETYPE'].replace(1, 'Natural Out')
    firetype_df2['FIRETYPE'] = firetype_df2['FIRETYPE'].replace(2, 'Support Action/Assist Fire')
    firetype_df2['FIRETYPE'] = firetype_df2['FIRETYPE'].replace(3, 'Fire Management/Perscribed')
    firetype_df2['FIRETYPE'] = firetype_df2['FIRETYPE'].replace(4, 'False Alarm')
    firetype_df2['FIRETYPE'] = firetype_df2['FIRETYPE'].replace(5, 'Severe')
    
    base = alt.Chart(firetype_df2, width=600, height=400).mark_point(filled=True).encode(
    x=alt.X('YEAR_:N', axis=alt.Axis(labelAngle=360, values = [1980,1985,1990, 1995, 2000, 2005, 2010, 2016]), title = 'Year'),
    y='Firetype Count:Q',
    tooltip=["FIRETYPE:N", 'YEAR_:N']
    )

    type_radio = alt.binding_radio(options=types)
    type_select = alt.selection_single(fields=['FIRETYPE'], bind=type_radio, name='Pick a')
    type_color_condition = alt.condition(type_select,
                      alt.Color('FIRETYPE:N'),
                      alt.value('lightgray'))
    highlight_types = base.add_selection(
    type_select
    ).encode(
    color=type_color_condition
    ).properties(title="U.S. Number of Fires (1980-2016)")

    
    highlight_types

if __name__ == "__main__":
    other_viz(result)
    other_viz3(result)
