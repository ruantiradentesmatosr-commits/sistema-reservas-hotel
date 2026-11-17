from datetime import datetime, date
from models import Cliente, QuartoSolteiro, QuartoCasal, SuiteLuxo, Reserva
from exceptions import HotelError,QuartoIndisponivelError, DataInvalidaError, RegistroNaoEncontradoError
from storage import salvar_dados, carregar_dados


def ler_data(texto):
    data_str = input(texto)
    try:
        data_convertida = datetime.strptime(data_str, "%d/%m/%Y").date()
        return data_convertida
    except ValueError:
        raise DataInvalidaError("Data invalida! Digite no formato DD/MM/AAAA.")


def buscar_cliente(clientes, cpf):
    for c in clientes:
        if c.cpf == cpf:
            return c
    raise RegistroNaoEncontradoError("Cliente nao encontrado.")


def buscar_quarto(quartos, numero):
    for q in quartos:
        if q.numero == numero:
            return q
    raise RegistroNaoEncontradoError("Quarto nao encontrado.")


def cadastrar_cliente(clientes):
    print("\n--- Cadastrar Cliente ---")
    nome = input("Nome: ")
    cpf = input("CPF: ")
    telefone = input("Telefone: ")

    if nome == "" or cpf == "":
        raise ValueError("Nome e CPF nao podem ficar vazios.")

    for c in clientes:
        if c.cpf == cpf:
            raise ValueError("Ja existe um cliente com esse CPF.")

    novo = Cliente(nome, cpf, telefone)
    clientes.append(novo)
    print("Cliente cadastrado com sucesso!")


def cadastrar_quarto(quartos):
    print("\n--- Cadastrar Quarto ---")
    numero = int(input("Numero do quarto: "))

    for q in quartos:
        if q.numero == numero:
            raise ValueError("Esse numero de quarto ja existe.")

    diaria = float(input("Valor da diaria: "))
    if diaria <= 0:
        raise ValueError("A diaria precisa ser maior que zero.")

    print("Tipos: 1 - Solteiro | 2 - Casal | 3 - Suite")
    tipo = input("Escolha o tipo: ")

    if tipo == "1":
        quarto = QuartoSolteiro(numero, diaria)
    elif tipo == "2":
        quarto = QuartoCasal(numero, diaria)
    elif tipo == "3":
        quarto = SuiteLuxo(numero, diaria)
    else:
        raise ValueError("Opcao de quarto invalida.")

    quartos.append(quarto)
    print("Quarto cadastrado com sucesso!")


def realizar_reserva(clientes, quartos, reservas):
    print("\n--- Nova Reserva ---")
    cpf = input("Digite o CPF do cliente: ")
    cliente = buscar_cliente(clientes, cpf)

    numero = int(input("Digite o numero do quarto: "))
    quarto = buscar_quarto(quartos, numero)

    check_in = ler_data("Data de check-in (DD/MM/AAAA): ")
    check_out = ler_data("Data de check-out (DD/MM/AAAA): ")

    if check_in < date.today():
        raise DataInvalidaError("Nao pode reservar para uma data que ja passou.")

    for r in reservas:
        if r.quarto.numero == quarto.numero:
            if r.tem_conflito(check_in, check_out):
                raise QuartoIndisponivelError(
                    quarto.numero,
                    r.check_in.strftime("%d/%m/%Y"),
                    r.check_out.strftime("%d/%m/%Y")
                )

    codigo = len(reservas) + 1
    nova_reserva = Reserva(codigo, cliente, quarto, check_in, check_out)
    reservas.append(nova_reserva)
    print(f"Reserva feita! Valor total: R$ {nova_reserva.valor_total:.2f}")


def cancelar_reserva(reservas):
    print("\n--- Cancelar Reserva ---")
    codigo = int(input("Codigo da reserva: "))

    for r in reservas:
        if r.codigo == codigo:
            if r.status == "Cancelada":
                print("Essa reserva ja foi cancelada antes.")
                return
            r.status = "Cancelada"
            print("Reserva cancelada com sucesso!")
            return

    raise RegistroNaoEncontradoError("Codigo de reserva nao encontrado.")


def listar_tudo(clientes, quartos, reservas):
    print("\n--- Lista de Clientes ---")
    if len(clientes) == 0:
        print("Nenhum cliente cadastrado.")
    else:
        for c in clientes:
            print(c)

    print("\n--- Lista de Quartos ---")
    if len(quartos) == 0:
        print("Nenhum quarto cadastrado.")
    else:
        for q in quartos:
            print(q)

    print("\n--- Lista de Reservas ---")
    if len(reservas) == 0:
        print("Nenhuma reserva feita.")
    else:
        for r in reservas:
            print(r)


def main():
    clientes, quartos, reservas = carregar_dados()

    while True:
        print("\n=== MENU DO HOTEL ===")
        print("1 - Cadastrar Cliente")
        print("2 - Cadastrar Quarto")
        print("3 - Fazer Reserva")
        print("4 - Cancelar Reserva")
        print("5 - Listar Tudo")
        print("0 - Sair")

        opcao = input("Escolha uma opcao: ")

        try:
            if opcao == "1":
                cadastrar_cliente(clientes)
                salvar_dados(clientes, quartos, reservas)
            elif opcao == "2":
                cadastrar_quarto(quartos)
                salvar_dados(clientes, quartos, reservas)
            elif opcao == "3":
                realizar_reserva(clientes, quartos, reservas)
                salvar_dados(clientes, quartos, reservas)
            elif opcao == "4":
                cancelar_reserva(reservas)
                salvar_dados(clientes, quartos, reservas)
            elif opcao == "5":
                listar_tudo(clientes, quartos, reservas)
            elif opcao == "0":
                salvar_dados(clientes, quartos, reservas)
                print("Saindo do sistema...")
                break
            else:
                print("Opcao invalida!")
        except (HotelError, ValueError) as erro:
            print("Erro:", erro)


if __name__ == "__main__":
    main()