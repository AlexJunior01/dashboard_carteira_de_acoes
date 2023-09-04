import plotly.express as px


def cria_grafico_proventos(proventos):
    valor_por_mes = proventos.groupby('mes_pagamento')
    somas = valor_por_mes.sum()['valor_bruto']

    labels = {'codigo': 'Código',
              'data_pagamento': 'Data Pagamento',
              'valor_bruto': 'Valor pago R$',
              'tipo': 'Tipo',
              'mes_pagamento': 'Mês do Pagamento'}

    plot = px.bar(proventos, x='mes_pagamento', y='valor_bruto', color='codigo',
                  labels=labels, hover_data=['tipo'], width=800,
                  hover_name='codigo')

    for index, value in somas.items():
        plot.add_annotation(x=index, y=value,
                            text='{}'.format(round(value, 2)),
                            showarrow=False,
                            yshift=5)
    return plot


def cria_grafico_rendimento_por_ativo(rendimentos):
    labels = {'codigo': 'Código',
              'data_pagamento': 'Data Pagamento',
              'valor_bruto': 'Valor pago R$',
              'tipo': 'Tipo',
              'mes_pagamento': 'Mês do Pagamento'}

    plot = px.bar(rendimentos, x='codigo', y='valor_bruto', color='codigo', width=800,
                  height=400, labels=labels)
    plot.update_layout(barmode='stack', xaxis={'categoryorder':'total ascending'},
                       overwrite=True)

    return plot


def cria_grafico_carteira_atual_por_ativo(carteira_atual):
    plot_acoes = px.pie(data_frame=carteira_atual, names='codigo',
                        values='valor_total',
                        color_discrete_sequence=px.colors.cmocean.balance,
                        hover_name='codigo',
                        width=800, height=400)
    plot_acoes.update_traces(textfont={"size": 15}, overwrite=True)
    return plot_acoes


def cria_grafico_carteira_atual_por_tipo(carteira_atual):
    plot = px.pie(data_frame=carteira_atual, names='categoria',
                  values='valor_total',
                  color_discrete_sequence=px.colors.cmocean.balance)
    return plot
