
# Dashboard Carteira de Investimento

## Conceito do projeto
Esta é uma aplicação para o monitoramento de carteira de investimentos, que possuam ativos em diversas corretoras,
em um único. Ela fornece uma visão geral da distribuição do portfólio, da receita recebida e do crescimento do patrimônio.

## Pré-requisitos e recursos utilizados
Para o desenvolvimento do dashboard foi utilizado Python e MySQL como tecnologias principais. Além de utilizar as
seguintes bibliotecas:

* `seaborn` e `plotly`: para criação dos gráficos;
* `yfinance`: para buscar as informações sobre os ativos;
* `pandas`: para organizar as informações recuperadas pelo script de webscrap;
* `streamlit`; para criação do Data App.

## Instalação e Execução
Para conseguir executar o projeto é preciso ter o Docker e docker-compose V2 instalados. Após instalar ambos é só executar
os comandos abaixo:

```shell
# Construi as imagens
docker compose build

# Inicia os serviçoes
docker compose up
```

Após esses comandos o serviço será iniciado, utilizando a porta 8051 para a aplicação e 3306 para o banco de dados MySQL.

OBS: Os comandos acima estão considerando a utilização do docker compose V2. Caso você tenha instalado primeira versão
é só utilizar os comando com `docker-compose ...` ao invés de `docker compose ...`.

## Funcionalidades
### Distribuição Atual da Carteira
A primeira funcionalidade do Dashboard é mostrar, de maneira simples e objetiva, a distribuição atual do portfólio de investimentos.
A distribuição é exibida por duas óticas distintas:

* **Por Ativo:** Apresenta a participação de cada ativo na sua carteira, oferecendo uma visão de onde estão concentradas suas maiores posições.
<img src="img/carteira_atual_por_acao.png">

* **Por Classe de Ativo:** Exibe a distribuição do portfólio por classes de ativo, auxiliando na melhor análise
da sua estratégia de investimento.
<img src="img/carteira_atual_por_classe.png">

### Rendimentos
Os rendimentos são um aspecto vital do investimento, especialmente para investidores de longo prazo que buscam um fluxo constante de renda passiva.
Para facilitar um monitoramento eficaz desses rendimentos, o Dashboard apresenta dois gráficos distintos.

O primeiro gráfico apresenta os rendimentos mensais, compilando a renda recebida a cada mês e fornecendo informações detalhadas
sobre cada desembolso, incluindo a data e a natureza da receita. O segundo gráfico agrega
os rendimentos de cada ativo, ilustrando os ganhos totais recebidos desde o momento da compra.

#### Rendimentos Mensais
<img src="img/rendimentos_mensais.png">

#### Rendimentos por Ativo
<img src="img/rendimentos_por_ativo.png">

### Crescimento do Patrimônio
Por fim, mas não menos importante, o gráfico de acumulação de patrimio oferece uma perspectiva concisa sobre seus **investimentos**
e seu **valor bruto** conforme eles evoluem ao longo do tempo.
<img src="img/crescimento_patrimonial.png">

## Autores

| Nome do Autor           | LinkedIn                                                   | GitHub                                          |
|-------------------------|------------------------------------------------------------|-------------------------------------------------|
| Alex Sandro Momi Junior | [Alex Junior](https://www.linkedin.com/in/alexmomijunior/) | [AlexJunior01](https://github.com/AlexJunior01) |
