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

st.set_page_config(layout="wide")

####DATA#####
df = pd.read_excel('Data.xlsx')
df1 = pd.read_excel('Data.xlsx',3)
df2 = pd.read_csv('significant-fires_2005-2019.csv')
df3 = pd.read_csv('Perscribed_Fires.csv')
df4 = pd.read_csv('acres_merged_prediction_results.csv')
df5 = pd.read_csv('predict_raw.csv')

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
    df['cost_thousands'] = df['Total']/1000000
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

@st.cache
def load5():
    df5 = pd.read_csv('predict_raw.csv')
    return df5

result = load5()
def other_viz3(result):
    
    firetype_df2 = result.groupby(['YEAR_','FIRETYPE']).size().reset_index(name="Firetype Count")
    firetype_df2['FIRETYPE'] = firetype_df2['FIRETYPE'].replace(0, 'Action Fires/Supressed Fires')
    firetype_df2['FIRETYPE'] = firetype_df2['FIRETYPE'].replace(1, 'Natural Out')
    firetype_df2['FIRETYPE'] = firetype_df2['FIRETYPE'].replace(2, 'Support Action/Assist Fire')
    firetype_df2['FIRETYPE'] = firetype_df2['FIRETYPE'].replace(3, 'Fire Management/Perscribed')
    firetype_df2['FIRETYPE'] = firetype_df2['FIRETYPE'].replace(4, 'False Alarm')
    firetype_df2['FIRETYPE'] = firetype_df2['FIRETYPE'].replace(5, 'Severe')

    acreage =  result.groupby(['YEAR_','FIRETYPE'])['TOTALACRES'].sum().reset_index(name="Firetype Acres")
    acreage['YEAR_'] = acreage['YEAR_'].astype(str)
    acreage['FIRETYPE'] = acreage['FIRETYPE']

    selection = alt.selection_multi(fields=['FIRETYPE'], bind='legend')
     
    base = alt.Chart(firetype_df2).mark_point(filled=True).encode(
    x=alt.X('YEAR_:N', axis=alt.Axis(labelAngle=360, values = [1980,1985,1990, 1995, 2000, 2005, 2010, 2016]), title = 'Year'),
    y='Firetype Count:Q',
    color=alt.Color('FIRETYPE:N', scale=alt.Scale(scheme='category20b')),
    tooltip=["FIRETYPE:N", 'YEAR_:N'],
    opacity=alt.condition(selection, alt.value(1), alt.value(0.2))
    ).add_selection(selection).properties(width=700, height=400, title='Figure 13: National wildfires count by type')

    base
    st.subheader('Inspite the groups focus on Human and Natural causes of fires, the illustration above illustrates the different fire types, their count, and trend for the past 37 years. Natural out and action fires have been the most dominant in terms of count of fires. The primary insight for this chart is to better understand how monetary resources could best be utilized. Information gathered from governmental budget requests, suggests that fund allocations and distribuitions is determined by the most recent 3 year observations. Additionally, it is also influenced by the current fiscal year lines of efforts. The intent of this graph is to understand trends in order to aid the decision making process for budget distribution.')
    st.subheader('In recent years the western states have began to adjust their strategic plans for combating wildfires. Past initiatives primarily focused on positioning states to have a reactive posture to wildfires since it is a seasonal occurrence. The residual effect was that major portions of the fiscal year budget (approx. 50% land management budget) was allocated for personnel and equipment. In California’s 2020-21 budget proposal, it was stated that the wildfire threat has been enhanced by the inability to maintain public lands and the population growth outpacing the state’s ability to emplace proper infrastructure. The proposal highlights enduring initiatives that shifts the states focus to emplace proactive counter measures.')

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
    predict_df2['Cost'] = predict_df2['Cost']/1000000
    predict_df2['Acres'] = predict_df2['Acres']/1000000
    predict_df2 = predict_df2.round(4)
    predict3 = predict_df2[predict_df2['Cause']== 'Human']
    predict4 = predict_df2[predict_df2['Cause']== 'Natural']
    return predict_df2, predict3, predict4

@st.cache(allow_output_mutation=True)
def dataChanger2(humanperc, naturalperc):
    predict, predict2, predict3 = dataLoader2()
    predict['Acre_result'] = np.where(predict['Cause']=='Human', predict['Acres'] - predict['Acres']*humanperc, predict['Acres'] - predict['Acres']*naturalperc)
    predict['Cost_result'] = np.where(predict['Cause']=='Human', predict['Cost'] - predict['Cost']*humanperc, predict['Cost'] - predict['Cost']*naturalperc)
    predict4 = predict[predict['Cause']== 'Human']
    predict5 = predict[predict['Cause']== 'Natural']
    return predict, predict4, predict5

def predictPlot(predict3, predict4, flag, num):
    col1, col2 = area51.beta_columns((2,1))
    if flag == 1: 
        charted = alt.Chart().mark_bar(color='firebrick').encode(alt.X('Acres', axis=alt.Axis(title='Acres (millions)')), alt.Y('Year:O'), tooltip=['Acres', 'Year'])
        texted = charted.mark_text(align='left', baseline='middle', dx=3, fontSize=25).encode(text='Acres:Q')
        col1.altair_chart(alt.layer(charted, texted, data=predict3).properties(width=1000, height=350, title='Human Predictions').configure_axis(labelFontSize=20, titleFontSize=20))
        charted = alt.Chart().mark_bar(color='forestgreen').encode(alt.X('Acres', axis=alt.Axis(title='Acres (millions)')), alt.Y('Year:O'), tooltip=['Acres', 'Year'])
        texted = charted.mark_text(align='left', baseline='middle', dx=3, fontSize=25).encode(text='Acres:Q')
        col1.altair_chart(alt.layer(charted, texted, data=predict4).properties(width=1000, height=350, title='Natural Predictions').configure_axis(labelFontSize=20, titleFontSize=20))
    elif flag == 2: 
        charted = alt.Chart().mark_bar(color='firebrick').encode(alt.X('Acre_result', axis=alt.Axis(title='Acres (millions)')), alt.Y('Year:O'), tooltip=['Acre_result', 'Year'])
        texted = charted.mark_text(align='left', baseline='middle', dx=3, fontSize=25).encode(text='Acre_result:Q')
        col1.altair_chart(alt.layer(charted, texted, data=predict3).properties(width=1000, height=350, title='Human Predictions').configure_axis(labelFontSize=20, titleFontSize=20))
        charted = alt.Chart().mark_bar(color='forestgreen').encode(alt.X('Acre_result', axis=alt.Axis(title='Acres (millions)')), alt.Y('Year:O'), tooltip=['Acre_result', 'Year'])
        texted = charted.mark_text(align='left', baseline='middle', dx=3, fontSize=25).encode(text='Acre_result:Q')
        col1.altair_chart(alt.layer(charted, texted, data=predict4).properties(width=1000, height=350, title='Natural Predictions').configure_axis(labelFontSize=20, titleFontSize=20))

    file_ = open("fire.gif", "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()
    num = 700 - 700*num
    col2.markdown(f'<img src="data:image/gif;base64,{data_url}" width="{num}" height="{num}" alt="fire gif">', unsafe_allow_html=True)
    col2.write('Watch the fire proportionally decrease by your human-caused fire input')

def predictCost(predict3, predict4, flag, num):
    col21, col22 = location2.beta_columns((2,1))
    if flag == 1: 
        charted = alt.Chart().mark_bar(color='firebrick').encode(alt.X('Cost', axis=alt.Axis(format='$', title='Cost (millions)')), alt.Y('Year:O'), tooltip=['Cost', 'Year'])
        texted = charted.mark_text(align='left', baseline='middle', dx=3, fontSize=25).encode(text='Cost:Q')
        col21.altair_chart(alt.layer(charted, texted, data=predict3).properties(width=1000, height=350, title='Human Predictions').configure_axis(labelFontSize=20, titleFontSize=20))
        charted = alt.Chart().mark_bar(color='forestgreen').encode(alt.X('Cost', axis=alt.Axis(format='$', title='Cost (millions)')), alt.Y('Year:O'), tooltip=['Cost', 'Year'])
        texted = charted.mark_text(align='left', baseline='middle', dx=3, fontSize=25).encode(text=alt.Text('Cost:Q', format=','))
        col21.altair_chart(alt.layer(charted, texted, data=predict4).properties(width=1000, height=350, title='Natural Predictions').configure_axis(labelFontSize=20, titleFontSize=20))
    elif flag == 2: 
        charted = alt.Chart().mark_bar(color='firebrick').encode(alt.X('Cost_result', axis=alt.Axis(format='$', title='Cost (millions)')), alt.Y('Year:O'), tooltip=['Cost_result', 'Year'])
        texted = charted.mark_text(align='left', baseline='middle', dx=3, fontSize=25).encode(text='Cost:Q')
        col21.altair_chart(alt.layer(charted, texted, data=predict3).properties(width=1000, height=350, title='Human Predictions').configure_axis(labelFontSize=20, titleFontSize=20))
        charted = alt.Chart().mark_bar(color='forestgreen').encode(alt.X('Cost_result', axis=alt.Axis(format='$', title='Cost (millions)')), alt.Y('Year:O'), tooltip=['Cost_result', 'Year'])
        texted = charted.mark_text(align='left', baseline='middle', dx=3, fontSize=25).encode(text=alt.Text('Cost_result:Q', format=','))
        col21.altair_chart(alt.layer(charted, texted, data=predict4).properties(width=1000, height=350, title='Natural Predictions').configure_axis(labelFontSize=20, titleFontSize=20))
    file_ = open("money.gif", "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()
    num = 700 - 700*num
    col22.markdown(f'<img src="data:image/gif;base64,{data_url}" width="{num}" height="{num}" alt="fire gif">', unsafe_allow_html=True,)
    col22.write('Watch the money proportionally decrease by your human-caused fire input')

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
                title='Figure 11: Wild Fires by State'
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
                alt.X('year(YEAR2):T',title='Year',scale=alt.Scale(zero=False),axis=alt.Axis(titleFontSize=18,labelFontSize=14)),
                alt.Y('sum(TOTALACRES):Q',title='Total Acres Burned', scale=alt.Scale(zero=False), axis=alt.Axis(titleFontSize=18,labelFontSize=14)),
                color='CAUSE:N',
                tooltip=[alt.Tooltip("YEAR2",title='Year'), alt.Tooltip('mean(TOTALACRES)',title='Acres Burned', format=",.4r")]
            ).properties(
                width=550,
                height=300,
                title="Figure 9: Total acres burned per year from 1980 to 2016"
    )

    chart_2 = alt.Chart(df).mark_line(point=True).encode(
                alt.X('year(YEAR2):T',title='Year',scale=alt.Scale(zero=False),axis=alt.Axis(titleFontSize=18,labelFontSize=14)),
                alt.Y('sum(Days):Q',title='Total Number of Days per Fires', scale=alt.Scale(zero=False), axis=alt.Axis(titleFontSize=14,labelFontSize=14)),
                color='CAUSE:N',
                tooltip=[alt.Tooltip("YEAR2",title='Year'), alt.Tooltip('mean(Days)',title='Days of Fire', format=".2r")]
    ).properties(
                width=550,
                height=300,
                title="Figure 10: Total number of days of fires per year from 1980 to 2016"
    )

    chart_3 = alt.Chart(df).mark_bar().encode(
                alt.X('STATE',title='State', sort='-y', axis=alt.Axis(titleFontSize=18,labelFontSize=14)),
                alt.Y('sum(TOTALACRES):Q',title='Acres Burned', axis=alt.Axis(titleFontSize=14,labelFontSize=14, format=',.4r')),
                color=alt.Color('CAUSE:N'),
                tooltip=[alt.Tooltip("CAUSE",title='Cause'), alt.Tooltip('sum(TOTALACRES)',title='Acres Burned', format=",.4r")]
            ).add_selection(
                select_year
            ).transform_filter(
                select_year
            ).properties(
                title="Figure 12: Acres burned by state (cause breakdown)"
    )

    US_map = alt.Chart(states).mark_geoshape().encode(
                color=alt.Color('acres:Q',title='Acreage Burned', axis=alt.Axis(titleFontSize=18,labelFontSize=14)),
                tooltip=['State:N',alt.Tooltip('acres:Q',title='Total Acres Burned', format = ",.4r")]
            ).transform_lookup(
                lookup='id',
                from_=alt.LookupData(source,'id',variables),
            ).project(
                type='albersUsa'
    )

    brush = alt.selection(type='interval', encodings=['x'])

    bar1 = alt.Chart(df_main).mark_bar().encode(
            x = alt.X('Year:O', scale=alt.Scale(zero=False),axis=alt.Axis(titleFontSize=18,labelFontSize=14)),
            y = alt.Y('cost_thousands:Q', scale=alt.Scale(zero=False), title='Suppression Cost (Millions)', axis=alt.Axis(titleFontSize=20,labelFontSize=14, format = "$,.0r")),
            opacity=alt.condition(brush, alt.OpacityValue(1), alt.OpacityValue(0.7)),
            tooltip=[alt.Tooltip("Total:Q",title='Total Cost', format="$,.4r"), alt.Tooltip("Year",title='Year')]
        ).add_selection(
            brush
        ).properties(
        width=550,
        title='Figure 1: Overview of supression costs from 1985 to 2019'
    )

    rule1 = alt.Chart(df_main).mark_rule(color='red').encode(
                y='mean(cost_thousands):Q',
                size=alt.SizeValue(3)
            ).transform_filter(
                brush
    )


    bar2 = alt.Chart(df_main).mark_bar().encode(
            x = alt.X('Year:O', scale=alt.Scale(zero=False),axis=alt.Axis(titleFontSize=18,labelFontSize=14)),
            y = alt.Y('Acres:Q', scale=alt.Scale(zero=False), title='Acres Burned', axis=alt.Axis(titleFontSize=18,labelFontSize=14)),
            opacity=alt.condition(brush, alt.OpacityValue(1), alt.OpacityValue(0.7)),
            tooltip=[alt.Tooltip("Acres",title='Acres Burned', format=",.6r"), alt.Tooltip("Year",title='Year')]
        ).add_selection(
            brush
        ).properties(
        width=550,
        title='Figure 7: Total acres burned per year from 1985 to 2019'
    )

    rule2 = alt.Chart(df_main).mark_rule(color='red').encode(
            y='mean(Acres):Q',
            size=alt.SizeValue(3)
        ).transform_filter(
            brush
    )

    bar3 = alt.Chart(df_main).mark_bar().encode(
            x = alt.X('Year:O', scale=alt.Scale(zero=False),axis=alt.Axis(titleFontSize=18,labelFontSize=14)),
            y = alt.Y('Fires:Q', scale=alt.Scale(zero=False), title='Number of Fires', axis=alt.Axis(titleFontSize=18,labelFontSize=14)),
            opacity=alt.condition(brush, alt.OpacityValue(1), alt.OpacityValue(0.7)),
            tooltip=[alt.Tooltip("Fires",title='Number of Fires', format=",.4r"),alt.Tooltip("Year",title='Year')]
        ).add_selection(
            brush
        ).properties(
        width=550,
        title='Figure 8: Total number of fires per year from 1985 to 2019'
    )

    rule3 = alt.Chart(df_main).mark_rule(color='red').encode(
            y='mean(Fires):Q',
            size=alt.SizeValue(3)
    ).transform_filter(
            brush
    )

    bar4 = alt.Chart(df_main).mark_bar().encode(
            x = alt.X('Year:O', scale=alt.Scale(zero=False),axis=alt.Axis(titleFontSize=18,labelFontSize=14)),
            y = alt.Y('cost_per_acre:Q', scale=alt.Scale(zero=False), title='Cost per Acre Burned', axis=alt.Axis(titleFontSize=18,labelFontSize=14, format = "$,.2r")),
            opacity=alt.condition(brush, alt.OpacityValue(1), alt.OpacityValue(0.7)),
            tooltip=[alt.Tooltip("cost_per_acre",title='Cost per Acre Burned', format="$,.2r"),alt.Tooltip("Year",title='Year')]
        ).add_selection(
            brush
        ).properties(
        width=550,
        title='Figure 2: Cost per acre burned breakdown from 1985 to 2019'         
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

    brush1 = alt.selection(type='interval')

    scatter = alt.Chart(df_sig).mark_circle(size=200
    ).encode(
        x=alt.X('Days:Q', title='Days of Fire',scale=alt.Scale(domain=(0,260)),axis=alt.Axis(titleFontSize=18,labelFontSize=14)),
        y=alt.Y('cost_per_acre:Q', title='Cost per Acre Burned', scale=alt.Scale(domain=(0,2000)),axis=alt.Axis(titleFontSize=18,labelFontSize=14,format="$,.2r")),
        color= alt.Color('Cause:N'),
        tooltip=[alt.Tooltip('Name:N',title='Name of Fire'), alt.Tooltip('State:N'), alt.Tooltip('Acres:Q',title='Acres Burned'), alt.Tooltip('cost_per_acre:Q',title="Cost per Acre", format="$,.2r"),alt.Tooltip('Days:Q',title="Days of Fire")],
        size=alt.Size("Acres:Q", title='Acres Burned',scale=alt.Scale(range=[0, 1000],domain=(0,300000))),
    ).properties(
        width=550,
        height=400,
        title='Figure 5: Cost per acre vs days of fire broken down by human vs natural cause and acreage burned'
    ).transform_filter(
       brush1
    # ).add_selection(
    #   select_year1
    # ).transform_filter(
    #   select_year1
    ).interactive()

    scatter1 = alt.Chart(df_sig).mark_circle(size=200
    ).encode(
        x=alt.X('State:N', title='State',scale=alt.Scale(zero=False),axis=alt.Axis(titleFontSize=18,labelFontSize=14)),
        y=alt.Y('cost_per_acre:Q', title='Cost per Acre',axis=alt.Axis(titleFontSize=18,labelFontSize=14,format="$,.2r")),
        color= alt.Color('Cause:N'),
        tooltip=[alt.Tooltip('Name:N',title='Name of Fire'), alt.Tooltip('State:N',title='State'), alt.Tooltip('Acres:Q',title='Acres Burned'), alt.Tooltip('cost_per_acre:Q',title="Cost per Acre", format="$,.2r"),alt.Tooltip('Days:Q',title="Days of Fire")],
        size=alt.Size("Days:Q", title='Days Burned')
    ).properties(
        width=550,
        height=400,
        title='Figure 6: Cost per acre vs state broken down by human vs natural cause and days of fire'
    ).add_selection(
       brush1

    #).interactive()
    )
    single = alt.selection_single(fields=['Cause'])

    nat_human = alt.Chart(df_sig).mark_line(point=True).encode(
                alt.X('Year:O',title='Year',scale=alt.Scale(zero=False),axis=alt.Axis(titleFontSize=18,labelFontSize=14)),
                alt.Y('mean(cost_per_acre):Q',title='Cost per Acre Burned', scale=alt.Scale(zero=False), axis=alt.Axis(titleFontSize=18,labelFontSize=14, format='$,.3r')),
                color='Cause:N',
                tooltip=[alt.Tooltip("Year:O",title='Year'),alt.Tooltip("mean(cost_per_acre):Q",title='Cost per Acre Burned',format='$,.3r')]
        ).properties(
                width=800,
                height=300,
                title='Figure 3: Cost per Acre (cause breakdown)'

    )

    nat_human1 = alt.Chart(df_sig).mark_bar(
        ).encode(
            y=alt.Y('Cause:N',title='Cause',axis=alt.Axis(titleFontSize=18,labelFontSize=14)),
            x=alt.X('mean(cost_per_acre):Q', title='Cost per Acre Burned', axis=alt.Axis(titleFontSize=18,labelFontSize=14, format='$,.3r')),
            color='Cause:N',
            tooltip=[alt.Tooltip("mean(cost_per_acre):Q",title='Cost per Acre Burned',format='$,.3r')]
        ).properties(
            title='Figure 4: 14 year average of cost per acre (cause breakdown)'

    )
    text1 = nat_human1.mark_text(
            align='left',
            baseline='middle',
            dx=3  # Nudges text to right so it doesn't appear on top of the bar
        ).encode(
            text=alt.Text('mean(cost_per_acre):Q',format='$.3r')
    )
#        ).add_selection(
#        select_year1
#        ).transform_filter(
#        select_year1

    st.markdown('# Overview')
    st.subheader('In this section we will explore and analyze the impact of wildfires in the United States from both an economic and an enviornmental perspective. We will also be breaking down human vs natural caused fires and identify the impacts of each. Finally we will discuss different fire protections and fire types.')
    st.header('Impact on the Economy')
    
    (bar1 + rule1) | (bar4 + rule4)
    st.subheader("You can select an interval on either graph to see the mean (red line) of a certain period of time and this will be reflected on the other chart as well. You can also hover over each bar to get the exact dollar ($) ammount per year.")
    st.subheader("Over the years, the cost of suppressing wildfires has gone up significantly especially at the turn of the century. Looking at Figure 1 alone, we can assume that a significant increase in suppression cost per year is due to either one or both of rising operational costs or a rise in the size or amount of fires. Figure 2 gives us some insight into why we see such a sharp increase because it looks at the cost per acre, which keeps the 'size of fires' variable constant. We can infer that the operational costs have gone up for fire suppression. However, the increase in 'cost per acre' is not proportional to the increase in suppression costs, which leads us to believe the size or amount of fires plays a role in the increase of total suppression costs.") 
    nat_human & (nat_human1 + text1)
    
    #st.write('Figure 2: Cost per Acre Burned Breakdown')
    st.subheader("Hover over figue 3's data points to get the exact values for each year.")
    st.subheader("When we look at the past 14 years significant fire information (Figure 2), cost to the US government to put down a fire cause by humans is $251 per acre which is 64% more than money spent to put down the fires caused by natural causes ($153). However, 85% of the total wildfires land was burned by natural causes.")
    st.write()

    st.write(alt.concat(scatter,scatter1).resolve_scale(size='independent'))
    st.subheader("You can hover over the circles on Figure 5 and 6 to see more information about each fire. You can also zoom in and out of Figure 5. Finally, you have the option to select an interval on Figure 6, which will highlight those same points on Figure 5 to give you a better sense of the cost per acre relative to the days of fire for each state. ")
    st.subheader("Although, there is no significant correlation between cost of acre burned and duration of fire, the illustration below demonstrates an interesting spread of significant fires across the state in past 14 years. From Figure 6 we can identify that California has a much higher cost per acre burned. We assume this is due to high operational costs in Calfiornia. On the flip slide we also noticed that Alaska despite having multiple large firest that burned for a high number of days, maintained a relatively low cost per acre, which is contrast to California. ")
    st.header('Impact on the Enviornment')
    (bar2 + rule2) | (bar3 + rule3)
    st.subheader("You can select an interval on either graph to see the mean (red line) of a certain period of time and this will be reflected on the other chart as well. You can also hover over each bar to get the exact number of fires or acres burned per year.")
    
    chart_1 | chart_2
    
    map_chart = background + fire_points
    map_chart
    st.subheader("You can hover over each circle to get more details about each fire. You can also use the year slider to cycle through the years to see the differences from one year to another.")
    st.subheader("Throughout the years, it is evident that fires have been more significant on the west coast rather than east coast. Natural caused fires seem to be larger than human caused ones, which fits with what we discussed earlier with 85% of land burned by natural caused fires. One other interesting observation is the presence of small human caused fires in the mid-west and east coast.")
    chart_3
    st.subheader('The significant wildfires for human causes has been 415k acers on an average every year but the land burned due to natural causes has been 2.3m acres (5.5 times than the human causes).')


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
    col1.image(image_bank[x - 1980], width=725)
	
    #Create Pie Chart for Acres Burned
    human = df[df['Cause'] == 'Human']
    natural = df[df['Cause'] == 'Natural']
   
    if human['BurnTime'].iloc[0] == 0 and natural['BurnTime'].iloc[0] == 0: 
        col2.subheader('Both human-caused and nature-caused fires average 0 days for this year')
    else: 
        fig = px.pie(df, values='BurnTime', names='Cause', title=f'Burn Days per Fire in {x}', color='Cause', color_discrete_map={'Human':'red', 'Natural':'blue'})
        fig.update_layout(width=375,height=275)
        col2.plotly_chart(fig, width=375,height=275)

        #create Pie Chart for Average Burn Time
        fig2 = px.pie(df, values='Acres', names='Cause', title=f'Acres Burned per Fire in {x}', color='Cause', color_discrete_map={'Human':'red', 'Natural':'blue'})
        fig2.update_layout(width=375,height=275)
        col2.plotly_chart(fig2, width=375,height=275)

        col3.title('Understanding Fire Trends by Cause')
        col3.subheader('View the side-by-side comparison of human-caused and naturally-caused fires from the years 1985 - 2019. Observe the changes in number of fires (seen on the map) versus burn days and acres burned. Consider the fact that the greater amount of burn days increase the length of time resources are expended to suppress a fire. Also consider that, as acres-burned grows, the ability of fire fighters to supppress a fire lessens.')

def render_slider(year):
    key = random.random() if animation_speed else None
    year = sliderloc.slider("",min_value=1980, max_value=2016, key=key)
    return year

def showCount3(counter1, counter2):
    col1, col2 = countLoc.beta_columns(2)
    col1.title('Acres Burned Clock')
    col1.subheader('Watch the clock as wildfires to see the rate of acres of land burned per second across the US')
    col1.title(f'{counter1}')
    col2.title('Reforestation Clock')
    col2.subheader('Watch the clock as humans attempt to reforest per second across the US')
    col2.title(f'{counter2}')
    
def showCount4(): 
    i2 = .15
    count2 = 4700398
    i = .30
    count1 = 9500000
    for number in range(1, 10000):
        count1 += i
        count2 += i2
        showCount3(count1, count2)
        time.sleep(1)


def reforestationInputs(): 
    st.title('Change your Impact')
    st.subheader("Use the inputs below to catch deforestation rates with increased reforestation efforts")
    human_input = st.text_input('Enter a number to increase millions of acres reforested per year:')
    if human_input == '':
        human_input = 0
    try: 
        x= int(human_input)
    except: 
        x = 0
    return x

def displayForest(count1, count2):
    col1, col2 = reforestLoc.beta_columns(2)
    col1.title('Acres Burned Clock')
    col1.subheader('Watch the clock as wildfires to see the rate of acres of land burned per second across the US')
    col1.title(f'{count1}')
    col2.title('Reforestation Clock')
    col2.subheader('Watch the clock as humans attempt to reforest per second across the US')
    col2.title(f'{count2}')

def showCountForest(reforest): 
    i = .30
    count1 = 9500000
    count2 = 4700398
    if reforest == 0: 
        i2 = .158
    else: 
        i2 = ((((5000000 + reforest*1000000)/365)/24)/60)/60
    for number in range(1, 10000000):
        count1 += i
        count2 += i2
        displayForest(count1, count2)
        time.sleep(1)

if __name__ == "__main__":
    #st.set_page_config(layout="wide")

    add_selectbox = st.sidebar.selectbox(
    "Select Naviation Page",
    ("Introduction", "Exploration", "Predictions")
    )
    
    if (add_selectbox == 'Introduction'):
        st.title('Map of Wildfires caused by Humans and Nature over time')
        buttLoc= st.button("Animate")
        buttLoc2= st.button("Stop Animate")
        animation_speed = None
        location1 = st.empty()
        sliderloc = st.empty()
        years_values = [year for year in range(1980, 2017)]
        if buttLoc:
            if not buttLoc2:
                for year in cycle(years_values):
                    animation_speed= .4
                    time.sleep(animation_speed)
                    render_slider(year)
                    causePlots(year)
        else:
            year = render_slider(1980)
            causePlots(year)
        countLoc = st.empty()
        showCount4()
    elif(add_selectbox == 'Exploration'):
        sammys_viz()
        other_viz3()

    elif(add_selectbox == 'Predictions'):
        st.title('Time Series Forecasting: Future Acres Burned and Furure Cost of Suppression')
        st.subheader('Below you can see the forecasting results of a time series analysis on acres burned from both naturally-caused and human-caused fires. Our model projects five years out from the conclusion of the dataset. Evidently, fires are on the rise. Perhaps shockingly, fires caused by humans are not comparable to those caused by nature. This is likely due to climate change inciting longer dry spells and increasing the length of time for which our nation is at risk for wild fires. As the nation looks into the future, we need to prepare for these rising fire-counts, as well as their subsequent suppression costs. Based on these metrics, we must start to consider what kind of influence we can have on these predictions. Was Smokey Bear right? Are we the only ones who can prevent wildfires?')
        st.subheader('Inspired by this mantra, explore the predictor model below to investigate for yourself. If we were able to reduce human-caused fires by 30% how many acres would still burn? How much would it cost? ')
        human, natural = render_predictions()
        st.title('Human vs. Natural Fire Predictions')
        other = st.empty()
        area51 = st.empty()
        st.title('Human vs. Natural Cost Predictions')
        location2 = st.empty()
        if human == 0 and natural == 0:
            df, predict3, predict4 = dataLoader2()
            flag = 1
            num = 0
        else:
            df, predict3, predict4 = dataChanger2(human/100, natural/100)
            flag = 2
            num = human/100
        predictPlot(predict3, predict4, flag, num)
        predictCost(predict3, predict4, flag, num)
        display_pred_code()
        st.subheader('While we may assign a budget to suppress wildfires more quickly, these actions alone will not reduce the negative effects of wildfires on our climate. Below are the Acres-Burned and Reforestation Clocks. Right now, the reforestation clock is running behind, but all of us together can speed it up.')
        reforestLoc = st.empty()
        reforest = reforestationInputs()
        showCountForest(reforest)
   
