# 💰 Sistema Bancário DIO.me

## 📝 Resolução do Projeto

Este repositório contém a implementação de um **Sistema Bancário Simples**, desenvolvido como parte dos requisitos do projeto da [DIO.me](https://www.dio.me).

```python
# Exemplo de código (ilustrativo)
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
