import pandas as pd
import streamlit as st
import plotly.express as px
import datetime
# pylint: disable=E1120


def carregar_carteira_atual(caminho_do_arquivo):
  carteira_atual = pd.read_csv(caminho_do_arquivo)
  return carteira_atual

def carregar_rendimentos(caminho_do_arquivo):
  rendimentos = pd.read_csv(caminho_do_arquivo)
  rendimentos['data_pagamento'] = pd.to_datetime(rendimentos['data_pagamento'])
  return rendimentos




# Arquivos utilizados
rendimentos = carregar_rendimentos('datasets/rendimentos.csv')
carteira_atual = carregar_carteira_atual('datasets/carteira_cot.csv')


option = st.sidebar.selectbox(label='Opções',
                              options=['Carteira Atual', 'Rendimentos Mensais',
                                       'Crescimento Patrimonial'])


if option == 'Carteira Atual':
    labels_carteira_atual = {'codigo': 'Ativos',
                             'valor_total': 'Valor Aplicado',
                             'valor_atual': 'Saldo Bruto'}
    st.title(body='Carteira Atual')

    plot = px.pie(carteira_atual, names='codigo',
                  values='valor_atual', title='Carteira Atual',
                  labels=labels_carteira_atual,
                  color_discrete_sequence=px.colors.cmocean.balance,
                  hover_data=['valor_total'],
                  hover_name='codigo')
    st.plotly_chart(plot)

    if st.checkbox('Mostrar tabela'):
        carteira_atual

elif option == 'Rendimentos Mensais':
    st.title(body='Rendimentos Mensais')
    month = st.sidebar.slider('month', 1, 12, value=(3, 7))
    selecao = (rendimentos['data_pagamento'].dt.month >= month[0]) & (rendimentos['data_pagamento'].dt.month <= month[1])
    data_filtrada = rendimentos[selecao]
    label = {'ativo': 'Ativo',
            'data_pagamento': 'Data Pagamento',
            'total': 'Valor pago R$',
            'tipo': 'Tipo',
            'mes_pagamento': 'Mês do Pagamento'}

    plot = px.bar(data_filtrada, x='mes_pagamento', y='total', color='ativo',
                labels= label, hover_data=['tipo'], width=1000, hover_name='ativo',
                text='total')
    st.plotly_chart(plot)

    if st.checkbox('Mostrar tabela'):
        st.write(data_filtrada)

elif option == 'Crescimento Patrimonial':
    st.title(body='Crescimento Patrimonials')
    st.info('Esta funcionalidade está em produção')
