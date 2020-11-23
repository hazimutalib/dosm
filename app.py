import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
sns.set()
import base64

st.write(""" # Malaysia's Trade Perfomance Dashboard Application """)
st.info("Instant Dashboard of Malaysia's Trade Perfomance")

df = pd.read_csv('trade_new.csv')

def get_table_download_link_drop_index(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="my_trade_whole.csv">Download the whole csv file here</a>'

st.markdown(get_table_download_link_drop_index(df),  unsafe_allow_html=True)

def get_table_download_link(df):
    csv = df.to_csv(index=True)
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="my_trade.csv">Download csv file</a>'

show = []
show = st.sidebar.multiselect('Metric(s):', ['IMPORT (MILLION RM)', 'EXPORT (MILLION RM)', 'DEFICIT/SURPLUS (MILLION RM)'], default = ['IMPORT (MILLION RM)', 'EXPORT (MILLION RM)', 'DEFICIT/SURPLUS (MILLION RM)'], key='1')

def single_graph_line():
    fig, ax = plt.subplots(1, 1)
    df.groupby('YEAR')[show].sum().plot(ax=ax, figsize=(12, 8), title = "Trade Perfomance of Malaysia from 2013 to 2019")
    st.pyplot(fig)
    st.text("Trade Perfomance of Malaysia from 2013 to 2019")
    st.dataframe(df.groupby('YEAR')[show].sum())
    st.markdown(get_table_download_link(df.groupby('YEAR')[show].sum()),  unsafe_allow_html=True)

def bi_graph_line(column, i):
    fig, ax = plt.subplots(1, 1)
    df[df[column] == i].groupby('YEAR')[show].sum().plot(ax=ax, figsize=(12, 8), title = "Trade Perfomance of Malaysia in {}: {} from 2013 to 2019".format(column,i));
    st.pyplot(fig)
    st.text("Trade Perfomance of Malaysia in {}: {} from 2013 to 2019".format(column,i))
    st.dataframe(df[df[column] == i].groupby('YEAR')[show].sum())
    st.markdown(get_table_download_link(df[df[column] == i].groupby('YEAR')[show].sum()), unsafe_allow_html=True)

def multiple_graph_line(column_1, i, column_2, j):
    fig, ax = plt.subplots(1, 1)
    df[(df[column_1] == i) & (df[column_2] == j)].groupby('YEAR')[show].sum().plot( ax = ax, figsize=(12, 8), title = "Trade Perfomance of Malaysia in {}: {} and {}: {} from 2013 to 2019".format(column_1, i, column_2, j));
    st.pyplot(fig)
    st.text("Trade Perfomance of Malaysia in {}: {} and {}: {} from 2013 to 2019".format(column_1, i, column_2, j))
    st.dataframe(df[(df[column_1] == i) & (df[column_2] == j)].groupby('YEAR')[show].sum())
    st.markdown(get_table_download_link(df[(df[column_1] == i) & (df[column_2] == j)].groupby('YEAR')[show].sum()), unsafe_allow_html=True)

def line_graph():
    st.subheader("Time-Series Graph of Malaysia's Trade Perfomance from 2013 to 2019")
    if len(show) != 0:
        columns = []
        columns = st.sidebar.multiselect('Specification(s):', ['COUNTRY', 'SITC 1 DIGIT', 'SITC 2 DIGIT'], key='8')
        if ('SITC 1 DIGIT' in columns) & ('SITC 2 DIGIT' in columns):
            st.warning("You may only choose either one of SITC 1 DIGIT and SITC 2 DIGIT")
        else:
            if len(columns) == 1:
                i = st.sidebar.selectbox(columns[0] + ':', np.sort(df[columns[0]].unique()), key='9')
                bi_graph_line(columns[0], i, )
            elif len(columns) == 2:
                i = st.sidebar.selectbox(columns[0] + ':', np.sort(df[columns[0]].unique()), key='10')
                j = st.sidebar.selectbox(columns[1] + ':', np.sort(df[columns[1]].unique()), key='11')
                multiple_graph_line(columns[0], i, columns[1], j)
            else:
                single_graph_line()
    else:
        st.warning('Select at least one metric!')

def single_graph_bar(column,sort):
    fig, ax = plt.subplots(1, 1)
    k = st.sidebar.slider('Top:', 1, df[column].nunique(), 7, key='22')
    df.groupby(column)[show].sum().sort_values(by=sort, ascending=False).iloc[:k].plot(kind='bar', ax=ax, figsize=(12, 8), title = "Trade Perfomance of Malaysia based on {}".format(column))
    st.pyplot(fig)
    st.text("Trade Perfomance of Malaysia based on {}".format(column))
    st.dataframe(df.groupby(column)[show].sum().sort_values(by=sort, ascending=False).iloc[:k])
    st.markdown(get_table_download_link(df.groupby(column)[show].sum().sort_values(by=sort, ascending=False).iloc[:k]),unsafe_allow_html=True)

def bi_graph_bar(column_1, column_2, i, sort):
    fig, ax = plt.subplots(1, 1)
    k = st.sidebar.slider('Top:', 1, df[column_1].nunique(), 7, key='23')
    df[df[column_2] == i].groupby(column_1)[show].sum().sort_values(by=sort, ascending=False).iloc[:k].plot(kind='bar', ax=ax, figsize=(12, 8), title = "Trade Perfomance of Malaysia based on {} in {}: {}".format(column_1,column_2, i));
    st.pyplot(fig)
    st.text("Trade Perfomance of Malaysia based on {} in {}: {}".format(column_1,column_2, i))
    st.dataframe(df[df[column_2] == i].groupby(column_1)[show].sum().sort_values(by=sort, ascending=False).iloc[:k])
    st.markdown(get_table_download_link(df[df[column_2] == i].groupby(column_1)[show].sum().sort_values(by=sort, ascending=False).iloc[:k]),unsafe_allow_html=True)

def multiple_graph_bar(column_1, column_2, i, column_3, j, sort):
    fig, ax = plt.subplots(1, 1)
    k = st.sidebar.slider('Top:', 1, df[column_1].nunique(), 7, key='24')
    df[(df[column_2] == i) & (df[column_3] == j)].groupby(column_1)[show].sum().sort_values(by=sort, ascending=False).iloc[:k].plot(kind='bar', ax=ax, figsize=(12, 8), title = "Trade Perfomance of Malaysia based on {} in {}: {} and {}: {}".format(column_1, column_2, i, column_3, j));
    st.pyplot(fig)
    st.text("Trade Perfomance of Malaysia based on {} in {}: {} and {}: {}".format(column_1, column_2, i, column_3, j))
    st.dataframe(df[(df[column_2] == i) & (df[column_3] == j)].groupby(column_1)[show].sum().sort_values(by=sort, ascending=False).iloc[:k])
    st.markdown(get_table_download_link(df[(df[column_2] == i) & (df[column_3] == j)].groupby(column_1)[show].sum().sort_values(by=sort, ascending=False).iloc[:k]),unsafe_allow_html=True)


def bar_graph():
    st.subheader("Pie Chart of Malaysia's Trade Perfomance")
    feature = st.sidebar.selectbox('Feature:', ['YEAR', 'COUNTRY', 'SITC 1 DIGIT', 'SITC 2 DIGIT'])
    columns = []
    if (feature == 'SITC 1 DIGIT') or (feature == 'SITC 2 DIGIT'):
        columns = st.sidebar.multiselect('Specification(s):', df[['YEAR', 'COUNTRY', 'SITC 1 DIGIT', 'SITC 2 DIGIT']].drop(['SITC 1 DIGIT', 'SITC 2 DIGIT'], axis = 1).columns,  key = '52')
    else:
        columns = st.sidebar.multiselect('Specification(s):', df[['YEAR', 'COUNTRY', 'SITC 1 DIGIT', 'SITC 2 DIGIT']].drop(feature, axis = 1).columns,  key = '53')
    try:
        if ('SITC 1 DIGIT' in columns) & ('SITC 2 DIGIT' in columns):
            st.write("You may only choose either one of SITC 1 DIGIT and SITC 2 DIGIT")
        else:
            if len(columns) == 0:
                sort = st.sidebar.selectbox('Sort by:', show, key='2')
                single_graph_bar(feature, sort)
            elif len(columns) == 1:
                i = st.sidebar.selectbox(columns[0] + ':', np.sort(df[columns[0]].unique()), key='3')
                sort = st.sidebar.selectbox('Sort by:', show, key='4')
                bi_graph_bar(feature, columns[0], i, sort)
            elif len(columns) == 2:
                i = st.sidebar.selectbox(columns[0] + ':', np.sort(df[columns[0]].unique()), key='5')
                j = st.sidebar.selectbox(columns[1] + ':', np.sort(df[columns[1]].unique()), key='6')
                sort = st.sidebar.selectbox('Sort by:', show, key='7')
                multiple_graph_bar(feature, columns[0], i, columns[1], j, sort)
    except KeyError:
        st.warning('Select at least one metric!')

def single_pie(column,k,sort):
    pie = df.groupby(column)[show].sum().sort_values(by=sort, ascending=False)
    q = pie[sort].quantile((len(pie) - k) / (len(pie)))
    df1 = pie.reset_index()
    df1.loc[df1[sort] < q, column] = 'OTHERS'
    fig, ax = plt.subplots()
    df1.groupby(column)[show].sum().sort_values(by = sort, ascending = False).plot.pie(y=sort, autopct='%1.1f%%', ax = ax, figsize=(12,8), legend = False, title = "Trade Perfomance of Malaysia based on {}".format(column))
    st.pyplot(fig)
    st.text("Trade Perfomance of Malaysia based on {}".format(column))
    st.dataframe(df1.groupby(column)[show].sum().sort_values(by = sort, ascending = False))
    st.markdown(get_table_download_link(df1.groupby(column)[show].sum().sort_values(by = sort, ascending = False)),unsafe_allow_html=True)

def bi_pie(column_1, k, column_2, i, sort):
    pie = df[df[column_2] == i].groupby(column_1)[show].sum().sort_values(by=sort, ascending=False)
    q = pie[sort].quantile((len(pie) - k) / (len(pie)))
    df1 = pie.reset_index()
    df1.loc[df1[sort] < q, column_1] = 'OTHERS'
    fig, ax = plt.subplots(1, 1)
    df1.groupby(column_1)[show].sum().sort_values(by = sort, ascending = False).plot.pie(y=sort, autopct='%1.1f%%', ax=ax,figsize=(12, 8), legend = False, title = "Trade Perfomance of Malaysia based on {} in {}: {}".format(column_1, column_2, i))
    st.pyplot(fig)
    st.text("Trade Perfomance of Malaysia based on {} in {}: {}".format(column_1, column_2, i))
    st.dataframe(df1.groupby(column_1)[show].sum().sort_values(by = sort, ascending = False))
    st.markdown(get_table_download_link(df1.groupby(column_1)[show].sum().sort_values(by = sort, ascending = False)),unsafe_allow_html=True)

def multiple_pie(column_1, k, column_2, i, column_3, j, sort):
    pie = df[(df[column_2] == i) & (df[column_3] == j)].groupby(column_1)[show].sum().sort_values(by=sort, ascending=False)
    q = pie[sort].quantile((len(pie) - k) / (len(pie)))
    df1 = pie.reset_index()
    df1.loc[df1[sort] < q, column_1] = 'OTHERS'
    fig, ax = plt.subplots(1, 1)
    df1.groupby(column_1)[show].sum().sort_values(by = sort, ascending = False).plot.pie(y=sort, autopct='%1.1f%%', legend = False, ax=ax,figsize=(12, 8), title = "Trade Perfomance of Malaysia based on {} in {}: {} and {}: {}".format(column_1, column_2, i, column_3, j))
    st.pyplot(fig)
    st.text("Trade Perfomance of Malaysia based on {} in {}: {} and {}: {}".format(column_1, column_2, i, column_3, j))
    st.dataframe(df1.groupby(column_1)[show].sum().sort_values(by = sort, ascending = False))
    st.markdown(get_table_download_link(df1.groupby(column_1)[show].sum().sort_values(by = sort, ascending = False)),unsafe_allow_html=True)

def pie_graph():
    st.subheader("Pie Chart of Malaysia's Trade Perfomance")
    feature = st.sidebar.selectbox('Feature:', ['YEAR', 'COUNTRY', 'SITC 1 DIGIT', 'SITC 2 DIGIT'], key = '51')
    columns = []
    columns = st.sidebar.multiselect('Specification(s):', df[['YEAR', 'COUNTRY', 'SITC 1 DIGIT', 'SITC 2 DIGIT']].drop(feature, axis=1).columns, key = '50')
    k = st.sidebar.slider('Top:',1, df[feature].nunique(), 5, key='31')
    try:
        if ('SITC 1 DIGIT' in columns) & ('SITC 2 DIGIT' in columns):
            st.write("You may only choose either one of SITC 1 DIGIT and SITC 2 DIGIT")
        else:
            if len(columns) == 0:
                sort = st.sidebar.selectbox('Sort by:', show, key='32')
                single_pie(feature, k, sort)
            elif len(columns) == 1:
                i = st.sidebar.selectbox(columns[0] + ':', np.sort(df[columns[0]].unique()), key='33')
                sort = st.sidebar.selectbox('Sort by:', show, key='34')
                bi_pie(feature, k, columns[0], i, sort)
            elif len(columns) == 2:
                i = st.sidebar.selectbox(columns[0] + ':', np.sort(df[columns[0]].unique()), key='35')
                j = st.sidebar.selectbox(columns[1] + ':', np.sort(df[columns[1]].unique()), key='36')
                sort = st.sidebar.selectbox('Sort by:', show, key='37')
                multiple_pie(feature,k, columns[0], i, columns[1], j, sort)
    except KeyError:
        st.warning('Select at least one metric!')


def plot_graph():
    graph = st.selectbox('Type of graph:', ['Time-Series', 'Bar Chart', 'Pie Chart'])
    if graph == 'Bar Chart':
        bar_graph()
    elif graph == 'Time-Series':
        line_graph()
    else:
        pie_graph()

plot_graph()