# %%
#import dependencies 
import streamlit as st
import pdblp as bbg
from datetime import date

ticker = st.text_input('Ticker', 'HD US Equity')

con = bbg.BCon(port=8194, timeout=50000, debug=False)
con.debug = False
con.start()

last_price_s = con.bdh(ticker, "PX_LAST", start_date='20000101',end_date=today)

st.plotly_chart(last_price_s)
        