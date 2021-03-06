import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
sns.set()
import base64
import plotly.express as px

st.write(""" # Malaysia's Trade Performance Dashboard Application """)

df = pd.read_csv('trade_new.csv')
sitc_1 = pd.read_csv('sitc_1.csv')
sitc_2 = pd.read_csv('sitc_2.csv')
df_country = pd.read_csv("region.csv")

if st.sidebar.button("SITC 1 DIGIT's Description"):
    st.dataframe(sitc_1)

if st.sidebar.button("SITC 2 DIGIT's Description"):
    st.dataframe(sitc_2)

def get_table_download_link_drop_index(data):
    csv = data.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="trade_data.csv">Download the whole csv</a>'

def get_table_download_link(data):
    csv = data.to_csv(index=True)
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="data.csv">Download csv file</a>'

graph = st.sidebar.selectbox('Type of graph:', ['TIME-SERIES', 'BAR CHART', 'PIE CHART', 'TREE MAP', 'BUBBLE PLOT', 'AREA PLOT'])

if (graph == 'PIE CHART') or (graph == 'TREE MAP') or (graph == 'BUBBLE PLOT') or (graph == 'AREA PLOT'):
    show = st.sidebar.selectbox('Metric:', ['IMPORT (MILLION RM)', 'EXPORT (MILLION RM)'], key='1')
else:
    show = st.sidebar.multiselect('Metric(s):', ['IMPORT (MILLION RM)', 'EXPORT (MILLION RM)', 'DEFICIT/SURPLUS (MILLION RM)'], default=['IMPORT (MILLION RM)', 'EXPORT (MILLION RM)'], key='1')



def single_graph_line():
    fig, ax = plt.subplots(1, 1)
    df.groupby('YEAR')[show].sum().plot(ax=ax, figsize=(12, 8), title = "Trade Performance of Malaysia from 2013 to 2019")
    st.pyplot(fig)
    if st.button('Show Datasets'):
        st.text("Trade Performance of Malaysia from 2013 to 2019")
        st.dataframe(df.groupby('YEAR')[show].sum())
        st.markdown(get_table_download_link(df.groupby('YEAR')[show].sum()), unsafe_allow_html=True)
    if 'DEFICIT/SURPLUS (MILLION RM)' in show:
        show.remove('DEFICIT/SURPLUS (MILLION RM)')
    if st.button('Show Growth Rate'):
        if len(show) == 0:
            st.error('Not Available')
        else:
            fig1, ax1 = plt.subplots()
            year = df.groupby('YEAR')[show].sum()
            list = []
            for metric in show:
                lol = '{} GROWTH RATE (%)'.format(metric.split()[0])
                year[lol] = year[metric].pct_change() * 100
                list.append(lol)
            year[list].dropna().plot(ax=ax1, figsize=(12, 8), title="Growth Rate of Malaysia's Trade Perfomance from 2014 to 2019")
            st.pyplot(fig1)

def bi_graph_line(column, i):
    fig, ax = plt.subplots(1, 1)
    df[df[column] == i].groupby('YEAR')[show].sum().plot(ax=ax, figsize=(12, 8), title = "Trade Performance of Malaysia in {}: {} from 2013 to 2019".format(column,i))
    st.pyplot(fig)
    if st.button('Show Datasets'):
        st.text("Trade Performance of Malaysia in {}: {} from 2013 to 2019".format(column,i))
        st.dataframe(df[df[column] == i].groupby('YEAR')[show].sum())
        st.markdown(get_table_download_link(df[df[column] == i].groupby('YEAR')[show].sum()), unsafe_allow_html=True)
    if 'DEFICIT/SURPLUS (MILLION RM)' in show:
        show.remove('DEFICIT/SURPLUS (MILLION RM)')
    if st.button('Show Growth Rate'):
        if (len(show) == 0):
            st.error('Not Available')
        else:
            fig1, ax1 = plt.subplots()
            year = df[df[column] == i].groupby('YEAR')[show].sum()
            list = []
            for metric in show:
                lol = '{} GROWTH RATE (%)'.format(metric.split()[0])
                year[lol] = year[metric].pct_change() * 100
                list.append(lol)
            year[list].dropna().plot(ax=ax1, figsize=(12, 8), title="Growth Rate of Malaysia's Trade Perfomance in {}: {} from 2014 to 2019".format(column, i))
            st.pyplot(fig1)

def multiple_graph_line(column_1, i, column_2, j):
    fig, ax = plt.subplots(1, 1)
    df[(df[column_1] == i) & (df[column_2] == j)].groupby('YEAR')[show].sum().plot( ax = ax, figsize=(12, 8), title = "Trade Performance of Malaysia in {}: {} and {}: {} from 2013 to 2019".format(column_1, i, column_2, j))
    st.pyplot(fig)
    if st.button('Show Datasets'):
        st.text("Trade Performance of Malaysia in {}: {} and {}: {} from 2013 to 2019".format(column_1, i, column_2, j))
        st.dataframe(df[(df[column_1] == i) & (df[column_2] == j)].groupby('YEAR')[show].sum())
        st.markdown(get_table_download_link(df[(df[column_1] == i) & (df[column_2] == j)].groupby('YEAR')[show].sum()), unsafe_allow_html=True)
    if 'DEFICIT/SURPLUS (MILLION RM)' in show:
        show.remove('DEFICIT/SURPLUS (MILLION RM)')
    if st.button('Show Growth Rate'):
        if (len(show) == 0):
            st.error('Not Available')
        else:
            fig1, ax1 = plt.subplots()
            year = df[(df[column_1] == i) & (df[column_2] == j)].groupby('YEAR')[show].sum()
            list = []
            for metric in show:
                lol = '{} GROWTH RATE (%)'.format(metric.split()[0])
                year[lol] = year[metric].pct_change() * 100
                list.append(lol)
            year[list].dropna().plot(ax=ax1, figsize=(12, 8),title="Growth Rate of Malaysia's Trade Perfomance in {}: {} and {}: {} from 2014 to 2019".format(column_1, i, column_2, j))
            st.pyplot(fig1)

def line_graph():
    st.subheader("Time-Series Graph of Malaysia's Trade Performance from 2013 to 2019")
    if len(show) != 0:
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

def single_graph_bar(column,sort,k):
    fig, ax = plt.subplots(1, 1)
    df.groupby(column)[show].sum().sort_values(by=sort, ascending=False).iloc[:k].plot(kind='bar', ax=ax, figsize=(12, 8), title = "Trade Performance of Malaysia based on {} from 2013 to 2019".format(column))
    st.pyplot(fig)
    if st.button('Show Datasets'):
        st.text("Trade Performance of Malaysia based on {} from 2013 to 2019".format(column))
        st.dataframe(df.groupby(column)[show].sum().sort_values(by=sort, ascending=False).iloc[:k])
        st.markdown(get_table_download_link(df.groupby(column)[show].sum().sort_values(by=sort, ascending=False).iloc[:k]),unsafe_allow_html=True)

def bi_graph_bar(column_1, column_2, i, sort, k):
    if column_2 == 'YEAR':
        title = "Trade Performance of Malaysia based on {} in {}: {}".format(column_1,column_2, i)
    else:
        title = "Trade Performance of Malaysia based on {} in {}: {} from 2013 to 2019".format(column_1,column_2, i)
    fig, ax = plt.subplots(1, 1)
    df[df[column_2] == i].groupby(column_1)[show].sum().sort_values(by=sort, ascending=False).iloc[:k].plot(kind='bar', ax=ax, figsize=(12, 8), title = title)
    st.pyplot(fig)
    if st.button('Show Datasets'):
        st.text(title)
        st.dataframe(df[df[column_2] == i].groupby(column_1)[show].sum().sort_values(by=sort, ascending=False).iloc[:k])
        st.markdown(get_table_download_link(df[df[column_2] == i].groupby(column_1)[show].sum().sort_values(by=sort, ascending=False).iloc[:k]),unsafe_allow_html=True)

def multiple_graph_bar(column_1, column_2, i, column_3, j, sort, k):
    fig, ax = plt.subplots(1, 1)
    df[(df[column_2] == i) & (df[column_3] == j)].groupby(column_1)[show].sum().sort_values(by=sort, ascending=False).iloc[:k].plot(kind='bar', ax=ax, figsize=(12, 8), title = "Trade Performance of Malaysia based on {} in {}: {} and {}: {}".format(column_1, column_2, i, column_3, j))
    st.pyplot(fig)
    if st.button('Show Datasets'):
        st.text("Trade Performance of Malaysia based on {} in {}: {} and {}: {}".format(column_1, column_2, i, column_3, j))
        st.dataframe(df[(df[column_2] == i) & (df[column_3] == j)].groupby(column_1)[show].sum().sort_values(by=sort, ascending=False).iloc[:k])
        st.markdown(get_table_download_link(df[(df[column_2] == i) & (df[column_3] == j)].groupby(column_1)[show].sum().sort_values(by=sort, ascending=False).iloc[:k]),unsafe_allow_html=True)


def bar_graph():
    st.subheader("Bar Chart of Malaysia's Trade Performance")
    feature = st.sidebar.selectbox('Feature:', ['COUNTRY', 'SITC 1 DIGIT', 'SITC 2 DIGIT', 'YEAR'])
    k = st.sidebar.slider('Top:', 1, df[feature].nunique(), 7, key='22')
    if (feature == 'SITC 1 DIGIT') or (feature == 'SITC 2 DIGIT'):
        columns = st.sidebar.multiselect('Specification(s):', df[['COUNTRY', 'SITC 1 DIGIT', 'SITC 2 DIGIT', 'YEAR']].drop(['SITC 1 DIGIT', 'SITC 2 DIGIT'], axis = 1).columns,  key = '52')
    else:
        columns = st.sidebar.multiselect('Specification(s):', df[['COUNTRY', 'SITC 1 DIGIT', 'SITC 2 DIGIT', 'YEAR']].drop(feature, axis = 1).columns,  key = '53')
    try:
        if ('SITC 1 DIGIT' in columns) & ('SITC 2 DIGIT' in columns):
            st.write("You may only choose either one of SITC 1 DIGIT and SITC 2 DIGIT")
        else:
            if len(columns) == 0:
                sort = st.sidebar.selectbox('Sort by:', show, key='2')
                single_graph_bar(feature, sort, k)
            elif len(columns) == 1:
                if 'YEAR' in columns:
                    i = st.sidebar.slider(columns[0] + ':', 2013,2019,2018, key='60')
                else:
                    i = st.sidebar.selectbox(columns[0] + ':', np.sort(df[columns[0]].unique()), key='3')
                sort = st.sidebar.selectbox('Sort by:', show, key='4')
                bi_graph_bar(feature, columns[0], i, sort, k)
            elif len(columns) == 2:
                if 'YEAR' in columns:
                    i = st.sidebar.slider(columns[0] + ':', 2013,2019,2018, key='60')
                else:
                    i = st.sidebar.selectbox(columns[0] + ':', np.sort(df[columns[0]].unique()), key='5')
                j = st.sidebar.selectbox(columns[1] + ':', np.sort(df[columns[1]].unique()), key='6')
                sort = st.sidebar.selectbox('Sort by:', show, key='7')
                multiple_graph_bar(feature, columns[0], i, columns[1], j, sort, k)
    except KeyError:
        st.warning('Select at least one metric!')

def single_pie(column,k):
    pie = df.groupby(column)[[show]].sum().sort_values(by=show, ascending=False)
    q = pie[show].quantile((len(pie) - k) / (len(pie)))
    df1 = pie.reset_index()
    df1.loc[df1[show] < q, column] = 'OTHERS'
    fig, ax = plt.subplots()
    df1.groupby(column)[[show]].sum().sort_values(by = show, ascending = False).plot.pie(y=show, autopct='%1.1f%%', ax = ax, figsize=(12,8), legend = False, title = "Trade Performance of Malaysia based on {} from 2013 to 2019".format(column))
    st.pyplot(fig)
    if st.button('Show Datasets'):
        st.text("Trade Performance of Malaysia based on {}".format(column))
        st.dataframe(df1.groupby(column)[show].sum().sort_values(by = show, ascending = False))
        st.markdown(get_table_download_link(df1.groupby(column)[[show]].sum().sort_values(by = show, ascending = False)),unsafe_allow_html=True)

def bi_pie(column_1, k, column_2, i):
    if column_2 == 'YEAR':
        title = "Trade Performance of Malaysia based on {} in {}: {}".format(column_1,column_2, i)
    else:
        title = "Trade Performance of Malaysia based on {} in {}: {} from 2013 to 2019".format(column_1,column_2, i)
    pie = df[df[column_2] == i].groupby(column_1)[[show]].sum().sort_values(by=show, ascending=False)
    q = pie[show].quantile((len(pie) - k) / (len(pie)))
    df1 = pie.reset_index()
    df1.loc[df1[show] < q, column_1] = 'OTHERS'
    fig, ax = plt.subplots(1, 1)
    df1.groupby(column_1)[[show]].sum().sort_values(by = show, ascending = False).plot.pie(y=show, autopct='%1.1f%%', ax=ax,figsize=(12, 8), legend = False, title = title)
    st.pyplot(fig)
    if st.button('Show Datasets'):
        st.text(title)
        st.dataframe(df1.groupby(column_1)[[show]].sum().sort_values(by = show, ascending = False))
        st.markdown(get_table_download_link(df1.groupby(column_1)[[show]].sum().sort_values(by = show, ascending = False)),unsafe_allow_html=True)

def multiple_pie(column_1, k, column_2, i, column_3, j):
    pie = df[(df[column_2] == i) & (df[column_3] == j)].groupby(column_1)[[show]].sum().sort_values(by=show, ascending=False)
    q = pie[show].quantile((len(pie) - k) / (len(pie)))
    df1 = pie.reset_index()
    df1.loc[df1[show] < q, column_1] = 'OTHERS'
    fig, ax = plt.subplots(1, 1)
    df1.groupby(column_1)[[show]].sum().sort_values(by = show, ascending = False).plot.pie(y=show, autopct='%1.1f%%', legend = False, ax=ax,figsize=(12, 8), title = "Trade Performance of Malaysia based on {} in {}: {} and {}: {}".format(column_1, column_2, i, column_3, j))
    st.pyplot(fig)
    if st.button('Show Datasets'):
        st.text("Trade Performance of Malaysia based on {} in {}: {} and {}: {}".format(column_1, column_2, i, column_3, j))
        st.dataframe(df1.groupby(column_1)[[show]].sum().sort_values(by = show, ascending = False))
        st.markdown(get_table_download_link(df1.groupby(column_1)[[show]].sum().sort_values(by = show, ascending = False)),unsafe_allow_html=True)

def pie_graph():
    st.subheader("Pie Chart of Malaysia's Trade Performance")
    feature = st.sidebar.selectbox('Feature:', ['COUNTRY', 'SITC 1 DIGIT', 'SITC 2 DIGIT', 'YEAR'], key = '51')
    k = st.sidebar.slider('Top:', 1, df[feature].nunique(), 5, key='31')
    columns = st.sidebar.multiselect('Specification(s):', df[['COUNTRY', 'SITC 1 DIGIT', 'SITC 2 DIGIT', 'YEAR']].drop(feature, axis=1).columns, key = '50')
    try:
        if ('SITC 1 DIGIT' in columns) & ('SITC 2 DIGIT' in columns):
            st.write("You may only choose either one of SITC 1 DIGIT and SITC 2 DIGIT")
        else:
            if len(columns) == 0:
                single_pie(feature, k)
            elif len(columns) == 1:
                if 'YEAR' in columns:
                    i = st.sidebar.slider(columns[0] + ':', 2013,2019,2018, key='60')
                else:
                    i = st.sidebar.selectbox(columns[0] + ':', np.sort(df[columns[0]].unique()), key='33')
                bi_pie(feature, k, columns[0], i)
            elif len(columns) == 2:
                if 'YEAR' in columns:
                    i = st.sidebar.slider(columns[0] + ':', 2013,2019,2018, key='60')
                else:
                    i = st.sidebar.selectbox(columns[0] + ':', np.sort(df[columns[0]].unique()), key='35')
                j = st.sidebar.selectbox(columns[1] + ':', np.sort(df[columns[1]].unique()), key='36')
                multiple_pie(feature,k, columns[0], i, columns[1], j)
    except KeyError:
        st.warning('Select at least one metric!')

def single_graph_tree(feature):
    title = 'Trade Performance of Malaysia based on {} from 2013 to 2019'.format(feature)
    if feature == 'COUNTRY':
        df_group = df.groupby('COUNTRY')[show].sum().reset_index()
        df_merge = df_group.merge(df_country, on='COUNTRY', how='inner')
        df_merge = df_merge[df_merge[show] > 0]
        df_merge["WORLD"] = "WORLD"
        fig = px.treemap(df_merge, path=['WORLD', 'Region', feature], values=show, color=show, hover_data=[show],color_continuous_scale='RdBu', title = title)
        fig.update_layout(height=700, width=900)
        st.plotly_chart(fig)
    elif feature == 'SITC 2 DIGIT':
        df_merge = df.groupby([feature, 'SITC 1 DIGIT'])[show].sum().reset_index()
        df_merge = df_merge[df_merge[show] > 0]
        df_merge["COMMODITY"] = "COMMODITY"
        fig = px.treemap(df_merge, path=['COMMODITY', 'SITC 1 DIGIT', feature], values=show, color=show, hover_data=[show], color_continuous_scale='RdBu', title = title)
        fig.update_layout(height=700, width=900)
        st.plotly_chart(fig)
    else:
        fig = px.treemap(df, path=[feature], values=show, color=show, hover_data=[show], color_continuous_scale='RdBu', title = title)
        fig.update_layout(height=700, width=900)
        st.plotly_chart(fig)

def bi_graph_tree(feature,column, i):
    try:
        if column == 'YEAR':
            title = "Trade Performance of Malaysia based on {} in {}: {}".format(feature, column, i)
        else:
            title = "Trade Performance of Malaysia based on {} in {}: {} from 2013 to 2019".format(feature, column, i)
        if feature == 'COUNTRY':
            df_group = df[df[column] == i].groupby('COUNTRY')[show].sum().reset_index()
            df_merge = df_group.merge(df_country, on='COUNTRY', how='inner')
            df_merge = df_merge[df_merge[show] > 0]
            df_merge["WORLD"] = "WORLD"
            fig = px.treemap(df_merge, path=['WORLD', 'Region', feature], values=show, color=show,hover_data=[show], color_continuous_scale='RdBu', title = title)
            fig.update_layout(height=700, width=900)
            st.plotly_chart(fig)
        elif feature == 'SITC 2 DIGIT':
            df_merge = df[df[column] == i].groupby([feature, 'SITC 1 DIGIT'])[show].sum().reset_index()
            df_merge = df_merge[df_merge[show] > 0]
            df_merge["COMMODITY"] = "COMMODITY"
            fig = px.treemap(df_merge, path=['COMMODITY', 'SITC 1 DIGIT', feature], values=show, color=show, hover_data=[show], color_continuous_scale='RdBu', title =  title)
            fig.update_layout(height=700, width=900)
            st.plotly_chart(fig)
        else:
            fig = px.treemap(df[df[column] == i], path=[feature], values=show, color=show, hover_data=[show],color_continuous_scale='RdBu', title = title)
            fig.update_layout(height=700, width=900)
            st.plotly_chart(fig)
    except:
        st.warning('The COUNTRY you have selected is not available!')

def multiple_graph_tree(feature, column_1, i, column_2, j,):
    try:
        title = "Trade Performance of Malaysia based on {} in {}: {} and {}: {}".format(feature, column_1, i, column_2, j)
        if feature == 'COUNTRY':
            df_group = df[(df[column_1] == i) & (df[column_2] == j)].groupby('COUNTRY')[show].sum().reset_index()
            df_merge = df_group.merge(df_country, on='COUNTRY', how='inner')
            df_merge = df_merge[df_merge[show] > 0]
            df_merge["WORLD"] = "WORLD"
            fig = px.treemap(df_merge, path=['WORLD', 'Region', feature], values=show, color=show,hover_data=[show], color_continuous_scale='RdBu', title = title)
            fig.update_layout(height=700, width=900)
            st.plotly_chart(fig)
        elif feature == 'SITC 2 DIGIT':
            df_merge = df[(df[column_1] == i) & (df[column_2] == j)].groupby([feature, 'SITC 1 DIGIT'])[
                show].sum().reset_index()
            df_merge = df_merge[df_merge[show] > 0]
            df_merge["COMMODITY"] = "COMMODITY"
            fig = px.treemap(df_merge, path=['COMMODITY', 'SITC 1 DIGIT', feature], values=show, color=show, hover_data=[show], color_continuous_scale='RdBu', title=title)
            fig.update_layout(height=700, width=900)
            st.plotly_chart(fig)
        else:
            temp = df[(df[column_1] == i) & (df[column_2] == j)]
            temp = temp[temp[show] > 0]
            fig = px.treemap(temp, path=[feature], values=show, color=show, hover_data=[show], color_continuous_scale='RdBu', title=title)
            fig.update_layout(height=700, width=900)
            st.plotly_chart(fig)
    except:
        st.warning('The COUNTRY you have selected is not available!')

def tree_map():
    st.subheader("Tree Map of Malaysia's Trade Performance from 2013 to 2019")
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
                if 'YEAR' in columns:
                    i = st.sidebar.slider(columns[0] + ':', 2013,2019,2018, key='60')
                else:
                    i = st.sidebar.selectbox(columns[0] + ':', np.sort(df[columns[0]].unique()), key='3')
                bi_graph_tree(feature, columns[0], i)
            elif len(columns) == 2:
                if 'YEAR' in columns:
                    i = st.sidebar.slider(columns[0] + ':', 2013,2019,2018, key='60')
                else:
                    i = st.sidebar.selectbox(columns[0] + ':', np.sort(df[columns[0]].unique()), key='5')
                j = st.sidebar.selectbox(columns[1] + ':', np.sort(df[columns[1]].unique()), key='6')
                multiple_graph_tree(feature, columns[0], i, columns[1], j)
    except KeyError:
        st.warning('Select at least one show!')


def bubble_graph():
    st.subheader("Bubble Plot of Malaysia's Trade Performance from 2013 to 2019")
    year = st.sidebar.slider('YEAR:', 2013, 2019, 2018)
    rca = pd.read_csv('Malaysia_RCA_stats.csv')
    rca = rca.drop(['Reporter Name', 'Partner Name', 'Trade Flow'], axis=1)
    rca_melt = rca.melt(id_vars=['1D DESC'], value_vars=['2013', '2014', '2015', '2016', '2017', '2018', '2019'])
    rca_melt = rca_melt.rename(columns={'variable': 'YEAR', 'value': 'RCA Value'})
    rca_melt['YEAR'] = rca_melt['YEAR'].astype(str).astype(int)
    df_import_dynamic = df.groupby(['YEAR', 'SITC 1 DIGIT'])[[show]].sum().reset_index().sort_values( by=['SITC 1 DIGIT', 'YEAR'])
    df_import_dynamic['Percent Change'] = df_import_dynamic.groupby(['SITC 1 DIGIT'])[[show]].pct_change().fillna(0) * 100
    df_import_dynamic = df_import_dynamic.sort_values(by=['YEAR', 'SITC 1 DIGIT'])
    df_import_dynamic = df_import_dynamic.merge(sitc_1, on='SITC 1 DIGIT').merge(rca_melt, on=['YEAR', '1D DESC'])
    df_import_dynamic['SITC 1 DIGIT'] = df_import_dynamic['SITC 1 DIGIT'].astype(str)
    fig = px.scatter(df_import_dynamic.query("YEAR=={}".format(year)), x="RCA Value", y="Percent Change", size=show, color="SITC 1 DIGIT", hover_name="1D DESC", log_x=False, size_max=60)
    fig.update_layout(title_text="Trade Performance of Malaysia on YEAR: {} based on {}".format(year, show.split()[0]))
    fig.update_layout(height=600, width=900)
    st.plotly_chart(fig)

def area_graph():
    st.subheader("Area Plot of Malaysia's Trade Performance from 2013 to 2019")
    sitc = st.sidebar.selectbox('SITC:', ['SITC 1 DIGIT', 'SITC 2 DIGIT'])
    if sitc == 'SITC 1 DIGIT':
        df_sitc_1 = df.groupby(['SITC 1 DIGIT', 'YEAR'])[show].agg(['sum']).reset_index()
        df_sitc_1 = df_sitc_1.merge(sitc_1, on='SITC 1 DIGIT')
        fig = px.area(df_sitc_1, x="YEAR", y="sum", color="1D DESC")
        fig.update_layout(height=600, width=900)
    else:
        df_sitc_1 = df.groupby(['SITC 2 DIGIT', 'YEAR'])[show].agg(['sum']).reset_index()
        df_sitc_1 = df_sitc_1.merge(sitc_2, on='SITC 2 DIGIT')
        fig = px.area(df_sitc_1, x="YEAR", y="sum", color="2D DESC")
        fig.update_layout(showlegend=False, height=600, width=900)
    fig.update_layout(title_text="Trade Performance of Malaysia from 2013 to 2019 based on {}".format(show.split()[0]))
    st.plotly_chart(fig)



def plot_graph():
    if graph == 'PIE CHART':
        pie_graph()
    elif graph == 'TIME-SERIES':
       line_graph()
    elif graph == 'TREE MAP':
        tree_map()
    elif graph == 'BUBBLE PLOT':
        bubble_graph()
    elif graph == 'AREA PLOT':
        area_graph()
    else:
        bar_graph()
        
plot_graph()

