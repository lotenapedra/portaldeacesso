import streamlit as st
import requests
import sqlite3
import pandas as pd

st.set_page_config(page_title='Portal de Acesso',page_icon='clean.png')

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)



# Side bar menu
menu_option = st.sidebar.radio("Menu", ["Entrada", "Gestão de Entrada","Excluir Entrada","Solicitação de Embarque","Criar Usuário"])

if menu_option == "Entrada":
    exec(open("entrada.py").read())


# Resto do seu código...
if menu_option == "Excluir Entrada":
    exec(open("editar_excluir.py").read())
    
if menu_option == "Gestão de Entrada":
    exec(open("gestao_entrada.py").read())
    
if menu_option == "Solicitação de Embarque":
    exec(open("valid_user_frete.py").read())
    
if menu_option == "Criar Usuário":
    exec(open("loginadm.py").read())
        

if menu_option == "Cadastros":
    st.write("")
    
