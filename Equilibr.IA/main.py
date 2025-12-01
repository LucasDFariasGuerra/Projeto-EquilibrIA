from user_manager import GerenciadorUsuarios
from interface import InterfaceUsuario
from utils import Utils

class EquilibrIA_App:
    def __init__(self):
        self.gerenciador = GerenciadorUsuarios()
        self.usuario_logado = None 

    def executar(self):
        while True:
            Utils.limpar_tela()
            
            if self.usuario_logado is None:
                escolha = InterfaceUsuario.exibir_menu_principal()

                if escolha == '1':
                    self.gerenciador.cadastrar_usuario()
                    Utils.pausar_tela()
                
                elif escolha == '2':
                    usuario = self.gerenciador.autenticar()
                    if usuario:
                        self.usuario_logado = usuario
                    Utils.pausar_tela()
                
                elif escolha == '0':
                    print("Saindo e salvando...")
                    break
                else:
                    print(Utils.COR_ERRO + "Opção inválida.")

            else:
                escolha = InterfaceUsuario.exibir_menu_logado(self.usuario_logado)

                if escolha == '1':
                    InterfaceUsuario.exibir_dashboard(self.usuario_logado)
                    Utils.pausar_tela()

                elif escolha == '2':
                    # Nova opção: Hidratação
                    self.gerenciador.registrar_agua(self.usuario_logado)
                    Utils.pausar_tela()

                elif escolha == '3':
                    # Nova opção: Evolução
                    InterfaceUsuario.exibir_evolucao(self.usuario_logado)
                    Utils.pausar_tela()

                elif escolha == '4':
                    self.gerenciador.editar_usuario(self.usuario_logado)
                    Utils.pausar_tela()

                elif escolha == '5':
                    excluiu = self.gerenciador.excluir_usuario(self.usuario_logado)
                    if excluiu:
                        self.usuario_logado = None
                    Utils.pausar_tela()

                elif escolha == '0':
                    print("Logout realizado.")
                    self.usuario_logado = None
                    Utils.pausar_tela()

if __name__ == "__main__":
    app = EquilibrIA_App()
    app.executar()