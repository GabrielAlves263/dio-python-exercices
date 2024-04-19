from abc import ABC, abstractmethod

class Transacao(ABC):

    @abstractmethod
    def registrar(conta):
        pass

class Historico:
    
    transacoes = []

    def adicionar_transacoes(self, transacao: Transacao):
        self.transacoes.append(transacao)

    def __str__(self) -> str:
        return f"Transações:\n{'\n'.join([f'{trancacao.__class__.__name__}={trancacao.valor}' for trancacao in self.transacoes])}"

class Conta():
    _saldo = 0.0
    agencia = 1
    historico = Historico()

    def __init__(self, numero) -> None:
        self.numero = numero

    @property
    def saldo(self) -> float:
        return self._saldo or 0
    
    @classmethod
    def nova_conta(cls, numero):
        return cls(numero)
    
    def _sacar(self, valor) -> bool:
        if(self._saldo >= valor):
            self._saldo -= valor
            return True
        return False
    
    def _depositar(self, valor):
        self._saldo += valor
        return True

class ContaCorrente(Conta):
    
    def __init__(self, numero, limite, limite_saques) -> None:
        super().__init__(numero)
        self.limite = limite
        self.limite_saques = limite_saques

    def _sacar(self, valor):
        if(valor <= self._saldo and valor <= self.limite and self.limite_saques > 0):
            self._saldo -= valor
            self.limite_saques -= 1
            return True
        
        return False
    
class Cliente():
    contas = []

    def __init__(self, endereco) -> None:
        self.endereco = endereco

    def realizar_transacao(self, conta: Conta, transacao: Transacao):
        if(conta in self.contas):
            transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):

    def __init__(self, endereco, cpf, nome, data_nascimento) -> None:
        super().__init__(endereco)
        self.cpf= cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

class Saque(Transacao):
    
    def __init__(self, valor) -> None:
        self.valor = valor

    def registrar(self, conta: Conta):
        if(conta._sacar(self.valor)):
            conta.historico.adicionar_transacoes(self)

class Deposito(Transacao):
    
    def __init__(self, valor) -> None:
        self.valor = valor

    def registrar(self, conta: Conta):
        if(conta._depositar(self.valor)):
            conta.historico.adicionar_transacoes(self)

usuarios = []
contas = []
COUNT = 0

def verificar_usuario(cpf) -> PessoaFisica:
    for u in usuarios:
        if cpf == u.cpf:
            return u
    
    return None

def criar_usuario():
    nome = input("Nome: ")
    nasc = input("Data de nascimento: ")
    cpf = int(input("CPF: "))
    end = input("Endereço: ")

    usuario = PessoaFisica(end, cpf, nome, nasc)


    if verificar_usuario(usuario.cpf) == None:
        usuarios.append(usuario)
        print("\033[32mUsuário criado!\033[m")
    else:
        print(f"\033[33mUsuário com cpf {cpf} já existe!\033[m")

def criar_conta(COUNT):
    cpf = int(input("CPF do titular: "))

    usuario = verificar_usuario(cpf)
    if usuario == None:
        print(f"\033[31mUsuário com CPF: {cpf} não existe!\033[m")
    else:
        conta = ContaCorrente(COUNT, 500, 3)
        contas.append(conta)
        COUNT += 1
        usuario.adicionar_conta(conta)
        print(f"\033[32mConta {COUNT} criada com sucesso!\033[m")


def main():
    menu = """

    [u] Criar usuário
    [c] Criar conta corrente
    [p] Selecionar conta
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [q] Sair

    => """

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
            valor = float(input("Insira o valor para depositar: R$"))
            cliente : PessoaFisica = usuarios[-1]
            conta : Conta = contas[-1]
            cliente.realizar_transacao(conta, Deposito(valor))

        elif opcao == "s":
            valor = float(input("Insira o valor para sacar: R$"))
            cliente : PessoaFisica = usuarios[-1]
            conta : Conta = contas[-1]
            cliente.realizar_transacao(conta, Saque(valor))

        elif opcao == "e":
            print(contas[-1].historico)

        elif opcao == "q":  
            print("Saindo do sistema...")
            exit()
        else:
            print("\033[31mOperação inválida!\033[m")


if __name__ == "__main__":
    main()