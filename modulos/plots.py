import streamlit as st
import plotly.express as px

def plot_histograma(df, coluna):
    fig = px.histogram(df, x=coluna)
    st.plotly_chart(fig)

def plot_boxplot(df, coluna):
    fig = px.box(df, y=coluna, points="all")
    st.plotly_chart(fig)

def plot_frequencia(df, coluna, n_top=10):
    vc = df[coluna].value_counts()
    vc_top = vc.iloc[:n_top]
    outros = vc.iloc[n_top:].sum()
    if outros > 0:
        vc_top["Outros"] = outros
    fig = px.bar(vc_top, x=vc_top.index, y=vc_top.values, labels={"x":coluna, "y":"Contagem"})
    st.plotly_chart(fig)