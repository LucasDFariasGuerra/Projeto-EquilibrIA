from datetime import datetime

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
        
        self.agua_hoje = 0
        self.meta_agua = 0
        self.historico_peso = []

    def atualizar_dados_fisicos(self, peso, altura):
        """Atualiza dados se estiverem dentro dos limites realistas."""
        mudou_peso = False
        
        # Limite de Peso: Até 250kg
        if 0 < peso <= 250: 
            self.peso = peso
            self.meta_agua = peso * 35 
            mudou_peso = True
            
        # Limite de Altura: Até 2.20m
        if 0.5 < altura <= 2.20: 
            self.altura = altura

        if mudou_peso and self.peso > 0:
            data_atual = datetime.now().strftime("%d/%m/%Y")
            if self.historico_peso and self.historico_peso[-1]['data'] == data_atual:
                self.historico_peso[-1]['peso'] = self.peso
            else:
                self.historico_peso.append({'data': data_atual, 'peso': self.peso})

    def definir_meta(self, objetivo, nivel_treino):
        self.objetivo = objetivo
        self.nivel_treino = nivel_treino

    def registrar_agua(self, ml):
        if ml > 0:
            self.agua_hoje += ml

    def to_dict(self):
        return {
            "username": self.username, "senha": self.senha, "nome": self.nome,
            "sexo": self.sexo, "idade": self.idade, "backup_codes": self.backup_codes,
            "peso": self.peso, "altura": self.altura, "objetivo": self.objetivo,
            "nivel_treino": self.nivel_treino, "agua_hoje": self.agua_hoje,
            "meta_agua": self.meta_agua, "historico_peso": self.historico_peso
        }

    @classmethod
    def from_dict(cls, data):
        user = cls(
            data['username'], data['senha'], data['nome'], 
            data['sexo'], data['idade'], data['backup_codes']
        )
        user.peso = data.get('peso', 0.0)
        user.altura = data.get('altura', 0.0)
        user.objetivo = data.get('objetivo', "Não definido")
        user.nivel_treino = data.get('nivel_treino', "iniciante")
        user.agua_hoje = data.get('agua_hoje', 0)
        user.meta_agua = data.get('meta_agua', 0)
        user.historico_peso = data.get('historico_peso', [])
        return user