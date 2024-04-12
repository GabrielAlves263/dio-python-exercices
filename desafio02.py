menu = """

[u] Criar usuário
[c] Criar conta corrente
[p] Selecionar conta
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

COUNT = 1

usuarios = []
conta_selecionada = None
contas = []

conta = {
    "saldo": 0,
    "limite": 500,
    "extrato": "",
    "numero_saques": 0,
    "LIMITE_SAQUES": 3
}

def verificar_usuario(cpf):
    for u in usuarios:
        if cpf == u.get("cpf"):
            return False
    
    return True

def criar_usuario():
    nome = input("Nome: ")
    nasc = input("Data de nascimento: ")
    cpf = int(input("CPF: "))
    end = input("Endereço: ")

    usuario = {"nome": nome, "nascimento": nasc, "cpf": cpf, "endereco": end}


    if verificar_usuario(usuario.get("cpf")):
        usuarios.append(usuario)
        print("\033[32mUsuário criado!\033[m")
    else:
        print(f"\033[33mUsuário com cpf {cpf} já existe!\033[m")

def criar_conta(COUNT):
    cpf = int(input("CPF do titular: "))

    if verificar_usuario(cpf):
        print(f"\033[31mUsuário com CPF: {cpf} não existe!\033[m")
    else:
        conta = {
            "agencia": "0001",
            "conta": COUNT,
            "cpf_titular": cpf,
            "saldo": 0,
            "limite": 500,
            "extrato": "",
            "numero_saques": 0,
            "LIMITE_SAQUES": 3}
        contas.append(conta)
        COUNT += 1
        print(f"\033[32mConta {COUNT} criada com sucesso!\033[m")

def depositar(conta, /):
    valor = float(input("Insira o valor para depositar: R$"))
    if valor > 0:
        conta["saldo"] += valor
        conta["extrato"] += f"Depósito no valor de R${valor:.2f}\n"
        return ("\033[32mValor depositado com sucesso!\033[m")
    else:
            return ("\033[33mNão foi possível realizar o depósito, valor inválido!\033[m")

def sacar(*, conta):
    if conta["numero_saques"] >= conta["LIMITE_SAQUES"]:
        return ("\033[33mLimite de saques excedido!\033[m")
    else:
        valor = float(input("Insira o valor para sacar: R$"))

        if valor < 0:
            return ("\033[33mValor inválido!\033[m")
        elif valor > conta["limite"]:
            return ("\033[33mValor acima do limite de saque!\033[m")
        elif valor > conta["saldo"]:
            return ("\033[33mSaldo insuficiente!\033[m")
        else:
            conta["saldo"] -= valor
            conta["numero_saques"] += 1
            conta["extrato"] += f"Saque no valor de R${valor:.2f}\n"
            return ("\033[32mSaque realizado com sucesso!\033[m")

def imprimir_extrato(conta):
    print(conta["extrato"])
    print(f"Saldo atual: R${conta["saldo"]:.2f}")


def sair():
    print("Saindo do sistema...")
    print(usuarios, "\n", contas)
    exit()

while True:

    try:
        opcao = str(input(menu)).lower()[0]
    except:
        opcao = ""
    
    if opcao == "u":
        criar_usuario()

    elif opcao == "c":
        criar_conta(COUNT)

    elif opcao == "d":
        print(depositar(conta))

    elif opcao == "s":
        print(sacar(conta=conta))

    elif opcao == "e":
        imprimir_extrato(conta)

    elif opcao == "q":
        sair()
    else:
        print("\033[31mOperação inválida!\033[m")