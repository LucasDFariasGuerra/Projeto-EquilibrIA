import utils

# A nossa "base de dados" em memória vive neste módulo.
usuarios = {}

def get_valid_input(prompt, valid_options):
    utils.limpar_tela()
    while True:
        value = input(prompt).strip().lower()
        if value in valid_options:
            return value
        print(utils.COR_ERRO + f"Opção inválida. Por favor, escolha uma das seguintes: {', '.join(valid_options)}")

def cadastrar_usuario():
    utils.limpar_tela()
    print(utils.COR_TITULO + "\n--- CADASTRO ---")
    
    while True:
        username = input("Crie um nome de usuário: ").strip()
        if not username:
            print(utils.COR_AVISO + "O nome de usuário não pode ser vazio.")
        elif username in usuarios:
            print(utils.COR_AVISO + "Este nome de usuário já existe. Tente outro.")
        else:
            break
    
    password = input("Crie uma senha: ").strip()
    nome_completo = input("Digite seu nome completo: ").strip()
    
    while True:
        sexo = input("Sexo (M/F): ").strip().upper()
        if sexo in ['M', 'F']:
            break
        else:
            print(utils.COR_ERRO + "Entrada inválida. Digite 'M' ou 'F'.")
    
    while True:
        try:
            idade = int(input("Idade (anos): ").strip())
            if 10 < idade < 120:
                break
            else:
                print(utils.COR_ERRO + "Idade deve ser um número entre 10 e 120.")
        except ValueError:
            print(utils.COR_ERRO + "Por favor, digite um número para a idade.")

    while True:
        try:
            peso = float(input("Peso em kg (ex: 75.5): ").strip())
            if peso > 0:
                break
            else:
                print(utils.COR_AVISO + "O peso deve ser maior que zero.")
        except ValueError:
            print(utils.COR_AVISO +"Por favor, digite um número válido para o peso.")
    
    while True:
        try:
            altura = float(input("Altura em metros (ex: 1.75): ").strip())
            if 0.5 < altura < 3.0:
                break
            else:
                print(utils.COR_AVISO +"A altura deve estar entre 0.5 e 3.0 metros.")
        except ValueError:
            print(utils.COR_AVISO +"Por favor, digite um número válido para a altura.")

    objetivo = get_valid_input(
        "Qual seu objetivo principal (perder gordura / manter peso / ganhar massa): ",
        ['perder gordura', 'manter peso', 'ganhar massa']
    )
    nivel_treino = get_valid_input(
        "Qual seu nível de treino (iniciante / intermediario / avancado): ",
        ['iniciante', 'intermediario', 'avancado']
    )
    
    usuarios[username] = {
        'senha': password,
        'nome': nome_completo,
        'sexo': sexo,
        'idade': idade,
        'peso': peso,
        'altura': altura,
        'objetivo': objetivo,
        'nivel_treino': nivel_treino
    }
    print(utils.COR_SUCESSO + f"\n✅ Usuário {username} cadastrado com sucesso!")

def verificar_login():
    utils.limpar_tela()
    print(utils.COR_TITULO + "\n--- ACESSAR CONTA ---")
    username = input("Digite o nome de usuário: ").strip()
    password = input("Digite a senha: ").strip()

    if username in usuarios and usuarios[username]['senha'] == password:
        print(utils.COR_SUCESSO + f"\n✅ Acesso liberado! Bem-vindo(a), {usuarios[username]['nome']}!")
        return username
    else:
        print(utils.COR_ERRO + "\n❌ Usuário ou senha incorretos.")
        return None

# Adicione esta função ao final de user_manager.py

def editar_usuario(username):
    utils.limpar_tela()
    if username not in usuarios:
        print(utils.COR_ERRO + "\n❌ Usuário não encontrado. Ocorreu um erro.")
        return

    print(utils.COR_TITULO + f"\n--- EDITANDO PERFIL DE {username} ---")
    print("(Pressione Enter para manter a informação atual)")

    user_data = usuarios[username]

    # Editar dados pessoais
    novo_nome = input(f"Nome completo ({user_data['nome']}): ").strip()
    if novo_nome:
        user_data['nome'] = novo_nome

    while True:
        novo_sexo = input(f"Sexo (M/F) ({user_data['sexo']}): ").strip().upper()
        if novo_sexo in ['M', 'F']:
            user_data['sexo'] = novo_sexo
            break
        elif not novo_sexo: # Se o usuário pressionar Enter
            break
        else:
            print(utils.COR_ERRO + "Entrada inválida. Digite 'M' ou 'F'.")

    # Editar dados físicos
    while True:
        try:
            nova_idade_str = input(f"Idade ({user_data['idade']}): ").strip()
            if not nova_idade_str:
                break
            nova_idade = int(nova_idade_str)
            if 10 < nova_idade < 120:
                user_data['idade'] = nova_idade
                break
            else:
                print(utils.COR_AVISO + "Idade deve ser um número entre 10 e 120.")
        except ValueError:
            print(utils.COR_AVISO + "Por favor, digite um número para a idade.")

    while True:
        try:
            novo_peso_str = input(f"Peso em kg ({user_data['peso']}): ").strip()
            if not novo_peso_str:
                break
            novo_peso = float(novo_peso_str)
            if novo_peso > 0:
                user_data['peso'] = novo_peso
                break
            else:
                print(utils.COR_AVISO + "O peso deve ser maior que zero.")
        except ValueError:
            print(utils.COR_AVISO +"Por favor, digite um número válido para o peso.")
            
    while True:
        try:
            nova_altura_str = input(f"Altura em metros ({user_data['altura']}): ").strip()
            if not nova_altura_str:
                break
            nova_altura = float(nova_altura_str)
            if 0.5 < nova_altura < 3.0:
                user_data['altura'] = nova_altura
                break
            else:
                print(utils.COR_AVISO + "A altura deve estar entre 0.5 e 3.0 metros.")
        except ValueError:
            print(utils.COR_AVISO + "Por favor, digite um número válido para a altura.")

    print(utils.COR_SUCESSO + "\n✅ Perfil atualizado com sucesso!")


def excluir_usuario():
    utils.limpar_tela()
    print(utils.COR_TITULO + "\n--- EXCLUIR PERFIL ---")
    username = input("Digite o nome de usuário que deseja excluir: ").strip()
    
    if username in usuarios:
        password = input("Confirme a senha para excluir: ").strip()
        if usuarios[username]['senha'] == password:
            del usuarios[username]
            print(utils.COR_SUCESSO + f"\n✅ Perfil de {username} excluído com sucesso.")
        else:
            print(utils.COR_ERRO + "\n❌ Senha incorreta. Exclusão cancelada.")
    else:
        print(utils.COR_ERRO + "\n❌ Usuário não encontrado.")