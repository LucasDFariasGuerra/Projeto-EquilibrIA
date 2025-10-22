import health_calculator
import suggestions 
import utils

def exibir_menu_deslogado():
    utils.limpar_tela()
    print("\n=========================")
    print(utils.COR_TITULO + " BEM-VINDO AO Equilibr.IA")
    print("=========================")
    print("1. Cadastrar Novo Usuário")
    print("2. Acessar Conta (Login)")
    print("0. Sair do Programa")
    return input("Qual função deseja acessar? ")

def exibir_menu_logado(username):
    utils.limpar_tela()
    print(utils.COR_TITULO + f"\n--- MENU DO USUÁRIO: {username} ---")
    print("1. Ver meu Painel de Saúde")
    print("2. Editar Perfil")
    print("3. Excluir Perfil")
    print("0. Logout (Voltar ao menu principal)")
    return input("Escolha uma opção: ")

def exibir_dashboard(user_data):
    utils.limpar_tela()
    peso = user_data['peso']
    altura = user_data['altura']
    sexo = user_data['sexo']
    idade = user_data['idade']
    objetivo = user_data['objetivo']
    nivel_treino = user_data['nivel_treino']
    
    imc = health_calculator.calcular_imc(peso, altura)
    tmb = health_calculator.calcular_tmb(sexo, peso, altura, idade)
    
    dieta_sugestao = suggestions.gerar_sugestao_dieta(tmb, peso, objetivo, nivel_treino)
    treino_sugestao = suggestions.gerar_sugestao_treino(nivel_treino, objetivo,)

    print(utils.COR_TITULO + "\n" + "="*20 + " SEU PAINEL DE SAÚDE " + "="*20)
    print(f"IMC: {imc:.2f} (Índice de Massa Corporal)")
    print(f"TMB: {tmb:.0f} kcal (Taxa Metabólica Basal diária)")
    print("-" * 64)
    
    print(utils.COR_TITULO + "\n--- SUGESTÃO DE DIETA ---")
    print(dieta_sugestao)
    
    print(utils.COR_TITULO + "\n--- SUGESTÃO DE TREINO ---")
    print(treino_sugestao)
    print("=" * 64)