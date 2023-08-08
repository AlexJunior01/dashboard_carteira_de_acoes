import tkinter
from tkinter import ttk
from tkinter import messagebox
import databaseFunctions as db_func

import sys
import os

if os.environ.get('DISPLAY','') == '':
    os.environ.__setitem__('DISPLAY', ':0.0')


def windowsAddNegociacao():

    def pegarNegociacao():
        data_negociacao = data_entry.get()
        tipo = tipo_entry.get()
        codigo = cod_entry.get()
        quantidade = qtd_entry.get()
        preco = preco_entry.get()

        msg = messagebox.showinfo('Mensagem', 'Negociação adicionada com sucesso')

        data_entry.delete(0, len(data_negociacao))
        tipo_entry.delete(0, len(tipo))
        cod_entry.delete(0, len(codigo))
        qtd_entry.delete(0, len(quantidade))
        preco_entry.delete(0, len(preco))

        db_func.novaNegociacao(data_negociacao, tipo, codigo, quantidade, preco)

    root = tkinter.Tk()
    root.title("Adicionar Negociação")
    root.geometry("500x300")

    frame = ttk.Frame(root, padding="3 3 12 12")
    frame.grid(column=0, row=0, sticky=(tkinter.N, tkinter.W, tkinter.E, tkinter.S))
    root.columnconfigure(0, weight=2)
    root.rowconfigure(0, weight=2)

    # Data
    data_entry = tkinter.Entry(frame, width=15)
    data_entry.grid(column=2, row=1, sticky=(tkinter.W, tkinter.E))
    ttk.Label(frame, text="Data Negociação").grid(column=1, row=1)

    # Ativo
    cod_entry = tkinter.Entry(frame, width=15)
    cod_entry.grid(column=2, row=2, sticky=(tkinter.W, tkinter.E))
    ttk.Label(frame, text="Código").grid(column=1, row=2)

    # Tipo da Operação
    tipo_entry = ttk.Combobox(frame, values=["Compra", "Venda"])
    tipo_entry.grid(column=2, row=3, sticky=(tkinter.W, tkinter.E))
    ttk.Label(frame, text="Tipo da Operação").grid(column=1, row=3)

    # Quantidade
    qtd_entry = tkinter.Entry(frame, width=15)
    qtd_entry.grid(column=2, row=4, sticky=(tkinter.W, tkinter.E))
    ttk.Label(frame, text="Quantidade").grid(column=1, row=4)

    # Preço
    preco_entry = tkinter.Entry(frame, width=15)
    preco_entry.grid(column=2, row=5, sticky=(tkinter.W, tkinter.E))
    ttk.Label(frame, text="Preço").grid(column=1, row=5)

    # Adicionar no BD
    btn = ttk.Button(frame, text='Adicionar', command=pegarNegociacao)
    btn.grid(column=2, row=6)

    for child in frame.winfo_children():
        child.grid_configure(padx=5, pady=5)

    root.mainloop()


def windowsAddProvento():
    def pegarProvento():
        data_pagamento = data_entry.get()
        codigo = cod_entry.get()
        tipo = tipo_entry.get()
        quantidade_base = qtd_entry.get()
        valor_bruto = valor_entry.get()

        msg = messagebox.showinfo('Mensagem', 'Provento adicionado com sucesso')

        data_entry.delete(0, len(data_pagamento))
        cod_entry.delete(0, len(codigo))
        tipo_entry.delete(0, len(tipo))
        qtd_entry.delete(0, len(quantidade_base))
        valor_entry.delete(0, len(valor_bruto))

        db_func.novoProvento(data_pagamento, codigo, tipo, quantidade_base, valor_bruto)


    root = tkinter.Tk()
    root.title("Adicionar Negociação")
    root.geometry("500x300")

    frame = ttk.Frame(root, padding="3 3 12 12")
    frame.grid(column=0, row=0, sticky=(tkinter.N, tkinter.W, tkinter.E, tkinter.S))
    root.columnconfigure(0, weight=2)
    root.rowconfigure(0, weight=2)

    # Data
    data_entry = tkinter.Entry(frame, width=15)
    data_entry.grid(column=2, row=1, sticky=(tkinter.W, tkinter.E))
    ttk.Label(frame, text="Data Pagamento").grid(column=1, row=1)

    # Codigo
    cod_entry = tkinter.Entry(frame, width=15)
    cod_entry.grid(column=2, row=2, sticky=(tkinter.W, tkinter.E))
    ttk.Label(frame, text="Código").grid(column=1, row=2)


    # Tipo
    tipo_entry = tkinter.Entry(frame, width=15)
    tipo_entry.grid(column=2, row=3, sticky=(tkinter.W, tkinter.E))
    ttk.Label(frame, text="Tipo").grid(column=1, row=3)


    # Quantidade Base
    qtd_entry = tkinter.Entry(frame, width=15)
    qtd_entry.grid(column=2, row=4, sticky=(tkinter.W, tkinter.E))
    ttk.Label(frame, text="Quantidade Base").grid(column=1, row=4)

    # Valor Bruto
    valor_entry = tkinter.Entry(frame, width=15)
    valor_entry.grid(column=2, row=5, sticky=(tkinter.W, tkinter.E))
    ttk.Label(frame, text="Valor").grid(column=1, row=5)


    # Adicionar no BD
    btn = ttk.Button(frame, text='Adicionar', command=pegarProvento)
    btn.grid(column=2, row=6)

    for child in frame.winfo_children():
        child.grid_configure(padx=5, pady=5)

    root.mainloop()
