import streamlit as st
import sqlite3
from datetime import datetime
import csv


st.title('Gestao Entradas')
with open("visualizacao.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Função para atualizar o status no banco de dados e recriar o arquivo CSV
def atualizar_status(id, novo_status):
    conn = sqlite3.connect('novo.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE entrada SET Status=? WHERE ID=?", (novo_status, id))
    conn.commit()
    
    # Atualizar o arquivo CSV automaticamente
    csv_data = []
    cursor.execute("SELECT * FROM entrada")
    data = cursor.fetchall()
    for row in data:
        csv_data.append(row)
    
    with open(csv_filename, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(column_names)  # Escrever cabeçalho
        csv_writer.writerows(csv_data)  # Escrever dados
    
    conn.close()

# Conectar ao banco de dados
conn = sqlite3.connect('novo.db')
cursor = conn.cursor()

# Executar a consulta SQL para obter os dados da tabela 'frete'
cursor.execute("SELECT * FROM entrada")
data = cursor.fetchall()

# Obter os nomes das colunas
column_names = [description[0] for description in cursor.description]

# Fechar a conexão com o banco de dados
conn.close()

# Filtro por status
unique_statuses = list(set([row[column_names.index("Status")] for row in data]))
selected_status = st.selectbox("Filtrar por status:", ["Todos"] + unique_statuses)
filtered_data = data
if selected_status != "Todos":
    filtered_data = [row for row in filtered_data if row[column_names.index("Status")] == selected_status]

# Filtro por motivo
unique_motivo = list(set([row[column_names.index("motivo")] for row in data]))
selected_motivo = st.selectbox("Filtrar por Motivo:", ["Todos"] + unique_motivo)
if selected_motivo != "Todos":
    filtered_data = [row for row in filtered_data if row[column_names.index("motivo")] == selected_motivo]

# Filtro por data de entrada (mostrar apenas as entradas de hoje)
data_atual = datetime.now().strftime('%Y-%m-%d')
filtered_data = [row for row in filtered_data if row[column_names.index("data")] == data_atual]

# Atualizar o status selecionado
col1, col2 = st.columns(2)
with col1:
    selected_id = st.selectbox("Para atualizar selecione o ID:", [str(row[0]) for row in filtered_data])
with col2:
    novo_status = st.selectbox("Selecione o novo status:", ['Liberar Entrada', 'Descarregando', 'Carregando', 'Operacao Finalizada'])

if st.button('Atualizar'):
    atualizar_status(selected_id, novo_status)

# Criar uma tabela no Streamlit
table = "<style>tbody tr:nth-of-type(odd) {background-color: #f5f5f5;}</style>"
table += "<table><thead><tr>"
for col_name in column_names:
    table += f"<th>{col_name}</th>"
table += "</tr></thead><tbody>"

# Exibir os dados filtrados na tabela
for row in filtered_data:
    if row[column_names.index("Status")] == "Operacao Finalizada":
        table += "<tr style='background-color: green; color: white;'>"
    elif row[column_names.index("Status")] == "Liberar Entrada":
        table += "<tr style='background-color: yellow;'>"
    else:
        table += "<tr>"
    for value in row:
        table += f"<td>{value}</td>"
    table += "</tr>"
table += "</tbody></table>"

# Exibir a tabela no Streamlit
st.write(table, unsafe_allow_html=True)
