class HotelError(Exception):
    pass
class QuartoIndisponivelError(HotelError):
    def __init__(self, numero, inicio, fim):
        mensagem = f"O quarto {numero} ja esta reservado de {inicio} ate {fim}."
        super().__init__(mensagem)
class DataInvalidaError(HotelError):
    pass
class RegistroNaoEncontradoError(HotelError):
    pass