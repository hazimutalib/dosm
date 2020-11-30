import plotly.express as px
import pandas as pd
import streamlit as st

st.write(""" # Malaysia's Trade Performance Dashboard Application """)

df_all = pd.read_csv("trade_new.csv")
sitc_1 = pd.read_csv('sitc_1.csv')
sitc_2 = pd.read_csv('sitc_2.csv')

show = st.selectbox('Metric:', ['IMPORT (MILLION RM)', 'EXPORT (MILLION RM)'], key='1')
sitc = st.selectbox('SITC:', ['SITC 1 DIGIT', 'SITC 2 DIGIT'])

if sitc == 'SITC 1 DIGIT':
    df_sitc_1 = df_all.groupby(['SITC 1 DIGIT', 'YEAR'])[show].agg(['sum']).reset_index()
    df_sitc_1 = df_sitc_1.merge(sitc_1, on='SITC 1 DIGIT')
    fig = px.area(df_sitc_1, x="YEAR", y="sum", color="1D DESC")
else:
    df_sitc_1 = df_all.groupby(['SITC 2 DIGIT', 'YEAR'])[show].agg(['sum']).reset_index()
    df_sitc_1 = df_sitc_1.merge(sitc_2, on='SITC 2 DIGIT')
    fig = px.area(df_sitc_1, x="YEAR", y="sum", color="2D DESC")
    fig.update_layout(showlegend=False)
st.plotly_chart(fig)