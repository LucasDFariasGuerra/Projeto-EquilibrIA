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
        print("1. Ver Painel de Saúde (Dashboard)")
        print("2. Registrar Água (Hidratação)")
        print("3. Ver Evolução (Histórico)")
        print("4. Editar Perfil")
        print("5. Excluir Perfil")
        print("0. Logout")
        return input("Escolha uma opção: ")

    @staticmethod
    def exibir_dashboard(usuario):
        Utils.limpar_tela()
        
        # 1. MOSTRA TELA DE CARREGAMENTO
        print(Utils.COR_TITULO + "=== PROCESSANDO DADOS ===")
        print("Calculando índices corporais...")
        
        imc = CalculadoraSaude.calcular_imc(usuario.peso, usuario.altura)
        tmb = CalculadoraSaude.calcular_tmb(usuario.sexo, usuario.peso, usuario.altura, usuario.idade)
        
        # As funções de sugestão agora vão printar "Aguarde..." aqui
        dieta = GeradorSugestoes.gerar_sugestao_dieta(
            tmb, usuario.peso, usuario.altura, usuario.idade, 
            usuario.sexo, usuario.objetivo, usuario.nivel_treino
        )
        
        treino = GeradorSugestoes.gerar_sugestao_treino(
            usuario.nivel_treino, usuario.objetivo, usuario.idade
        )
        
        # 2. LIMPA A TELA DE CARREGAMENTO E MOSTRA O RESULTADO FINAL
        Utils.limpar_tela()
        
        print(Utils.COR_TITULO + "\n=== SEU DASHBOARD DE SAÚDE ===")
        print(f"Objetivo: {usuario.objetivo.upper()} | Nível: {usuario.nivel_treino.upper()}")
        print(f"IMC: {imc:.2f} | TMB: {tmb:.0f} kcal")
        
        # BARRA DE HIDRATAÇÃO
        meta = usuario.meta_agua if usuario.meta_agua > 0 else 2000
        perc = min(1.0, usuario.agua_hoje / meta)
        comp_barra = 20
        preenchido = int(perc * comp_barra)
        visual = "█" * preenchido + "-" * (comp_barra - preenchido)
        cor_barra = Utils.COR_SUCESSO if perc >= 1.0 else Utils.COR_AVISO
        
        print(f"\n💧 Água: [{cor_barra}{visual}{Utils.COR_NORMAL}] {usuario.agua_hoje}/{meta:.0f} ml")

        print("\n" + Utils.COR_TITULO + "--- PLANEJAMENTO ---")
        print(Utils.COR_AVISO + dieta)
        print("\n" + Utils.COR_AVISO + treino)

    @staticmethod
    def exibir_evolucao(usuario):
        Utils.limpar_tela()
        print(Utils.COR_TITULO + "=== HISTÓRICO DE EVOLUÇÃO ===")
        
        if not usuario.historico_peso:
            print(Utils.COR_AVISO + "Sem dados. Atualize seu peso em 'Editar Perfil'.")
            return

        print(f"{'Data':<12} | {'Peso (kg)':<10} | {'Variação'}")
        print("-" * 40)
        
        peso_ant = None
        for registro in usuario.historico_peso:
            data = registro['data']
            peso = registro['peso']
            diff_str = "---"
            
            if peso_ant:
                diff = peso - peso_ant
                cor = Utils.COR_SUCESSO if diff < 0 else Utils.COR_ERRO
                if usuario.objetivo == 'ganhar massa':
                    cor = Utils.COR_SUCESSO if diff > 0 else Utils.COR_ERRO
                sinal = "+" if diff > 0 else ""
                diff_str = f"{cor}{sinal}{diff:.1f} kg{Utils.COR_NORMAL}"

            print(f"{data:<12} | {peso:<10.1f} | {diff_str}")
            peso_ant = peso
        print("-" * 40)