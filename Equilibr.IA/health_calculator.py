def calcular_imc(peso, altura):
    """Calcula o Índice de Massa Corporal (IMC)."""
    if altura == 0:
        return 0
    return peso / (altura * altura)

def calcular_tmb(sexo, peso, altura, idade):
    """Calcula a Taxa Metabólica Basal (TMB) usando a fórmula de Mifflin-St Jeor."""
    altura_cm = altura * 100
    if sexo.upper() == 'M':
        # Fórmula para homens
        tmb = (10 * peso) + (6.25 * altura_cm) - (5 * idade) + 5
    else: 
        # Fórmula para mulheres
        tmb = (10 * peso) + (6.25 * altura_cm) - (5 * idade) - 161
    return tmb