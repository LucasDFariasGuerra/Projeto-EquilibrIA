import google.generativeai as genai
from utils import Utils

# --- SUA CHAVE (QUE FUNCIONOU NO TESTE) ---
API_KEY = "AIzaSyDMff60jdApUbLa5NUvR9ctoGlq6yaNwGE" 

class GeradorSugestoes:
    
    @staticmethod
    def _consultar_ia(prompt):
        # Verificação de segurança simples
        if API_KEY == "SUA_CHAVE_NOVA_AQUI":
            print(Utils.COR_ERRO + "ERRO: Chave não configurada.")
            return None 

        try:
            genai.configure(api_key=API_KEY)
            
            # --- ATUALIZADO PARA O SEU MODELO DA LISTA ---
            # Usando o Gemini 2.0 Flash (Rápido e Moderno)
            model = genai.GenerativeModel('gemini-2.0-flash')
            
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            # Mostra o erro se houver (para sabermos o que corrigir)
            print(Utils.COR_ERRO + f"\n[ERRO DA IA]: {e}")
            return None

    @staticmethod
    def gerar_sugestao_dieta(tmb, peso, altura, idade, sexo, objetivo, nivel_treino):
        print(Utils.COR_AVISO + "Consultando Nutricionista IA (Gemini 2.0)...")

        prompt_dieta = (
            f"Atue como um nutricionista esportivo. "
            f"Crie um plano alimentar de 1 dia resumido para:\n"
            f"- Perfil: {sexo}, {idade} anos, {peso}kg, {altura}m\n"
            f"- TMB: {tmb:.0f} kcal | Nível: {nivel_treino}\n"
            f"- Objetivo: {objetivo}\n\n"
            f"Requisitos: Calcule macros. Liste apenas: Café, Almoço, Jantar e Lanche. Seja breve."
        )

        resposta_ia = GeradorSugestoes._consultar_ia(prompt_dieta)
        
        if resposta_ia:
            return f"\n✨ **SUGESTÃO GERADA POR IA (GEMINI 2.0)** ✨\n{resposta_ia}"

        # --- BACKUP (Caso falhe) ---
        print(Utils.COR_ERRO + ">> IA falhou. Usando cálculo padrão.")
        
        fatores = {'iniciante': 1.2, 'intermediario': 1.375, 'avancado': 1.55}
        fator_atividade = fatores.get(nivel_treino, 1.2)
        calorias_manutencao = tmb * fator_atividade

        if objetivo == 'perder gordura':
            calorias_alvo = calorias_manutencao - 400
            proteina = peso * 1.8
            gordura = (calorias_alvo * 0.30) / 9
        elif objetivo == 'ganhar massa':
            calorias_alvo = calorias_manutencao + 300
            proteina = peso * 2.0
            gordura = (calorias_alvo * 0.25) / 9
        else:
            calorias_alvo = calorias_manutencao
            proteina = peso * 1.6
            gordura = (calorias_alvo * 0.30) / 9

        carboidratos = (calorias_alvo - (proteina * 4) - (gordura * 9)) / 4

        return (
            f"\n**Sugestão Padrão ({objetivo.upper()})**\n"
            f"Calorias: {calorias_alvo:.0f} kcal\n"
            f"P: {proteina:.0f}g | C: {carboidratos:.0f}g | G: {gordura:.0f}g"
        )

    @staticmethod
    def gerar_sugestao_treino(nivel_treino, objetivo, idade):
        print(Utils.COR_AVISO + "Consultando Personal Trainer IA (Gemini 2.0)...")
        
        prompt_treino = (
            f"Atue como um personal trainer. "
            f"Crie um treino resumido para: {nivel_treino}, Objetivo: {objetivo}, Idade: {idade}.\n"
            f"Dê apenas a divisão (ex: ABC) e os exercícios principais."
        )

        resposta_ia = GeradorSugestoes._consultar_ia(prompt_treino)

        if resposta_ia:
            return f"\n✨ **TREINO GERADO POR IA (GEMINI 2.0)** ✨\n{resposta_ia}"

        # --- BACKUP ---
        if objetivo == 'perder gordura':
            txt = "Foco: Alta intensidade e Cardio (30min)."
        elif objetivo == 'ganhar massa':
            txt = "Foco: Hipertrofia e Carga."
        else:
            txt = "Foco: Manutenção e Saúde."

        return f"\n**Treino Padrão ({nivel_treino.upper()})**\n{txt}"