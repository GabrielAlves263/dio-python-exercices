menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    opcao = str(input(menu)).lower()[0]
    
    if opcao == "d":
        valor = float(input("Insira o valor para depositar: R$"))
        if valor > 0:
            saldo += valor
            extrato += f"Depósito no valor de R${valor:.2f}\n"
            print("\033[32mValor depositado com sucesso!\033[m")

        else:
            print("\033[33mNão foi possível realizar o depósito, valor inválido!\033[m")

    elif opcao == "s":
        if numero_saques >= LIMITE_SAQUES:
            print("\033[33mLimite de saques excedido!\033[m")
        else:
            valor = float(input("Insira o valor para sacar: R$"))

            if valor < 0:
                print("\033[33mValor inválido!\033[m")
            elif valor > limite:
                print("\033[33mValor acima do limite de saque!\033[m")
            elif valor > saldo:
                print("\033[33mSaldo insuficiente!\033[m")
            else:
                saldo -= valor
                numero_saques += 1
                extrato += f"Saque no valor de R${valor:.2f}\n"
                print("\033[32mSaque realizado com sucesso!\033[m")

    elif opcao == "e":
        print(extrato)
        print(f"Saldo atual: R${saldo:.2f}")

    elif opcao == "q":
        print("Saindo do sistema...")
        exit()
    
    else:
        print("\033[31mOperação inválida!\033[m")