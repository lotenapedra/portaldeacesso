import streamlit as st
import sqlite3
from datetime import datetime

# Function to update the status in the database
def atualizar_status(selected_id, novo_status):
    conn = sqlite3.connect('novo.db')
    cursor = conn.cursor()
    update_query = "UPDATE entrada SET Status = ? WHERE ID = ?"
    cursor.execute(update_query, (novo_status, selected_id))
    conn.commit()
    conn.close()

st.title('Gestao Entradas')
with open("visualizacao.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

conn = sqlite3.connect('novo.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM entrada")
data = cursor.fetchall()
column_names = [description[0] for description in cursor.description]
conn.close()

unique_statuses = list(set([row[column_names.index("Status")] for row in data]))
selected_status = st.selectbox("Filtrar por status:", ["Todos"] + unique_statuses)
filtered_data = data
if selected_status != "Todos":
    filtered_data = [row for row in filtered_data if row[column_names.index("Status")] == selected_status]

unique_motivo = list(set([row[column_names.index("motivo")] for row in data]))
selected_motivo = st.selectbox("Filtrar por Motivo:", ["Todos"] + unique_motivo)
if selected_motivo != "Todos":
    filtered_data = [row for row in filtered_data if row[column_names.index("motivo")] == selected_motivo]

data_atual = datetime.now().strftime('%Y-%m-%d')
filtered_data = [row for row in filtered_data if row[column_names.index("data")] == data_atual]

col1, col2 = st.columns(2)
with col1:
    selected_id = st.selectbox("Para atualizar selecione o ID:", [str(row[0]) for row in filtered_data])
with col2:
    novo_status = st.selectbox("Selecione o novo status:", ['Liberar Entrada', 'Descarregando', 'Carregando', 'Operacao Finalizada'])

if st.button('Atualizar'):
    atualizar_status(selected_id, novo_status)

table = "<style>tbody tr:nth-of-type(odd) {background-color: #f5f5f5;}</style>"
table += "<table><thead><tr>"
for col_name in column_names:
    table += f"<th>{col_name}</th>"
table += "</tr></thead><tbody>"

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
############################################################################
import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# Resto do seu código...

# Create a DataFrame from the filtered_data
df = pd.DataFrame(filtered_data, columns=column_names)

# Display the DataFrame in Streamlit
st.write(df)

# Allow user to generate a CSV URL
csv_url = get_csv_url(df)
st.write("CSV URL:", csv_url)

# Move the "Atualizar" button code here
selected_id = st.selectbox("Para atualizar selecione o ID:", [str(row[0]) for row in filtered_data])
novo_status = st.selectbox("Selecione o novo status:", ['Liberar Entrada', 'Descarregando', 'Carregando', 'Operacao Finalizada'])

if st.button('Atualizar'):
    atualizar_status(selected_id, novo_status)

import base64

def get_csv_url(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    csv_url = f"data:text/csv;charset=utf-8;base64,{b64}"
    return csv_url


####




st.write(table, unsafe_allow_html=True)

