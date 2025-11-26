import os
from colorama import Fore, init

init(autoreset=True)

class Utils:
    COR_ERRO = Fore.RED
    COR_SUCESSO = Fore.GREEN
    COR_AVISO = Fore.YELLOW
    COR_TITULO = Fore.CYAN
    COR_NORMAL = Fore.WHITE

    @staticmethod
    def limpar_tela():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def pausar_tela():
        input('\nPressione "enter" para continuar...')