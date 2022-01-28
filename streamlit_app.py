# %%
#import dependencies 
from fredapi import Fred 
import matplotlib.pyplot as plt 
import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from datetime import date

# API key
## !!!MOVE OVER!!!
fred = Fred(api_key='cf633e2039d5b9a641d4b05bcb1a1095')

st.set_page_config(
    page_title = "Consumer Dashboard", 
    layout="wide")


st.sidebar.title("Dashboard for Consumer Sector")

# 30-yr mortgage rates US - WEEKLY
mortgage30us =fred.get_series('MORTGAGE30US', observation_start='2000-1-1')
mortgage30us_df =pd.DataFrame(mortgage30us, columns =['MORTGAGE30US'])
mortgage30us_df.index = mortgage30us_df.index.rename('Date')
mortgage30us_df.columns = ['30Y Mortgage Rate (%)']
mortgage30us_twelvemonthavg = mortgage30us_df.iloc[[-12,-11,-10,-9,-8,-7,-6,-5,-4,-3,-2,-1],-1].mean()
mortgage30us_threemonthavg = mortgage30us_df.iloc[[-3,-2,-1],-1].mean()
mortgage30us_diff = mortgage30us_df.iloc[-13,-1]-mortgage30us_df.iloc[-1,-1]
mortgage30us_current = mortgage30us_df.iloc[-1,-1]


    #====================================COST OF LIVING ====================================
st.subheader("Cost of Living")
with st.expander(label = '',expanded=True):
    col1, col2 = st.columns(2)
    col3.metric(label = "30Y Mortgage Rate", value = f"{mortgage30us_current:.1f}%", delta = f"{mortgage30us_diff:.1f}% YoY", delta_color = 'inverse')
        
col1, col2 = st.columns(2)
with col1:
    #30Y Mortgage Rate line chart 
    mortgage30us_fig = px.line(mortgage30us_df, title='<b>30Y Mortgage Rate<b>')
    mortgage30us_fig.update_traces(line=dict(color = 'rgb(4, 128, 154)', width = 3))
    mortgage30us_fig.update_xaxes(rangeslider_visible=True)
    mortgage30us_fig.update_layout(height = 300, title_font_color ='rgb(114,117,117)', title_font_size = 18, xaxis=dict(
        showline=True,
        showticklabels=True,
        showgrid = True,
        gridcolor='rgb(114,117,117)',
        linecolor='rgb(114,117,117)',
        ticks='outside',
        tickfont=dict(
            family='Arial',
            size=11,
            color='rgb(114,117,117)',
        ),
    ),
    st.plotly_chart(mortgage30us_fig,use_container_width= True)
        
    #30Y Mortgage Rate heatmap 
    mortgage30us_recent = mortgage30us_df.tail(78)
    mortgage30us_recent = mortgage30us_recent.transpose()

    mortgage30us_fig2 = px.imshow(mortgage30us_recent, color_continuous_scale='temps', zmin =2, zmax =4.5)
    mortgage30us_fig2.update_layout(height=70, coloraxis_showscale=False, margin=dict(l=40, r=30, t=20, b=20))
    mortgage30us_fig2.update_xaxes(showticklabels=True, title = '')
    mortgage30us_fig2.update_yaxes(showticklabels=False)
    st.plotly_chart(mortgage30us_fig2, use_container_width= True)


    with col2:
        