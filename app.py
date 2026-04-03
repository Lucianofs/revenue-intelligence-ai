import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import requests
from bs4 import BeautifulSoup

st.set_page_config(layout="wide")

st.title("🚀 Revenue Intelligence AI - Sistema Profissional")

# =========================================
# 📂 UPLOAD OU SIMULAÇÃO
# =========================================
file = st.file_uploader("Upload de dados (CSV)")

if file:
    df = pd.read_csv(file)
else:
    df = pd.DataFrame({
        'campanha': np.random.choice(['Google','Meta','TikTok'],200),
        'cliques': np.random.randint(100,1000,200),
        'reservas': np.random.randint(10,200,200),
        'valor': np.random.randint(1000,10000,200),
        'custo': np.random.randint(500,5000,200)
    })

# =========================================
# 📊 ABAS
# =========================================
aba1, aba2, aba3, aba4, aba5, aba6, aba7 = st.tabs([
    "📊 Visão Geral",
    "📈 Marketing",
    "🔻 Funil",
    "🔮 Simulador",
    "👥 CRM",
    "🌐 URL",
    "🤖 IA"
])

# =========================================
# 📊 VISÃO GERAL
# =========================================
with aba1:
    receita = df['valor'].sum()
    custo = df['custo'].sum()
    reservas = df['reservas'].sum()
    cliques = df['cliques'].sum()

    ticket = receita / reservas if reservas else 0
    roas = receita / custo if custo else 0
    cac = custo / reservas if reservas else 0
    conversao = reservas / cliques if cliques else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Receita", f"R$ {receita:,.0f}")
    col2.metric("📦 Reservas", reservas)
    col3.metric("📈 ROAS", round(roas,2))
    col4.metric("💸 CAC", round(cac,2))

    st.markdown("### 📈 Receita por Campanha")
    fig = px.bar(df, x='campanha', y='valor', color='campanha')
    st.plotly_chart(fig, use_container_width=True)

# =========================================
# 📈 MARKETING
# =========================================
with aba2:
    st.markdown("### Performance por Canal")

    df_group = df.groupby('campanha').sum().reset_index()
    df_group['ROAS'] = df_group['valor'] / df_group['custo']
    df_group['CAC'] = df_group['custo'] / df_group['reservas']

    st.dataframe(df_group)

    fig = px.bar(df_group, x='campanha', y='ROAS')
    st.plotly_chart(fig, use_container_width=True)

# =========================================
# 🔻 FUNIL
# =========================================
with aba3:
    funil = pd.DataFrame({
        'Etapa': ['Cliques','Reservas'],
        'Valor': [cliques, reservas]
    })

    fig = px.funnel(funil, x='Valor', y='Etapa')
    st.plotly_chart(fig, use_container_width=True)

# =========================================
# 🔮 SIMULADOR PROFISSIONAL
# =========================================
with aba4:
    st.markdown("### Simulação de Cenário")

    investimento = st.number_input("Investimento", value=10000)
    cpc = st.number_input("CPC", value=2.0)
    conv = st.slider("Conversão", 0.0, 0.1, 0.02)
    ticket = st.number_input("Ticket médio", value=1000)
    custo_op = st.number_input("Custo operacional", value=300)

    trafego = investimento / cpc
    clientes = trafego * conv
    receita_sim = clientes * ticket
    custo_total = investimento + (clientes * custo_op)
    lucro = receita_sim - custo_total
    roi = receita_sim / investimento

    col1, col2, col3 = st.columns(3)
    col1.metric("Receita", f"R$ {receita_sim:,.0f}")
    col2.metric("Lucro", f"R$ {lucro:,.0f}")
    col3.metric("ROI", round(roi,2))

# =========================================
# 👥 CRM / CHURN
# =========================================
with aba5:
    st.markdown("### Análise de Clientes")

    df['churn_risco'] = np.random.choice(['Alto','Médio','Baixo'], len(df))

    fig = px.pie(df, names='churn_risco')
    st.plotly_chart(fig)

# =========================================
# 🌐 ANÁLISE DE URL
# =========================================
with aba6:
    st.markdown("### Diagnóstico de Site")

    url = st.text_input("Digite URL")

    if url:
        try:
            r = requests.get(url, verify=False)
            soup = BeautifulSoup(r.text, 'html.parser')

            st.success("Site analisado com sucesso")

            title = soup.title.string if soup.title else "Sem título"
            st.write("Título:", title)

        except:
            st.error("Erro ao acessar URL")

# =========================================
# 🤖 IA / INSIGHTS
# =========================================
with aba7:
    st.markdown("### Insights Automáticos")

    if roas < 1:
        st.error("❌ Marketing com prejuízo")
    else:
        st.success("🚀 Marketing lucrativo")

    if conversao < 0.02:
        st.warning("⚠️ Conversão baixa — melhorar página")

    st.info("💡 Escalar campanhas com maior ROAS")
