import user_manager
import interface
import utils 

def main():
    """Função principal que executa o loop do aplicativo."""
    
    usuario_logado = None

    while True:
        utils.limpar_tela()
        if usuario_logado is None:
            escolha = interface.exibir_menu_deslogado()

            if escolha == '1':
                user_manager.cadastrar_usuario()
                utils.pausar_tela()
            
            elif escolha == '2':
                username_valido = user_manager.verificar_login()
                if username_valido:
                    usuario_logado = username_valido
                utils.pausar_tela()
            
            elif escolha == '0':
                print("\nObrigado por usar o Equilibr.IA! Saindo...")
                break
            
            else:
                print(utils.COR_ERRO + "\n Opção inválida. Por favor, tente novamente.")

        #Menu de usuário
        else:
            escolha = interface.exibir_menu_logado(usuario_logado)
            
            if escolha == '1':
                dados_do_usuario = user_manager.usuarios[usuario_logado]
                interface.exibir_dashboard(dados_do_usuario)
                utils.pausar_tela()
            
            elif escolha == '2':
                #Edição de conta
                user_manager.editar_usuario(usuario_logado)
                utils.pausar_tela()
            
            elif escolha == '3':
                user_manager.excluir_usuario()
                #Exclusão de conta 
                usuario_logado = None
                utils.pausar_tela()
            
            elif escolha == '0':
                print(utils.COR_SUCESSO + "\nFazendo logout...")
                usuario_logado = None #Desloga o usuário
                utils.pausar_tela()
            
            else:
                print(utils.COR_ERRO + "\n❌ Opção inválida. Por favor, tente novamente.")
                utils.pausar_tela()

#Garante que a função main() só será executada quando este arquivo for o principal
if __name__ == "__main__":
    main()