class Usuario:
    def __init__(self, username, senha, nome, sexo, idade, backup_codes):
        self.username = username
        self.senha = senha
        self.nome = nome
        self.sexo = sexo
        self.idade = idade
        self.backup_codes = backup_codes
        self.peso = 0.0
        self.altura = 0.0
        self.objetivo = "Não definido"
        self.nivel_treino = "iniciante"

    def atualizar_dados_fisicos(self, peso, altura):
        if peso > 0: self.peso = peso
        if 0.5 < altura < 3.0: self.altura = altura

    def definir_meta(self, objetivo, nivel_treino):
        self.objetivo = objetivo
        self.nivel_treino = nivel_treino