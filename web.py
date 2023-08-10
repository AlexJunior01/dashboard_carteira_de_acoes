import streamlit as st
from Scripts import telas
from Scripts import databaseFunctions
from Scripts import graficos
import yfinance as yf

@st.cache
def pegarCotacoes():
    temp = databaseFunctions.recuperarCarteiraAtual()
    codigos = temp["codigo"]
    cotacoes = []

    for codigo in codigos:
        codigo = codigo+'.SA'
        cota = yf.Ticker(codigo)
        ultima_cotacao = cota.history(period='day')["Close"]
        cotacoes.append(ultima_cotacao[0])

    temp['preco_atual'] = cotacoes
    temp['valor_total'] = temp['preco_atual'] * temp['quantidade']
    return temp



sidebar = st.sidebar
grafico = sidebar.selectbox(label='Opções',
                            options=['Carteira Atual', 'Proventos'])
negociacoes = databaseFunctions.recuperarNegociacao()
proventos = databaseFunctions.recuperarProvento()
carteira_atual = pegarCotacoes()


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

    grafico_carteira = graficos.graficoCarteiraAtual(carteira_atual)
    st.plotly_chart(grafico_carteira)

    if st.checkbox(label='See raw data'):
        st.write(carteira_atual)


