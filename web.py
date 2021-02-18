import streamlit as st
from Scripts import telas
from Scripts import databaseFunctions
from Scripts import graficos


sidebar = st.sidebar
grafico = sidebar.selectbox(label='Opções',
                            options=['Carteira Atual', 'Proventos'])
negociacoes = databaseFunctions.recuperarNegociacao()
proventos = databaseFunctions.recuperarProvento()


if grafico == 'Proventos':
    st.title('Rendimentos Mensais')

    novo_provento = sidebar.button('Adicionar Provento')
    if novo_provento:
        telas.windowsAddProvento()

    excluir_provento = sidebar.number_input('Id do provento', value=0,
                                             step=1)
    btn_excluir_provento = sidebar.button('Excluir Provento')
    if btn_excluir_provento:
        telas.confirmarExclusaoProvento(excluir_provento)

    grafico_provento = graficos.graficoProventos(proventos)
    st.plotly_chart(grafico_provento)

    if st.checkbox(label='Saw raw data'):
        st.write(proventos)

elif grafico == 'Carteira Atual':
    st.title('Carteira Atual')

    nova_negociacao = sidebar.button('Adicionar Negociação')
    if nova_negociacao:
        telas.windowsAddNegociacao()

    input_excluir_negociacao = sidebar.number_input('Id da negociacao', value=0,
                                             step=1)
    btn_excluir_negociacao = sidebar.button('Excluir Negociacao')
    if btn_excluir_negociacao:
        teste = int(input_excluir_negociacao)
        telas.confirmarExclusaoNegociacao(teste)

    if st.checkbox(label='See raw data'):
        st.write(negociacoes)


