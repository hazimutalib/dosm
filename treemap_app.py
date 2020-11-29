import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
sns.set()
import base64
import plotly.express as px

st.write(""" # Malaysia's Trade Performance Dashboard Application """)

df = pd.read_csv("trade_new.csv")
df_country = pd.read_csv("region.csv")


feature = st.selectbox('Feature:', ['COUNTRY', 'SITC 1 DIGIT', 'SITC 2 DIGIT', 'YEAR'])
metric = st.selectbox('Metric:', ['IMPORT (MILLION RM)','EXPORT (MILLION RM)'] )
columns = st.selectbox('Specification(s):', df[['COUNTRY', 'SITC 1 DIGIT', 'SITC 2 DIGIT', 'YEAR']].drop(feature, axis=1).columns, key='52')
i = i = st.selectbox(columns + ':', np.sort(df[columns].unique()), key='3')
if feature == 'COUNTRY':
    df_group = df[df[columns] == i ].groupby('COUNTRY')[metric].sum().reset_index()
    df_merge = df_group.merge(df_country, on='COUNTRY', how='inner')
    df_merge = df_merge[df_merge[metric] > 0]
    df_merge["WORLD"] = "WORLD"
    fig = px.treemap(df_merge, path=['WORLD', 'Region', feature], values=metric, color=metric, hover_data=[metric], color_continuous_scale='RdBu')
    st.plotly_chart(fig)
elif feature == 'SITC 2 DIGIT':
    df_merge = df[df[columns] == i ].groupby([feature,'SITC 1 DIGIT'])[metric].sum().reset_index()
    df_merge = df_merge[df_merge[metric] > 0]
    df_merge["COMMODITY"] = "COMMODITY"
    fig = px.treemap(df_merge, path=['COMMODITY', 'SITC 1 DIGIT', feature], values=metric, color=metric, hover_data=[metric], color_continuous_scale='RdBu')
    st.plotly_chart(fig)
else:
    fig = px.treemap(df[df[columns] == i], path=[feature], values=metric, color=metric, hover_data=[metric],color_continuous_scale='RdBu')
    st.plotly_chart(fig)