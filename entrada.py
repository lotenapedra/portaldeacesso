import sqlite3
import csv
import streamlit as st
from datetime import date

with open("entrada.css", encoding='utf-8') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ... (Rest of your code remains the same)

# Function to handle form submission and validation
def handle_submit():
    # Get form values
    nome_completo_value = nome_completo
    tipo_veiculo_value = tipo_veiculo
    motivo_value = motivo
    placa_value = placa
    status_veiculo_value = status_veiculo
    empresa_origem_value = empresa_origem
    estado_origem_value = estado_origem
    cidade_origem_value = cidade_origem
    telefone_value = telefone
    frete_retorno_value = frete_retono
    info_complementar_value = info

    # Perform validation
    if not (nome_completo_value and tipo_veiculo_value and motivo_value and placa_value and status_veiculo_value and empresa_origem_value and estado_origem_value and cidade_origem_value and telefone_value and frete_retorno_value):
        st.error("Por favor, preencha todos os campos obrigatórios antes de salvar.")
    else:
        # Connect to the database or create a new one if it doesn't exist
        conn = sqlite3.connect('novo.db')

        # Create a cursor object to execute SQL queries
        cursor = conn.cursor()

        # Create the 'entrada' table if it doesn't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS entrada (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            data TEXT,
                            estado_origem TEXT,
                            cidade_origem TEXT,
                            empresa_origem TEXT,
                            motivo TEXT,
                            tipo_veiculo TEXT,
                            frete_retorno TEXT,
                            status_veiculo TEXT,
                            placa TEXT,
                            nome_completo TEXT,
                            telefone TEXT,
                            info_complementar TEXT
                        )''')

        # Get the values from the fields
        data_value = date.today().strftime("%Y-%m-%d")
        estado_origem_value = estado_origem
        cidade_origem_value = cidade_origem
        empresa_origem_value = empresa_origem
        motivo_value = motivo
        tipo_veiculo_value = tipo_veiculo
        frete_retorno_value = frete_retono
        status_veiculo_value = status_veiculo
        placa_value = placa
        nome_completo_value = nome_completo
        telefone_value = telefone
        info_complementar_value = info

        # Insert the values into the 'entrada' table
        cursor.execute('''INSERT INTO entrada (
                            data,
                            estado_origem,
                            cidade_origem,
                            empresa_origem,
                            motivo,
                            tipo_veiculo,
                            frete_retorno,
                            status_veiculo,
                            placa,
                            nome_completo,
                            telefone,
                            info_complementar
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (
                           data_value,
                           estado_origem_value,
                           cidade_origem_value,
                           empresa_origem_value,
                           motivo_value,
                           tipo_veiculo_value,
                           frete_retorno_value,
                           status_veiculo_value,
                           placa_value,
                           nome_completo_value,
                           telefone_value,
                           info_complementar_value
                       ))

        # Commit the changes and close the connection
        conn.commit()
        conn.close()
        st.success("Dados salvos com sucesso!")

# Call the handle_submit function when the button is clicked
if st.button("Salvar"):
    handle_submit()
