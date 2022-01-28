# %%
#import dependencies 
import pandas as pd
import streamlit as st
import plotly.express as px
import pdblp as bbg
from datetime import date

ticker = st.text_input('Ticker', 'HD US Equity')

con = bbg.BCon(port=8194, timeout=50000, debug=False)
con.debug = False
con.start()
today_date = date.today()
today = today_date.strftime("%Y%m%d")

last_price_s = con.bdh(ticker, "PX_LAST", start_date='20000101',end_date=today)
last_price_s.index = last_price_s.index.rename('Date')
last_price_s.columns = [ticker]

last_price_fig = px.line(last_price_s, title='<b>US Consumer Price Index (CPI)<b>')
st.plotly_chart(last_price_fig)
        