def simular_negocio(investimento, cpc, conv, ticket, custo_op):
    trafego = investimento / cpc
    clientes = trafego * conv

    receita = clientes * ticket
    custo_total = investimento + (clientes * custo_op)
    lucro = receita - custo_total
    roi = receita / investimento

    return {
        "clientes": clientes,
        "receita": receita,
        "lucro": lucro,
        "roi": roi
    }
