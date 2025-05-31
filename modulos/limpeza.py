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
