import pandas as pd
import datetime
from pandas_datareader import data as web

def atualizar_cotacao(carteira_atual):
  carteira_cot = carteira_atual.copy()
  codigos = carteira_atual['codigo'].copy()
  end = datetime.date.today()
  start = end - datetime.timedelta(days=3)
  cotacoes = list()

  for codigo in codigos:
    codigo = codigo+'.SA'
    cotacao = web.DataReader(name=codigo, data_source='yahoo', start=start, end=end)['Close']
    cotacao = cotacao[-1]
    cotacoes.append(cotacao)

  carteira_cot['preco_atual'] = cotacoes
  carteira_cot['valor_atual'] = carteira_cot['quantidade']*carteira_cot['preco_atual']
  return carteira_cot

carteira_atual = pd.read_csv('datasets/carteira_atual.csv')
carteira_cot = atualizar_cotacao(carteira_atual)

carteira_cot.to_csv('datasets/carteira_cot.csv', index=False)
