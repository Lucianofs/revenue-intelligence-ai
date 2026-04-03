import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(layout="wide")

st.title("🚀 Revenue Intelligence AI")

# =============================
# 📂 UPLOAD
# =============================
file = st.file_uploader("Upload de dados (CSV)")

if file:
    df = pd.read_csv(file)
else:
    # dados simulados
    df = pd.DataFrame({
        'campanha': np.random.choice(['Google','Meta','TikTok'],200),
        'valor': np.random.randint(100,5000,200),
        'custo': np.random.randint(100,3000,200)
    })

# =============================
# 📊 DASHBOARD
# =============================
st.subheader("📊 Receita por Campanha")

fig = px.bar(df, x='campanha', y='valor', color='campanha')
st.plotly_chart(fig, use_container_width=True)

# =============================
# 📈 KPI
# =============================
receita = df['valor'].sum()
custo = df['custo'].sum()
roi = receita / custo

col1, col2, col3 = st.columns(3)
col1.metric("💰 Receita", f"R$ {receita:,.0f}")
col2.metric("💸 Custo", f"R$ {custo:,.0f}")
col3.metric("📈 ROI", round(roi,2))

# =============================
# 🔮 SIMULADOR
# =============================
st.subheader("🔮 Simulador de Decisão")

preco = st.number_input("Preço médio", value=1000)
conv = st.slider("Conversão", 0.0, 0.1, 0.02)
trafego = st.number_input("Tráfego", value=10000)
cpc = st.number_input("CPC", value=2.0)
custo_op = st.number_input("Custo operacional", value=300)
capacidade = st.number_input("Capacidade máxima", value=500)

clientes = min(trafego * conv, capacidade)
receita_sim = clientes * preco
custo_total = trafego * cpc + clientes * custo_op
lucro = receita_sim - custo_total
roi_sim = receita_sim / (trafego * cpc)

col1, col2, col3 = st.columns(3)
col1.metric("Clientes", int(clientes))
col2.metric("Receita", f"R$ {receita_sim:,.0f}")
col3.metric("Lucro", f"R$ {lucro:,.0f}")

# =============================
# 🤖 IA
# =============================
st.subheader("🤖 Recomendação Inteligente")

if lucro > 0 and roi_sim > 1:
    st.success("🚀 Implementar cenário — viável e lucrativo")
else:
    st.error("⚠️ Não recomendado — risco de prejuízo")

# =============================
# 📊 GRÁFICO SIMULAÇÃO
# =============================
sim_df = pd.DataFrame({
    "Métrica": ["Receita","Custo","Lucro"],
    "Valor": [receita_sim, custo_total, lucro]
})

fig2 = px.bar(sim_df, x="Métrica", y="Valor", color="Métrica")
st.plotly_chart(fig2, use_container_width=True)
