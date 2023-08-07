from Scripts import cei_scrap
from Scripts import manutencao_dados
import datetime

print('Atualizando...\nTempo estimado 20 segundos')

cei_scrap.buscando_carteira_atual()
cei_scrap.buscando_negociacoes()


manutencao_dados.crescimento_do_patrimonio()


data_atualizacao = datetime.date.today()
arq_data = open('data_atualizacao.txt', 'w')
arq_data.write(str(data_atualizacao))
arq_data.close()
print('Atualização finalizada')
