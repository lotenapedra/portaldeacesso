import streamlit as st
import sqlite3
from datetime import date, timedelta

st.title('Status de entradas')

# Função para inativar um registro no banco de dados
def inativar_registro(id):
    conn = sqlite3.connect('novo.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE entrada SET Status='Inativo' WHERE ID=?", (id,))
    conn.commit()
    conn.close()

# Função para atualizar o status de um registro no banco de dados
def atualizar_status(id, novo_status):
    conn = sqlite3.connect('novo.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE entrada SET Status=? WHERE ID=?", (novo_status, id))
    conn.commit()
    conn.close()

# Conectar ao banco de dados
conn = sqlite3.connect('novo.db')
cursor = conn.cursor()

# Criar componentes de seleção de data
start_date = st.date_input("Selecione a data de início:", date.today() - timedelta(days=30))
end_date = st.date_input("Selecione a data de término:", date.today())

# Executar a consulta SQL para obter os dados da tabela 'entrada' dentro do intervalo de datas selecionado
cursor.execute("SELECT * FROM entrada WHERE DATE(data) >= ? AND DATE(data) <= ?", (start_date, end_date))
data = cursor.fetchall()

# Obter os nomes das colunas
column_names = [description[0] for description in cursor.description]

# Filtros para Empresa de origem, Motivo e Local de entrada
local_entrada_filter = st.selectbox("Empresa de origem:", ["Todos"] + list(set(row[4] for row in data)))
motivo_filter = st.selectbox("Motivo da entrada:", ["Todos"] + list(set(row[5] for row in data)))
local_entrada_filter_2 = st.selectbox("Local de entrada:", ["Todos"] + list(set(row[15] for row in data)))

# Aplicar filtros
filtered_data = []
for row in data:
    if (local_entrada_filter == "Todos" or row[4] == local_entrada_filter) and \
       (motivo_filter == "Todos" or row[5] == motivo_filter) and \
       (local_entrada_filter_2 == "Todos" or (len(row) > 15 and row[15] == local_entrada_filter_2)):
        filtered_data.append(row)

# Criar uma tabela no Streamlit
table = "<style>tbody tr:nth-of-type(odd) {background-color: #f5f5f5;}</style>"
table += "<table><thead><tr>"
for col_name in column_names:
    table += f"<th>{col_name}</th>"
table += "</tr></thead><tbody>"

# Exibir os dados na tabela
for row in filtered_data:
    table += "<tr>"
    for value in row:
        table += f"<td>{value}</td>"
    table += "</tr>"
table += "</tbody></table>"

# Exibir a tabela no Streamlit
st.write(table, unsafe_allow_html=True)

# Seletor de ID para inativar
selected_id = st.selectbox("Para inativar, selecione o ID:", [str(row[0]) for row in filtered_data])
if st.button('Inativar'):
    inativar_registro(selected_id)

# Seletor de ID e status para atualizar
selected_id_update = st.selectbox("Selecione o ID para atualizar o status:", [str(row[0]) for row in filtered_data])
new_status = st.selectbox("Selecione o novo status:", ["Liberar Entrada", "Descarregando", "Carregando", "Carregamento Finalizado", "Descarregamento Finalizado"])

if st.button('Atualizar Status'):
    atualizar_status(selected_id_update, new_status)
    st.success(f"Status atualizado com sucesso para {new_status}")
