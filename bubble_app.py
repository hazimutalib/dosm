import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
sns.set()
import base64
import plotly.express as px

st.write(""" # Malaysia's Trade Performance Dashboard Application """)

df_all = pd.read_csv("trade_new.csv")
# get RCA
rca = pd.read_csv('Malaysia_RCA_stats.csv')
sitc_1 = pd.read_csv('sitc_1.csv')

'''PreProcessing'''

show = st.selectbox('Metric:', ['IMPORT (MILLION RM)', 'EXPORT (MILLION RM)'], key='1')
year = st.slider('YEAR:', 2013,2019,2018)
rca = rca.drop(['Reporter Name', 'Partner Name', 'Trade Flow'], axis=1)
rca_melt = rca.melt(id_vars=['1D DESC'], value_vars=['2013', '2014', '2015', '2016', '2017', '2018', '2019'])
rca_melt = rca_melt.rename(columns={'variable': 'YEAR', 'value': 'RCA Value'})
rca_melt['YEAR'] = rca_melt['YEAR'].astype(str).astype(int)
df_import_dynamic = df_all.groupby(['YEAR','SITC 1 DIGIT'])[[show]].sum().reset_index().sort_values(by=['SITC 1 DIGIT', 'YEAR'])
df_import_dynamic['Percent Change'] = df_import_dynamic.groupby(['SITC 1 DIGIT'])[[show]].pct_change().fillna(0)*100
df_import_dynamic = df_import_dynamic.sort_values(by=['YEAR','SITC 1 DIGIT'])
df_import_dynamic = df_import_dynamic.merge(sitc_1, on='SITC 1 DIGIT').merge(rca_melt, on=['YEAR', '1D DESC'])
df_import_dynamic['SITC 1 DIGIT'] = df_import_dynamic['SITC 1 DIGIT'].astype(str)

fig = px.scatter(df_import_dynamic.query("YEAR=={}".format(year)), x="RCA Value", y="Percent Change",size=show, color="SITC 1 DIGIT", hover_name="1D DESC", log_x=False, size_max=60)
st.plotly_chart(fig)