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
carteira_atual = carregar_carteira_atual('datasets/carteira_atual.csv')


option = st.sidebar.selectbox(label='Opções',
                              options=['Carteira Atual', 'Rendimentos Mensais',
                                       'Crescimento Patrimonial'])


if option == 'Carteira Atual':
    st.title(body='Carteira Atual')
    tipo_carteira_atual = st.selectbox(label='Selecione',
                                       options=['Por ação', 'Por classe de ativo'])

    if tipo_carteira_atual == 'Por ação':
        plot_acoes = px.pie(data_frame=carteira_atual, names='Cód. de Negociação',
                            values='Valor (R$)',
                            color_discrete_sequence=px.colors.cmocean.balance,
                            hover_name='Cód. de Negociação')
        plot_acoes.update_traces(textfont={"size": 15}, overwrite=True)
        st.plotly_chart(plot_acoes)
    elif tipo_carteira_atual == 'Por classe de ativo':
        plot_classe = px.pie(data_frame=carteira_atual, names='Classe',
                             values='Valor (R$)',
                             color_discrete_sequence=px.colors.cmocean.balance)
        st.plotly_chart(plot_classe)

    if st.checkbox('Mostrar tabela'):
        carteira_atual

elif option == 'Rendimentos Mensais':
    st.title(body='Rendimentos Mensais')
    month = st.sidebar.slider('month', 1, 12, value=(3, 7))
    selecao = ((rendimentos['data_pagamento'].dt.month >= month[0]) &
              (rendimentos['data_pagamento'].dt.month <= month[1]))
    data_filtrada = rendimentos[selecao]
    label = {'ativo': 'Ativo',
            'data_pagamento': 'Data Pagamento',
            'total': 'Valor pago R$',
            'tipo': 'Tipo',
            'mes_pagamento': 'Mês do Pagamento'}

    plot_rend_mensal = px.bar(data_filtrada, x='mes_pagamento', y='total', color='ativo',
                labels= label, hover_data=['tipo'], width=800, hover_name='ativo',
                text='total')
    st.plotly_chart(plot_rend_mensal)

    plot = px.bar(rendimentos, x='ativo', y='total', color='ativo', width=400, height=400)
    plot.update_layout(barmode='stack', xaxis={'categoryorder':'total ascending'},
                       overwrite=True)
    st.plotly_chart(plot)

    if st.checkbox('Mostrar tabela'):
        st.write(data_filtrada)

elif option == 'Crescimento Patrimonial':
    st.title(body='Crescimento Patrimonials')
    st.info('Esta funcionalidade está em produção')
