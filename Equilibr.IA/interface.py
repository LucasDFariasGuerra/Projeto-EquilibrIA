from utils import Utils
from health_calculator import CalculadoraSaude
from suggestions import GeradorSugestoes

class InterfaceUsuario:
    
    @staticmethod
    def exibir_menu_principal():
        Utils.limpar_tela()
        print("\n=========================")
        print(Utils.COR_TITULO + " BEM-VINDO AO Equilibr.IA ")
        print("=========================")
        print("1. Cadastrar Novo Usuário")
        print("2. Acessar Conta (Login)")
        print("0. Sair do Programa")
        return input("Qual função deseja acessar? ")

    @staticmethod
    def exibir_menu_logado(usuario):
        Utils.limpar_tela()
        print(Utils.COR_TITULO + f"\n--- PAINEL DE: {usuario.nome} ---")
        print("1. Ver meu Painel de Saúde (Dashboard)")
        print("2. Editar Perfil")
        print("3. Excluir Perfil")
        print("0. Logout")
        return input("Escolha uma opção: ")

    @staticmethod
    def exibir_dashboard(usuario):
        Utils.limpar_tela()
        
        imc = CalculadoraSaude.calcular_imc(usuario.peso, usuario.altura)
        tmb = CalculadoraSaude.calcular_tmb(usuario.sexo, usuario.peso, usuario.altura, usuario.idade)
        
        dieta = GeradorSugestoes.gerar_sugestao_dieta(tmb, usuario.peso, usuario.objetivo, usuario.nivel_treino)
        treino = GeradorSugestoes.gerar_sugestao_treino(usuario.nivel_treino, usuario.objetivo)

        print(Utils.COR_TITULO + "\n--- SEUS RESULTADOS ---")
        print(f"IMC: {imc:.2f}")
        print(f"TMB: {tmb:.0f} kcal")
        print("\n" + dieta)
        print("\n" + treino)