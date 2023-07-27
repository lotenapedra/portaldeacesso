import sqlite3
import streamlit as st

with open("master.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Função para verificar as credenciais de login
def verifica_login(usuario, senha):
    conn = sqlite3.connect('novo.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE user = ? AND senha = ?", (usuario, senha))
    resultado = cursor.fetchone()
    conn.close()
    return resultado

# Tela de login
def tela_login():
    st.title("Portal de Acesso")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("Login"):
        resultado = verifica_login(usuario, senha)
        if resultado:
            st.success("Login realizado com sucesso!")
            # Utilize o "empty" markdown para limpar o conteúdo atual da página
            st.markdown("", unsafe_allow_html=True)
            # Cria o link para a página desejada após o login
            st.markdown('<a href="https://appdeaceapp-ufxe2nf7esptswcoubjwv6.streamlit.app/" target="_self">Acesso ao sistema</a>', unsafe_allow_html=True)
        else:
            st.error("Credenciais inválidas!")

# Executa a tela de login
tela_login()
