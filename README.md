[![author](https://img.shields.io/badge/author-AlexJunior-yellow.svg)](https://www.linkedin.com/in/alex-sandro-momi-junior-382bb8157/) [![](https://img.shields.io/badge/python-3.6-yellow.svg)](https://www.python.org/downloads/release/python-365/) [![GPLv3 license](https://img.shields.io/badge/License-GPLv3-yellow.svg)](http://perso.crans.org/besson/LICENSE.html)

# AVISO:
    Documentação desatualizada, irei atualizar assim que a nova versão com MySQL estiver completa.

# Dashboard de carteira de investimentos
Para possuir um melhor entendimento sobre a situação dos meus investimentos e poder tomar decisões mais assertivas elaborei o Dashboard. O Dashboard consiste em uma plataforma para acompanhar minha carteira de investimentos, que possui ativos em diversas corretoras, em um lugar só, disponibilizando uma visão geral da distribuição da carteira, rendimentos recebidos e do crescimento patrimonial.

## Funcionalidades:
### Distribuição atual da carteira
A primeira função do Dashboard é mostrar de forma simples e objetiva a atual distribuição da carteira de investimentos. Ele mostra a distribuição de duas óticas diferentes:

* **Por ativo:** demostrando a participação de cada ativo em sua carteira, proporcionando uma visão de onde estão concentradas suas maiores posições.
<img src="img/carteira_atual_por_acao.png">

* **Por classe de ativo:** demonstra a distribuição da carteira entre as classes de ativos, possibilitando uma melhor análise da sua estratégia de investimento como, método do 80 ou dividindo em quatro classes de ativos, entre outras.
<img src="img/carteira_atual_por_classe.png">

### Rendimentos
Uma das principais partes de investir, principalmente para quem investe no longo prazo para possuir uma renda passiva, são os rendimentos provisionados pelos ativos. Para proporcionar um bom acompanhamento sobre eles o Dashboard possui dois gráficos.

O primeiro é dos rendimentos mensais, que agrupa os rendimentos recebidos por mês e mostra informações sobre cada pagamento, como a data e o tipo de provento. O segundo agrupa os rendimentos por cada ativo mostrando o total recebido desde a sua aquisição.

#### Rendimentos mensais
<img src="img/rendimentos_mensais.png">

#### Rendimentos por ativos
<img src="img/rendimentos_por_ativo.png">


### Crescimento patrimonial
Por último mas não menos importante, o crescimento patrimonial, mostra uma visão simples do **capital aplicado** e o **valor bruto** ao longo do tempo. Um gráfico simples mas que pode mostrar o resultado de suas escolhas e muitas vezes o motivar a continuar ou repensar a estratégia.
<img src="img/crescimento_patrimonial.png">

## Obtenção dos dados:
1. **Negociações** e **carteira atual**: ambos foram obtidos no [CEI](https://cei.b3.com.br/CEI_Responsivo/) com a utilização do algoritmo de scraping `atualizar_dados.py` disponível no repositório;

2. **Cotações**: foram obtidas utilizando a biblioteca `pandas datareader` utilizando como canal de busca o _Yahoo Finance_;

3. **Rendimentos**: essa é uma tabela que eu possuo desde que comecei a investir que vou alimentando sempre quando cai rendimento novo. Sempre utilizei ela para me manter focado e continuar investindo.


## Observações:
* **Não possui suporte a todos tipos de investimentos**: como mostrado nas imagens acima meus investimentos estão em fase inicial possuindo pouquíssimos ativos e de apenas duas classes então não tenho acesso a como outros tipos de ativos são disponibilizados no CEI;

* **Contribuições:** contribuições são **7000% bem vindas** esse é meu primeiro projeto que envolve _web scraping_ e _dashboards_, imagino que de para perceber ao olhar o projeto, então eu ficaria super feliz se quisesse contribuir com o projeto com algoritmos mais eficientes, melhor arquitetura, nova funcionalidade ou suporte um tipo de ativo, ou qualquer mudança que ache que deixaria o projeto melhor.

## Como usar:

1. No arquivo `requisitos.txt` tem as bibliotecas instaladas e suas respectivas versões;

2. Ter o Chrome e o webdriver do Chrome na pasta raiz do projeto ([link para obter o webdriver](https://chromedriver.chromium.org/));
3. Colocar o CPF e senha no script `cei_scrap.py`;
<img src="img/login_cei.png">

4. Executar o script `atualizar_dados.py` e esperar a obtenção dos dados;
    >`python atualizar_dados.py`

    * Tabela rendimentos não é criada nesse script, da para usar o modelo que está no repositório e colocar os seus valores.

5. Executar o Dashboard.
    >`streamlit run dashboard.py`


## Próximos updates:

* Melhorar a qualidade dos gráficos e mostar mais informações relevantes neles;
* Adicionar a opção de inserir novas negociações e rendimentos através do dashboard;
* Criar um botão para atualizar os dados com pegando as informarções do CEI.
