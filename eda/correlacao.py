import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def matriz_correlacao(df):
    num_cols = df.select_dtypes(include='number').columns
    corr = df[num_cols].corr()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
    # Análise de correlações
    explic = []
    hipoteses = []
    for i in corr.columns:
        for j in corr.columns:
            if i != j and abs(corr.loc[i, j]) > 0.7:
                explic.append(f"{i} x {j}: correlação = {corr.loc[i, j]:.2f}")
                hipoteses.append(f"Existe relação forte entre {i} e {j}. Pode ser efeito causal ou fator em comum.")
    explic_text = "Principais correlações:\n" + ("\n".join(explic) if explic else "Nenhuma forte detectada.")
    hipoteses = list(set(hipoteses))[:3] if hipoteses else ["Não há hipóteses automáticas fortes."]
    return fig, explic_text, hipoteses