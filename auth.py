import streamlit as st

USERS = {
    "hotel1": {"senha": "123", "empresa": "Hotel Cana Brava"},
    "empresa2": {"senha": "123", "empresa": "Empresa Transporte"}
}

def login():
    st.sidebar.title("🔐 Login")

    user = st.sidebar.text_input("Usuário")
    senha = st.sidebar.text_input("Senha", type="password")

    if st.sidebar.button("Entrar"):
        if user in USERS and USERS[user]["senha"] == senha:
            st.session_state["logado"] = True
            st.session_state["empresa"] = USERS[user]["empresa"]
        else:
            st.error("Login inválido")

    return st.session_state.get("logado", False)
