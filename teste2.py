import streamlit as st
import folium
from streamlit_folium import folium_static

def main():
    # Coordenadas das cidades
    curitiba_coords = (-25.4284, -49.2733)
    sao_jose_coords = (-25.5344, -49.2062)
    cotia_coords = (-23.605, -46.9186)

    # Criar o mapa
    m = folium.Map(location=curitiba_coords, zoom_start=10)

    # Adicionar marcadores para as cidades
    folium.Marker(location=curitiba_coords, popup='Curitiba').add_to(m)
    folium.Marker(location=sao_jose_coords, popup='São José dos Pinhais').add_to(m)
    folium.Marker(location=cotia_coords, popup='Cotia').add_to(m)

    # Exibir o mapa no Streamlit
    folium_static(m)

if __name__ == '__main__':
    main()
