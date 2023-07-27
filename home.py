import streamlit as st
import requests
import sqlite3
import pandas as pd



with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)



#
# Side bar menu
menu_option = st.sidebar.radio("Menu", ["Entrada", "Excluir Entrada","Gestão de Entrada","Requesição de Frete","Criar Usuário"])

if menu_option == "Entrada":
    exec(open("entrada.py").read())

if menu_option == "Cadastros":
    st.write("")
# Resto do seu código...
if menu_option == "Excluir Entrada":
    exec(open("editar_excluir.py").read())
    
if menu_option == "Gestão de Entrada":
    exec(open("gestao_entrada.py").read())
    
if menu_option == "Requesição de Frete":
    exec(open("valid_user_frete.py").read())
    
if menu_option == "Criar Usuário":
    exec(open("loginadm.py").read())
        

if menu_option == "Cadastros":
    st.write("")
    
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}    