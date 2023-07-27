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
            # Define uma variável de sessão para indicar que o usuário está logado
            st.session_state.is_logged_in = True
        else:
            st.error("Credenciais inválidas!")

# Tela intermediária para redirecionar após o login
def tela_intermediaria():
    if hasattr(st.session_state, 'is_logged_in') and st.session_state.is_logged_in:
        # Utilize o "components.html" para criar um elemento HTML com redirecionamento
        st.components.v1.html(
            """
            <script>
                window.location.href = "https://appdeaceapp-ufxe2nf7esptswcoubjwv6.streamlit.app/";
            </script>
            """
        )

# Executa a tela de login
tela_login()

# Executa a tela intermediária
tela_intermediaria()
