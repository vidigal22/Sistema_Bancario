saldo = 0
saque = 0
limite_saque = 3
historico_depositos = []  
historico_saques = [] 
menu = '\n!!!Bem vindo ao caixa Rapido!!! \noperações disponíveis: \n D = Deposito \n S = Saque \n E = Extrato \n Q = Sair\n\nQual operação você deseja realizar? ' 

while True:
    operacao = input(menu).upper()
    
    if operacao == "D":
        while True:
            valor = float(input('Valor do Depósito: R$ '))
            if valor >= 0:
                saldo += valor
                historico_depositos.append(valor)
                print(f'✅ Depósito realizado! Saldo: R$ {saldo:.2f}')
                break
            else:
                print('❌ Valor inválido! Digite um número positivo.')
    
    elif operacao == 'S':
        while True:            
            if saque == limite_saque:
                print('Limite de saque diario exedido, volte amanha!!!')
                break

            valor = int(input('Valor do saque R$:'))
            
            if valor > 500:
                print('Saque indevido, por favor tente outro valor de até no máximo R$500,00')

            else:
                saldo -= valor
                saque += 1
                historico_saques.append(valor)
                print(f'✅ Saque realizado! Saldo: R$ {saldo:.2f}')
                break
    elif operacao == 'E':
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
    
    elif operacao == "Q":
        print('Obrigado pela preferencia, volte sempre!')
        break
    
    else:
        print('❌ Operação inválida!!!')