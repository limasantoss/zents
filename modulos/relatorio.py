def gerar_pdf_mem(df, resumo_limpeza):
    from fpdf import FPDF

    nulos = df.isnull().sum()
    nulos = nulos[nulos > 0]
    colunas_num = df.select_dtypes(include=['number']).columns

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 12, "Relatório Zents EDA", 0, 1, "C")
    pdf.ln(3)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Total de linhas: {len(df)}", 0, 1)
    pdf.cell(0, 10, f"Total de colunas: {len(df.columns)}", 0, 1)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Resumo da Limpeza:", 0, 1)
    pdf.set_font("Arial", "", 11)
    for item in resumo_limpeza:
        pdf.multi_cell(0, 8, "- " + item)
    pdf.ln(2)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Valores Ausentes por Coluna:", 0, 1)
    pdf.set_font("Arial", "", 11)
    if nulos.empty:
        pdf.cell(0, 8, "Nenhuma coluna com valores ausentes.", 0, 1)
    else:
        for coluna, valor in nulos.items():
            pdf.cell(0, 8, f"{coluna}: {valor}", 0, 1)
    pdf.ln(2)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Tipos de Dados:", 0, 1)
    pdf.set_font("Arial", "", 11)
    for col in df.dtypes.index:
        tipo = str(df.dtypes[col])
        pdf.cell(0, 8, f"{col:20} {tipo}", 0, 1)
    pdf.ln(2)

    if len(colunas_num) > 0:
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Resumo Estatístico das Colunas Numéricas:", 0, 1)
        pdf.set_font("Arial", "", 11)
        desc = df[colunas_num].describe().T
        for col in desc.index:
            pdf.cell(0, 8, f"{col}:", 0, 1)
            pdf.cell(0, 8, f"   Média:   {desc.loc[col, 'mean']:.2f}", 0, 1)
            pdf.cell(0, 8, f"   Mediana: {df[col].median():.2f}", 0, 1)
            pdf.cell(0, 8, f"   Mínimo:  {desc.loc[col, 'min']:.2f}", 0, 1)
            pdf.cell(0, 8, f"   Máximo:  {desc.loc[col, 'max']:.2f}", 0, 1)
            pdf.ln(2)
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    return pdf_bytes
