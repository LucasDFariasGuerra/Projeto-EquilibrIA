
print("===== MENU PRINCIPAL =====")
print("1 - Somar dois números")
print("2 - Subtrair dois números")
print("3 - Multiplicar dois números")
print("4 - Dividir dois números")
print("0 - Sair do programa")
print("===========================")

opcao = int(input("Escolha uma opção: "))

if opcao == 1:
    n1 = float(input("Digite o primeiro número: "))
    n2 = float(input("Digite o segundo número: "))
    print("Resultado da soma:", n1 + n2)

elif opcao == 2:
    n1 = float(input("Digite o primeiro número: "))
    n2 = float(input("Digite o segundo número: "))
    print("Resultado da subtração:", n1 - n2)

elif opcao == 3:
    n1 = float(input("Digite o primeiro número: "))
    n2 = float(input("Digite o segundo número: "))
    print("Resultado da multiplicação:", n1 * n2)

elif opcao == 4:
    n1 = float(input("Digite o primeiro número: "))
    n2 = float(input("Digite o segundo número: "))
    if n2 != 0:
        print("Resultado da divisão:", n1 / n2)
    else:
        p
