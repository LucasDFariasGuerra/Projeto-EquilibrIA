# utils.py
import os
from colorama import Fore, Style, init

# Inicializa o colorama para que as cores funcionem no terminal
# autoreset=True garante que a cor volta ao normal após cada print
init(autoreset=True)

# --- FUNÇÃO PARA LIMPAR A TELA ---
def limpar_tela():
    """Limpa a tela do terminal, compatível com Windows, Mac e Linux."""
    # 'nt' é para Windows, 'posix' é para Mac/Linux
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar_tela():
    input('\nPressione "enter" para continuar...')

# --- DEFINIÇÃO DE CORES PARA PADRONIZAR O PROJETO ---
COR_ERRO = Fore.RED
COR_SUCESSO = Fore.GREEN
COR_AVISO = Fore.YELLOW
COR_TITULO = Fore.CYAN
COR_NORMAL = Fore.WHITE

# Cores para as zonas de IMC
COR_ZONA_VERMELHA = Fore.RED
COR_ZONA_AMARELA = Fore.YELLOW
COR_ZONA_VERDE = Fore.GREEN