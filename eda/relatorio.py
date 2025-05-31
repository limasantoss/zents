from fpdf import FPDF

def gerar_pdf(df_original, df_limpo, variaveis, estatisticas, resumo_limpeza, outliers, correlacao_img, hipoteses):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Zents EDA - Relatório Completo", 0, 1, "C")
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 8, f"Linhas originais: {len(df_original)}, após limpeza: {len(df_limpo)}", 0, 1)
    pdf.ln(2)
    # Variáveis
    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 8, "Variáveis", 0, 1)
    pdf.set_font("Arial", "", 11)
    for _, row in variaveis.iterrows():
        pdf.cell(0, 6, f"- {row['Coluna']}: {row['Tipo']} ({row['Função']})", 0, 1)
    # Estatísticas
    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 8, "Estatísticas", 0, 1)
    pdf.set_font("Arial", "", 11)
    for col in estatisticas.index:
        pdf.cell(0, 6, f"- {col}: {estatisticas.loc[col].to_dict()}", 0, 1)
    # Limpeza
    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 8, "Limpeza", 0, 1)
    pdf.set_font("Arial", "", 11)
    for _, row in resumo_limpeza.iterrows():
        pdf.cell(0, 6, f"- {row['Coluna']}: {row['Porcentagem de Nulos']}% nulos", 0, 1)
    # Outliers
    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 8, "Outliers", 0, 1)
    pdf.set_font("Arial", "", 11)
    for _, row in outliers.iterrows():
        pdf.cell(0, 6, f"- {row['Coluna']}: {row['Porcentagem']} outliers", 0, 1)
    # Hipóteses
    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 8, "Hipóteses", 0, 1)
    pdf.set_font("Arial", "", 11)
    for h in hipoteses:
        pdf.cell(0, 6, f"- {h}", 0, 1)
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    return pdf_bytes