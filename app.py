import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time
import re
import requests
import urllib3

from bs4 import BeautifulSoup
from auth import login
from ml_models import modelo_churn, previsao_receita
from simulador import simular_negocio
from insights import gerar_insights
from pdf_report import gerar_pdf
from fpdf import FPDF
from textblob import TextBlob


ttt

st.set_page_config(layout="wide")

# =============================
# 🔐 LOGIN
# =============================
if not login():
    st.stop()

st.title(f"🚀 Revenue Intelligence AI | {st.session_state['empresa']}")

# =============================
# 📂 DADOS
# =============================
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

# =============================
# 📊 ABAS
# =============================
aba1, aba2, aba3, aba4, aba5, aba6, aba7 = st.tabs([
    "📊 Visão Geral",
    "📈 Marketing",
    "🔻 Funil",
    "🔮 Simulador",
    "👥 CRM",
    "🌐 URL",
    "🤖 IA"
])

# =============================
# 📊 VISÃO GERAL
# =============================
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

# =============================
# 📈 MARKETING
# =============================
with aba2:
    df_group = df.groupby('campanha').sum().reset_index()
    df_group['ROAS'] = df_group['valor'] / df_group['custo']
    df_group['CAC'] = df_group['custo'] / df_group['reservas']

    st.dataframe(df_group)

    fig = px.bar(df_group, x='campanha', y='ROAS')
    st.plotly_chart(fig, use_container_width=True)

# =============================
# 🔻 FUNIL
# =============================
with aba3:
    funil = pd.DataFrame({
        'Etapa': ['Cliques','Reservas'],
        'Valor': [df['cliques'].sum(), df['reservas'].sum()]
    })

    fig = px.funnel(funil, x='Valor', y='Etapa')
    st.plotly_chart(fig, use_container_width=True)

# =============================
# 🔮 SIMULADOR
# =============================
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

# =============================
# 👥 CRM
# =============================
with aba5:
    df = modelo_churn(df)

    fig = px.pie(df, names='churn_pred')
    st.plotly_chart(fig)

# =============================
# 🌐 URL INTELIGENTE ABA 6
# ============================ 
# Desativar avisos de segurança
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# =========================================================
# 🧠 FUNÇÕES DE INTELIGÊNCIA (EPC, SENTIMENTO & AUDITORIA)
# =========================================================

def estimar_epc(score_conversao, ticket_medio=5000):
    """Calcula o EPC (Earnings Per Click) - Quanto cada clique vale para o hotel."""
    taxa_conv_est = (score_conversao / 100) * 0.02  # Média de mercado de 2% ajustada pelo score
    epc = taxa_conv_est * ticket_medio
    return round(epc, 2)

def analisar_sentimento_texto(texto):
    if not texto: return 0
    analysis = TextBlob(texto)
    return round((analysis.sentiment.polarity + 1) * 50, 2)

def realizar_auditoria_master(url):
    if not url.startswith('http'): url = 'https://' + url
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    start_time = time.time()
    
    try:
        r = requests.get(url, headers=headers, verify=False, timeout=15)
        load_time = time.time() - start_time
        html = r.text.lower()
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Pixels e Tags
        techs = {
            "GTM": "googletagmanager" in html,
            "Pixel Meta": "fbevents.js" in html or "://facebook.com" in html,
            "GA4": "gtag" in html or "ga4" in html
        }
        
        # Gatilhos de Venda
        gatilhos = ["oferta", "desconto", "promoção", "all inclusive", "reserva", "vip", "casamento"]
        score_venda = sum(15 for g in gatilhos if g in html)
        title = soup.title.string if soup.title else "Sem Título"

        return {
            "URL": url,
            "Velocidade (s)": round(load_time, 2),
            "Score Conversão": min(score_venda + 10, 100),
            "Sentimento de Marca": analisar_sentimento_texto(title),
            "Pixel Ativo": "Sim" if techs["Pixel Meta"] else "Não",
            "EPC Estimado (R$)": estimar_epc(min(score_venda + 10, 100))
        }
    except: return None

# =========================================================
# 🌐 INTERFACE STREAMLIT: GLOBAL REVENUE INTELLIGENCE
# =========================================================

with aba6:
    st.title("🚀 Global Revenue Intelligence Hub")
    st.write("Auditoria de Performance, Sentimento e **Potencial de Lucro por Clique (EPC)**.")

    # Parâmetros de Simulação
    with st.sidebar:
        st.subheader("⚙️ Configurações de ROI")
        ticket_simulacao = st.number_input("Ticket Médio do Pacote (R$):", value=5500)
        cpc_alvo = st.number_input("Custo por Clique Médio (R$):", value=2.50)

    urls_input = st.text_area("URLs para Auditoria (uma por linha):", 
                              "https://canabravaresort.com.br\nhttps://costadosauipe.com.br")

    if st.button("📡 Executar Auditoria 360º & Alertas"):
        urls = [u.strip() for u in urls_input.split("\n") if u.strip()]
        resultados = []

        for url in urls:
            with st.spinner(f"Analisando Big Data: {url}..."):
                res = realizar_auditoria_master(url)
                if res: 
                    # Atualiza EPC com o ticket da simulação
                    res["EPC Estimado (R$)"] = estimar_epc(res["Score Conversão"], ticket_simulacao)
                    resultados.append(res)

        if resultados:
            df_final = pd.DataFrame(resultados)

            # --- 🚨 ALERTAS DE ARBITRAGEM (QUEM ESTÁ GANHANDO DINHEIRO?) ---
            st.subheader("🚨 Alertas de Arbitragem Financeira")
            for _, row in df_final.iterrows():
                # Se o EPC for maior que o CPC, a campanha é lucrativa (ROI > 1)
                if row['EPC Estimado (R$)'] > cpc_alvo:
                    st.success(f"✅ **Oportunidade em `{row['URL']}`:** O EPC (R$ {row['EPC Estimado (R$)']}) é maior que o CPC. Esta estrutura de site suporta escala de anúncios lucrativa.")
                else:
                    st.error(f"⚠️ **Risco em `{row['URL']}`:** O EPC (R$ {row['EPC Estimado (R$)']}) é menor que o CPC de R$ {cpc_alvo}. Este site está perdendo dinheiro em anúncios agora.")

            # --- VISUALIZAÇÃO DE BI ---
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("💰 Potencial de Receita por Clique (EPC)")
                fig_epc = px.bar(df_final, x="URL", y="EPC Estimado (R$)", color="EPC Estimado (R$)", color_continuous_scale="Greens", text_auto=True)
                st.plotly_chart(fig_epc, use_container_width=True)
            
            with col2:
                st.subheader("❤️ Brand Sentiment vs Performance")
                fig_scat = px.scatter(df_final, x="Velocidade (s)", y="Sentimento de Marca", size="Score Conversão", color="URL", hover_name="URL")
                st.plotly_chart(fig_scat, use_container_width=True)

            # --- TABELA DE DADOS ---
            st.subheader("📋 Dashboard de Métricas Globais")
            st.dataframe(df_final, use_container_width=True)

            # --- ESPIONAGEM DE ADS ---
            st.divider()
            for url in urls:
                clean = url.replace("https://","").replace("www.","").split("/")[0]
                st.link_button(f"🔍 Ver Criativos Reais: {clean}", f"https://facebook.com{clean}&active_status=all&country=BR")

            st.success("Auditoria internacional concluída. Utilize o EPC para ajustar seus lances no Google Ads.")

# =============================
# 🤖 IA
# =============================
with aba7:
    df = previsao_receita(df)

    fig = px.line(df, y='forecast')
    st.plotly_chart(fig)

    insights = gerar_insights(df)

    for i in insights:
        st.write("👉", i)
