# user_manager.py
import random
import string
from utils import Utils
from models import Usuario

class GerenciadorUsuarios:
    def __init__(self):
        # Simulação de banco de dados em memória
        # Em POO, atributos privados (self.usuarios) protegem os dados
        self.usuarios = {} 

    def _gerar_backup_codes(self, num_codes=4, code_length=6):
        """Método interno (protegido) para gerar códigos."""
        caracteres = string.ascii_uppercase + string.digits
        codes = set()
        while len(codes) < num_codes:
            code = ''.join(random.choices(caracteres, k=code_length))
            codes.add(code)
        return list(codes)

    def validar_senha(self, password):
        if not (4 <= len(password) <= 22):
            return False, "A senha deve ter entre 4 e 22 caracteres."
        # Adicione aqui suas outras verificações de regex se necessário
        return True, "Senha válida."

    def cadastrar_usuario(self):
        Utils.limpar_tela()
        print(Utils.COR_TITULO + "\n--- CADASTRO ---")
        
        username = input("Nome de Usuário: ").strip()
        if username in self.usuarios:
            print(Utils.COR_ERRO + "Usuário já existe.")
            return

        senha = input("Senha: ").strip()
        valida, msg = self.validar_senha(senha)
        if not valida:
            print(Utils.COR_ERRO + msg)
            return

        nome = input("Nome Completo: ").strip()
        sexo = input("Sexo (M/F): ").strip().upper()
        
        try:
            idade = int(input("Idade: "))
        except ValueError:
            print(Utils.COR_ERRO + "Idade inválida.")
            return

        backup_codes = self._gerar_backup_codes()
        
        # Criação do OBJETO Usuario
        novo_usuario = Usuario(username, senha, nome, sexo, idade, backup_codes)
        
        # Persistência na memória
        self.usuarios[username] = novo_usuario
        
        print(Utils.COR_SUCESSO + "Usuário cadastrado com sucesso!")
        print(f"Códigos de recuperação: {backup_codes}")

    def autenticar(self):
        print(Utils.COR_TITULO + "\n--- LOGIN ---")
        username = input("Usuário: ").strip()
        senha = input("Senha: ").strip()

        usuario = self.usuarios.get(username)
        
        if usuario and usuario.senha == senha:
            print(Utils.COR_SUCESSO + f"Bem-vindo, {usuario.nome}!")
            return usuario  # Retorna o OBJETO usuário logado
        else:
            print(Utils.COR_ERRO + "Credenciais inválidas.")
            return None

    def editar_usuario(self, usuario_logado):
        # Recebe o objeto usuario_logado diretamente
        print(f"Editando perfil de {usuario_logado.nome}...")
        # Lógica de input para novos dados...
        try:
            novo_peso = float(input(f"Novo Peso ({usuario_logado.peso}): "))
            nova_altura = float(input(f"Nova Altura ({usuario_logado.altura}): "))
            usuario_logado.atualizar_dados_fisicos(novo_peso, nova_altura)
            print(Utils.COR_SUCESSO + "Dados atualizados!")
        except ValueError:
            print(Utils.COR_ERRO + "Erro nos valores numéricos.")

    def excluir_usuario(self, usuario_logado):
        confirmacao = input("Digite sua senha para confirmar a exclusão: ")
        if confirmacao == usuario_logado.senha:
            del self.usuarios[usuario_logado.username]
            print(Utils.COR_SUCESSO + "Conta excluída.")
            return True # Indica que a exclusão ocorreu
        return False