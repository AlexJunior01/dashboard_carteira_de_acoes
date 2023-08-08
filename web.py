import streamlit as st
from Scripts import telas
from Scripts import databaseFunctions
from Scripts import graficos


sidebar = st.sidebar
nova_negociacao = sidebar.button('Adicionar Negociação')
novo_provento = sidebar.button('Adicionar Provento')


if nova_negociacao:
    telas.windowsAddNegociacao()

if novo_provento:
    telas.windowsAddProvento()


negociacoes = databaseFunctions.recuperarNegociacao()
proventos = databaseFunctions.recuperarProvento()


st.write('# Rendimentos Mensais')
grafico_provento = graficos.graficoProventos(proventos)
st.plotly_chart(grafico_provento)
