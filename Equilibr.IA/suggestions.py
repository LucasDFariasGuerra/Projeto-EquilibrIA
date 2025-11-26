from utils import Utils

class GeradorSugestoes:
    @staticmethod
    def gerar_sugestao_dieta(tmb, peso, objetivo, nivel_treino):
        Utils.limpar_tela()
        if tmb <= 0 or peso <= 0:
            return Utils.COR_ERRO + "Dados insuficientes para calcular a dieta."

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
            return "Objetivo não reconhecido."

        carboidratos = (calorias_alvo - (proteina * 4) - (gordura * 9)) / 4

        return (
            f"**Sugestão de Dieta ({objetivo.upper()})**\n"
            f"Calorias Totais: {calorias_alvo:.0f} kcal\n"
            f"Macronutrientes:\n"
            f" - Proteínas: {proteina:.0f}g\n"
            f" - Carboidratos: {carboidratos:.0f}g\n"
            f" - Gorduras: {gordura:.0f}g"
        )

    @staticmethod
    def gerar_sugestao_treino(nivel, objetivo):
        if nivel == 'iniciante':
            return "Plano Iniciante: Foco em adaptação e execução correta..."
        elif nivel == 'intermediario':
            return "Plano Intermediário: Aumento de volume e cargas..."
        return "Plano Avançado: Foco em periodização e técnicas avançadas..."