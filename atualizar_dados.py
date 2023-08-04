from Scripts import cei_scrap
import datetime

print('Atualizando...\nTempo estimado 20 segundos')
cei_scrap.buscando_carteira_atual()
cei_scrap.buscando_negociacoes()

data_atualizacao = datetime.date.today()
arq_data = open('datasets/data_atualizacao.txt', 'w')
arq_data.write(str(data_atualizacao))
arq_data.close()
print('Atualização finalizada')
