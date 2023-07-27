import sqlite3
import csv
import streamlit as st
from datetime import date

with open("entrada.css", encoding='utf-8') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ... (Rest of your code remains the same)

# Obtém a lista de estados
estados = []
arquivo_csv = 'dados.csv'

with open(arquivo_csv, 'r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file, delimiter=';')
    for row in reader:
        if 'UF' in row:
            estado = row['UF']
            if estado not in estados:
                estados.append(estado)

# Função para obter os municípios de um estado específico
def obter_municipios(estado):
    municipios = []

    # Caminho para o arquivo CSV local
    arquivo_csv = 'dados.csv'

    with open(arquivo_csv, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            if 'UF' in row and row['UF'] == estado:
                municipios.append(row['Município'])

    return municipios

# Your form elements go here

# Add a button to trigger the form submission and validation
if st.button("Salvar"):
    # Perform validation
    if not (nome_completo and tipo_veiculo and motivo and placa and status_veiculo and empresa_origem and estado_origem and cidade_origem and telefone and frete_retono):
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
        data_value = data.strftime("%Y-%m-%d")
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
