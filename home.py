import streamlit as st
import requests
import sqlite3
import pandas as pd





with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)




# Side bar menu
menu_option = st.sidebar.radio("Menu", ["Entrada", "Gestão de Entrada","Excluir Entrada","teste"])

if menu_option == "Entrada":
    exec(open("entrada.py").read())


# Resto do seu código...
if menu_option == "Excluir Entrada":
    exec(open("editar_excluir.py").read())
    
if menu_option == "Gestão de Entrada":
    exec(open("gestao_entrada.py").read())
if menu_option == "teste":
    exec(open("teste.py").read())
    

    
