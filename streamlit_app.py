# %%
#import dependencies 
import matplotlib.pyplot as plt 
import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import pdblp as bbg
from datetime import date
from xbbg import blp
#import altair as alt


st.set_page_config(
    page_title = "Consumer Dashboard", 
    layout="wide")

# %%
st.sidebar.title("Dashboard for Consumer Sector")

# Create a page dropdown 
page = st.sidebar.radio("SECTIONS",["State of the US Consumer", "Macroeconomic Indicators"]) 

if page == "State of the US Consumer":
    # Display details of page 1
    st.title("State of the US Consumer")

elif page == "Macroeconomic Indicators":
    # Display details of page 1
    st.title("Macroeconomic Indicators")
    st.sidebar.subheader("")
    st.sidebar.subheader("")
    st.sidebar.subheader("Macroeconomic Indicators")
    st.sidebar.write("   1.    Cost of Living")
    st.sidebar.write("   2.    Consumer Confidence and Sentiment")
    st.sidebar.write("   3.    Economic Growth and Retail Sales")
    st.sidebar.write("   4.    Financial Indicators")       

    # %% Bloomberg data 

    con = bbg.BCon(port=8194, timeout=50000, debug=False)
    con.debug = False
    con.start()
    today_date = date.today()
    today = today_date.strftime("%Y%m%d")

    #Monthly CPI 
    cpiyoy_s = con.bdh("CPI YOY Index", "PX_LAST", start_date='20000101',end_date=today)
    #cpiyoy_df = pd.DataFrame(cpiyoy)
    cpiyoy_s.index = cpiyoy_s.index.rename('Date')
    cpiyoy_s.columns = ['CPI (%)']
    cpiyoy_twelvemonthavg = cpiyoy_s.iloc[[-12,-11,-10,-9,-8,-7,-6,-5,-4,-3,-2,-1],-1].mean()
    cpiyoy_threemonthavg = cpiyoy_s.iloc[[-3,-2,-1],-1].mean()
    cpiyoy_diff = cpiyoy_s.iloc[-1,-1]-cpiyoy_s.iloc[-13,-1]
    cpiyoy_current = cpiyoy_s.iloc[-1,-1]
    cpiyoy_previous = cpiyoy_s.iloc[-2,-1]

    # ====================================COST OF LIVING ====================================
    st.subheader("Cost of Living")
        
    col1, col2 = st.columns(2)
    with col1:
        #CPI line chart 
        cpiyoy_fig = px.line(cpiyoy_s, title='<b>US Consumer Price Index (CPI)<b>')
        cpiyoy_fig.update_traces(line=dict(color = 'rgb(213,0,50)', width = 3))
        cpiyoy_fig.update_xaxes(rangeslider_visible=True)
        cpiyoy_fig.update_layout(height = 300, title_font_color ='rgb(114,117,117)', title_font_size = 18, xaxis=dict(
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
        yaxis=dict(
            title = 'Inflation (%)',
            title_font_size=12,
            title_font_family='Arial',
            zeroline=False,
            showgrid = True,
            gridcolor='rgb(114,117,117)',      
            showline=True,
            showticklabels=True,
        ),
        autosize=False,
        margin=dict(
            autoexpand=False,
            l=40,
            r=30,
            t=30
        ), showlegend = False,
        legend = dict(
            title = 'Inflation',
            yanchor = 'top',
            y = 0.99, 
            xanchor = 'left',
            x = 0.01))
        cpiyoy_fig.add_annotation(text = f'Current:         {cpiyoy_current:.1f}% <br>YoY change:  {cpiyoy_diff:.1f}% <br>3M avg:          {cpiyoy_threemonthavg: .1f}% <br>12M avg:       {cpiyoy_twelvemonthavg: .1f}%',
                        align='left',
                        showarrow=False,
                        xref='paper',
                        yref='paper',
                        x=0.02,
                        y=0.98,
                        bgcolor = 'white')
        st.plotly_chart(cpiyoy_fig,use_container_width= True)
        
        #CPI heatmap 
        cpiyoy_recent = cpiyoy_s.tail(18)
        cpiyoy_recent = cpiyoy_recent.transpose()

        cpiyoy_fig2 = px.imshow(cpiyoy_recent, color_continuous_scale='temps', zmin =1, zmax = 6)
        cpiyoy_fig2.update_layout(height=70, coloraxis_showscale=False, margin=dict(l=40, r=30, t=20, b=20))
        cpiyoy_fig2.update_xaxes(showticklabels=True, title = '')
        cpiyoy_fig2.update_yaxes(showticklabels=False)
        st.plotly_chart(cpiyoy_fig2, use_container_width= True)

    