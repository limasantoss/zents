import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def exibir_graficos(df, stobj):
    """
    Exibe gráficos exploratórios para todas as colunas numéricas do DataFrame.
    Para cada coluna:
      - Mostra um histograma com curva de densidade.
      - Mostra um boxplot para identificar outliers.
      - Gera uma explicação automática sobre a simetria da distribuição.
    Parâmetros:
        df (pd.DataFrame): DataFrame dos dados já tratados.
        stobj (st): Objeto do Streamlit, geralmente 'st'.
    """
    # Seleciona apenas as colunas numéricas
    num_cols = df.select_dtypes(include='number').columns

    if len(num_cols) == 0:
        stobj.warning("Nenhuma coluna numérica encontrada para exibir gráficos.")
        return

    # Para cada coluna numérica, gera um gráfico exploratório
    for col in num_cols:
        # Cria uma figura com dois gráficos lado a lado
        fig, axs = plt.subplots(1, 2, figsize=(10, 4))

        # Histograma com linha de densidade (KDE)
        sns.histplot(df[col].dropna(), ax=axs[0], kde=True)
        axs[0].set_title(f"Histograma de {col}")

        # Boxplot para visualizar outliers
        sns.boxplot(x=df[col], ax=axs[1])
        axs[1].set_title(f"Boxplot de {col}")

        # Exibe a figura no Streamlit
        stobj.pyplot(fig)
        plt.close(fig)  # Evita sobreposição de gráficos na memória

        # Cálculo da assimetria (skewness) para explicar o formato da distribuição
        skew = df[col].skew()
        if skew > 1:
            stobj.info(f"Distribuição de {col}: assimétrica à direita (mais valores baixos, poucos muito altos).")
        elif skew < -1:
            stobj.info(f"Distribuição de {col}: assimétrica à esquerda (mais valores altos, poucos muito baixos).")
        else:
            stobj.info(f"Distribuição de {col}: aproximadamente simétrica.")

