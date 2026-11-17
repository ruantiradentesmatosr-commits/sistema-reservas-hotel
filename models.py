from exceptions import DataInvalidaError

class Cliente:
    def __init__(self, nome, cpf, telefone):
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone

    def para_dicionario(self):
        return {
            "nome": self.nome,
            "cpf": self.cpf,
            "telefone": self.telefone
        }
    def __str__(self):
        return f"Nome: {self.nome} | CPF: {self.cpf} | Tel: {self.telefone}"

class Quarto:
    def __init__(self, numero, diaria):
        self.numero = numero
        self.diaria = diaria
        self.tipo = "Padrao"

    def calcular_total(self, dias):
        return self.diaria * dias

    def para_dicionario(self):
        return {
            "numero": self.numero,
            "diaria": self.diaria,
            "tipo": self.tipo
        }

    def __str__(self):
        return f"Quarto {self.numero} ({self.tipo}) - Diaria: R$ {self.diaria:.2f}"


class QuartoSolteiro(Quarto):
    def __init__(self, numero, diaria):
        super().__init__(numero, diaria)
        self.tipo = "Solteiro"

    def calcular_total(self, dias):
        return self.diaria * dias

class QuartoCasal(Quarto):
    def __init__(self, numero, diaria):
        super().__init__(numero, diaria)
        self.tipo = "Casal"

    def calcular_total(self, dias):
        valor = self.diaria * dias
        return valor + (valor * 0.10)

class SuiteLuxo(Quarto):
    def __init__(self, numero, diaria):
        super().__init__(numero, diaria)
        self.tipo = "Suite"

    def calcular_total(self, dias):
        valor = self.diaria * dias
        return valor + (valor * 0.25) + 80.0

class Reserva:
    def __init__(self, codigo, cliente, quarto, check_in, check_out, status="Ativa"):
        if check_out <= check_in:
            raise DataInvalidaError("A data de saida tem que ser depois da data de entrada.")
        self.codigo = codigo
        self.cliente = cliente
        self.quarto = quarto
        self.check_in = check_in
        self.check_out = check_out
        self.status = status
        self.dias = (check_out - check_in).days
        self.valor_total = self.quarto.calcular_total(self.dias)

    def tem_conflito(self, inicio, fim):
        if self.status != "Ativa":
            return False
        if inicio < self.check_out and fim > self.check_in:
            return True
        return False

    def para_dicionario(self):
        return {
            "codigo": self.codigo,
            "cliente_cpf": self.cliente.cpf,
            "quarto_numero": self.quarto.numero,
            "check_in": self.check_in.strftime("%Y-%m-%d"),
            "check_out": self.check_out.strftime("%Y-%m-%d"),
            "status": self.status
        }
    def __str__(self):
        entrada = self.check_in.strftime("%d/%m/%Y")
        saida = self.check_out.strftime("%d/%m/%Y")
        return (
            f"Reserva {self.codigo} [{self.status}] - Cliente: {self.cliente.nome} | "
            f"Quarto {self.quarto.numero} ({self.quarto.tipo}) | {entrada} ate {saida} | "
            f"Total: R$ {self.valor_total:.2f}"
        )