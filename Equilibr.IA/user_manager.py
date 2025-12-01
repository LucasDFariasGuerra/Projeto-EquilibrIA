import random
import string
from utils import Utils
from models import Usuario
from database import BancoDeDados

class GerenciadorUsuarios:
    def __init__(self):
        self.usuarios = {} 
        self._carregar_dados()

    def _carregar_dados(self):
        dados_brutos = BancoDeDados.carregar_dados()
        for username, dados_dict in dados_brutos.items():
            self.usuarios[username] = Usuario.from_dict(dados_dict)

    def _salvar_dados(self):
        BancoDeDados.salvar_dados(self.usuarios)

    def _gerar_backup_codes(self, num_codes=4, code_length=6):
        caracteres = string.ascii_uppercase + string.digits
        codes = set()
        while len(codes) < num_codes:
            code = ''.join(random.choices(caracteres, k=code_length))
            codes.add(code)
        return list(codes)

    def validar_senha(self, password):
        if not (4 <= len(password) <= 22):
            return False, "A senha deve ter entre 4 e 22 caracteres."
        return True, "Senha válida."

    def cadastrar_usuario(self):
        Utils.limpar_tela()
        print(Utils.COR_TITULO + "\n--- CADASTRO DE NOVO USUÁRIO ---")
        
        # 1. Dados de Acesso
        username = input("Nome de Usuário: ").strip()
        if username in self.usuarios:
            print(Utils.COR_ERRO + "Usuário já existe.")
            return

        senha = input("Senha: ").strip()
        valida, msg = self.validar_senha(senha)
        if not valida:
            print(Utils.COR_ERRO + msg)
            return

        # 2. Dados Pessoais
        nome = input("Nome Completo: ").strip()
        
        while True:
            sexo = input("Sexo (M/F): ").strip().upper()
            if sexo in ['M', 'F']: break
            print(Utils.COR_ERRO + "Digite M ou F.")
            
        while True:
            try:
                idade = int(input("Idade: "))
                # LIMITAÇÃO DE IDADE: 0 a 100 anos
                if 0 < idade <= 100: 
                    break
                print(Utils.COR_ERRO + "Idade inválida (Máximo: 100 anos).")
            except ValueError:
                print(Utils.COR_ERRO + "Digite um número inteiro.")

        # 3. Dados Físicos (OBRIGATÓRIO)
        print("\n" + Utils.COR_TITULO + "--- DADOS CORPORAIS E METAS ---")
        
        while True:
            try:
                peso = float(input("Peso atual (kg): "))
                altura = float(input("Altura (m) (ex: 1.75): "))
                
                # LIMITAÇÃO DE PESO (250kg) E ALTURA (2.20m)
                if (0 < peso <= 250) and (0.5 < altura <= 2.20): 
                    break
                
                print(Utils.COR_ERRO + "Valores fora do limite (Max Peso: 250kg, Max Altura: 2.20m).")
            except ValueError:
                print(Utils.COR_ERRO + "Digite apenas números (use ponto para decimais).")

        print("\nEscolha seu Objetivo:")
        print("1. Perder Gordura")
        print("2. Ganhar Massa")
        print("3. Manter Peso")
        op_obj = input("Opção: ")
        mapa_obj = {'1': 'perder gordura', '2': 'ganhar massa', '3': 'manter peso'}
        objetivo = mapa_obj.get(op_obj, 'manter peso')

        print("\nNível de Experiência em Treino:")
        print("1. Iniciante")
        print("2. Intermediário")
        print("3. Avançado")
        op_treino = input("Opção: ")
        mapa_treino = {'1': 'iniciante', '2': 'intermediario', '3': 'avancado'}
        nivel_treino = mapa_treino.get(op_treino, 'iniciante')

        # Criação do Objeto
        backup_codes = self._gerar_backup_codes()
        novo_usuario = Usuario(username, senha, nome, sexo, idade, backup_codes)
        
        novo_usuario.atualizar_dados_fisicos(peso, altura)
        novo_usuario.definir_meta(objetivo, nivel_treino)
        
        self.usuarios[username] = novo_usuario
        self._salvar_dados()
        
        print(Utils.COR_SUCESSO + "\nCadastro realizado com sucesso!")
        print(f"Seus códigos de recuperação: {backup_codes}")

    def autenticar(self):
        print(Utils.COR_TITULO + "\n--- LOGIN ---")
        username = input("Usuário: ").strip()
        senha = input("Senha: ").strip()

        usuario = self.usuarios.get(username)
        
        if usuario and usuario.senha == senha:
            print(Utils.COR_SUCESSO + f"Bem-vindo, {usuario.nome}!")
            return usuario
        else:
            print(Utils.COR_ERRO + "Credenciais inválidas.")
            return None

    def editar_usuario(self, usuario_logado):
        print(f"Editando perfil de {usuario_logado.nome}...")
        try:
            print(f"Peso atual: {usuario_logado.peso}kg | Altura atual: {usuario_logado.altura}m")
            
            
            novo_peso_str = input("Novo Peso (Enter para manter): ")
            nova_altura_str = input("Nova Altura (Enter para manter): ")
            
            p = float(novo_peso_str) if novo_peso_str else usuario_logado.peso
            a = float(nova_altura_str) if nova_altura_str else usuario_logado.altura
            
            
            if p > 250 or a > 2.20:
                print(Utils.COR_ERRO + "Valores acima do permitido (Max: 250kg, 2.20m). Alteração cancelada.")
                return

            usuario_logado.atualizar_dados_fisicos(p, a)
            self._salvar_dados()
            
            print(Utils.COR_SUCESSO + "Dados atualizados!")
        except ValueError:
            print(Utils.COR_ERRO + "Erro nos valores numéricos.")

    def registrar_agua(self, usuario_logado):
        print(f"\nMeta diária: {usuario_logado.meta_agua:.0f} ml")
        print(f"Já bebeu: {usuario_logado.agua_hoje} ml")
        try:
            qtd = int(input("Qtd bebida agora (ml): "))
            usuario_logado.registrar_agua(qtd)
            self._salvar_dados()
            print(Utils.COR_SUCESSO + "Hidratação registrada!")
        except ValueError:
            print(Utils.COR_ERRO + "Valor inválido.")

    def excluir_usuario(self, usuario_logado):
        confirmacao = input("Digite sua senha para confirmar a exclusão: ")
        if confirmacao == usuario_logado.senha:
            del self.usuarios[usuario_logado.username]
            self._salvar_dados()
            print(Utils.COR_SUCESSO + "Perfil excluído.")
            return True
        else:
            print(Utils.COR_ERRO + "Senha incorreta.")
            return False