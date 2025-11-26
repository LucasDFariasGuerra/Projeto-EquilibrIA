class CalculadoraSaude:
    @staticmethod
    def calcular_imc(peso, altura):
        """Calcula o Índice de Massa Corporal (IMC)."""
        if altura <= 0:
            return 0
        return peso / (altura * altura)

    @staticmethod
    def calcular_tmb(sexo, peso, altura, idade):
        """Calcula a Taxa Metabólica Basal (TMB) - Mifflin-St Jeor."""
        if peso <= 0 or altura <= 0:
            return 0
            
        altura_cm = altura * 100
        base = (10 * peso) + (6.25 * altura_cm) - (5 * idade)
        
        if sexo.upper() == 'M':
            return base + 5
        else:
            return base - 161