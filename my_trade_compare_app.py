import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
sns.set()
import base64

st.write(""" # Malaysia's Trade Perfomance Dashboard Application """)

df = pd.read_csv('trade_new.csv')

sitc1 = st.radio("SITC 1 DIGIT's Description:", ['No', 'Yes'])
if sitc1 == 'Yes':
    table1 = pd.read_csv('sitc_1.csv')
    st.dataframe(table1)

sitc2 = st.radio("SITC 2 DIGIT's Description:", ['No', 'Yes'])
if sitc2 == 'Yes':
    table2 = pd.read_csv('sitc_2.csv')
    st.dataframe(table2)

def get_table_download_link_drop_index(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="trade_data.csv">Download the whole csv</a>'

def get_table_download_link(df):
    csv = df.to_csv(index=True)
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="data.csv">Download csv file</a>'


graph = st.sidebar.selectbox('Type of graph:', ['Time-Series', 'Bar Chart', 'Pie Chart'])

if graph == 'Pie Chart':
    show = st.sidebar.selectbox('Metric(s):', ['IMPORT (MILLION RM)', 'EXPORT (MILLION RM)', 'DEFICIT/SURPLUS (MILLION RM)'], key='1')
else:
    show = st.sidebar.selectbox('Metric(s):', ['IMPORT (MILLION RM)', 'EXPORT (MILLION RM)', 'DEFICIT/SURPLUS (MILLION RM)'], key='1')



def single_graph_line():
    fig, ax = plt.subplots(1, 1)
    df.groupby('YEAR')[show].sum().plot(ax=ax, figsize=(12, 8), title = "Trade Perfomance of Malaysia from 2013 to 2019")
    st.pyplot(fig)
    data = st.radio('Show Datasets:', ['No', 'Yes'])
    if data == 'Yes':
        st.text("Trade Perfomance of Malaysia from 2013 to 2019")
        st.dataframe(df.groupby('YEAR')[show].sum())
        st.markdown(get_table_download_link(df.groupby('YEAR')[show].sum()), unsafe_allow_html=True)
    growth = st.radio('Show Growth Rate:' , ['No', 'Yes'])
    if growth == 'Yes':
        fig1, ax1 = plt.subplots()
        year = df.groupby('YEAR')[show].sum()
        list = []
        for metric in show:
            if  'DEFICIT/SURPLUS (MILLION RM)' in show:
                show.remove('DEFICIT/SURPLUS (MILLION RM)')
            lol = '{} GROWTH RATE (%)'.format(metric.split()[0])
            year[lol] = year[metric].pct_change() * 100
            list.append(lol)
        year[list].dropna().plot(ax=ax1, figsize=(12, 8), title = "Growth Rate of Malaysia's Trade Perfomance from 2014 to 2019")
        st.pyplot(fig1)
        gr = st.radio('Show Growth Rate Datasets:', ['No', 'Yes'])
        if gr == 'Yes':
            st.text("Growth Rate of Malaysia's Trade Perfomance from 2014 to 2019")
            st.dataframe(year[list])
            st.markdown(get_table_download_link(year[list]), unsafe_allow_html=True)

def bi_graph_line(column, i):
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    for z in range(len(i)):
        df[df[column] == i[z]].groupby('YEAR')[[show]].sum().rename(columns = {show : i[z]}).plot(ax=ax,  title = "Trade Perfomance of Malaysia in from 2013 to 2019");
    st.pyplot(fig)
    data = st.radio('Show Datasets:', ['No', 'Yes'])
    if data == 'Yes':
        st.text("Trade Perfomance of Malaysia in {}: {} from 2013 to 2019".format(column,i))
        st.dataframe(df[df[column] == i].groupby('YEAR')[show].sum())
        st.markdown(get_table_download_link(df[df[column] == i].groupby('YEAR')[show].sum()), unsafe_allow_html=True)
    growth = st.radio('Show Growth Rate:', ['No', 'Yes'])
    if growth == 'Yes':
        fig1, ax1 = plt.subplots()
        year = df[df[column] == i].groupby('YEAR')[show].sum()
        list = []
        for metric in show:
            if  'DEFICIT/SURPLUS (MILLION RM)' in show:
                show.remove('DEFICIT/SURPLUS (MILLION RM)')
            lol = '{} GROWTH RATE (%)'.format(metric.split()[0])
            year[lol] = year[metric].pct_change() * 100
            list.append(lol)
        year[list].dropna().plot(ax=ax1, figsize=(12, 8), title = "Growth Rate of Malaysia's Trade Perfomance in {}: {} from 2014 to 2019".format(column,i))
        st.pyplot(fig1)
        gr = st.radio('Show Growth Rate Datasets:', ['No', 'Yes'])
        if gr == 'Yes':
            st.text("Growth Rate of Malaysia's Trade Perfomance in {}: {} from 2014 to 2019".format(column,i))
            st.dataframe(year[list])
            st.markdown(get_table_download_link(year[list]), unsafe_allow_html=True)

def multiple_graph_line(column_1, i, column_2, j):
    fig, ax = plt.subplots(1, 1)
    df[(df[column_1] == i) & (df[column_2] == j)].groupby('YEAR')[show].sum().plot( ax = ax, figsize=(12, 8), title = "Trade Perfomance of Malaysia in {}: {} and {}: {} from 2013 to 2019".format(column_1, i, column_2, j));
    st.pyplot(fig)
    data = st.radio('Show Datasets:', ['No', 'Yes'])
    if data == 'Yes':
        st.text("Trade Perfomance of Malaysia in {}: {} and {}: {} from 2013 to 2019".format(column_1, i, column_2, j))
        st.dataframe(df[(df[column_1] == i) & (df[column_2] == j)].groupby('YEAR')[show].sum())
        st.markdown(get_table_download_link(df[(df[column_1] == i) & (df[column_2] == j)].groupby('YEAR')[show].sum()), unsafe_allow_html=True)
    growth = st.radio('Show Growth Rate:', ['No', 'Yes'])
    if growth == 'Yes':
        fig1, ax1 = plt.subplots()
        year = df[(df[column_1] == i) & (df[column_2] == j)].groupby('YEAR')[show].sum()
        list = []
        for metric in show:
            if  'DEFICIT/SURPLUS (MILLION RM)' in show:
                show.remove('DEFICIT/SURPLUS (MILLION RM)')
            lol = '{} GROWTH RATE (%)'.format(metric.split()[0])
            year[lol] = year[metric].pct_change() * 100
            list.append(lol)
        year[list].dropna().plot(ax=ax1, figsize=(12, 8), title = "Growth Rate of Malaysia's Trade Perfomance in {}: {} and {}: {} from 2014 to 2019". format(column_1, i, column_2, j))
        st.pyplot(fig1)
        gr = st.radio('Show Growth Rate Datasets:', ['No', 'Yes'])
        if gr == 'Yes':
            st.text("Growth Rate of Malaysia's Trade Perfomance in {}: {} and {}: {} from 2014 to 2019". format(column_1, i, column_2, j))
            st.dataframe(year[list])
            st.markdown(get_table_download_link(year[list]), unsafe_allow_html=True)

def line_graph():
    st.subheader("Time-Series Graph of Malaysia's Trade Perfomance from 2013 to 2019")
    if len(show) != 0:
        columns = []
        columns = st.sidebar.multiselect('Specification(s):', ['COUNTRY', 'SITC 1 DIGIT', 'SITC 2 DIGIT'], key='8')
        if ('SITC 1 DIGIT' in columns) & ('SITC 2 DIGIT' in columns):
            st.warning("You may only choose either one of SITC 1 DIGIT and SITC 2 DIGIT")
        else:
            if len(columns) == 1:
                i = st.sidebar.multiselect(columns[0] + ':', np.sort(df[columns[0]].unique()), key='9')
                bi_graph_line(columns[0], i )
            elif len(columns) == 2:
                i = st.sidebar.selectbox(columns[0] + ':', np.sort(df[columns[0]].unique()), key='10')
                j = st.sidebar.selectbox(columns[1] + ':', np.sort(df[columns[1]].unique()), key='11')
                multiple_graph_line(columns[0], i, columns[1], j)
            else:
                single_graph_line()
    else:
        st.warning('Select at least one metric!')


def plot_graph():
    if  graph == 'Time-Series':
        line_graph()


plot_graph()