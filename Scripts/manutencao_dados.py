import pandas as pd
from pandas_datareader import data as web

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
    # Ajustando casas decimais dos valores
    negociacoes['Preço (R$)'] = negociacoes['Preço (R$)']/100
    negociacoes['Valor Total(R$)'] = negociacoes['Preço (R$)'] * negociacoes['Quantidade']

    # Tirando linha nula
    negociacoes.dropna(axis='rows', subset=['Quantidade'], inplace=True)

    # Convertendo para datetime
    negociacoes['Data do Negócio'] = pd.to_datetime(negociacoes['Data do Negócio'], format='%d/%m/%Y')

    # Ordenando pela data e resetando o index
    negociacoes.sort_values(by='Data do Negócio', inplace=True)
    negociacoes.index = range(negociacoes.shape[0])

    # Agrupando os ativos do mercado fracionário
    codigos = negociacoes['Código Negociação']
    codigos_agrupados = list()

    for codigo in codigos:
        if codigo.endswith('F'):
            codigo = codigo[:-1]
        codigos_agrupados.append(codigo)
    negociacoes['Código Negociação'] = codigos_agrupados

    return negociacoes


# Pegar cotações até o dia atual
def pegar_cotacoes(codigos, data_atualizacao):
    # Pegar cotações no Yahoo Finance
    cotacoes = dict()
    for codigo in codigos:
        cotacoes[codigo] = 0

    for codigo in codigos:
        cotacao = web.DataReader(name=codigo+'.SA', data_source='yahoo', start=data_atualizacao)['Close']
        cotacoes[codigo] = cotacao.copy()

    df_cotacoes = pd.DataFrame(cotacoes)
    df_cotacoes.fillna(method='ffill', axis='rows', inplace=True)
    return df_cotacoes



def crescimento_do_patrimonio():
    try:
        arq = open('datasets/data_atualizacao.txt', 'r')
    except FileNotFoundError:
        data_inicio_da_carteira()
        crescimento_do_patrimonio()

    # Data da ultima atualização
    data_atualizacao = arq.read()
    arq.close()

    # Pegar códigos que possui
    negociacoes = pd.read_csv('datasets/negociacoes.csv')
    codigos = negociacoes['Código Negociação'].unique()

    # Pegando cotações atuais
    cotacoes = pegar_cotacoes(codigos, data_atualizacao)
    #cotacoes.to_csv('datasets/cotacoes.csv', index=False)

    data_negocios = cotacoes.index

    qtd_cotas = quantidade_cotas(codigos, data_negocios, negociacoes)
    valor_aplicado = pegar_valor_aplicado(data_negocios, negociacoes)

    patrimonio = qtd_cotas * cotacoes
    patrimonio['Total'] = patrimonio.sum(axis='columns')
    patrimonio['Valor Aplicado'] = valor_aplicado

    patrimonio.to_csv('datasets/crescimento_patrimonio.csv')



def quantidade_cotas(codigos, data_negocios, negociacoes):
    qtd_cotas = dict()
    for codigo in codigos:
        qtd_cotas[codigo] = 0

    colunas = ['Data do Negócio', 'Compra/Venda', 'Quantidade']

    for codigo in codigos:
        # Series que irá guarda as quantidades
        data = pd.Series(index=data_negocios)

        # Negociações com um código
        selecao = negociacoes['Código Negociação'] == codigo
        df = negociacoes[selecao][colunas]

        # Preparação para fazer as operações acumulativas
        df.index = range(df.shape[0])
        primeira_negociacao = pd.to_datetime(df.iloc[0, 0])
        data.fillna({primeira_negociacao: 0}, inplace=True)
        data_anterior = primeira_negociacao

        for linha in df.values:
            if linha[1] == 'C':
                data[linha[0]] = data[data_anterior] + linha[2]
            else:
                data[linha[0]] = data[data_anterior] - linha[2]

            data_anterior = linha[0]
        qtd_cotas[codigo] = data.copy()

    df_cotas = pd.DataFrame(qtd_cotas)
    df_cotas.fillna(method='ffill', axis='rows', inplace=True)
    df_cotas.fillna(0, inplace=True)
    return df_cotas


def pegar_valor_aplicado(data_negocios, negociacoes):
    colunas = ['Data do Negócio', 'Compra/Venda', 'Valor Total(R$)']

    valor_aplicado = pd.Series(index=data_negocios)
    valor_aplicado['2020-02-17'] = 0
    data_anterior = '2020-02-17'
    for linha in negociacoes[colunas].values:
        if linha[1] == 'C':
            valor_aplicado[linha[0]] = valor_aplicado[data_anterior] + linha[2]
        else:
            valor_aplicado[linha[0]] = valor_aplicado[data_anterior] - linha[2]
        data_anterior = linha[0]

    valor_aplicado.fillna(method='ffill', inplace=True)
    return valor_aplicado



def data_inicio_da_carteira():
    negociacoes = pd.read_csv('datasets/negociacoes.csv')
    data_atualizacao = negociacoes['Data do Negócio']
    data_atualizacao = data_atualizacao[0]

    arq = open('datasets/data_atualizacao.txt', 'w')
    arq.write(data_atualizacao)
    arq.close()


