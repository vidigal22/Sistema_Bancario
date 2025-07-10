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


def deposito(saldo, historico_depositos, /):
    while True:
        valor = float(input('Valor do Depósito: R$ '))
        if valor >= 0:
            saldo += valor
            historico_depositos.append(valor)
            print(f'✅ Depósito realizado! Saldo: R$ {saldo:.2f}')
            return saldo, historico_depositos
        else:
            print('❌ Valor inválido! Digite um número positivo.')

def saque(*, saldo, historico_saques, limite_saque, num_saque):
    while True:            
        if num_saque == limite_saque:
            print('Limite de saque diario exedido, volte amanha!!!')
            return saldo, historico_saques, num_saque

        valor = int(input('Valor do saque R$:'))
                
        if valor > 500:
            print('Saque indevido, por favor tente outro valor de até no máximo R$500,00')
        elif valor > saldo:
            print('Saldo insuficiente')
            return saldo, historico_saques, num_saque
        elif valor <= 0:
            print('Valor inválido')
        else:
            saldo -= valor
            num_saque += 1
            historico_saques.append(valor)
            print(f'✅ Saque realizado! Saldo: R$ {saldo:.2f}')
            return saldo, historico_saques, num_saque

def extrato(saldo, historico_depositos,/,*,historico_saques,):
    print('\n========== EXTRATO ==========')
    print('DEPÓSITOS:')
    if not historico_depositos:
        print('Nenhum depósito realizado.')
    else:
        for i, valor in enumerate(historico_depositos, 1):
            print(f'{i}º depósito: R$ {valor:.2f}')
            
    print('\nSAQUES:')
    if not historico_saques:
        print('Nenhum saque realizado.')
    else:
        for i, valor in enumerate(historico_saques, 1):
            print(f'{i}º saque: R$ {valor:.2f}')
            
    print(f'\nSALDO ATUAL: R$ {saldo:.2f}')
    print('============================\n')

def criar_usuario(usuarios):
    cpf=input('informe o seu CPF: ')
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print('CPF ja cadastrado')
        return
    
    nome = input('Informe seu nome completo: ').title()
    data_nascimento = input('Informe sua data de nascimento(dd-mm-aaaa): ')
    endereco = input('informe seu endereço (Rua, nº, Bairro, cidade - UF )')

    usuarios.append({'nome' : nome, 'data_nascimento' : data_nascimento, 'cpf' : cpf, 'endereco' : endereco})

    print('!!!Usuario registrado com sucesso!!!')

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario['cpf']==cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, num_conta, usuarios):
    cpf = input('informe o CPF de usuario: ')
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print('====CONTA CRIADA COM SUCESSO====')
        return {'agencia' : agencia, 'num_conta' : num_conta, 'usuario' : usuario}

    print('XXXX USUARIO NÃO ENCONTRADO XXXX')
    return None

def listar_contas(contas):
    for conta in contas:
        linha = f'''\n Agência: {conta['agencia']}
        C/C: {conta['num_conta']}
        Titular: {conta['usuario']['nome']}
        '''
        print('='*100)
        print(linha)
        print('='*100)

def main():
    saldo = 0
    num_saque = 0
    limite_saque = 3
    historico_depositos = []  
    historico_saques = [] 
    AGENCIA = "0001"
    usuarios = []
    contas = []

    while True:
        operacao = menu()
        
        if operacao == "D":
            saldo, historico_depositos = deposito(saldo, historico_depositos)


        elif operacao == 'S':
            saldo, historico_saques, num_saque = saque(saldo=saldo, historico_saques=historico_saques, limite_saque=limite_saque, num_saque=num_saque)

        elif operacao == 'E':
            extrato(saldo, historico_depositos, historico_saques=historico_saques)
        
        elif operacao == 'NU':
            criar_usuario(usuarios)

        elif operacao == 'NC':
            num_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, num_conta, usuarios)

            if conta:
                contas.append(conta)
        
        elif operacao == 'LC':
            listar_contas(contas)

        elif operacao == "A":
            print('Obrigado pela preferencia, volte sempre!')
            break
        
        else:
            print('❌ Operação inválida!!!')

main()