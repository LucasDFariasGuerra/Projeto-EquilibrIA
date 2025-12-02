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
        print("1. Ver Painel de Saúde (Status + Água)")
        print(Utils.COR_AVISO + "2. 🤖 Gerar Nova Dieta/Treino (IA Generativa)")
        print(Utils.COR_SUCESSO + "3. 📋 Ver Meu Plano Atual (Salvo)")
        print(Utils.COR_NORMAL + "4. Ver Evolução (Histórico)")
        print("5. Editar Perfil")
        print("6. Excluir Perfil")
        print("0. Logout")
        return input("Escolha uma opção: ")

    
    @staticmethod
    def _imprimir_caixa(titulo, conteudo, cor_borda):
        
        largura = 60
        print(cor_borda + "╔" + "═" * largura + "╗")
        print(f"║ {titulo.center(largura - 2)} ║")
        print("╠" + "═" * largura + "╣")
        
        
        linhas = conteudo.split('\n')
        for linha in linhas:
            
            print(cor_borda + "║ " + Utils.COR_NORMAL + f"{linha:<{largura - 2}}" + cor_borda + "║")
            
        print(cor_borda + "╚" + "═" * largura + "╝" + Utils.COR_NORMAL)

    @staticmethod
    def exibir_dashboard_status(usuario):
        
        Utils.limpar_tela()
        
        imc = CalculadoraSaude.calcular_imc(usuario.peso, usuario.altura)
        tmb = CalculadoraSaude.calcular_tmb(usuario.sexo, usuario.peso, usuario.altura, usuario.idade)
        
        print(Utils.COR_TITULO + "\n=== SEU STATUS CORPORAL ===")
        print(f"Objetivo: {usuario.objetivo.upper()}")
        print(f"IMC: {imc:.2f} | TMB: {tmb:.0f} kcal")
        
        
        meta = usuario.meta_agua if usuario.meta_agua > 0 else 2000
        perc = min(1.0, usuario.agua_hoje / meta)
        comp_barra = 20
        preenchido = int(perc * comp_barra)
        visual = "█" * preenchido + "-" * (comp_barra - preenchido)
        cor_barra = Utils.COR_SUCESSO if perc >= 1.0 else Utils.COR_AVISO
        
        print(f"\n💧 Hidratação: [{cor_barra}{visual}{Utils.COR_NORMAL}] {usuario.agua_hoje}/{meta:.0f} ml")
        print("\n(Para ver sua dieta, selecione a opção 'Ver Meu Plano Atual' no menu)")

    @staticmethod
    def gerar_e_salvar_plano(usuario, gerenciador):
        
        Utils.limpar_tela()
        print(Utils.COR_TITULO + "=== INTELIGÊNCIA ARTIFICIAL ATIVADA ===")
        print("Analisando seu perfil para criar a melhor rotina...")
        
        imc = CalculadoraSaude.calcular_imc(usuario.peso, usuario.altura)
        tmb = CalculadoraSaude.calcular_tmb(usuario.sexo, usuario.peso, usuario.altura, usuario.idade)
        
       
        dieta = GeradorSugestoes.gerar_sugestao_dieta(
            tmb, usuario.peso, usuario.altura, usuario.idade, 
            usuario.sexo, usuario.objetivo, usuario.nivel_treino
        )
        
        
        treino = GeradorSugestoes.gerar_sugestao_treino(
            usuario.nivel_treino, usuario.objetivo, usuario.idade
        )
        
        
        gerenciador.salvar_plano_gerado(usuario, dieta, treino)
        
        Utils.limpar_tela()
        print(Utils.COR_SUCESSO + "✅ PLANO GERADO E SALVO COM SUCESSO!\n")
        InterfaceUsuario._imprimir_caixa("NOVA DIETA", dieta, Utils.COR_AVISO)
        print()
        InterfaceUsuario._imprimir_caixa("NOVO TREINO", treino, Utils.COR_TITULO)

    @staticmethod
    def exibir_plano_salvo(usuario):
        """Lê o plano do JSON e mostra bonito na tela."""
        Utils.limpar_tela()
        
        if usuario.data_plano:
            print(Utils.COR_TITULO + f"=== SEU PLANO (Gerado em: {usuario.data_plano}) ===")
        else:
            print(Utils.COR_TITULO + "=== SEU PLANO ATUAL ===")
            
        InterfaceUsuario._imprimir_caixa("DIETA", usuario.plano_dieta, Utils.COR_AVISO)
        print()
        InterfaceUsuario._imprimir_caixa("TREINO", usuario.plano_treino, Utils.COR_TITULO)
        
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