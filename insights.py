def gerar_insights(df):
    insights = []

    roas = df['valor'].sum() / df['custo'].sum()

    if roas < 1:
        insights.append("Marketing está dando prejuízo")

    if df['reservas'].sum() / df['cliques'].sum() < 0.02:
        insights.append("Conversão baixa")

    top = df.groupby('campanha')['valor'].sum().idxmax()
    insights.append(f"Melhor campanha: {top}")

    return insights
