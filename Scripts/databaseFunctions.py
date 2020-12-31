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


def novaNegociacao(data_negociacao, tipo, codigo, quantidade, preco):
    if tipo == 'Compra':
        tipo = 'c'
    else:
        tipo = 'v'

    connection, cursor = connectDB()
    query =("INSERT INTO negociacao"
            "(data_negociacao, codigo, tipo, quantidade, preco)"
            "VALUES(%s, %s, %s, %s, %s)")
    data = (data_negociacao, codigo, tipo, quantidade, preco)

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
    df.columns = ['data_negociacao', 'codigo', 'tipo', 'quantidade', 'valor_bruto']

    closeDB(connection, cursor)
    return df


def recuperarProvento():
    connection, cursor = connectDB()
    query = ("SELECT * FROM provento")
    cursor.execute(query)

    rows = cursor.fetchall()
    df = pd.DataFrame([[ij for ij in i] for i in rows])
    df.columns = ['data_pagamento', 'codigo', 'tipo', 'quantidade_base', 'valor_bruto']

    closeDB(connection, cursor)

    df['data_pagamento'] = pd.to_datetime(df['data_pagamento'])
    mes_pag = []
    for data in  df['data_pagamento']:
        mes = datetime.datetime(data.year, data.month, 1)
        mes_pag.append(mes)

    df['mes_pagamento'] = mes_pag
    return df


def createTables():
    TABLES = {}
    TABLES['negociacao'] = (
        "CREATE TABLE `negociacao` ("
        "`data_negociacao` date NOT NULL,"
        "`codigo` varchar(10) NOT NULL,"
        "`tipo` char NOT NULL,"
        "`quantidade` int(10) NOT NULL,"
        "`preco` DECIMAL(8,2))"
    )

    TABLES['provento'] = (
        "CREATE TABLE `provento` ("
        "`data_pagamento` date NOT NULL,"
        "`codigo` varchar(10) NOT NULL,"
        "`tipo` varchar(10) NOT NULL,"
        "`quantidade_base` int(10) NOT NULL,"
        "`valor_bruto` DECIMAL(8,2))"
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
