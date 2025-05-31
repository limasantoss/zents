import streamlit as st
import pandas as pd
from eda import (
    estatisticas, limpeza, visualizacoes, correlacao, relatorio, recomendacoes
)

st.set_page_config(page_title="Zents EDA Automação", layout="wide")
st.title("Zents EDA - Análise Exploratória Inteligente")

uploaded_file = st.file_uploader("Arraste seu CSV/Excel aqui", type=['csv', 'xlsx'])
if uploaded_file:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    st.subheader("1. Identificação das Variáveis")
    var_doc, explic_var = estatisticas.identificar_variaveis(df)
    st.dataframe(var_doc)
    st.caption(explic_var)
    st.download_button("Download documentação", var_doc.to_csv(index=False), "documentacao_variaveis.csv")

    st.subheader("2. Estatísticas Descritivas")
    stats, insights = estatisticas.gerar_estatisticas(df)
    st.dataframe(stats)
    st.markdown(insights)

    st.subheader("3. Limpeza e Análise de Valores Ausentes")
    limpeza_df, resumo_limpeza, explic_nulos = limpeza.limpeza_nulos(df)
    st.dataframe(resumo_limpeza)
    st.markdown(explic_nulos)

    st.subheader("4. Gráficos Exploratórios com Insights Automáticos")
    visualizacoes.exibir_graficos(limpeza_df, st)

    st.subheader("5. Outliers: Detecção, Quantificação e Recomendações")
    outlier_tab, explic_outliers = limpeza.detectar_outliers(limpeza_df)
    st.dataframe(outlier_tab)
    st.markdown(explic_outliers)

    st.subheader("6. Correlações e Hipóteses Automáticas")
    corr_img, explic_corr, hipoteses = correlacao.matriz_correlacao(limpeza_df)
    st.pyplot(corr_img)
    st.markdown(explic_corr)
    st.markdown("### Hipóteses automáticas baseadas nos dados:")
    for h in hipoteses:
        st.info(h)

    st.subheader("7. Recomendações para Modelagem")
    st.markdown(recomendacoes.sugerir_variaveis(limpeza_df, outlier_tab, corr_img))

    st.subheader("8. Relatório PDF Automático")
    if st.button("Gerar PDF"):
        pdf_bytes = relatorio.gerar_pdf(
            df_original=df,
            df_limpo=limpeza_df,
            variaveis=var_doc,
            estatisticas=stats,
            resumo_limpeza=resumo_limpeza,
            outliers=outlier_tab,
            correlacao_img=corr_img,
            hipoteses=hipoteses
        )
        st.download_button("Download PDF", pdf_bytes, "relatorio_zents_eda.pdf", "application/pdf")
else:
    st.warning("Faça upload de um arquivo para começar.")