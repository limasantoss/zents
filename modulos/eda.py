import streamlit as st

def mostrar_tipos(df):
    st.write("**Tipos de dados:**")
    st.dataframe(df.dtypes.astype(str), use_container_width=True)

def mostrar_estatisticas(df):
    st.write("**Estatísticas descritivas:**")
    st.dataframe(df.describe(include='all'), use_container_width=True)

def mostrar_ausentes(df):
    st.write("**Valores ausentes por coluna:**")
    nulos = df.isnull().sum()
    nulos = nulos[nulos > 0]
    if nulos.empty:
        st.success("Nenhuma coluna com valores ausentes!")
    else:
        st.dataframe(nulos, use_container_width=True)