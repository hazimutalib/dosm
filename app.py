import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
sns.set()

st.write(""" # Malaysia's Trade Perfomance Dashboard Application """)
st.info("Instant Dashboard of Malaysia's Trade Perfomance")

df = pd.read_csv('trade_new.csv')

show = []
show = st.sidebar.multiselect('Metric(s):', ['IMPORT (MILLION RM)', 'EXPORT (MILLION RM)', 'DEFICIT/SURPLUS (MILLION RM)'], default = ['IMPORT (MILLION RM)', 'EXPORT (MILLION RM)', 'DEFICIT/SURPLUS (MILLION RM)'], key='1')

def single_graph_line():
    fig, ax = plt.subplots(1, 1)
    df.groupby('YEAR')[show].sum().plot(ax=ax, figsize=(12, 8))
    st.pyplot(fig)
    st.write("Table of Malaysia's Trade Perfomance from 2013 to 2019")
    st.dataframe(df.groupby('YEAR')[show].sum())

def bi_graph_line(column, i):
    fig, ax = plt.subplots(1, 1)
    df[df[column] == i].groupby('YEAR')[show].sum().plot(ax=ax, figsize=(12, 8), title=column + ': ' + str(i));
    st.pyplot(fig)
    st.write("Table of Malaysia's Trade Perfomance of {}: {} from 2013 to 2019".format(column,i))
    st.dataframe(df[df[column] == i].groupby('YEAR')[show].sum())

def multiple_graph_line(column_1, i, column_2, j):
    fig, ax = plt.subplots(1, 1)
    df[(df[column_1] == i) & (df[column_2] == j)].groupby('YEAR')[show].sum().plot( ax = ax, figsize=(12, 8), title = column_1 + ': ' + str(i) + ' and ' + column_2 + ': '+ str(j));
    st.pyplot(fig)
    st.write("Table of Malaysia's Trade Perfomance of {}: {} and {}: {} from 2013 to 2019".format(column_1, i, column_2, j))
    st.dataframe(df[(df[column_1] == i) & (df[column_2] == j)].groupby('YEAR')[show].sum())

def line_graph():
    if len(show) != 0:
        columns = []
        columns = st.multiselect('Specification(s):', ['COUNTRY', 'SITC 1 DIGIT', 'SITC 2 DIGIT'], key='8')
        if ('SITC 1 DIGIT' in columns) & ('SITC 2 DIGIT' in columns):
            st.warning("You may only choose either one of SITC 1 DIGIT and SITC 2 DIGIT")
        else:
            if len(columns) == 1:
                i = st.selectbox(columns[0] + ':', np.sort(df[columns[0]].unique()), key='9')
                bi_graph_line(columns[0], i, )
            elif len(columns) == 2:
                i = st.selectbox(columns[0] + ':', np.sort(df[columns[0]].unique()), key='10')
                j = st.selectbox(columns[1] + ':', np.sort(df[columns[1]].unique()), key='11')
                multiple_graph_line(columns[0], i, columns[1], j)
            else:
                single_graph_line()
    else:
        st.warning('Select at least one metric!')
st.subheader("Time-Series Graph of Malaysia's Trade Perfomance from 2013 to 2019")
line_graph()

def single_graph_bar(column,sort):
    fig, ax = plt.subplots(1, 1)
    if (column == 'COUNTRY') or (column == 'SITC 2 DIGIT'):
        k = st.slider('Top:', 1, df[column].nunique(), 10, key='22')
        df.groupby(column)[show].sum().sort_values(by=sort, ascending=False).iloc[:k].plot(kind='bar', ax=ax, figsize=(12, 8))
        st.pyplot(fig)
        st.dataframe(df.groupby(column)[show].sum().sort_values(by=sort, ascending=False).iloc[:k])
    else:
        df.groupby(column)[show].sum().sort_values(by=sort, ascending=False).plot(kind='bar', ax=ax, figsize=(12, 8))
        st.pyplot(fig)
        st.dataframe(df.groupby(column)[show].sum().sort_values(by=sort, ascending=False))

def bi_graph_bar(column_1, column_2, i, sort):
    fig, ax = plt.subplots(1, 1)
    if (column_1 == 'COUNTRY') or (column_1 == 'SITC 2 DIGIT'):
        k = st.slider('Top:', 1, df[column_1].nunique(), 10, key='23')
        df[df[column_2] == i].groupby(column_1)[show].sum().sort_values(by=sort, ascending=False).iloc[:k].plot(kind='bar', ax=ax, figsize=(12, 8), title=column_2 + ': ' + str(i));
    else:
        df[df[column_2] == i].groupby(column_1)[show].sum().sort_values(by=sort, ascending=False).plot(kind='bar', ax=ax, figsize=(12, 8), title=column_2 + ': ' + str(i));
    st.pyplot(fig)

def multiple_graph_bar(column_1, column_2, i, column_3, j, sort):
    fig, ax = plt.subplots(1, 1)
    if (column_1 == 'COUNTRY') or (column_1 == 'SITC 2 DIGIT'):
        k = st.slider('Top:', 1, df[column_1].nunique(), 10, key='24')
        df[(df[column_2] == i) & (df[column_3] == j)].groupby(column_1)[show].sum().sort_values(by=sort, ascending=False).iloc[:k].plot(kind='bar', ax=ax, figsize=(12, 8), title=column_2 + ': ' + str(i) + ' and ' + column_3 + ': ' + str(j));
    else:
        df[(df[column_2] == i) & (df[column_3] == j)].groupby(column_1)[show].sum().sort_values(by=sort, ascending=False).plot(kind='bar', ax=ax, figsize=(12, 8), title=column_2 + ': ' + str(i) + ' and ' + column_3 + ': ' + str(j));
    st.pyplot(fig)

def bar_graph():
    feature = st.selectbox('Feature:', ['YEAR', 'COUNTRY', 'SITC 1 DIGIT', 'SITC 2 DIGIT'])
    columns = []
    columns = st.multiselect('Specification(s):', df[['YEAR', 'COUNTRY', 'SITC 1 DIGIT', 'SITC 2 DIGIT']].drop(feature, axis = 1).columns,  key = '1')
    try:
        if ('SITC 1 DIGIT' in columns) & ('SITC 2 DIGIT' in columns):
            st.write("You may only choose either one of SITC 1 DIGIT and SITC 2 DIGIT")
        else:
            if len(columns) == 0:
                sort = st.selectbox('Sort by:', show, key='2')
                single_graph_bar(feature, sort)
            elif len(columns) == 1:
                i = st.selectbox(columns[0] + ':', np.sort(df[columns[0]].unique()), key='3')
                sort = st.selectbox('Sort by:', show, key='4')
                bi_graph_bar(feature, columns[0], i, sort)
            elif len(columns) == 2:
                i = st.selectbox(columns[0] + ':', np.sort(df[columns[0]].unique()), key='5')
                j = st.selectbox(columns[1] + ':', np.sort(df[columns[1]].unique()), key='6')
                sort = st.selectbox('Sort by:', show, key='7')
                multiple_graph_bar(feature, columns[0], i, columns[1], j, sort)
    except IndexError:
        st.error('No data available')

st.subheader("Bar Graph Graph of Malaysia's Trade Perfomance")
bar_graph()