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

metric = st.sidebar.selectbox('Metric:', ['IMPORT (MILLION RM)', 'EXPORT (MILLION RM)'])

def single_graph_tree(feature):
    title = 'Trade Performance of Malaysia based on {} from 2013 to 2019'.format(feature)
    if feature == 'COUNTRY':
        df_group = df.groupby('COUNTRY')[metric].sum().reset_index()
        df_merge = df_group.merge(df_country, on='COUNTRY', how='inner')
        df_merge = df_merge[df_merge[metric] > 0]
        df_merge["WORLD"] = "WORLD"
        fig = px.treemap(df_merge, path=['WORLD', 'Region', feature], values=metric, color=metric, hover_data=[metric],color_continuous_scale='RdBu', title = title)
        st.plotly_chart(fig)
    elif feature == 'SITC 2 DIGIT':
        df_merge = df.groupby([feature, 'SITC 1 DIGIT'])[metric].sum().reset_index()
        df_merge = df_merge[df_merge[metric] > 0]
        df_merge["COMMODITY"] = "COMMODITY"
        fig = px.treemap(df_merge, path=['COMMODITY', 'SITC 1 DIGIT', feature], values=metric, color=metric, hover_data=[metric], color_continuous_scale='RdBu', title = title)
        st.plotly_chart(fig)
    else:
        fig = px.treemap(df, path=[feature], values=metric, color=metric, hover_data=[metric], color_continuous_scale='RdBu', title = title)
        st.plotly_chart(fig)

def bi_graph_tree(feature,column, i):
    try:
        title = "Trade Performance of Malaysia based on {} in {}: {} from 2013 to 2019".format(feature, column, i)
        if feature == 'COUNTRY':
            df_group = df[df[column] == i].groupby('COUNTRY')[metric].sum().reset_index()
            df_merge = df_group.merge(df_country, on='COUNTRY', how='inner')
            df_merge = df_merge[df_merge[metric] > 0]
            df_merge["WORLD"] = "WORLD"
            fig = px.treemap(df_merge, path=['WORLD', 'Region', feature], values=metric, color=metric,hover_data=[metric], color_continuous_scale='RdBu', title = title)
            st.plotly_chart(fig)
        elif feature == 'SITC 2 DIGIT':
            df_merge = df[df[column] == i].groupby([feature, 'SITC 1 DIGIT'])[metric].sum().reset_index()
            df_merge = df_merge[df_merge[metric] > 0]
            df_merge["COMMODITY"] = "COMMODITY"
            fig = px.treemap(df_merge, path=['COMMODITY', 'SITC 1 DIGIT', feature], values=metric, color=metric, hover_data=[metric], color_continuous_scale='RdBu', title =  title)
            st.plotly_chart(fig)
        else:
            fig = px.treemap(df[df[column] == i], path=[feature], values=metric, color=metric, hover_data=[metric],color_continuous_scale='RdBu', title = title)
            st.plotly_chart(fig)
    except:
        st.warning('The COUNTRY you have selected is not available!')

def multiple_graph_tree(feature, column_1, i, column_2, j,):
    try:
        title = "Trade Performance of Malaysia based on {} in {}: {} and {}: {}".format(feature, column_1, i, column_2, j)
        if feature == 'COUNTRY':
            df_group = df[(df[column_1] == i) & (df[column_2] == j)].groupby('COUNTRY')[metric].sum().reset_index()
            df_merge = df_group.merge(df_country, on='COUNTRY', how='inner')
            df_merge = df_merge[df_merge[metric] > 0]
            df_merge["WORLD"] = "WORLD"
            fig = px.treemap(df_merge, path=['WORLD', 'Region', feature], values=metric, color=metric,hover_data=[metric], color_continuous_scale='RdBu', title = title)
            st.plotly_chart(fig)
        elif feature == 'SITC 2 DIGIT':
            df_merge = df[(df[column_1] == i) & (df[column_2] == j)].groupby([feature, 'SITC 1 DIGIT'])[
                metric].sum().reset_index()
            df_merge = df_merge[df_merge[metric] > 0]
            df_merge["COMMODITY"] = "COMMODITY"
            fig = px.treemap(df_merge, path=['COMMODITY', 'SITC 1 DIGIT', feature], values=metric, color=metric, hover_data=[metric], color_continuous_scale='RdBu', title=title)
            st.plotly_chart(fig)
        else:
            temp = df[(df[column_1] == i) & (df[column_2] == j)]
            temp = temp[temp[metric] > 0]
            fig = px.treemap(temp, path=[feature], values=metric, color=metric, hover_data=[metric], color_continuous_scale='RdBu', title=title)
            st.plotly_chart(fig)
    except:
        st.warning('The COUNTRY you have selected is not available!')


def tree_map():
    st.subheader("Tree Map of Malaysia's Trade Performance")
    feature = st.sidebar.selectbox('Feature:', ['COUNTRY', 'SITC 1 DIGIT', 'SITC 2 DIGIT', 'YEAR'])
    if (feature == 'SITC 1 DIGIT') or (feature == 'SITC 2 DIGIT'):
        columns = st.sidebar.multiselect('Specification(s):', df[['COUNTRY', 'SITC 1 DIGIT', 'SITC 2 DIGIT', 'YEAR']].drop(['SITC 1 DIGIT', 'SITC 2 DIGIT'], axis = 1).columns,  key = '52')
    else:
        columns = st.sidebar.multiselect('Specification(s):', df[['COUNTRY', 'SITC 1 DIGIT', 'SITC 2 DIGIT', 'YEAR']].drop(feature, axis = 1).columns,  key = '53')
    try:
        if ('SITC 1 DIGIT' in columns) & ('SITC 2 DIGIT' in columns):
            st.write("You may only choose either one of SITC 1 DIGIT and SITC 2 DIGIT")
        else:
            if len(columns) == 0:
                single_graph_tree(feature)
            elif len(columns) == 1:
                i = st.sidebar.selectbox(columns[0] + ':', np.sort(df[columns[0]].unique()), key='3')
                bi_graph_tree(feature, columns[0], i)
            elif len(columns) == 2:
                i = st.sidebar.selectbox(columns[0] + ':', np.sort(df[columns[0]].unique()), key='5')
                j = st.sidebar.selectbox(columns[1] + ':', np.sort(df[columns[1]].unique()), key='6')
                multiple_graph_tree(feature, columns[0], i, columns[1], j)
    except KeyError:
        st.warning('Select at least one metric!')


tree_map()