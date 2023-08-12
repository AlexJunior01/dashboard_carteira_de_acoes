import pandas as pd
import streamlit as st
import plotly.express as px
import datetime
import plotly.graph_objects as go
# pylint: disable=E1120

# Carregamento dos Dados
@st.cache
def carregar_carteira_atual(caminho_do_arquivo):
  carteira_atual = pd.read_csv(caminho_do_arquivo)
  return carteira_atual


@st.cache
def carregar_rendimentos(caminho_do_arquivo):
  rendimentos = pd.read_csv(caminho_do_arquivo)
  rendimentos['data_pagamento'] = pd.to_datetime(rendimentos['data_pagamento'])
  return rendimentos


@st.cache
def carregar_patrimonio(caminho_do_arquivo):
    patrimonio = pd.read_csv(caminho_do_arquivo)
    return patrimonio


def ultima_atualizacao():
    with open('data_atualizacao.in', 'r') as arq_data:
        data_atualizacao = arq_data.readline().strip()
        data_atualizacao = datetime.datetime.strptime(data_atualizacao, '%Y-%m-%d')
    return data_atualizacao


# Gráficos
def grafico_carteira_atual_por_acao(carteira_atual):
    plot_acoes = px.pie(data_frame=carteira_atual, names='Cód. de Negociação',
                            values='Valor (R$)',
                            color_discrete_sequence=px.colors.cmocean.balance,
                            hover_name='Cód. de Negociação',
                            width=800, height=400)
    plot_acoes.update_traces(textfont={"size": 15}, overwrite=True)
    return plot_acoes


def grafico_carteira_atual_por_tipo(carteira_atual):
    plot = px.pie(data_frame=carteira_atual, names='Classe',
                             values='Valor (R$)',
                             color_discrete_sequence=px.colors.cmocean.balance)
    return plot


def grafico_rendimento_mensal(rendimentos, label):
    plot = px.bar(data_filtrada, x='mes_pagamento', y='total', color='ativo',
                                 labels= label, hover_data=['tipo'], width=800,
                                 hover_name='ativo',
                                 text='total')

    return plot


def grafico_rendimento_por_ativo(rendimentos, label):
    plot = px.bar(rendimentos, x='ativo', y='total', color='ativo', width=800,
                  height=400, labels=label)
    plot.update_layout(barmode='stack', xaxis={'categoryorder':'total ascending'},
                       overwrite=True)

    return plot


def grafico_crescimento_patrimonial(patrimonio):
    fig = go.Figure(go.Scatter(x=patrimonio['Date'],
                          y=patrimonio['Valor Aplicado'],
                          name='Valor Aplicado',
                          line_shape='spline',
                          fill='tozeroy'))

    fig.add_trace(go.Scatter(x=patrimonio['Date'],
                             y=patrimonio['Total'],
                             name='Total',
                             line_shape='spline',
                             fill='tozeroy'))

    fig.update_xaxes(rangeslider_visible=True)
    fig.update_xaxes(rangeselector=dict(
                        buttons=list([
                            dict(count=1, label="1m", step="month", stepmode="backward"),
                            dict(count=3, label='3m', step='month', stepmode='backward'),
                            dict(count=1, label="1y", step="year", stepmode="backward"),
                            dict(step="all")
                        ])
                    )
    )
    fig.update_layout({'height': 600, 'width': 900})

    return fig




# Arquivos utilizados
data_atualizacao = ultima_atualizacao()
rendimentos = carregar_rendimentos('datasets/rendimentos.csv')
carteira_atual = carregar_carteira_atual('datasets/carteira_atual.csv')
patrimonio = carregar_patrimonio('datasets/crescimento_patrimonio.csv')


option = st.sidebar.selectbox(label='Opções',
                              options=['Carteira Atual', 'Rendimentos Mensais',
                                       'Crescimento Patrimonial'])

st.write('**Ultima Atualização:**{}'.format(data_atualizacao.strftime('%d/%m/%Y')))


if option == 'Carteira Atual':
    st.title(body='Carteira Atual')
    # Selecionar gráfico
    tipo_carteira_atual = st.selectbox(label='Selecione',
                                       options=['Por ação', 'Por classe de ativo'])

    # Por ativo
    if tipo_carteira_atual == 'Por ação':
        plot_acoes = grafico_carteira_atual_por_acao(carteira_atual)
        st.plotly_chart(plot_acoes)

    # Por classe de ativo
    elif tipo_carteira_atual == 'Por classe de ativo':
        plot_classe = grafico_carteira_atual_por_tipo(carteira_atual)
        st.plotly_chart(plot_classe)

    if st.checkbox('Mostrar tabela'):
        carteira_atual

elif option == 'Rendimentos Mensais':
    st.title(body='Rendimentos Mensais')

    # Slider dos rendimentos
    month = st.sidebar.slider('month', 1, 12, value=(3, 7))
    selecao = ((rendimentos['data_pagamento'].dt.month >= month[0]) &
              (rendimentos['data_pagamento'].dt.month <= month[1]))
    data_filtrada = rendimentos[selecao]

    # Labels dos gráficos que serão exibidos
    label = {'ativo': 'Ativo',
             'data_pagamento': 'Data Pagamento',
             'total': 'Valor pago R$',
             'tipo': 'Tipo',
             'mes_pagamento': 'Mês do Pagamento'}

    # Rendimento mensal
    plot_rend_mensal = grafico_rendimento_mensal(rendimentos, label)
    st.plotly_chart(plot_rend_mensal)

    # Rendimento por ativo
    st.title('Rendimentos por Ativo')
    plot = grafico_rendimento_por_ativo(rendimentos, label)
    st.plotly_chart(plot)

    if st.checkbox('Mostrar tabela'):
        st.write(data_filtrada)

elif option == 'Crescimento Patrimonial':
    st.title(body='Crescimento Patrimonial')

    fig = grafico_crescimento_patrimonial(patrimonio)
    st.plotly_chart(fig)
