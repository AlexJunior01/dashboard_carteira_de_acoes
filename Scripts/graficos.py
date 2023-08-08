import plotly.express as px
import pandas as pd

def graficoProventos(proventos):
    labels = {'codigo': 'Código',
             'data_pagamento': 'Data Pagamento',
             'valor_bruto': 'Valor pago R$',
             'tipo': 'Tipo',
             'mes_pagamento': 'Mês do Pagamento'}

    plot = px.bar(proventos, x='mes_pagamento', y='valor_bruto', color='codigo',
                                 labels= labels, hover_data=['tipo'], width=800,
                                 hover_name='codigo')

    valor_por_mes = proventos.groupby('mes_pagamento')
    somas = valor_por_mes.sum()['valor_bruto']
    for index, value in  somas.items():
        plot.add_annotation(x=index, y=value,
                            text='{}'.format(round(value,2)),
                            showarrow=False,
                            yshift=5)
    return plot
