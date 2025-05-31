import pandas as pd

def identificar_variaveis(df):
    tipo_map = {
        'object': 'Categórico',
        'int64': 'Numérico (int)',
        'float64': 'Numérico (float)',
        'datetime64[ns]': 'Datetime',
        'bool': 'Booleano'
    }
    variaveis = []
    explic = []
    for col in df.columns:
        tipo = str(df[col].dtype)
        tipo_leg = tipo_map.get(tipo, tipo)
        if "id" in col.lower():
            funcao = "Identificador"
        elif "target" in col.lower() or "label" in col.lower():
            funcao = "Saída (target)"
        else:
            funcao = "Entrada"
        variaveis.append({'Coluna': col, 'Tipo': tipo_leg, 'Função': funcao})
        explic.append(f"Coluna **{col}**: tipo {tipo_leg}, função {funcao}.")
    doc = pd.DataFrame(variaveis)
    explic_text = "  \n".join(explic)
    return doc, explic_text

def gerar_estatisticas(df):
    desc = df.describe(include='all').T
    insights = []
    for col in df.select_dtypes(include=['number']).columns:
        std = df[col].std()
        mean = df[col].mean()
        if std > 2 * mean:
            insights.append(f"- A variável **{col}** possui alta dispersão (std > 2x média).")
    if not insights:
        insights.append("- Nenhuma coluna numérica apresenta dispersão incomum.")
    return desc, "  \n".join(insights)