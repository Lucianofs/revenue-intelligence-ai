import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import requests
from bs4 import BeautifulSoup

from auth import login
from ml_models import modelo_churn, previsao_receita
from simulador import simular_negocio
from insights import gerar_insights

st.set_page_config(layout="wide")

# LOGIN
if not login():
    st.stop()

st.title(f"🚀 Revenue Intelligence AI | {st.session_state['empresa']}")

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
# 📊 ABAS COMPLETAS
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

    fig = px.bar(df, x='campanha', y='valor', color='campanha')
    st.plotly_chart(fig, use_container_width=True)

# =========================================
# 📈 MARKETING
# =========================================
with aba2:
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
    investimento = st.number_input("Investimento", value=10000)
    cpc = st.number_input("CPC", value=2.0)
    conv = st.slider("Conversão", 0.0, 0.1, 0.02)
    ticket = st.number_input("Ticket médio", value=1000)
    custo_op = st.number_input("Custo operacional", value=300)

    res = simular_negocio(investimento, cpc, conv, ticket, custo_op)

    col1, col2, col3 = st.columns(3)
    col1.metric("Receita", f"R$ {res['receita']:,.0f}")
    col2.metric("Lucro", f"R$ {res['lucro']:,.0f}")
    col3.metric("ROI", round(res['roi'],2))

# =========================================
# 👥 CRM / CHURN
# =========================================
with aba5:
    df = modelo_churn(df)

    fig = px.pie(df, names='churn_pred')
    st.plotly_chart(fig)

# =========================================
# 🌐 URL
# =========================================
with aba6:
    url = st.text_input("Digite URL")

    if url:
        try:
            r = requests.get(url, verify=False)
            soup = BeautifulSoup(r.text, 'html.parser')

            st.success("Site analisado")

            title = soup.title.string if soup.title else "Sem título"
            st.write("Título:", title)

        except:
            st.error("Erro ao acessar URL")

# =========================================
# 🤖 IA / PREVISÃO + INSIGHTS
# =========================================
with aba7:
    df = previsao_receita(df)

    fig = px.line(df, y='forecast')
    st.plotly_chart(fig)

    insights = gerar_insights(df)

    for i in insights:
        st.write("👉", i)
