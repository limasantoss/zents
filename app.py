import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

st.set_page_config(page_title="Zents EDA", layout="wide")
st.title("Zents EDA ✨")
st.markdown("Bem-vindo ao Zents EDA! Faça upload do seu arquivo CSV ou Excel para começar.")

# --------- Funções utilitárias ---------

@st.cache_data
def carregar_arquivo(uploaded_file):
    if uploaded_file.name.lower().endswith('.csv'):
        return pd.read_csv(uploaded_file)
    else:
        return pd.read_excel(uploaded_file)

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

def limpeza_personalizada(df, estrategias):
    df_limpo = df.copy()
    resumo = []
    for coluna, estrategia in estrategias.items():
        n_antes = df_limpo[coluna].isnull().sum()
        if estrategia == "Preencher com média":
            valor = df_limpo[coluna].mean()
            df_limpo[coluna].fillna(valor, inplace=True)
            resumo.append(f"Coluna {coluna}: {n_antes} preenchidos com média.")
        elif estrategia == "Preencher com mediana":
            valor = df_limpo[coluna].median()
            df_limpo[coluna].fillna(valor, inplace=True)
            resumo.append(f"Coluna {coluna}: {n_antes} preenchidos com mediana.")
        elif estrategia == "Preencher com zero":
            df_limpo[coluna].fillna(0, inplace=True)
            resumo.append(f"Coluna {coluna}: {n_antes} preenchidos com zero.")
        elif estrategia == "Remover linhas":
            df_limpo = df_limpo[df_limpo[coluna].notnull()]
            resumo.append(f"Coluna {coluna}: {n_antes} linhas removidas.")
        elif estrategia == "Preencher com moda":
            valor = df_limpo[coluna].mode()[0]
            df_limpo[coluna].fillna(valor, inplace=True)
            resumo.append(f"Coluna {coluna}: {n_antes} preenchidos com moda.")
        elif estrategia == "Preencher com 'Desconhecido'":
            df_limpo[coluna].fillna("Desconhecido", inplace=True)
            resumo.append(f"Coluna {coluna}: {n_antes} preenchidos com 'Desconhecido'.")
    return df_limpo, resumo

def gerar_pdf_mem(df, resumo_limpeza):
    from fpdf import FPDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Relatório Zents EDA", 0, 1)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Total de linhas: {len(df)}", 0, 1)
    pdf.cell(0, 10, f"Total de colunas: {len(df.columns)}", 0, 1)
    pdf.cell(0, 10, "Resumo da Limpeza:", 0, 1)
    for item in resumo_limpeza:
        pdf.multi_cell(0, 10, item)  # quebra de linha automática
    pdf.cell(0, 10, "Tipos de Dados:", 0, 1)
    for col in df.dtypes.index:
        tipo = str(df.dtypes[col])
        pdf.cell(0, 10, f"{col}: {tipo}", 0, 1)
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    return pdf_bytes

# --------- Interface Streamlit ---------

uploaded_file = st.file_uploader("Faça upload do arquivo", type=["csv", "xlsx"])

if uploaded_file is not None:
    df = carregar_arquivo(uploaded_file)
    st.header("1. Visualização Inicial ✅")
    linhas = st.slider("Quantas linhas mostrar?", min_value=5, max_value=min(100, len(df)), value=10)
    st.dataframe(df.head(linhas))

    st.header("2. Tipos de Dados e Estatísticas 📊")
    mostrar_tipos(df)
    mostrar_estatisticas(df)

    st.header("3. Valores Ausentes ⚠️")
    mostrar_ausentes(df)

    st.header("4. Limpeza de Dados 🧹")
    estrategias = {}
    nulos = df.isnull().sum()
    colunas_nulas = nulos[nulos > 0].index.tolist()
    opcoes_num = ["Preencher com média", "Preencher com mediana", "Preencher com zero", "Remover linhas"]
    opcoes_cat = ["Preencher com moda", "Preencher com 'Desconhecido'", "Remover linhas"]
    for coluna in colunas_nulas:
        st.write(f"Coluna: **{coluna}** ({nulos[coluna]} nulos)")
        if df[coluna].dtype in ["float64", "int64"]:
            estrategias[coluna] = st.selectbox(f"Estratégia para '{coluna}'", opcoes_num, key=coluna)
        else:
            estrategias[coluna] = st.selectbox(f"Estratégia para '{coluna}'", opcoes_cat, key=coluna)

    if st.button("Executar Limpeza de Dados"):
        df_limpo, resumo_limpeza = limpeza_personalizada(df, estrategias)
        st.success("Dados limpos com sucesso! ✅")
        st.markdown("### Relatório da limpeza:")
        for item in resumo_limpeza:
            st.write("- " + item)
        st.markdown(f"Valores ausentes antes: **{nulos.sum()}**<br>Valores ausentes depois: **{df_limpo.isnull().sum().sum()}**", unsafe_allow_html=True)
        st.session_state.df_limpo = df_limpo
        st.session_state.resumo_limpeza = resumo_limpeza
    elif 'df_limpo' not in st.session_state:
        st.session_state.df_limpo = df.copy()
        st.session_state.resumo_limpeza = ["Limpeza padrão executada."]

    st.header("5. Visualização de Dados 📈")
    df_visu = st.session_state.df_limpo
    col_num = df_visu.select_dtypes(include=['number']).columns.tolist()
    col_cat = df_visu.select_dtypes(include=['object', 'category']).columns.tolist()
    LIMITE_GRAFICOS = 5000
    amostra_graficos = df_visu.sample(min(LIMITE_GRAFICOS, len(df_visu)), random_state=42) if len(df_visu) > LIMITE_GRAFICOS else df_visu

    if col_num:
        with st.expander("Histograma (Plotly)"):
            coluna_hist = st.selectbox("Coluna numérica para histograma", col_num, key='hist_int')
            fig_hist = px.histogram(amostra_graficos, x=coluna_hist)
            st.plotly_chart(fig_hist)
        with st.expander("Boxplot com Outliers"):
            coluna_box = st.selectbox("Coluna para boxplot", col_num, key='box_int')
            fig_box = px.box(amostra_graficos, y=coluna_box, points="all")
            st.plotly_chart(fig_box)
        with st.expander("Gráfico de Dispersão (Correlação)"):
            col_x = st.selectbox("Eixo X (numérico)", col_num, key='scatter_x')
            col_y = st.selectbox("Eixo Y (numérico)", col_num, key='scatter_y')
            if col_x != col_y:
                fig_scat = px.scatter(amostra_graficos, x=col_x, y=col_y)
                st.plotly_chart(fig_scat)
    if col_cat:
        with st.expander("Gráfico de Frequência (Top N)"):
            coluna_freq = st.selectbox("Coluna categórica", col_cat, key='freq_int')
            n_top = st.slider("Top quantas categorias mostrar?", min_value=3, max_value=30, value=10)
            vc = amostra_graficos[coluna_freq].value_counts()
            vc_top = vc.iloc[:n_top]
            outros = vc.iloc[n_top:].sum()
            if outros > 0:
                vc_top["Outros"] = outros
            fig_freq = px.bar(vc_top, x=vc_top.index, y=vc_top.values, labels={"x":coluna_freq, "y":"Contagem"})
            st.plotly_chart(fig_freq)

    st.header("6. Baixar Arquivo Tratado ou Relatório 📥")
    df_out = st.session_state.df_limpo
    nome_arquivo = uploaded_file.name.replace(".csv", "_limpo.csv").replace(".xlsx", "_limpo.xlsx")
    if uploaded_file.name.lower().endswith(".csv"):
        csv = df_out.to_csv(index=False).encode('utf-8')
        st.download_button("Baixar CSV Limpo", data=csv, file_name=nome_arquivo, mime="text/csv")
    else:
        saida = BytesIO()
        with pd.ExcelWriter(saida, engine='openpyxl') as writer:
            df_out.to_excel(writer, index=False)
        st.download_button("Baixar Excel Limpo", data=saida.getvalue(), file_name=nome_arquivo, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    # Relatório PDF (só aparece se fpdf instalado)
    try:
        from fpdf import FPDF
        if st.button("Baixar Relatório PDF (resumo)"):
            resumo = st.session_state.resumo_limpeza if 'resumo_limpeza' in st.session_state else ["Limpeza padrão executada."]
            pdf_bytes = gerar_pdf_mem(df_out, resumo)
            st.download_button("Baixar PDF", data=pdf_bytes, file_name="relatorio_eda.pdf", mime="application/pdf")
    except ImportError:
        st.info("Para baixar PDF, instale o pacote: pip install fpdf")
else:
    st.info("Envie seu arquivo para começar!")
