import textwrap
from abc import ABC, abstractclassmethod, abstractproperty, abstractmethod
from datetime import datetime
from time import sleep

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = '0001'
        self._cliente = cliente
        self._historico = Historico()


    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print('\n@@@ Operação falhou! Você não tem saldo suficiente. @@@')

        elif valor > 0:
            self._saldo -= valor
            print('\n=== Saque realizado com sucesso!===')
            return True

        else:
            print('\n@@@ Operação falhou! O valor informado é inválido. @@@')
        
        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print('\n=== Deposito realizado com sucesso! ===')

        else:
            print('\n@@@ Operação falhou! O valor informado é valálido. @@@')
            return False

        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao['tipo'] == Saque.__name__])

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print('\n@@@ Operação falhou! O valor do saque excede o limite. @@@')

        elif excedeu_saques:
            print('\n@@@ Operação falhou! Número máximo de saques excedido. @@@')

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f'''\
            Agência: \t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome} 
        '''


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            'tipo': transacao.__class__.__name__,
            'valor': transacao.valor,
            'data': datetime.now().strftime('%d-%m-%y %H:%M:%S'),
        })



class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self,valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self,conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


def menu():
    menu = '''\n  !!!Bem vindo ao caixa Rapido!!!
===============MENU================ 
!                                 !
!        D  - Deposito            !
!        S  - Saque               !
!        E  - Extrato             !
!        NC - Nova conta          !
!        LC - Lista de Contas     !
!        NU - Novo Usuario        !
!        A  - Abandonar           !
!                                 !
=================================== 
    \nQual operação você deseja realizar? ''' 
    return input(menu).upper()

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print('\n@@@ Cliente não possui conta! @@@')
        return

    # FIXME:
    return cliente.contas[0]


def depositar(clientes):
    cpf = input('Informe o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('\n@@@ Clinete não encontrado ou cadastrado! @@@')
        return

    valor = float(input('Valor do Depósito: R$ '))
    transacao = Deposito(valor)
    conta = recuperar_conta_cliente(cliente)

    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def sacar(clientes):
    cpf = input('Informe o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)
    
    if not cliente:
        print('\n@@@ Clinete não encontrado ou cadastrado! @@@')
        return

    valor = int(input('Valor do saque R$:'))
    transacao = Saque(valor)
    conta = recuperar_conta_cliente(cliente)

    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)             
    

def exibir_extrato(clientes):
    cpf = input('Informe o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)
    
    if not cliente:
        print('\n@@@ Clinete não encontrado ou cadastrado! @@@')
        return

    conta = recuperar_conta_cliente(cliente)

    if not conta:
        return

    print('\n========== EXTRATO ==========')
    transacoes = conta.historico.transacoes

    extrato = ''
    if not transacoes:
        extrato = 'Não foram realizadas movimentações.'
    else:
        for transacao in transacoes:
            extrato += f'\n{transacao['tipo']}: \n\tR${transacao['valor']:.2f}'
            
    print(extrato)
    print(f'\nSaldo:\n\tR$ {conta.saldo:.2f}')
    print('============================\n')


def criar_cliente(clientes):
    cpf = input('informe o seu CPF: ')
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print('CPF ja cadastrado')
        return
    
    nome = input('Informe seu nome completo: ').title()
    data_nascimento = input('Informe sua data de nascimento(dd-mm-aaaa): ')
    endereco = input('informe seu endereço (Rua, nº, Bairro, cidade - UF )')

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print('!!!Usuario registrado com sucesso!!!')


def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def criar_conta(numero_conta, clientes, contas):
    cpf = input('informe o CPF de usuario: ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado!')
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print('====CONTA CRIADA COM SUCESSO====')
    


def listar_contas(contas):
    for conta in contas:
        print('='*100)
        print(textwrap.dedent(str(conta)))


def main():
    clientes = []
    contas = []

    while True:
        operacao = menu()
        
        if operacao == "D":
            depositar(clientes)


        elif operacao == 'S':
            sacar(clientes)

        elif operacao == 'E':
            exibir_extrato(clientes)
        
        elif operacao == 'NU':
            criar_cliente(clientes)

        elif operacao == 'NC':
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
        
        elif operacao == 'LC':
            listar_contas(contas)

        elif operacao == "A":
            print('Obrigado pela preferencia, volte sempre!')
            break
        
        else:
            print('❌ Operação inválida!!!')

main()