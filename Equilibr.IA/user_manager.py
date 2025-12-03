import random
import string
import time
import os
import smtplib 
from email.mime.text import MIMEText 
from dotenv import load_dotenv 
from utils import Utils
from models import Usuario
from database import BancoDeDados

load_dotenv()

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

    # --- CORREÇÃO DA VALIDAÇÃO DE SENHA ---
    def validar_senha(self, password):
        """Regras: Mínimo 6 chars, 1 maiúscula, 1 número."""
        if len(password) < 6:
            return False, "A senha deve ter no mínimo 6 caracteres."
        
        tem_numero = any(char.isdigit() for char in password)
        tem_maiuscula = any(char.isupper() for char in password)
        
        if not tem_numero:
            return False, "A senha deve conter pelo menos um número."
        
        if not tem_maiuscula:
            return False, "A senha deve conter pelo menos uma letra maiúscula."
            
        return True, "Senha válida."

    def validar_email(self, email):
        dominios_permitidos = ["@ufrpe.br", "@gmail.com"]
        for dominio in dominios_permitidos:
            if email.endswith(dominio):
                return True
        return False

    def _enviar_email_real(self, destinatario, codigo):
        remetente = os.getenv("EMAIL_REMETENTE")
        senha_app = os.getenv("EMAIL_SENHA")

        if not remetente or not senha_app:
            print(Utils.COR_ERRO + "ERRO: Credenciais de email não configuradas no arquivo .env")
            return False

        msg = MIMEText(f"Olá!\n\nSeu código de recuperação é:\n\n{codigo}\n\n(Válido para o Equilibr.IA)")
        msg['Subject'] = "Código de Recuperação - Equilibr.IA"
        msg['From'] = remetente
        msg['To'] = destinatario

        try:
            print(Utils.COR_AVISO + "Conectando ao servidor de email...")
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(remetente, senha_app)
            server.sendmail(remetente, destinatario, msg.as_string())
            server.quit()
            return True
        except Exception as e:
            print(Utils.COR_ERRO + f"Falha ao enviar email: {e}")
            return False

    def cadastrar_usuario(self):
        Utils.limpar_tela()
        print(Utils.COR_TITULO + "\n--- CADASTRO DE NOVO USUÁRIO ---")
        
        # 1. Login
        username = input("Nome de Usuário (Login): ").strip()
        if username in self.usuarios:
            print(Utils.COR_ERRO + "Usuário já existe.")
            return

        print("---")
        # 2. Email
        while True:
            email = input("Email (@ufrpe.br ou @gmail.com): ").strip().lower()
            if self.validar_email(email):
                email_existente = False
                for u in self.usuarios.values():
                    if u.email == email:
                        email_existente = True
                        break
                if email_existente:
                    print(Utils.COR_ERRO + "Este email já está cadastrado em outra conta.")
                else:
                    print(Utils.COR_SUCESSO + "Email válido!")
                    break 
            else:
                print(Utils.COR_ERRO + "Email inválido! Use um email UFRPE ou Gmail.")
        print("---")

        # 3. Senha (COM LOOP CORRIGIDO E CONFIRMAÇÃO)
        while True:
            print(Utils.COR_AVISO + "Requisitos: Mínimo 6 chars, 1 Número, 1 Letra Maiúscula.")
            senha = input("Crie sua Senha: ").strip()
            
            valida, msg = self.validar_senha(senha)
            if not valida:
                print(Utils.COR_ERRO + f"Erro: {msg}")
                continue # Volta para pedir a senha de novo

            confirma_senha = input("Confirme a Senha: ").strip()
            if senha != confirma_senha:
                print(Utils.COR_ERRO + "As senhas não coincidem. Tente novamente.")
                continue

            break # Sai do loop se tudo estiver certo

        # 4. Dados Pessoais
        nome = input("Nome Completo: ").strip()
        while True:
            sexo = input("Sexo (M/F): ").strip().upper()
            if sexo in ['M', 'F']: break
            print(Utils.COR_ERRO + "Digite M ou F.")
            
        while True:
            try:
                idade = int(input("Idade: "))
                if 0 < idade <= 100: break
                print(Utils.COR_ERRO + "Idade inválida.")
            except ValueError:
                print(Utils.COR_ERRO + "Digite um número.")

        print("\n" + Utils.COR_TITULO + "--- DADOS CORPORAIS ---")
        while True:
            try:
                peso = float(input("Peso (kg): "))
                altura = float(input("Altura (m): "))
                if (0 < peso <= 250) and (0.5 < altura <= 2.20): break
                print(Utils.COR_ERRO + "Valores fora do limite.")
            except ValueError:
                print(Utils.COR_ERRO + "Digite números.")

        objetivo = "manter peso" 
        nivel_treino = "iniciante"

        backup_codes = self._gerar_backup_codes()
        novo_usuario = Usuario(username, senha, nome, email, sexo, idade, backup_codes)
        novo_usuario.atualizar_dados_fisicos(peso, altura)
        novo_usuario.definir_meta(objetivo, nivel_treino)
        
        self.usuarios[username] = novo_usuario
        self._salvar_dados()
        
        print(Utils.COR_SUCESSO + "\nCadastro realizado!")
        print(f"Códigos de recuperação: {backup_codes}")

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

    def recuperar_senha(self):
        Utils.limpar_tela()
        print(Utils.COR_TITULO + "--- RECUPERAÇÃO DE SENHA ---")
        
        email_input = input("Digite seu email cadastrado: ").strip().lower()
        
        usuario_alvo = None
        for u in self.usuarios.values():
            if u.email == email_input:
                usuario_alvo = u
                break
        
        if not usuario_alvo:
            print(Utils.COR_ERRO + "Email não encontrado em nossa base.")
            return

        codigo_verificacao = "".join(random.choices(string.digits, k=6))
        
        if self._enviar_email_real(email_input, codigo_verificacao):
            print(Utils.COR_SUCESSO + f"Email enviado para {email_input}!")
            ultimo_envio = time.time()
        else:
            return

        tentativas = 3
        while tentativas > 0:
            print(f"\n{Utils.COR_AVISO}Tentativas restantes: {tentativas}")
            print("Digite o código recebido ou 'R' para Reenviar.")
            entrada = input("Código: ").strip().upper()

            if entrada == 'R':
                agora = time.time()
                tempo_passado = agora - ultimo_envio
                if tempo_passado < 20:
                    tempo_espera = int(20 - tempo_passado)
                    print(Utils.COR_ERRO + f"⏳ Aguarde {tempo_espera} segundos.")
                else:
                    print(Utils.COR_AVISO + "Gerando novo código...")
                    codigo_verificacao = "".join(random.choices(string.digits, k=6))
                    if self._enviar_email_real(email_input, codigo_verificacao):
                        print(Utils.COR_SUCESSO + "Novo código enviado!")
                        ultimo_envio = time.time()
                    else:
                        print(Utils.COR_ERRO + "Erro ao reenviar.")
                continue

            if entrada == codigo_verificacao:
                print(Utils.COR_SUCESSO + "✅ Código verificado!")
                
                # LOOP PARA NOVA SENHA
                while True:
                    print(Utils.COR_AVISO + "Requisitos: Mínimo 6 chars, 1 Número, 1 Maiúscula.")
                    nova_senha = input("Digite a nova senha: ").strip()
                    valida, msg = self.validar_senha(nova_senha)
                    
                    if valida:
                        confirma = input("Confirme a nova senha: ").strip()
                        if nova_senha == confirma:
                            usuario_alvo.senha = nova_senha
                            self._salvar_dados()
                            print(Utils.COR_SUCESSO + "Senha alterada! Faça login novamente.")
                            return
                        else:
                            print(Utils.COR_ERRO + "As senhas não coincidem.")
                    else:
                        print(Utils.COR_ERRO + f"Senha inválida: {msg}")
            else:
                print(Utils.COR_ERRO + "❌ Código incorreto.")
                tentativas -= 1

        print(Utils.COR_ERRO + "\nNúmero máximo de tentativas excedido.")

    def editar_usuario(self, usuario_logado):
        print(f"Editando perfil de {usuario_logado.nome}...")
        try:
            p = float(input(f"Novo Peso ({usuario_logado.peso}): ") or usuario_logado.peso)
            a = float(input(f"Nova Altura ({usuario_logado.altura}): ") or usuario_logado.altura)
            if p > 250 or a > 2.20:
                print(Utils.COR_ERRO + "Valores acima do permitido.")
                return
            usuario_logado.atualizar_dados_fisicos(p, a)
            self._salvar_dados()
            print(Utils.COR_SUCESSO + "Atualizado!")
        except ValueError:
            print(Utils.COR_ERRO + "Erro numérico.")

    def registrar_agua(self, usuario_logado):
        try:
            qtd = int(input(f"Qtd bebida (ml) [Já bebeu {usuario_logado.agua_hoje}]: "))
            usuario_logado.registrar_agua(qtd)
            self._salvar_dados()
            print(Utils.COR_SUCESSO + "Registrado!")
        except ValueError:
            print(Utils.COR_ERRO + "Valor inválido.")

    def excluir_usuario(self, usuario_logado):
        if input("Senha para confirmar: ") == usuario_logado.senha:
            del self.usuarios[usuario_logado.username]
            self._salvar_dados()
            print(Utils.COR_SUCESSO + "Excluído.")
            return True
        return False

    def salvar_plano_gerado(self, usuario_logado, dieta, treino):
        usuario_logado.salvar_plano_ia(dieta, treino)
        self._salvar_dados()