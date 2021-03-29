import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
import pandas as pd
import datetime


def connectDB():
    try:
        connection = mysql.connector.connect(host='localhost',
                                            database='Investimentos',
                                            user='root',
                                            password='alexalex')

        if connection.is_connected():
            cursor = connection.cursor(buffered=True)
            cursor.execute("select database();")

    except Error as e:
        print('Erro while connecting to MySQL', e)

    return connection, cursor


def closeDB(connection, cursor):
    if (connection.is_connected()):
        cursor.close()
        connection.close()


def novaNegociacao(categoria, data_negociacao, tipo, codigo, quantidade, preco):

    # Pré processamento dos dados
    if tipo == 'Compra':
        tipo = 'C'
    else:
        tipo = 'V'

    quantidade = float(quantidade)
    preco = float(preco)

    # Lançando para o BD
    connection, cursor = connectDB()
    query =("INSERT INTO negociacao"
            "(categoria, data_negociacao, codigo, tipo, quantidade, preco, total)"
            "VALUES(%s, %s, %s, %s, %s, %s, %s)")
    data = (categoria, data_negociacao, codigo, tipo, quantidade, preco, quantidade*preco)

    cursor.execute(query, data)
    connection.commit()

    closeDB(connection, cursor)


def novoProvento(data_pagamento, codigo, tipo, quantidade_base, valor_bruto):
    connection, cursor = connectDB()

    query = ("INSERT INTO provento"
             "(data_pagamento, codigo, tipo, quantidade_base, valor_bruto)"
             "VALUES(%s, %s, %s, %s, %s)")
    data = (data_pagamento, codigo, tipo, quantidade_base, valor_bruto)

    cursor.execute(query, data)
    connection.commit()

    closeDB(connection, cursor)


def recuperarNegociacao():
    connection, cursor = connectDB()
    query = ("SELECT * FROM negociacao")
    cursor.execute(query)

    rows = cursor.fetchall()
    df = pd.DataFrame([[ij for ij in i] for i in rows])
    df.columns = ['id_negociacao', 'categoria', 'data_negociacao',
                 'codigo', 'tipo', 'quantidade', 'valor_bruto', 'total']

    closeDB(connection, cursor)
    return df


def recuperarProvento():
    connection, cursor = connectDB()
    query = ("SELECT * FROM provento")
    cursor.execute(query)

    rows = cursor.fetchall()
    df = pd.DataFrame([[ij for ij in i] for i in rows])
    df.columns = ['id_provento','data_pagamento', 'codigo', 'tipo', 'quantidade_base', 'valor_bruto']

    closeDB(connection, cursor)

    #Mês pagamento
    df['data_pagamento'] = pd.to_datetime(df['data_pagamento'])
    mes_pag = []
    for data in  df['data_pagamento']:
        mes = datetime.datetime(data.year, data.month, 1)
        mes_pag.append(mes)
    df['mes_pagamento'] = mes_pag

    #Conversão dos tipos
    df['valor_bruto'] = df['valor_bruto'].astype(str).astype(float)
    return df


def recuperarCarteiraAtual():
    connection, cursor = connectDB()
    query = ("SELECT * FROM carteira")
    cursor.execute(query)

    rows = cursor.fetchall()
    df = pd.DataFrame([[ij for ij in i] for i in rows])
    df.columns = ['codigo', 'categoria', 'quantidade']

    closeDB(connection, cursor)
    return df


def excluirNegociacao(id_negociacao):
    connection, cursor = connectDB()

    query = "DELETE FROM negociacao WHERE id_negociacao = %s;"

    cursor.execute(query, (id_negociacao,))
    connection.commit()

    closeDB(connection, cursor)


def excluirProvento(id_provento):
    connection, cursor = connectDB()

    query = "DELETE FROM provento WHERE id_provento = %s"


    cursor.execute(query, (id_provento,))
    connection.commit()

    closeDB(connection, cursor)


def createTables():
    TABLES = {}
    TABLES['negociacao'] = (
        "CREATE TABLE `negociacao` ("
        "`id_negociacao` int AUTO_INCREMENT,"
        "`categoria` varchar(20),"
        "`data_negociacao` date NOT NULL,"
        "`codigo` varchar(10) NOT NULL,"
        "`tipo` char NOT NULL,"
        "`quantidade` float(10) NOT NULL,"
        "`preco` DOUBLE(20,4) NOT NULL,"
        "`total` DOUBLE(20,4) NOT NULL,"
        "PRIMARY KEY (id_negociacao))"
    )

    TABLES['provento'] = (
        "CREATE TABLE `provento` ("
        "`id_provento` int AUTO_INCREMENT,"
        "`data_pagamento` date NOT NULL,"
        "`codigo` varchar(10) NOT NULL,"
        "`tipo` varchar(15) NOT NULL,"
        "`quantidade_base` int(10) NOT NULL,"
        "`valor_bruto` double(20,4) NOT NULL,"
        "PRIMARY KEY (id_provento))"
    )

    TABLES['carteira'] = (
        "CREATE TABLE `carteira` ("
	    "`codigo` varchar(10) not null,"
        "`categoria` varchar(20) not null,"
        "`quantidade` float,"
        "primary key(codigo));"
    )

    connection, cursor = connectDB()

    for table_name in TABLES:
        table_description = TABLES[table_name]

        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

    closeDB(connection, cursor)


def triggerDeletarNegociacao():
    connection, cursor = connectDB()

    cursor.execute(" drop trigger if exists tg_apagar_negociacao;")

    query = (
    """CREATE TRIGGER tg_apagar_negociacao BEFORE DELETE ON negociacao
	FOR EACH ROW
	BEGIN
		IF OLD.tipo = 'C' THEN
			UPDATE carteira SET quantidade = quantidade - OLD.quantidade WHERE codigo = OLD.codigo;
		ELSE
			UPDATE carteira SET quantidade = quantidade + OLD.quantidade WHERE codigo = OLD.codigo;
        END IF;

        IF (SELECT quantidade FROM carteira WHERE codigo = OLD.codigo) < 1 THEN
			DELETE FROM carteira WHERE codigo = OLD.codigo;
		END IF;
    END; """)

    cursor.execute(query)
    connection.commit()
    closeDB(connection, cursor)


def triggerNovaNegociação():
    connection, cursor = connectDB()

    cursor.execute(" drop trigger if exists tg_nova_negociacao")
    query = (
    """CREATE TRIGGER tg_nova_negociacao AFTER INSERT ON negociacao
	FOR EACH ROW
	BEGIN
		IF (SELECT codigo FROM carteira WHERE codigo = NEW.codigo) IS NULL THEN
			INSERT INTO carteira (codigo, categoria, quantidade) VALUES (NEW.codigo, NEW.categoria, NEW.quantidade);
		ELSE
			IF NEW.tipo = 'C' THEN
				UPDATE carteira SET quantidade = quantidade + NEW.quantidade WHERE codigo = NEW.codigo;
			ELSE
				UPDATE carteira SET quantidade = quantidade - NEW.quantidade WHERE codigo = NEW.codigo;
			END IF;

			IF (SELECT quantidade FROM carteira WHERE codigo = NEW.codigo) = 0 THEN
				DELETE FROM carteira WHERE codigo = NEW.codigo;
			END IF;
		END IF;
	END; """)

    cursor.execute(query)
    connection.commit()
    closeDB(connection, cursor)

