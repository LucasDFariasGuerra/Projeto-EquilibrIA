import os
from colorama import Fore, Style, init

init(autoreset=True)

def limpar_tela():
    
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar_tela():
    input('\nPressione "enter" para continuar...')

COR_ERRO = Fore.RED
COR_SUCESSO = Fore.GREEN
COR_AVISO = Fore.YELLOW
COR_TITULO = Fore.CYAN
COR_NORMAL = Fore.WHITE

COR_ZONA_VERMELHA = Fore.RED
COR_ZONA_AMARELA = Fore.YELLOW
COR_ZONA_VERDE = Fore.GREEN