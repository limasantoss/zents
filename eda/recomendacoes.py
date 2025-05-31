def sugerir_variaveis(df, outlier_tab, corr_img):
    sugestoes = []
    # Variáveis com menos de 5% nulos, sem outliers: boas para modelagem
    for col in df.select_dtypes(include='number').columns:
        if (df[col].isnull().mean() < 0.05):
            sugestoes.append(f"Coluna **{col}**: recomendada para modelagem (baixa taxa de nulos).")
    # Colunas categóricas com poucos valores únicos: sugerir one-hot
    for col in df.select_dtypes(include='object').columns:
        if df[col].nunique() < 10:
            sugestoes.append(f"Coluna **{col}**: recomendada para codificação one-hot.")
    if not sugestoes:
        sugestoes = ["Reveja as variáveis; nenhuma recomendação automática forte encontrada."]
    return "\n".join(sugestoes)