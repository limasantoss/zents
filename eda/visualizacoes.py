import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def exibir_graficos(df, stobj):
    num_cols = df.select_dtypes(include='number').columns
    for col in num_cols:
        fig, axs = plt.subplots(1, 2, figsize=(10, 4))
        sns.histplot(df[col].dropna(), ax=axs[0], kde=True)
        axs[0].set_title(f"Histograma de {col}")
        sns.boxplot(x=df[col], ax=axs[1])
        axs[1].set_title(f"Boxplot de {col}")
        stobj.pyplot(fig)
        # Explicação automática
        skew = df[col].skew()
        if skew > 1:
            stobj.info(f"Distribuição de {col}: assimétrica à direita.")
        elif skew < -1:
            stobj.info(f"Distribuição de {col}: assimétrica à esquerda.")
        else:
            stobj.info(f"Distribuição de {col}: aproximadamente simétrica.")