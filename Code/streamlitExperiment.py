import altair as alt
import pandas as pd
import streamlit as st
import os, vega, time, random, base64
import pandas as pd
import numpy as np
from datetime import datetime 
import plotly.express as px
import matplotlib.pyplot as plt
from itertools import cycle

# Screen Setup
st.beta_set_page_config(layout="wide")
st.title('Map of Wildfires caused by Humans and Nature over Time')
st.subheader("Animation")
animations = {"None": None, "Slow": 0.4, "Medium": 0.2, "Fast": 0.05}
animate = st.radio("", options=list(animations.keys()), index=2)
animation_speed = animations[animate]
location1 = st.empty()
sliderloc = st.empty()
years_values = [year for year in range(1980, 2017)]

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
    df = pd.read_csv('updated.csv')
    # df['Cause'] = df['CAUSE']
    # df['Year'] = df['YEAR_']
    # df['Acres'] = df['TOTALACRES']
    # df['STARTDATED'] = pd.to_datetime(df['STARTDATED'], errors='coerce')
    # df['OUTDATED'] = pd.to_datetime(df['OUTDATED'], errors='coerce')
    # df['BurnTime'] = abs(df['OUTDATED'] - df['STARTDATED'])
    # df['BurnTime'].fillna(pd.Timedelta(days=0), inplace=True)
    # df['BurnTime'] = df['BurnTime'].dt.days.astype(int)
    return df

def dataChanger(df, Year):
    df = df[ df['Year'] == Year ]
    # newdata = df.groupby(['Year', 'Cause'], as_index=False)[['BurnTime', 'Acres']].sum(numeric_only=False)
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


if animation_speed:
    for year in cycle(years_values):
        time.sleep(animation_speed)
        render_slider(year)
        causePlots(year)
else:
    year = render_slider(1980)
    causePlots(year)

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
    if flag == 1: 
        charted = alt.Chart().mark_bar().encode(alt.X('Acres'), alt.Y('Cause:O',  axis=alt.Axis(labels=False)), color='Cause:O',  tooltip=['Acres', 'Cause', 'Year'])
        texted = charted.mark_text(align='left', baseline='middle', dx=3, fontSize=25).encode(text='Acres:Q')

        col1.altair_chart(alt.layer(charted, texted, data=predict_df2).properties(width=1500, height=150).facet(row='Year:O').configure_legend(labelFontSize=20, titleFontSize=25).configure_axis(labelFontSize=20, titleFontSize=20))
    elif flag == 2: 
        charted = alt.Chart().mark_bar().encode(alt.X('Acre_result'), alt.Y('Cause:O',  axis=alt.Axis(labels=False)), color='Cause:O',  tooltip=['Acre_result', 'Cause', 'Year'])
        texted = charted.mark_text(align='left', baseline='middle', dx=3, fontSize=25).encode(text='Acre_result:Q')

        col1.altair_chart(alt.layer(charted, texted, data=predict_df2).properties(width=1500, height=150).facet(row='Year:O').configure_legend(labelFontSize=20, titleFontSize=25).configure_axis(labelFontSize=20, titleFontSize=20))

    file_ = open("fire.gif", "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()
    num = 900 - 900*num
    col2.markdown(f'<img src="data:image/gif;base64,{data_url}" width="{num}" height="{num}" alt="fire gif">', unsafe_allow_html=True)
    col2.markdown('<b> Watch the fire proportionally decrease by your human-caused fire input </b>', unsafe_allow_html=True)

def predictCost(df, flag, num):
    col21, col22 = location2.beta_columns((2,1))
    if flag == 1: 
        charted = alt.Chart().mark_bar().encode(alt.X('Cost'), alt.Y('Cause:O',  axis=alt.Axis(labels=False)), color='Cause:O',  tooltip=['Cost', 'Cause', 'Year'])
        texted = charted.mark_text(align='left', baseline='middle', dx=3, fontSize=25).encode(text='Cost:Q')

        col21.altair_chart(alt.layer(charted, texted, data=df).properties(width=1500, height=150).facet(row='Year:O').configure_legend(labelFontSize=20, titleFontSize=25).configure_axis(labelFontSize=20, titleFontSize=20))
    elif flag == 2: 
        charted = alt.Chart().mark_bar().encode(alt.X('Cost_result'), alt.Y('Cause:O',  axis=alt.Axis(labels=False)), color='Cause:O',  tooltip=['Cost_result', 'Cause', 'Year'])
        texted = charted.mark_text(align='left', baseline='middle', dx=3, fontSize=25).encode(text='Cost_result:Q')

        col21.altair_chart(alt.layer(charted, texted, data=df).properties(width=1500, height=150).facet(row='Year:O').configure_legend(labelFontSize=20, titleFontSize=25).configure_axis(labelFontSize=20, titleFontSize=20))

    file_ = open("money.gif", "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()
    num = 700 - 700*num
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

st.title('Human vs. Natural Fire Predictions')
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
