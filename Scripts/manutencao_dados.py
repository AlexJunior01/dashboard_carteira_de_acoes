import pandas as pd

# Script ajusta os dados após retirados do CEI
def ajuste_carteira_atual(carteira_atual):
    # Tirandos valores nulos do dataset
    carteira_atual.dropna(inplace=True)
    carteira_atual.index = range(carteira_atual.shape[0])

    # Ajustando valores da tabela
    carteira_atual['Preço (R$)*'] = carteira_atual['Preço (R$)*']/100
    carteira_atual['Valor (R$)'] = carteira_atual['Preço (R$)*']*carteira_atual['Qtde.']


    # Criação do atributo Classe
    classe = list()
    for acao in carteira_atual['Tipo']:
        if 'CI' in acao:
            classe.append('Fundo Imobiliário')
        else:
            classe.append('Ação')
    carteira_atual['Classe'] = classe
    return carteira_atual


def ajuste_negociacoes(negociacoes):
    negociacoes['Preço (R$)'] = negociacoes['Preço (R$)']/100
    negociacoes['Valor Total(R$)'] = negociacoes['Preço (R$)'] * negociacoes['Quantidade']
    negociacoes.dropna(axis='rows', subset=['Quantidade'], inplace=True)

    negociacoes['Data do Negócio'] = pd.to_datetime(negociacoes['Data do Negócio'], format='%d/%m/%Y')

    negociacoes.sort_values(by='Data do Negócio', inplace=True)
    negociacoes.index = range(negociacoes.shape[0])

    return negociacoes
