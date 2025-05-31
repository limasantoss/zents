def gerar_pdf_mem(df, resumo_limpeza):
    from fpdf import FPDF

    # 1. VISUALIZAÇÃO INICIAL
    n_linhas, n_colunas = df.shape
    texto_visualizacao = (
        f"O conjunto de dados analisado contém {n_linhas:,} linhas e {n_colunas} colunas. "
        "Isso indica um volume significativo de informações a serem exploradas."
    )

    # 2. TIPOS DE DADOS E ESTATÍSTICAS
    tipos = df.dtypes.astype(str)
    tipos_exp = []
    explicacoes_tipo = {
        "object": "texto/código",
        "int64": "número inteiro",
        "float64": "número decimal",
        "datetime64[ns]": "data/hora"
    }
    for col, tipo in tipos.items():
        t = explicacoes_tipo.get(tipo, tipo)
        tipos_exp.append(f"- {col}: {t}")
    colunas_num = df.select_dtypes(include=['number']).columns
    stats_linha = []
    if len(colunas_num) > 0:
        desc = df[colunas_num].describe().T
        for col in desc.index:
            stats_linha.append(
                f"- {col}: média {desc.loc[col, 'mean']:.2f}, mediana {df[col].median():.2f}, mínimo {desc.loc[col, 'min']:.2f}, máximo {desc.loc[col, 'max']:.2f}"
            )
    else:
        stats_linha.append("Nenhuma coluna numérica para análise estatística.")
    texto_tipos = (
        "Esta seção mostra o tipo de dado encontrado em cada coluna, como texto, número inteiro, número decimal ou data. "
        "É importante para saber como os dados podem ser usados nas análises e gráficos.\n"
        + "\n".join(tipos_exp) +
        "\n\nEstatísticas (colunas numéricas):\n" + "\n".join(stats_linha)
    )

    # 3. VALORES AUSENTES
    nulos = df.isnull().sum()
    nulos = nulos[nulos > 0]
    if nulos.empty:
        texto_nulos = (
            "Aqui são listadas as colunas que possuem dados faltantes (nulos ou vazios). "
            "No seu arquivo, nenhuma coluna possui valores ausentes, indicando boa qualidade dos dados."
        )
    else:
        texto_nulos = (
            "As seguintes colunas possuem dados ausentes (nulos ou vazios). "
            "Isso pode indicar problemas de coleta ou preenchimento dos dados:\n"
            + "\n".join([f"- {col}: {qtd}" for col, qtd in nulos.items()])
        )

    # 4. LIMPEZA DE DADOS
    if resumo_limpeza == ["Limpeza padrão executada."]:
        texto_limpeza = (
            "Não foi necessário aplicar estratégias de limpeza, pois não havia valores ausentes ou inconsistências detectadas."
        )
    else:
        texto_limpeza = (
            "As seguintes estratégias de limpeza foram aplicadas para melhorar a qualidade dos dados:\n"
            + "\n".join(["- " + item for item in resumo_limpeza])
        )

    # 5. VISUALIZAÇÃO DE DADOS
    texto_viz = (
        "A análise visual é fundamental para identificar padrões e possíveis problemas nos dados. "
        "Use os gráficos interativos do aplicativo para explorar distribuições, relações e outliers."
    )

    # 6. DOWNLOAD DE DADOS TRATADOS E RELATÓRIO
    texto_down = (
        "Você pode baixar os dados tratados e este relatório diretamente pelo app."
    )

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Relatório Zents EDA", 0, 1, "C")
    pdf.set_font("Arial", "", 12)
    pdf.ln(3)

    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 10, "1. Visualização Inicial", 0, 1)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 7, texto_visualizacao)
    pdf.ln(2)

    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 10, "2. Tipos de Dados e Estatísticas", 0, 1)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 7, texto_tipos)
    pdf.ln(2)

    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 10, "3. Valores Ausentes", 0, 1)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 7, texto_nulos)
    pdf.ln(2)

    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 10, "4. Limpeza de Dados", 0, 1)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 7, texto_limpeza)
    pdf.ln(2)

    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 10, "5. Visualização de Dados", 0, 1)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 7, texto_viz)
    pdf.ln(2)

    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 10, "6. Download de Dados Tratados e Relatório", 0, 1)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 7, texto_down)

    pdf_bytes = pdf.output(dest='S').encode('latin1')
    return pdf_bytes
