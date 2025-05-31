import pandas as pd
import numpy as np
from scipy.stats import zscore

def limpeza_nulos(df):
    na_perc = (df.isnull().mean() * 100).round(2)
    resumo = pd.DataFrame({'Coluna': na_perc.index, 'Porcentagem de Nulos': na_perc.values})
    explic = []
    for col, perc in na_perc.items():
        if perc > 0:
            tipo = str(df[col].dtype)
            if tipo.startswith('float') or tipo.startswith('int'):
                recomend = "Imputar média/mediana"
            elif tipo == 'object':
                recomend = "Imputar moda/valor constante"
            else:
                recomend = "Avaliar caso a caso"
            explic.append(f"Coluna **{col}**: {perc:.1f}% nulos. Recomendação: {recomend}.")
    explic_text = "\n".join(explic) if explic else "Não há colunas com nulos."
    # Exemplo de limpeza simples (remover linhas todas nulas)
    df_limpo = df.dropna(how='all')
    return df_limpo, resumo, explic_text

def detectar_outliers(df):
    outlier_table = []
    explic = []
    num_cols = df.select_dtypes(include=[np.number]).columns
    for col in num_cols:
        z = np.abs(zscore(df[col].dropna()))
        outliers = (z > 3).sum()
        perc = 100 * outliers / len(df[col].dropna())
        outlier_table.append({'Coluna': col, 'Outliers': outliers, 'Porcentagem': f"{perc:.2f}%"})
        if perc > 5:
            explic.append(f"Coluna **{col}**: {perc:.2f}% de outliers! Avaliar remoção ou imputação.")
    explic_text = "\n".join(explic) if explic else "Nenhuma coluna com excesso de outliers."
    return pd.DataFrame(outlier_table), explic_text