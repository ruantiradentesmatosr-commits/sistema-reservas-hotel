import json
import os
from datetime import datetime
from models import Cliente, QuartoSolteiro, QuartoCasal, SuiteLuxo, Reserva

ARQUIVO = "dados_hotel.json"

def salvar_dados(clientes, quartos, reservas):
    lista_clientes = []
    for c in clientes:
        lista_clientes.append(c.para_dicionario())

    lista_quartos = []
    for q in quartos:
        lista_quartos.append(q.para_dicionario())

    lista_reservas = []
    for r in reservas:
        lista_reservas.append(r.para_dicionario())

    dados = {
        "clientes": lista_clientes,
        "quartos": lista_quartos,
        "reservas": lista_reservas
    }

    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4)


def carregar_dados():
    if not os.path.exists(ARQUIVO):
        return [], [], []

    with open(ARQUIVO, "r", encoding="utf-8") as f:
        dados = json.load(f)

    clientes = []
    for item in dados["clientes"]:
        c = Cliente(item["nome"], item["cpf"], item["telefone"])
        clientes.append(c)

    quartos = []
    for item in dados["quartos"]:
        if item["tipo"] == "Solteiro":
            q = QuartoSolteiro(item["numero"], item["diaria"])
        elif item["tipo"] == "Casal":
            q = QuartoCasal(item["numero"], item["diaria"])
        else:
            q = SuiteLuxo(item["numero"], item["diaria"])
        quartos.append(q)

    reservas = []
    for item in dados["reservas"]:
        cliente_achado = None
        for c in clientes:
            if c.cpf == item["cliente_cpf"]:
                cliente_achado = c
                break

        quarto_achado = None
        for q in quartos:
            if q.numero == item["quarto_numero"]:
                quarto_achado = q
                break

        if cliente_achado is not None and quarto_achado!= None:
            dt_in = datetime.strptime(item["check_in"], "%Y-%m-%d").date()
            dt_out = datetime.strptime(item["check_out"], "%Y-%m-%d").date()
            r = Reserva(item["codigo"], cliente_achado, quarto_achado, dt_in, dt_out, item["status"])
            reservas.append(r)

    return clientes, quartos, reservas