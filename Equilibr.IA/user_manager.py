import utils
import re 
import random 
import string 

# A nossa "base de dados" em memória vive neste módulo.
usuarios = {}

# Função auxiliar para gerar códigos de backup
def gerar_backup_codes(num_codes=3, code_length=6):
    """Gera uma lista de códigos de backup únicos de uso único."""
    # Usando letras maiúsculas e números para os códigos
    caracteres = string.ascii_uppercase + string.digits
    codes = set()
    while len(codes) < num_codes:
        code = ''.join(random.choices(caracteres, k=code_length))
        codes.add(code)
    return list(codes)

def get_valid_input(prompt, valid_options):
    utils.limpar_tela()
    while True:
        value = input(prompt).strip().lower()
        if value in valid_options:
            return value
        print(utils.COR_ERRO + f"Opção inválida. Por favor, escolha uma das seguintes: {', '.join(valid_options)}")

# Função auxiliar para validar a senha
def validar_senha(password):
    """
    Valida a senha:
    - Mínimo 4 e Máximo 22 caracteres.
    - Obrigatório ter pelo menos 1 número.
    - Obrigatório ter pelo menos 1 caractere especial.
    """
    if not (4 <= len(password) <= 22):
        return False, "A senha deve ter entre 4 e 22 caracteres."
    
    # Verifica se contém pelo menos um número (0-9)
    if not re.search(r'\d', password):
        return False, "A senha deve conter pelo menos um número."
    
    # Verifica se contém pelo menos um caractere especial (não-alfanumérico)
    if not re.search(r'[^\w\s]', password):
        return False, "A senha deve conter pelo menos um caractere especial (ex: !, @, #)."
        
    return True, ""

# NOVA FUNÇÃO: Força a troca de senha após uso de código de backup
def trocar_senha_forcada(username):
    user_data = usuarios[username]
    utils.limpar_tela()
    print(utils.COR_TITULO + "\n--- TROCA DE SENHA OBRIGATÓRIA ---")
    print(utils.COR_AVISO + "Seu login foi feito com um código de backup. Por favor, cadastre uma nova senha.")
    
    while True:
        nova_senha = input("Crie sua nova senha: ").strip()
        valida, mensagem_erro = validar_senha(nova_senha)
        if valida:
            # Salva a nova senha
            user_data['senha'] = nova_senha
            print(utils.COR_SUCESSO + "\n✅ Senha alterada com sucesso! Seu acesso está seguro.")
            break
        else:
            print(utils.COR_AVISO + f"❌ Senha fraca ou inválida: {mensagem_erro}")
            print(utils.COR_AVISO + "Requisitos: 4-22 caracteres, 1 número, 1 caractere especial.")
            
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
    
    # Solicitar e validar Email com domínio @ufrpe.br
    while True:
        email = input("Digite seu Email (@ufrpe.br obrigatório): ").strip()
        # Regex para garantir que o email tem caracteres antes do @ e termina exatamente com @ufrpe.br
        if re.fullmatch(r"[\w\.-]+@ufrpe\.br$", email):
            break
        else:
            print(utils.COR_AVISO + "❌ Email inválido. O domínio deve ser @ufrpe.br.")

    # Validação de Senha 
    while True:
        password = input("Crie uma senha: ").strip()
        valida, mensagem_erro = validar_senha(password)
        if valida:
            break
        else:
            print(utils.COR_AVISO + f"❌ Senha fraca ou inválida: {mensagem_erro}")
            print(utils.COR_AVISO + "Requisitos: 4-22 caracteres, 1 número, 1 caractere especial.")

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
    
    # Geração dos Backup Codes
    backup_codes = gerar_backup_codes()
    
    usuarios[username] = {
        'senha': password,
        'email': email, 
        'backup_codes': backup_codes, 
        'nome': nome_completo,
        'sexo': sexo,
        'idade': idade,
        'peso': peso,
        'altura': altura,
        'objetivo': objetivo,
        'nivel_treino': nivel_treino
    }
    
    print(utils.COR_SUCESSO + f"\n✅ Usuário {username} cadastrado com sucesso!")
    print(utils.COR_TITULO + "\n*** CÓDIGOS DE BACKUP ***")
    print(utils.COR_AVISO + "GUARDE ESTES CÓDIGOS EM LOCAL SEGURO! Eles servem para login único caso esqueça a senha.")
    for code in backup_codes:
         print(f"- {code}")
    print(utils.COR_TITULO + "***************************")

# FUNÇÃO VERIFICAR LOGIN REESTRUTURADA
def verificar_login():
    utils.limpar_tela()
    print(utils.COR_TITULO + "\n--- ACESSAR CONTA ---")
    username = input("Digite o nome de usuário: ").strip()

    if username not in usuarios:
        print(utils.COR_ERRO + "\n❌ Usuário não encontrado.")
        return None

    user_data = usuarios[username]
    
    # 1. TENTATIVA DE LOGIN COM SENHA NORMAL (ÚNICA OPÇÃO INICIAL)
    password = input("Digite sua senha: ").strip()
    
    if user_data['senha'] == password:
        print(utils.COR_SUCESSO + f"\n✅ Acesso liberado! Bem-vindo(a), {user_data['nome']}!")
        return username
    
    # 2. SENHA INCORRETA -> LIBERAR "ESQUECI A SENHA"
    else:
        print(utils.COR_ERRO + "\n❌ Senha incorreta.")
        
        # Verifica se ainda há códigos de backup para oferecer a opção
        if not user_data.get('backup_codes'):
            print(utils.COR_AVISO + "Você não possui códigos de backup restantes.")
            return None
        
        # Pergunta sobre "Esqueci a Senha"
        usa_backup = input("Esqueceu a senha? Deseja tentar com um Código de Backup? (S/N): ").strip().upper()
        
        if usa_backup == 'S':
            print(utils.COR_AVISO + f"Você tem {len(user_data['backup_codes'])} códigos de backup restantes.")
            backup_code = input("Digite um Código de Backup: ").strip()
            
            # Tenta logar com Código de Backup
            if backup_code in user_data['backup_codes']:
                # O código é de uso único, então é removido
                user_data['backup_codes'].remove(backup_code)
                
                print(utils.COR_SUCESSO + f"\n✅ Login bem-sucedido com Código de Backup! Bem-vindo(a), {user_data['nome']}!")
                print(utils.COR_AVISO + f"⚠️ O código de backup usado foi invalidado.")
                
                # CHAMA A FUNÇÃO DE TROCA DE SENHA OBRIGATÓRIA
                trocar_senha_forcada(username)
                
                return username 
                
            else:
                print(utils.COR_ERRO + "\n❌ Código de Backup inválido ou já utilizado.")
                return None
        else:
            return None # Usuário errou a senha e não quer usar o backup code


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

    # Edição de Email
    while True:
        novo_email_str = input(f"Email (@ufrpe.br obrigatório) ({user_data['email']}): ").strip()
        if not novo_email_str: # Usuário pressionou Enter
            break
        # Regex para garantir que o email tem caracteres antes do @ e termina exatamente com @ufrpe.br
        if re.fullmatch(r"[\w\.-]+@ufrpe\.br$", novo_email_str):
            user_data['email'] = novo_email_str
            break
        else:
            print(utils.COR_AVISO + "❌ Email inválido. O domínio deve ser @ufrpe.br.")


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
    # Conteúdo da função excluir_usuario (sem alterações)
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