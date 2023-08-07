from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time
from Scripts import manutencao_dados

# Configuracoes pdo driver
options = Options()
options.headless = True
options.add_argument("--window-size=1366,768")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-dev-shm-using")
options.add_argument("--remote-debugging-port=9222")

def login_CEI(driver):
    # Selecionando campos
    CPF = driver.find_element_by_name('ctl00$ContentPlaceHolder1$txtLogin')
    senha = driver.find_element_by_name('ctl00$ContentPlaceHolder1$txtSenha')
    botao_enviar = driver.find_element_by_name('ctl00$ContentPlaceHolder1$btnLogar')

    # Enviando valores
    CPF.send_keys('SEU CPF')
    senha.send_keys('SUA SENHA')
    botao_enviar.click()


def buscando_carteira_atual():
    # Instancia do WebDriver
    driver = webdriver.Chrome('./chromedriver', chrome_options=options)

    driver.get('https://cei.b3.com.br/CEI_Responsivo/')
    login_CEI(driver)
    driver.implicitly_wait(10)

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
    driver.quit()

    carteira_atual = manutencao_dados.ajuste_carteira_atual(carteira_atual)
    carteira_atual.to_csv('datasets/carteira_atual.csv', index=False)


def buscando_negociacoes():
    driver = webdriver.Chrome('./chromedriver', chrome_options=options)

    driver.get('https://cei.b3.com.br/CEI_Responsivo/')
    login_CEI(driver)
    driver.implicitly_wait(10)
    actions = ActionChains(driver)

    # Passos até as tabelas
    extratos = driver.find_element_by_xpath('//div[@id="nav"]/div/nav/section/ul/li[4]')
    actions.move_to_element(extratos).perform()

    negociacoes = driver.find_element_by_link_text('Negociação de ativos')
    actions.move_to_element(negociacoes)
    actions.click().perform()
    time.sleep(3)



    # quantidade de corretoras
    contas = Select(driver.find_element_by_id('ctl00_ContentPlaceHolder1_ddlAgentes'))
    qtd_options = len(contas.options)
    #Pegando as tabelas
    negociacao = pd.DataFrame()
    for i in range(1, qtd_options):
        contas = Select(driver.find_element_by_id('ctl00_ContentPlaceHolder1_ddlAgentes'))
        contas.select_by_index(i)
        time.sleep(2)

        consultar = driver.find_element_by_id('ctl00_ContentPlaceHolder1_btnConsultar')
        consultar.click()
        time.sleep(2)

        content = driver.page_source
        soup = BeautifulSoup(content, 'html.parser')

        table = soup.find('table', attrs={'class': 'responsive'})
        table = str(table)

        temp = pd.read_html(table)[0]
        negociacao = pd.concat([negociacao, temp])


        driver.find_element_by_id('ctl00_ContentPlaceHolder1_btnConsultar')
        time.sleep(2)
        driver.refresh()
    driver.quit()

    negociacao = manutencao_dados.ajuste_negociacoes(negociacao)
    negociacao.to_csv('datasets/negociacoes.csv', index=False)
