import json
import os

ARQUIVO = "usuarios.json"
def carregar_dados():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}  
def salvar_dados():
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=4, ensure_ascii=False)
usuarios = carregar_dados()


def cadastrar():
    usuario = input("Digite seu nome de usuário: ")
    if usuario in usuarios:
        print("Usuário já existe!\n")
        return
    email = input("Digite seu email: ")
    senha = input("Digite sua senha: ")
    usuarios[usuario] = {"email": email, "senha": senha}
    salvar_dados()
    print(f"Usuário {usuario} cadastrado com sucesso!\n")


def entrar_no_aplicativo():
    usuario = input("Digite seu nome de usuário: ")
    senha = input("Digite sua senha: ")
    if usuario in usuarios and usuarios[usuario]["senha"] == senha:
        print(f"Login realizado com sucesso! Bem-vindo, {usuario}.\n")
    else:
        print("Usuário ou senha incorretos.\n")


def editar():
    usuario = input("Digite seu nome de usuário para editar: ")
    if usuario in usuarios:
        novo_email = input("Digite o novo email: ")
        nova_senha = input("Digite a nova senha: ")
        usuarios[usuario]["email"] = novo_email
        usuarios[usuario]["senha"] = nova_senha
        salvar_dados()
        print("Perfil atualizado com sucesso!\n")
    else:
        print("Usuário não encontrado.\n")


def excluir():
    usuario = input("Digite o nome de usuário para excluir: ")
    if usuario in usuarios:
        del usuarios[usuario]
        salvar_dados()
        print("Perfil excluído com sucesso!\n")
    else:
        print("Usuário não encontrado.\n")
opcao = -1
while opcao != 0:
    print("++Equilibr.IA++")
    print("1 - Cadastrar")
    print("2 - Acessar conta")
    print("3 - Editar perfil")
    print("4 - Excluir perfil")
    print("0 - Sair")
    
    try:
        opcao = int(input("Escolha uma opção: "))
    except ValueError:
        print("Digite apenas números!\n")
        continue

    if opcao == 1:
        cadastrar()

    elif opcao == 2:
        entrar_no_aplicativo()

    elif opcao == 3:
        editar()

    elif opcao == 4:
        excluir()

    elif opcao == 0:
        print("Moggando o sistema...") #teste

    else:
        print("Opção inválida! Tente novamente.\n")
