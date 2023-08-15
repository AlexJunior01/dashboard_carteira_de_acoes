import streamlit as st
import yfinance as yf

from Scripts.database import (
    recuperar_negociacao,
    recuperar_provento,
    recuperar_carteira_atual
)

from Scripts import telas, graficos

@st.cache
def pegar_cotacoes():
    temp = recuperar_carteira_atual()
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
grafico = sidebar.selectbox(label='Opções', options=['Carteira Atual', 'Proventos'])
negociacoes = recuperar_negociacao()
proventos = recuperar_provento()
carteira_atual = pegar_cotacoes()


if grafico == 'Proventos':
    st.title('Rendimentos Mensais')

    novo_provento = sidebar.button('Adicionar Provento')
    if novo_provento:
        telas.windows_add_provento()

    excluir_provento = sidebar.number_input('Id do provento', value=0,
                                             step=1)
    btn_excluir_provento = sidebar.button('Excluir Provento')
    if btn_excluir_provento:
        telas.confirmar_exclusao_provento(excluir_provento)

    grafico_provento = graficos.grafico_proventos(proventos)
    st.plotly_chart(grafico_provento)

    if st.checkbox(label='Saw raw data'):
        st.write(proventos)

elif grafico == 'Carteira Atual':
    st.title('Carteira Atual')

    nova_negociacao = sidebar.button('Adicionar Negociação')
    if nova_negociacao:
        telas.windows_add_negociacao()

    input_excluir_negociacao = sidebar.number_input('Id da negociacao', value=0,
                                             step=1)
    btn_excluir_negociacao = sidebar.button('Excluir Negociacao')
    if btn_excluir_negociacao:
        teste = int(input_excluir_negociacao)
        telas.confirmar_exclusao_negociacao(teste)

    grafico_carteira = graficos.grafico_carteira_atual(carteira_atual)
    st.plotly_chart(grafico_carteira)

    if st.checkbox(label='See raw data'):
        st.write(carteira_atual)


