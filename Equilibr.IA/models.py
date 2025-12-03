from datetime import datetime

class Usuario:
    def __init__(self, username, senha, nome, email, sexo, idade, backup_codes):
        self.username = username
        self.senha = senha
        self.nome = nome
        self.email = email  # NOVO CAMPO
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

        self.plano_dieta = "Nenhum plano gerado ainda."
        self.plano_treino = "Nenhum plano gerado ainda."
        self.data_plano = None

    def atualizar_dados_fisicos(self, peso, altura):
        mudou_peso = False
        if 0 < peso <= 250: 
            self.peso = peso
            self.meta_agua = peso * 35 
            mudou_peso = True
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
        if ml > 0: self.agua_hoje += ml

    def salvar_plano_ia(self, texto_dieta, texto_treino):
        self.plano_dieta = texto_dieta
        self.plano_treino = texto_treino
        self.data_plano = datetime.now().strftime("%d/%m/%Y")

    def dias_sem_atualizar_peso(self):
        if not self.historico_peso:
            return 0
        ultima_data_str = self.historico_peso[-1]['data']
        ultima_data_obj = datetime.strptime(ultima_data_str, "%d/%m/%Y")
        agora = datetime.now()
        diferenca = agora - ultima_data_obj
        return diferenca.days

    def to_dict(self):
        return {
            "username": self.username, "senha": self.senha, "nome": self.nome,
            "email": self.email, # SALVANDO EMAIL
            "sexo": self.sexo, "idade": self.idade, "backup_codes": self.backup_codes,
            "peso": self.peso, "altura": self.altura, "objetivo": self.objetivo,
            "nivel_treino": self.nivel_treino, "agua_hoje": self.agua_hoje,
            "meta_agua": self.meta_agua, "historico_peso": self.historico_peso,
            "plano_dieta": self.plano_dieta, "plano_treino": self.plano_treino,
            "data_plano": self.data_plano
        }

    @classmethod
    def from_dict(cls, data):
        # O .get('email', '') garante que usuários antigos sem email não quebrem o sistema
        user = cls(
            data['username'], data['senha'], data['nome'], 
            data.get('email', 'sem_email@sistema'), # RECUPERANDO EMAIL
            data['sexo'], data['idade'], data['backup_codes']
        )
        user.peso = data.get('peso', 0.0)
        user.altura = data.get('altura', 0.0)
        user.objetivo = data.get('objetivo', "Não definido")
        user.nivel_treino = data.get('nivel_treino', "iniciante")
        user.agua_hoje = data.get('agua_hoje', 0)
        user.meta_agua = data.get('meta_agua', 0)
        user.historico_peso = data.get('historico_peso', [])
        user.plano_dieta = data.get('plano_dieta', "Nenhum plano gerado ainda.")
        user.plano_treino = data.get('plano_treino', "Nenhum plano gerado ainda.")
        user.data_plano = data.get('data_plano', None)
        return user