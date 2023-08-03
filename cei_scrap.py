from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

# Login
# Instancia do WebDriver
driver = webdriver.Chrome('/home/alexjunior/Documentos/dashboard_acoes/chromedriver')

driver.get('https://cei.b3.com.br/CEI_Responsivo/')

# Selecionando campos
CPF = driver.find_element_by_name('ctl00$ContentPlaceHolder1$txtLogin')
senha = driver.find_element_by_name('ctl00$ContentPlaceHolder1$txtSenha')
botao_enviar = driver.find_element_by_name('ctl00$ContentPlaceHolder1$btnLogar')

# Enviando valores
driver.implicitly_wait(10)
CPF.send_keys('SEU CPF')
senha.send_keys('SUA SENHA')
botao_enviar.click()

# Passos até as tabelas
driver.find_element_by_id('ctl00_ContentPlaceHolder1_sectionCarteiraAtivos').click()
driver.find_element_by_id('ctl00_ContentPlaceHolder1_repTabelaAtivos_ctl04_LinkButton2').click()
time.sleep(5)

# Parse HTML
content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')
tables = soup.find_all('table', attrs={'class': 'Responsive'})
qtd_tabelas = len(tables)
tables = str(tables)

carteira_atual = pd.DataFrame()
for i in range(qtd_tabelas):
    df = pd.read_html(tables)[i]
    carteira_atual = pd.concat([carteira_atual, df.copy()], ignore_index=True)

carteira_atual.to_csv('datasets/carteira_atual.csv', index=False)
driver.quit()
