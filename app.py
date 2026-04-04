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
from pdf_report import gerar_pdf

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
    relatorio_ia = gerar_relatorio_ia(df_sites)

st.text_area("Relatório IA", relatorio_ia, height=300)

st.markdown("## 📱 Análise de Instagram")

insta_url = st.text_input("Digite URL do Instagram")

if insta_url:
    try:
        r = requests.get(insta_url, verify=False)
        soup = BeautifulSoup(r.text, 'html.parser')

        title = soup.title.string if soup.title else ""

        st.write("Perfil:", title)

        if "followers" in r.text:
            st.success("Perfil com presença ativa")

        st.info("💡 Recomendações:")
        st.write("- Melhorar frequência de posts")
        st.write("- Usar mais vídeos (Reels)")
        st.write("- Criar campanhas de tráfego")

    except:
        st.error("Erro ao analisar Instagram")

if st.button("📄 Gerar PDF Executivo"):
    gerar_pdf(relatorio_ia)

    with open("relatorio.pdf", "rb") as f:
        st.download_button("⬇️ Baixar PDF", f, file_name="relatorio.pdf")
    st.markdown("## 🌐 Diagnóstico Inteligente de Sites (Nível Consultoria)")

    urls_input = st.text_area("Digite URLs (uma por linha)")

    if urls_input:
        urls = urls_input.split("\n")

        resultados = []

        for url in urls:
            try:
                r = requests.get(url.strip(), verify=False, timeout=10)
                r.encoding = 'utf-8'
                soup = BeautifulSoup(r.text, 'html.parser')

                title = soup.title.string if soup.title else ""
                description = soup.find("meta", attrs={"name": "description"})
                description = description["content"] if description else ""

                h1 = soup.find_all("h1")

                scripts = [s.get("src") for s in soup.find_all("script") if s.get("src")]
                usa_google = any("google" in str(s) for s in scripts)
                usa_meta = any("facebook" in str(s) for s in scripts)

                tamanho = len(r.content) / 1024

                # =========================
                # 🎯 SCORE
                # =========================
                score = 0

                if title: score += 20
                if description: score += 20
                if len(h1) > 0: score += 20
                if usa_google: score += 15
                if usa_meta: score += 15
                if tamanho < 2000: score += 10

                resultados.append({
                    "url": url,
                    "score": score,
                    "titulo": title,
                    "description": description,
                    "performance_kb": round(tamanho,2),
                    "google": usa_google,
                    "meta": usa_meta
                })

            except:
                st.error(f"Erro em: {url}")

        df_sites = pd.DataFrame(resultados)

        # =========================
        # 📊 COMPARAÇÃO
        # =========================
        st.markdown("## 📊 Benchmark de Concorrentes")

        st.dataframe(df_sites)

        fig = px.bar(df_sites, x='url', y='score', color='score')
        st.plotly_chart(fig, use_container_width=True)

        # =========================
        # 🧠 DIAGNÓSTICO AUTOMÁTICO
        # =========================
        melhor = df_sites.sort_values("score", ascending=False).iloc[0]
        pior = df_sites.sort_values("score").iloc[0]

        st.markdown("## 🧠 Diagnóstico Estratégico")

        st.write(f"🏆 Melhor site: {melhor['url']} (Score {melhor['score']})")
        st.write(f"⚠️ Pior site: {pior['url']} (Score {pior['score']})")

        if pior['score'] < 60:
            st.error("Site com alto risco de baixa conversão")

        # =========================
        # 💰 RELATÓRIO EXECUTIVO
        # =========================
        def gerar_relatorio_ia(df_sites):
    melhor = df_sites.sort_values("score", ascending=False).iloc[0]
    pior = df_sites.sort_values("score").iloc[0]

    crescimento = ((melhor['score'] - pior['score']) / max(pior['score'],1)) * 100

    relatorio = f"""
    RELATÓRIO ESTRATÉGICO DE PRESENÇA DIGITAL

    1. VISÃO GERAL
    Foi realizada uma análise comparativa entre os sites avaliados.
    O melhor desempenho foi identificado em {melhor['url']} com score {melhor['score']}.
    O pior desempenho foi identificado em {pior['url']} com score {pior['score']}.

    2. DIAGNÓSTICO
    Foram identificados gargalos críticos:
    - Baixa otimização de SEO
    - Falta de rastreamento de marketing
    - Performance técnica abaixo do ideal

    3. IMPACTO NO NEGÓCIO
    Esses problemas impactam diretamente:
    - Aumento do CAC
    - Redução da taxa de conversão
    - Perda de receita potencial

    4. OPORTUNIDADE
    Com otimização adequada, é possível um ganho estimado de até {round(crescimento,2)}% em performance digital.

    5. RECOMENDAÇÕES
    - Implementar tracking (Google + Meta)
    - Otimizar velocidade do site
    - Melhorar SEO
    - Criar páginas de conversão

    6. CONCLUSÃO
    Existe uma oportunidade clara de crescimento com impacto direto no faturamento.
    """

    return relatorio
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
