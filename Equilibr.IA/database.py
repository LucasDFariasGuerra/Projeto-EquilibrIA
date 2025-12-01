import json
import os

class BancoDeDados:
    ARQUIVO_DB = "usuarios.json"

    @staticmethod
    def salvar_dados(usuarios_dict):
        dados_para_salvar = {}
        for username, obj_usuario in usuarios_dict.items():
            dados_para_salvar[username] = obj_usuario.to_dict()
        try:
            with open(BancoDeDados.ARQUIVO_DB, 'w', encoding='utf-8') as f:
                json.dump(dados_para_salvar, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Erro DB: {e}")
            return False

    @staticmethod
    def carregar_dados():
        if not os.path.exists(BancoDeDados.ARQUIVO_DB):
            return {}
        try:
            with open(BancoDeDados.ARQUIVO_DB, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}