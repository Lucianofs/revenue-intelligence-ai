import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from auth import login
from ml_models import modelo_churn, previsao_receita
from simulador import simular_negocio
from insights import gerar_insights

st.set_page_config(layout="wide")

# LOGIN
if not login():
    st.stop()

st.title(f"🚀 Revenue AI | {st.session_state['empresa']}")

# DADOS
df = pd.DataFrame({
    'campanha': np.random.choice(['Google','Meta','TikTok'],200),
    'cliques': np.random.randint(100,1000,200),
    'reservas': np.random.randint(10,200,200),
    'valor': np.random.randint(1000,10000,200),
    'custo': np.random.randint(500,5000,200)
})

# ABAS
aba1, aba2, aba3, aba4 = st.tabs([
    "📊 Dashboard",
    "🤖 IA",
    "🔮 Simulador",
    "💡 Insights"
])

# DASHBOARD
with aba1:
    fig = px.bar(df, x='campanha', y='valor')
    st.plotly_chart(fig, use_container_width=True)

# IA
with aba2:
    df = modelo_churn(df)
    df = previsao_receita(df)

    fig = px.line(df, y='forecast')
    st.plotly_chart(fig)

# SIMULADOR
with aba3:
    res = simular_negocio(10000,2,0.02,1000,300)
    st.write(res)

# INSIGHTS
with aba4:
    insights = gerar_insights(df)
    for i in insights:
        st.write("👉", i)
