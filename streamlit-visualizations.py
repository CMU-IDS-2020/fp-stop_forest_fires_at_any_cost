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
import numpy as np
from datetime import datetime 
import plotly.express as px
from itertools import cycle

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

####DATA#####
df = pd.read_excel('Data.xlsx')
df1 = pd.read_excel('Data.xlsx',3)
df2 = pd.read_csv('significant-fires_2005-2019.csv')
df3 = pd.read_csv('Perscribed_Fires.csv')
df4 = pd.read_csv('acres_merged_prediction_results.csv')
df5 = pd.read_csv('predict_raw.zip')

####DATA TRANSFORMATION / DATA QUERIES#####
@st.cache
def load():
    df = pd.read_csv('fire_data.csv')
    df['YEAR2'] = pd.to_datetime(df['YEAR'],format='%Y')
    df['STARTDATED'] = pd.to_datetime(df['STARTDATED'],errors='coerce')
    df['CONTRDATED'] = pd.to_datetime(df['CONTRDATED'],errors='coerce')
    df['Days'] = (df['CONTRDATED'] - df['STARTDATED']).dt.days
    return df

@st.cache
def load2():
    df = pd.read_excel('Data.xlsx',3)
    df['cost_per_acre'] = (df['Estimated Cost']/df['Acres'])
    df['Start Date'] = pd.to_datetime(df['Start Date'], errors='coerce')
    df['Contain or Last Report Date'] = pd.to_datetime(df['Contain or Last Report Date'],errors='coerce')
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

#Data processing for the Cost Predictor Model
#Not to be used for visualizations
def cost_predict_data(df2):
    cost_predict_df = df2[['Year', 'State', 'Acres', 'Estimated_Cost']]
    cost_predict_df['Year'] = cost_predict_df['Year'].fillna(0).astype(int)
    cost_predict_df['Acres'] = cost_predict_df['Acres'].replace(',', '', regex=True)#.fillna(0).astype(int)
    cost_predict_df['Estimated_Cost'] = cost_predict_df['Estimated_Cost'].replace(',', '', regex=True)
    cost_predict_df['Estimated_Cost'] = cost_predict_df['Estimated_Cost'].str.lstrip('$')
    # imp = SimpleImputer(missing_values=pd.NA, strategy='mean')
    # cost_predict_df['Estimated_Cost'] = imp.fit_transform(cost_predict_df['Estimated_Cost'])  
    # cost_predict_df['Estimated_Cost'] = imp.transform(cost_predict_df['Estimated_Cost'])    
    #cost_predict_df = cost_predict_df.groupby(['State'])
    #cost_predict_df['Cost per Acre'] = cost_predict_df['Estimated_Cost'] / cost_predict_df['Acres']
    #cost_predict_df.to_csv('file4.csv', index=True)
    return cost_predict_df['Estimated_Cost']

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
    cost_df = df2[['Year', 'Cause', 'State', 'Acres', 'Estimated_Cost']]
    cost_df['Year'] = cost_df['Year'].fillna(0).astype(int)
    cost_df['Acres'] = cost_df['Acres'].replace(',', '', regex=True).fillna(0).astype(int)
    cost_df['Estimated_Cost'] = cost_df['Estimated_Cost'].replace(',', '', regex=True)
    cost_df['Estimated_Cost'] = cost_df['Estimated_Cost'].str.lstrip('$').fillna(0).astype(int)
    #cost_df = cost_df.groupby(['Year', 'Cause']).sum()
    cost_df['Cost per Acre'] = cost_df['Estimated_Cost'] / cost_df['Acres']
    #cost_df.to_csv('file3.csv', index=True)
    return cost_df

#returns ONE DataFrame
#Breaks down perscribed fires for df3
@st.cache
def get_perscribed_fires(df3):
    perscribed_df = df3[['Year', 'Description', 'State/Other', 'Total']]
    perscribed_df[['State/Other', 'Total']] = perscribed_df[['State/Other', 'Total']].replace(',', '', regex=True)
    perscribed_df[['State/Other', 'Total']] = perscribed_df[['State/Other', 'Total']].astype(int)
    return perscribed_df

@st.cache
def get_bigData_cause(df5):
    result = df5[['CAUSE', 'YEAR_', 'STATE', 'FIRETYPE', 'PROTECTION', 'TOTALACRES']]
    return result

def human_v_natural():
    result = get_bigData_cause(df5)
    result = result.groupby(['YEAR_','STATE', 'CAUSE']).size().reset_index(name="cause count")

    h_v_n = alt.Chart(result).mark_bar(
    cornerRadiusTopLeft=3,
    cornerRadiusTopRight=3
    ).encode(
    x='YEAR_:O',
    y='cause count:Q',
    color='CAUSE:N'
    ).properties(width = 600, height = 400)

    st.header('1.Insert Section Header Here')
    st.subheader('1.1 If interactive Instructions:...')
    h_v_n
    st.subheader('1.2 Dataset...')
    st.write('something')
    st.subheader('1.3 Relevance')
    st.write('something...importance of viz')
    st.subheader('1.4 Summary')
    st.write('Summary of findings')

def other_viz():
    result = get_bigData_cause(df5)
    st.header('2. Insert Section Header Here')
    st.subheader('2.1 Instructions')
    st.write('Select a Year and State from the drop down menu.'),
    #'The metrics displayed is the average fires by type and the protection types for the assigned Year and State')
    st.write('')
    Selector_year = list(result['YEAR_'].sort_values().unique())
    Selector_state = list(result['STATE'].sort_values().unique())
    box1 = st.selectbox('Years', Selector_year, key='box1')
    box2 = st.selectbox('States', Selector_state, key='box2')

    firetype_df = result.groupby(['YEAR_','STATE', 'FIRETYPE']).size().reset_index(name="firetype count")
    firetype_df = firetype_df[firetype_df['YEAR_'].eq(box1)]
    firetype_df = firetype_df[firetype_df['STATE'].eq(box2)]
    firetype_df['Average'] = (firetype_df['firetype count'] / sum(firetype_df['firetype count']))
    firetype_df['FIRETYPE'] = firetype_df['FIRETYPE'].replace(0, 'Action Fires/Supressed Fires')
    firetype_df['FIRETYPE'] = firetype_df['FIRETYPE'].replace(1, 'Natural Out')
    firetype_df['FIRETYPE'] = firetype_df['FIRETYPE'].replace(2, 'Support Action/Assist Fire')
    firetype_df['FIRETYPE'] = firetype_df['FIRETYPE'].replace(3, 'Fire Management/Perscribed')
    firetype_df['FIRETYPE'] = firetype_df['FIRETYPE'].replace(4, 'False Alarm')
    firetype_df['FIRETYPE'] = firetype_df['FIRETYPE'].replace(5, 'Severe')

    protection_df = result.groupby(['YEAR_','STATE', 'PROTECTION']).size().reset_index(name="protection count")
    protection_df = protection_df[protection_df['YEAR_'].eq(box1)]
    protection_df = protection_df[protection_df['STATE'].eq(box2)]
    protection_df['Average'] = (protection_df['protection count'] / sum(protection_df['protection count']))

    fire_type = alt.Chart(firetype_df).mark_bar(color='firebrick').encode(
        x=alt.X('Average:Q', axis=alt.Axis(format='.0%')),
        y='FIRETYPE:N',
        #tooltip = [alt.Tooltip('Average:Q', title = f'FIRETYPE')]
    ).properties(width = 300, height = 200, title = f'{box1}, {box2}')

    text1 = fire_type.mark_text(
    align='left',
    baseline='middle',
    dx=3  # Nudges text to right so it doesn't appear on top of the bar
    ).encode(
    text=('Average:Q')
    )

    protect = alt.Chart(protection_df).mark_bar().encode(
        alt.X('Average:Q', axis=alt.Axis(format='.0%')),
        y='PROTECTION:N'
    ).properties(width = 300, height = 200, title = f'{box1}, {box2}')

    text2 = protect.mark_text(
    align='left',
    baseline='middle',
    dx=3  # Nudges text to right so it doesn't appear on top of the bar
    ).encode(
    text=('Average:Q')
    )


    fire_type + text1 | protect + text2

def other_viz2():
    result = get_bigData_cause(df5)

    Selector_year = list(result['YEAR_'].sort_values().unique())
    box3 = st.selectbox('Years', Selector_year, key='box3')

    firetype_df2 = result.groupby(['YEAR_','FIRETYPE']).size().reset_index(name="Firetype Count")
    firetype_df2['FIRETYPE'] = firetype_df2['FIRETYPE'].replace(0, 'Action Fires/Supressed Fires')
    firetype_df2['FIRETYPE'] = firetype_df2['FIRETYPE'].replace(1, 'Natural Out')
    firetype_df2['FIRETYPE'] = firetype_df2['FIRETYPE'].replace(2, 'Support Action/Assist Fire')
    firetype_df2['FIRETYPE'] = firetype_df2['FIRETYPE'].replace(3, 'Fire Management/Perscribed')
    firetype_df2['FIRETYPE'] = firetype_df2['FIRETYPE'].replace(4, 'False Alarm')
    firetype_df2['FIRETYPE'] = firetype_df2['FIRETYPE'].replace(5, 'Severe')

    protection_df2 = result.groupby(['YEAR_','PROTECTION']).size().reset_index(name="protection count")
    # protection_df2['PROTECTION'] = protection_df2['PROTECTION'].replace('1', 'Closed Season')
    # protection_df2['PROTECTION'] = protection_df2['PROTECTION'].replace('2', 'Partial Hootowl')
    # protection_df2['PROTECTION'] = protection_df2['PROTECTION'].replace('3', 'Partial Shutdown')
    # protection_df2['PROTECTION'] = protection_df2['PROTECTION'].replace('4', 'General Shutdown')
    protection_df2['Average'] = (protection_df2['protection count'] / sum(protection_df2['protection count']))
    protection_df2 = protection_df2[protection_df2['YEAR_'].eq(box3)]
    
    fire_total = alt.Chart(firetype_df2).mark_circle(
    opacity=0.8,
    stroke='black',
    strokeWidth=1
    ).encode(
    alt.X('YEAR_:O', axis=alt.Axis(labelAngle=45), title = 'Year'),
    alt.Y('FIRETYPE:N', title = 'Types of Fire'),
    alt.Size('Firetype Count:Q',
        scale=alt.Scale(range=[0, 1000]),
        legend = None
    ),
    alt.Color('FIRETYPE:N', legend=None),
    alt.Tooltip(['Firetype Count:Q', 'YEAR_']),
    ).properties(width=700, height=450, title ='Annual Count of Fires by Type')

    protect_total = alt.Chart(protection_df2).mark_bar(color='orange').encode(
        alt.X('Average:Q', axis=alt.Axis(format='.0%')),
        y='PROTECTION:N'
    ).properties(width = 300, height = 300, title = f'{box3}, National Statistics')

    text4 = protect_total.mark_text(
    align='left',
    baseline='middle',
    dx=3  # Nudges text to right so it doesn't appear on top of the bar
    ).encode(
    text=('Average:Q')
    )

    st.write('Instructions:')
    fire_total | (protect_total + text4)
    st.subheader('2.2 Definitions')
    st.write('2.2.1 Definition of Firetype')
    st.write('2.2.2 Definition of protection levels')
    st.subheader('2.3 Summary')
    st.write('Summary of findings')

def other_viz3():
    result = get_bigData_cause(df5)

    types = ['Action Fires/Supressed Fires', 'Natural Out', 'Support Action/Assist Fire', 'Fire Management/Perscribed', 'False Alarm', 'Severe']

    firetype_df2 = result.groupby(['YEAR_','FIRETYPE']).size().reset_index(name="Firetype Count")
    firetype_df2['FIRETYPE'] = firetype_df2['FIRETYPE'].replace(0, 'Action Fires/Supressed Fires')
    firetype_df2['FIRETYPE'] = firetype_df2['FIRETYPE'].replace(1, 'Natural Out')
    firetype_df2['FIRETYPE'] = firetype_df2['FIRETYPE'].replace(2, 'Support Action/Assist Fire')
    firetype_df2['FIRETYPE'] = firetype_df2['FIRETYPE'].replace(3, 'Fire Management/Perscribed')
    firetype_df2['FIRETYPE'] = firetype_df2['FIRETYPE'].replace(4, 'False Alarm')
    firetype_df2['FIRETYPE'] = firetype_df2['FIRETYPE'].replace(5, 'Severe')
    
    base = alt.Chart(firetype_df2, width=600, height=600).mark_point(filled=True).encode(
    x=alt.X('YEAR_:N', axis=alt.Axis(labelAngle=45), title = 'Year'),
    y='Firetype Count:Q',
    tooltip="FIRETYPE:N"
    )

    type_radio = alt.binding_radio(options=types)
    type_select = alt.selection_single(fields=['FIRETYPE'], bind=type_radio, name='Pick a')
    type_color_condition = alt.condition(type_select,
                      alt.Color('FIRETYPE:N', legend=None),
                      alt.value('lightgray'))
    highlight_types = base.add_selection(
    type_select
    ).encode(
    color=type_color_condition
    ).properties(title="Fill In")

    highlight_types


def display_pred_code():
    #big data acrage predictor
    big_pred = open('big-data predict.txt', 'r')
    content1 = big_pred.read()

    #cost data predictor
    cost_pred = open('Cost Predictor Model_v1.txt', 'r')
    content2 = cost_pred.read()

    option1 = st.checkbox('Display Acre Predictor Model Code')
    option2 = st.checkbox('Display Cost Predictor Model Code')
    if option1:
        st.code(content1, language='r')
    if option2:
        st.code(content2, language='r')

@st.cache(allow_output_mutation=True)
def dataLoader2():
    predict_df = pd.read_csv('national_cause_predictions.csv')
    predict_df2 = predict_df[predict_df['Year'] >=2017]
    predict_df2['Cost'] = predict_df2['Acres'] * 86
    return predict_df2

def dataChanger2(humanperc, naturalperc):
    predict = dataLoader2()
    predict['Acre_result'] = np.where(predict['Cause']=='Human', predict['Acres'] - predict['Acres']*humanperc, predict['Acres'] - predict['Acres']*naturalperc)
    predict['Cost_result'] = np.where(predict['Cause']=='Human', predict['Cost'] - predict['Cost']*humanperc, predict['Cost'] - predict['Cost']*naturalperc)
    return predict

def predictPlot(predict_df2, flag, num):
    col1, col2 = area51.beta_columns((2,1))
    predict3 = predict_df2[predict_df2['Cause']== 'Human']
    predict4 = predict_df2[predict_df2['Cause']== 'Natural']
    if flag == 1: 
        charted = alt.Chart().mark_bar(color='firebrick').encode(alt.X('Acres'), alt.Y('Year:O'), tooltip=['Acres', 'Year'])
        texted = charted.mark_text(align='left', baseline='middle', dx=3, fontSize=25).encode(text='Acres:Q')
        col1.altair_chart(alt.layer(charted, texted, data=predict3).properties(width=950, height=350, title='Human Predictions').configure_axis(labelFontSize=20, titleFontSize=20))
        charted = alt.Chart().mark_bar(color='forestgreen').encode(alt.X('Acres'), alt.Y('Year:O'), tooltip=['Acres', 'Year'])
        texted = charted.mark_text(align='left', baseline='middle', dx=3, fontSize=25).encode(text='Acres:Q')
        col1.altair_chart(alt.layer(charted, texted, data=predict4).properties(width=950, height=350, title='Natural Predictions').configure_axis(labelFontSize=20, titleFontSize=20))
    elif flag == 2: 
        charted = alt.Chart().mark_bar(color='firebrick').encode(alt.X('Acre_result'), alt.Y('Year:O'), tooltip=['Acre_result', 'Year'])
        texted = charted.mark_text(align='left', baseline='middle', dx=3, fontSize=25).encode(text='Acre_result:Q')
        col1.altair_chart(alt.layer(charted, texted, data=predict3).properties(width=950, height=350, title='Human Predictions').configure_axis(labelFontSize=20, titleFontSize=20))
        charted = alt.Chart().mark_bar(color='forestgreen').encode(alt.X('Acre_result'), alt.Y('Year:O'), tooltip=['Acre_result', 'Year'])
        texted = charted.mark_text(align='left', baseline='middle', dx=3, fontSize=25).encode(text='Acre_result:Q')
        col1.altair_chart(alt.layer(charted, texted, data=predict4).properties(width=950, height=350, title='Natural Predictions').configure_axis(labelFontSize=20, titleFontSize=20))

    file_ = open("fire.gif", "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()
    num = 700 - 700*num
    col2.markdown(f'<img src="data:image/gif;base64,{data_url}" width="{num}" height="{num}" alt="fire gif">', unsafe_allow_html=True)
    col2.markdown('<b> Watch the fire proportionally decrease by your human-caused fire input </b>', unsafe_allow_html=True)

def predictCost(df, flag, num):
    col21, col22 = location2.beta_columns((2,1))
    predict3 = df[df['Cause']== 'Human']
    predict4 = df[df['Cause']== 'Natural']
    if flag == 1: 
        charted = alt.Chart().mark_bar(color='firebrick').encode(alt.X('Cost'), alt.Y('Year:O'), tooltip=['Cost', 'Year'])
        texted = charted.mark_text(align='left', baseline='middle', dx=3, fontSize=25).encode(text='Cost:Q')
        col21.altair_chart(alt.layer(charted, texted, data=predict3).properties(width=900, height=350, title='Human Predictions').configure_axis(labelFontSize=20, titleFontSize=20))
        charted = alt.Chart().mark_bar(color='forestgreen').encode(alt.X('Cost'), alt.Y('Year:O'), tooltip=['Cost', 'Year'])
        texted = charted.mark_text(align='left', baseline='middle', dx=3, fontSize=25).encode(text='Cost:Q')
        col21.altair_chart(alt.layer(charted, texted, data=predict4).properties(width=900, height=350, title='Natural Predictions').configure_axis(labelFontSize=20, titleFontSize=20))
    elif flag == 2: 
        charted = alt.Chart().mark_bar(color='firebrick').encode(alt.X('Cost_result'), alt.Y('Year:O'), tooltip=['Cost_result', 'Year'])
        texted = charted.mark_text(align='left', baseline='middle', dx=3, fontSize=25).encode(text='Cost:Q')
        col21.altair_chart(alt.layer(charted, texted, data=predict3).properties(width=900, height=350, title='Human Predictions').configure_axis(labelFontSize=20, titleFontSize=20))
        charted = alt.Chart().mark_bar(color='forestgreen').encode(alt.X('Cost_result'), alt.Y('Year:O'), tooltip=['Cost_result', 'Year'])
        texted = charted.mark_text(align='left', baseline='middle', dx=3, fontSize=25).encode(text='Cost_result:Q')
        col21.altair_chart(alt.layer(charted, texted, data=predict4).properties(width=900, height=350, title='Natural Predictions').configure_axis(labelFontSize=20, titleFontSize=20))
    file_ = open("money.gif", "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()
    num = 600 - 600*num
    col22.markdown(f'<img src="data:image/gif;base64,{data_url}" width="{num}" height="{num}" alt="fire gif">', unsafe_allow_html=True,)
    col22.markdown('<b> Watch the money proportionally decrease by your human-caused fire input </b>', unsafe_allow_html=True)

def render_predictions():
    st.title('Decrease the Impact')
    st.markdown("Use the inputs below to determine prediction")
    human_input = st.text_input('Enter a number between 0 and 100 to decrease Human Impact:')
    fire_input = st.text_input('Enter a number between 0 and 100 to decrease Natural Impact:')
    if human_input == '':
        human_input = 0
    if fire_input == '':
        fire_input = 0
    try: 
        x, y = int(human_input), int(fire_input)
    except: 
        x, y = 0, 0
    return x, y 

def sammys_viz():
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

@st.cache
def dataloader():
    df = pd.read_csv('updated.csv')
    return df

def dataChanger(df, Year):
    df = df[ df['Year'] == Year ]
    return df

def causePlots(x):
    df1 = dataloader()
    df = dataChanger(df1, x)
    col1, col2, col3 = location1.beta_columns((2,1,1))
	
    #Map Image
    col1.image(image_bank[x - 1980], width=1225)
	
    #Create Pie Chart for Acres Burned
    human = df[df['Cause'] == 'Human']
    natural = df[df['Cause'] == 'Natural']
   
    if human['BurnTime'].iloc[0] == 0 and natural['BurnTime'].iloc[0] == 0: 
        col2.markdown('Both human-caused and nature-caused fires average 0 days for this year')
    else: 
        fig = px.pie(df, values='BurnTime', names='Cause', title=f'Burn Days per Fire in {x}', color='Cause', color_discrete_map={'Human':'red', 'Natural':'blue'})
        fig.update_layout(width=600,height=275)
        col2.plotly_chart(fig, width=600,height=275)

        #create Pie Chart for Average Burn Time
        fig2 = px.pie(df, values='Acres', names='Cause', title=f'Acres Burned per Fire in {x}', color='Cause', color_discrete_map={'Human':'red', 'Natural':'blue'})
        fig2.update_layout(width=600,height=275)
        col2.plotly_chart(fig2, width=600,height=275)

        col3.title('Understanding Fire Trends by Cause')
        col3.markdown('View the side-by-side comparison of human-caused and naturally-caused fires from the years 1985 - 2019. Observe the changes in number of fires (seen on the map) versus burn days and acres burned. Consider the fact that the greater amount of burn days increase the length of time resources are expended to suppress a fire. Also consider that, as acres-burned grows, the ability of fire fighters to supppress a fire lessens.')

def render_slider(year):
    key = random.random() if animation_speed else None
    year = sliderloc.slider("",min_value=1980, max_value=2016, key=key)
    return year

def showCount3(counter1, counter2):
    col1, col2 = st.beta_columns(2)
    col1.title('Acres Burned Clock')
    col1.markdown('Watch the clock as wildfires to see the rate of acres of land burned per second across the US')
    col1.title(f'{counter1}')
    col2.title('Reforestation Clock')
    col2.markdown('Watch the clock as humans attempt to reforest per second across the US')
    col2.title(f'{counter2}')
    
def showCount4(): 
    i2 = .15
    count2 = 4700398
    i = .30
    count1 = 9500000
    for number in range(1, 10000000):
        count1 += i
        count2 += i2
        showCount3(count1, count2)
        time.sleep(1)

if __name__ == "__main__":
    st.set_page_config(layout="wide")

    add_selectbox = st.sidebar.selectbox(
    "Select Naviation Page",
    ("Introduction", "Analysis", "Predictions")
    )
    
    if (add_selectbox == 'Introduction'):
        countLoc = st.empty()
        showCount4()
        st.title('Map of Wildfires caused by Humans and Nature over time')
	#buttLoc= st.button("Animate")
	#buttLoc2= st.button("Stop Animate")
        animation_speed = None
        location1 = st.empty()
        sliderloc = st.empty()
        years_values = [year for year in range(1980, 2017)]
        if st.button("Animate"):
            if not st.button("Stop Animate"):
                for year in cycle(years_values):
                    animation_speed= .4
                    time.sleep(animation_speed)
                    render_slider(year)
                    causePlots(year)
        else:
            year = render_slider(1980)
            causePlots(year)
    elif(add_selectbox == 'Analysis'):
        sammys_viz()
        other_viz()
        other_viz2()
        other_viz3()

    elif(add_selectbox == 'Predictions'):
        st.title('Time Series Forecasting: Future Acres Burned and Furure Cost of Suppression')
        st.markdown('## Below you can see the forecasting results of a time series analysis on acres burned from both naturally-caused and human-caused fires. Our model projects five years out from the conclusion of the dataset. Evidently, fires are on the rise. Perhaps shockingly, fires caused by humans are not comparable to those caused by nature. This is likely due to climate change inciting longer dry spells and increasing the length of time for which our nation is at risk for wild fires. As the nation looks into the future, we need to prepare for these rising fire-counts, as well as their subsequent suppression costs. Based on these metrics, we must start to consider what kind of influence we can have on these predictions. Was Smokey Bear right? Are we the only ones who can prevent wildfires?')
        st.markdown('## Inspired by this mantra, explore the predictor model below to investigate for yourself. If we were able to reduce human-caused fires by 30% how many acres would still burn? How much would it cost? ')
        st.title('Human vs. Natural Fire Predictions')
        other = st.empty()
        area51 = st.empty()
        human, natural = render_predictions()
        st.title('Human vs. Natural Cost Predictions')
        location2 = st.empty()
        if human == 0 and natural == 0:
            df = dataLoader2()
            flag = 1
            num = 0
        else:
            df = dataChanger2(human/100, natural/100)
            flag = 2
            num = human/100
        predictPlot(df, flag, num)
        predictCost(df, flag, num)
        display_pred_code()
   
