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
show = st.sidebar.multiselect('Metric(s):', ['IMPORT (MILLION RM)', 'EXPORT (MILLION RM)', 'DEFICIT/SURPLUS (MILLION RM)'], default = ['IMPORT (MILLION RM)'], key='1')

def single_graph_line():
    fig, ax = plt.subplots(1, 1)
    df.groupby('YEAR')[show].sum().plot(ax=ax)
    st.pyplot(fig)


def bi_graph_line(column, i):
    fig, ax = plt.subplots(1, 1)
    df[df[column] == i].groupby('YEAR')[show].sum().plot(ax=ax, figsize=(12, 8), title=column + ': ' + str(i));
    st.pyplot(fig)


def multiple_graph_line(column_1, i, column_2, j):
    fig, ax = plt.subplots(1, 1)
    df[(df[column_1] == i) & (df[column_2] == j)].groupby('YEAR')[show].sum().plot( ax = ax, title = column_1 + ': ' + str(i) + ' and ' + column_2 + ': '+ str(j));
    st.pyplot(fig)

def line_graph():
    if len(show) != 0:
        columns = []
        columns = st.multiselect('Feature(s):', ['COUNTRY', 'SITC 1 DIGIT', 'SITC 2 DIGIT'], key='8')
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

line_graph()