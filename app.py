# Zents EDA - App Completo com Relatório PDF 

import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

def gerar_pdf_melhorado(df_original, df_limpo, resumo_limpeza, linhas_removidas):
    from fpdf import FPDF
    from datetime import datetime
    import numpy as np

    pdf = FPDF()
    pdf.add_page()

    # Título e data/hora
    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 12, "Zents EDA - Relatório de Análise de Dados", 0, 1, "C")
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, "Gerado em: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 0, 1, "C")
    pdf.ln(4)

    # Quantidade de linhas e colunas antes/depois da limpeza
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, f"Dados originais: {len(df_original)} linhas, {len(df_original.columns)} colunas", 0, 1)
    pdf.cell(0, 8, f"Dados após limpeza: {len(df_limpo)} linhas", 0, 1)
    pdf.cell(0, 8, f"Linhas removidas na limpeza: {linhas_removidas}", 0, 1)
    pdf.ln(2)

    # Resumo da limpeza
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Resumo da Limpeza:", 0, 1)
    pdf.set_font("Arial", "", 12)
    for item in resumo_limpeza:
        pdf.multi_cell(0, 8, u"- " + str(item))
    pdf.ln(2)

    # Prévia dos dados (primeiras 5 linhas)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Pré-visualização dos dados (top 5 linhas):", 0, 1)
    pdf.set_font("Arial", "", 8)
    head = df_limpo.head(5)
    colunas = list(head.columns)
    larg_celula = max(25, int(170 / max(1, len(colunas))))
    # Cabeçalho da
