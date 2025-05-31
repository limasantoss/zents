import pandas as pd
import numpy as np
from scipy.stats import zscore

def limpeza_nulos(df):
    """
    Analisa valores nulos em cada coluna do DataFrame e recomenda ações de limpeza.
    - Calcula a porcentagem de nulos por coluna.
    - Sugere estratégia de imputação conforme o tipo de dado (número/texto).
    - Remove linhas completamente nulas (como exemplo de limpeza automática simples).

    Parâmetros:
        df (pd.DataFrame): Dados originais.
    Retorna:
        df_limpo (pd.DataFrame): DataFrame após limpeza mínima.
        resumo (pd.DataFrame): Tabela com porcentagem de nulos por coluna.
        explic_text (str): Texto explicativo com recomendações automáticas.
    """
    # Calcula a porcentagem de valores nulos por coluna
    na_perc = (df.isnull().mean() * 100).round(2)
    resumo = pd.DataFrame({'Coluna': na_perc.index, 'Porcentagem de Nulos': na_perc.values})

    # Gera explicações/recomendações baseadas no tipo da coluna
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

    # Exemplo: remove linhas completamente nulas (não remove linhas parcialmente nulas)
    df_limpo = df.dropna(how='all')
    return df_limpo, resumo, explic_text

def detectar_outliers(df):
    """
    Detecta outliers em todas as colunas numéricas usando Z-score.
    Para cada coluna:
      - Calcula o Z-score dos valores: quanto maior o Z, mais distante da média.
      - Valores com |Z| > 3 são considerados outliers (Regra Empírica - 99,7% dos dados ficam até 3 desvios-padrão).
      - Gera tabela com a contagem e porcentagem de outliers por coluna.
      - Explica quando o percentual é alto.

    Fórmula do Z-score:
        Z = (x - média) / desvio padrão

    Parâmetros:
        df (pd.DataFrame): DataFrame de entrada.
    Retorna:
        pd.DataFrame: Tabela de outliers por coluna.
        str: Explicação sobre os outliers detectados.
    """
    outlier_table = []
    explic = []
    num_cols = df.select_dtypes(include=[np.number]).columns
    for col in num_cols:
        # Calcula Z-score para cada valor não nulo
        z = np.abs(zscore(df[col].dropna()))
        # Considera outlier quem tem |Z| > 3
        outliers = (z > 3).sum()
        perc = 100 * outliers / len(df[col].dropna())
        outlier_table.append({'Coluna': col, 'Outliers': outliers, 'Porcentagem': f"{perc:.2f}%"})
        if perc > 5:
            explic.append(f"Coluna **{col}**: {perc:.2f}% de outliers! Avaliar remoção ou imputação.")
    explic_text = "\n".join(explic) if explic else "Nenhuma coluna com excesso de outliers."
    return pd.DataFrame(outlier_table), explic_text