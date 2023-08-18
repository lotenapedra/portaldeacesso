import sqlite3
import csv
import streamlit as st
from datetime import date

#arquivo css para estilização

with open("entrada.css") as f:
    st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)

st.title("Incluir Entrada")



# data de entrada não pode ser alterada!
data = st.date_input("Data Entrada", value=date.today(), disabled=True)
Local_Entrada = st.selectbox('Local de entrada', ['Clean Plastic', 'Clean Poa', 'Clean Jundiai', 'Clean Bottle', 'Clean Fortal', 'Raposo Plasticos', 'Raposo Minas', 'Fornecedor PF', 'Outro'])

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

col1, col2 = st.columns(2)
with col1:
    nome_completo = st.text_input("Nome Completo:")
    tipo_veiculo = st.selectbox('Tipo de Veiculo:', ["Truck-Side", "Carreta-Side", "Truck-Grade Baixa", "Carreta-Grade Baixa", "Carreta Graneleira", "Container","Bitrem","Bitruck"])
    motivo = st.selectbox('Motivo:', ['Carregar', 'Descarregar'])
    
    placa = st.text_input('Placa do Veiculo:')
    status_veiculo = st.selectbox('Status Veiculo',['Proprio','Terceiro','Transportadora'])

with col2:
    empresa_origem = st.selectbox('Empresa Origem', ['Clean Plastic', 'Clean Poa', 'Clean Jundiai', 'Clean Bottle', 'Clean Fortal', 'Raposo Plasticos', 'Raposo Minas', 'Fornecedor PF', 'Outro'])
    estado_origem = st.selectbox('Selecione o estado de origem', estados)
    municipios_origem = obter_municipios(estado_origem)
    cidade_origem = st.selectbox('Selecione a cidade de origem', municipios_origem)
    telefone = st.text_input('Telefone')
    frete_retono = st.selectbox('Possuem Frete Retorno?', ['Sim', 'Nao'])

info = st.text_area('Info. Complementar')

def is_form_valid():
    required_fields = [
        data,
        nome_completo,
        tipo_veiculo,
        motivo,
        placa,
        empresa_origem,
        estado_origem,
        cidade_origem,
        telefone,
        frete_retono,
    ]

    for field in required_fields:
        if not field:
            return False

    return True

if st.button("Salvar"):
    if is_form_valid():
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
    else:
        st.warning("Preencha todos os campos antes de salvar.")

import requests
import csv

def save_to_github_csv(data_row):
    csv_url = "https://raw.githubusercontent.com/lotenapedra/portaldeacesso/main/dados_exportados.csv"
    
    response = requests.get(csv_url)
    response.raise_for_status()
    
    # Convert the content into a list of lists (rows)
    existing_data = [line.split(',') for line in response.text.strip().split('\n')]
    
    existing_data.append(data_row)
    
    # Convert the updated data back into CSV format
    updated_csv_content = "\n".join([",".join(row) for row in existing_data])
    
    # Update the remote CSV file using the GitHub API
    headers = {
        "Authorization": "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",
        "Content-Type": "application/vnd.github.v3.raw"
    }
    
    response = requests.put(csv_url, data=updated_csv_content, headers=headers)
    response.raise_for_status()

# ... (rest of your code)

if st.button("Salvar"):
    if is_form_valid():
        # Connect to the database or create a new one if it doesn't exist
        conn = sqlite3.connect('novo.db')

        # ... (existing code)

        # Commit the changes and close the connection
        conn.commit()
        conn.close()
        

        # Call the function to save the data to the remote GitHub CSV file
        data_row = [
            data_value, estado_origem_value, cidade_origem_value, empresa_origem_value, 
            motivo_value, tipo_veiculo_value, frete_retorno_value, status_veiculo_value, 
            placa_value, nome_completo_value, telefone_value, info_complementar_value
        ]
        save_to_github_csv(data_row)
    else:
       



